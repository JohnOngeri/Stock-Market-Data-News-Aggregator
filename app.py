import os
import requests
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)  # Enable CORS for all routes

# Get API keys from environment variables
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Validate API keys are present
if not ALPHA_VANTAGE_API_KEY or not NEWS_API_KEY:
    raise ValueError("Missing required API keys. Please check your .env file.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stock/<symbol>')
def get_single_stock(symbol):
    """Get stock data for a specific symbol"""
    try:
        symbol = symbol.upper().strip()
        alpha_vantage_url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
        
        response = requests.get(alpha_vantage_url)
        response.raise_for_status()
        data = response.json()
        
        if "Global Quote" in data:
            quote = data["Global Quote"]
            return jsonify({
                "symbol": quote.get("01. symbol"),
                "price": quote.get("05. price"),
                "change": quote.get("09. change"),
                "volume": quote.get("06. volume")
            })
        else:
            return jsonify({"error": f"No data found for {symbol}"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/news')
def get_general_news():
    """Get general financial news"""
    try:
        news_api_url = f"https://newsapi.org/v2/everything?q=finance stock market&apiKey={NEWS_API_KEY}&language=en&sortBy=relevancy"
        
        response = requests.get(news_api_url)
        response.raise_for_status()
        news_response = response.json()
        
        if news_response.get("status") == "ok":
            articles = []
            for article in news_response.get("articles", [])[:10]:
                articles.append({
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "url": article.get("url"),
                    "publishedAt": article.get("publishedAt")
                })
            return jsonify({"articles": articles})
        else:
            return jsonify({"error": "Failed to fetch news"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/news/<symbol>')
def get_symbol_news(symbol):
    """Get news for a specific stock symbol"""
    try:
        symbol = symbol.upper().strip()
        news_api_url = f"https://newsapi.org/v2/everything?q={symbol} stock&apiKey={NEWS_API_KEY}&language=en&sortBy=relevancy"
        
        response = requests.get(news_api_url)
        response.raise_for_status()
        news_response = response.json()
        
        if news_response.get("status") == "ok":
            articles = []
            for article in news_response.get("articles", [])[:10]:
                articles.append({
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "url": article.get("url"),
                    "publishedAt": article.get("publishedAt")
                })
            return jsonify({"articles": articles})
        else:
            return jsonify({"error": f"No news found for {symbol}"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_stock_data', methods=['POST'])
def get_stock_data():
    try:
        if not request.json:
            return jsonify({"error": "Invalid request format"}), 400
            
        symbols_str = request.json.get('symbols', '')
        if not symbols_str.strip():
            return jsonify({"error": "No symbols provided"}), 400
            
        symbols = [s.strip().upper() for s in symbols_str.split(',') if s.strip()]
        if len(symbols) > 10:  # Limit to prevent abuse
            return jsonify({"error": "Too many symbols. Maximum 10 allowed."}), 400
        
        stock_data = []
        news_data = []
        errors = []
    except Exception as e:
        return jsonify({"error": "Server error processing request"}), 500

    for symbol in symbols:
        # Alpha Vantage Global Quote
        alpha_vantage_url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
        try:
            response = requests.get(alpha_vantage_url)
            response.raise_for_status() # Raise an exception for HTTP errors
            data = response.json()
            if "Global Quote" in data:
                quote = data["Global Quote"]
                stock_data.append({
                    "symbol": quote.get("01. symbol"),
                    "price": quote.get("05. price"),
                    "change": quote.get("09. change"),
                    "volume": quote.get("06. volume")
                })
            elif "Error Message" in data:
                errors.append(f"Alpha Vantage Error for {symbol}: {data['Error Message']}")
            else:
                errors.append(f"No data found for {symbol} from Alpha Vantage.")
        except requests.exceptions.RequestException as e:
            errors.append(f"Error fetching stock data for {symbol}: {e}")

    # NewsAPI.org for general financial news or news related to symbols
    news_query = "finance stock market"
    if symbols:
        news_query = " OR ".join(symbols) + " finance" # Broaden news search if symbols are provided
    
    news_api_url = f"https://newsapi.org/v2/everything?q={news_query}&apiKey={NEWS_API_KEY}&language=en&sortBy=relevancy"
    try:
        response = requests.get(news_api_url)
        response.raise_for_status()
        news_response = response.json()
        if news_response.get("status") == "ok":
            for article in news_response.get("articles", [])[:5]: # Limit to top 5 articles
                news_data.append({
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "url": article.get("url")
                })
        else:
            errors.append(f"News API Error: {news_response.get('message', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        errors.append(f"Error fetching news: {e}")

    return jsonify({"stock_data": stock_data, "news_data": news_data, "errors": errors})

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
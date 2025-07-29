import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env

app = Flask(__name__)

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_stock_data', methods=['POST'])
def get_stock_data():
    symbols_str = request.json.get('symbols', '')
    symbols = [s.strip().upper() for s in symbols_str.split(',') if s.strip()]
    
    stock_data = []
    news_data = []
    errors = []

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
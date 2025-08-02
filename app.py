import os
import requests
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_caching import Cache
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
import time

print("[DEBUG] Loading environment variables...")
load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Configure caching (5 minute timeout)
cache = Cache(app, config={
    'CACHE_TYPE': 'SimpleCache',
    'CACHE_DEFAULT_TIMEOUT': 300
})

print("[DEBUG] Flask app initialized.")

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

print(f"[DEBUG] ALPHA_VANTAGE_API_KEY: {bool(ALPHA_VANTAGE_API_KEY)}")
print(f"[DEBUG] NEWS_API_KEY: {bool(NEWS_API_KEY)}")

if not ALPHA_VANTAGE_API_KEY or not NEWS_API_KEY:
    raise ValueError("Missing required API keys. Please check your .env file.")

# Shared HTTP session for connection pooling
session = requests.Session()

@app.route('/')
def index():
    print("[DEBUG] Serving index.html")
    return render_template('index.html')

@app.route('/api/stock/<symbol>')
def get_single_stock(symbol):
    print(f"[DEBUG] Fetching stock data for symbol: {symbol}")
    try:
        symbol = symbol.upper().strip()
        cache_key = f"stock_{symbol}"
        
        # Check cache first
        if cached := cache.get(cache_key):
            print(f"[DEBUG] Returning cached stock data for {symbol}")
            return jsonify(cached)

        alpha_vantage_url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
        print(f"[DEBUG] Alpha Vantage URL: {alpha_vantage_url}")

        response = session.get(alpha_vantage_url, timeout=3)
        print(f"[DEBUG] Alpha Vantage response status: {response.status_code}")
        response.raise_for_status()
        data = response.json()
        print(f"[DEBUG] Alpha Vantage response data: {data}")

        if "Global Quote" in data:
            quote = data["Global Quote"]
            result = {
                "symbol": quote.get("01. symbol"),
                "price": quote.get("05. price"),
                "change": quote.get("09. change"),
                "volume": quote.get("06. volume")
            }
            cache.set(cache_key, result)
            return jsonify(result)
        else:
            print(f"[DEBUG] No Global Quote data for symbol: {symbol}")
            return jsonify({"error": f"No data found for {symbol}"}), 404

    except Exception as e:
        print(f"[ERROR] Exception fetching stock: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/news')
def get_general_news():
    print("[DEBUG] Fetching general news")
    try:
        cache_key = "general_news"
        if cached := cache.get(cache_key):
            print("[DEBUG] Returning cached general news")
            return jsonify({"articles": cached})

        news_api_url = f"https://newsapi.org/v2/everything?q=finance stock market&apiKey={NEWS_API_KEY}&language=en&sortBy=relevancy&pageSize=10"
        print(f"[DEBUG] News API URL: {news_api_url}")

        response = session.get(news_api_url, timeout=3)
        print(f"[DEBUG] News API response status: {response.status_code}")
        response.raise_for_status()
        news_response = response.json()
        print(f"[DEBUG] News API response: {news_response}")

        if news_response.get("status") == "ok":
            articles = []
            for article in news_response.get("articles", [])[:10]:
                articles.append({
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "url": article.get("url"),
                    "publishedAt": article.get("publishedAt")
                })
            cache.set(cache_key, articles)
            return jsonify({"articles": articles})
        else:
            print("[ERROR] Failed to fetch news")
            return jsonify({"error": "Failed to fetch news"}), 500

    except Exception as e:
        print(f"[ERROR] Exception fetching general news: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/news/<symbol>')
def get_symbol_news(symbol):
    print(f"[DEBUG] Fetching news for symbol: {symbol}")
    try:
        symbol = symbol.upper().strip()
        cache_key = f"news_{symbol}"
        
        if cached := cache.get(cache_key):
            print(f"[DEBUG] Returning cached news for {symbol}")
            return jsonify({"articles": cached})

        news_api_url = f"https://newsapi.org/v2/everything?q={symbol} stock&apiKey={NEWS_API_KEY}&language=en&sortBy=relevancy&pageSize=10"
        print(f"[DEBUG] News API URL for symbol: {news_api_url}")

        response = session.get(news_api_url, timeout=3)
        print(f"[DEBUG] News API response status: {response.status_code}")
        response.raise_for_status()
        news_response = response.json()
        print(f"[DEBUG] News API response for symbol: {news_response}")

        if news_response.get("status") == "ok":
            articles = []
            for article in news_response.get("articles", [])[:10]:
                articles.append({
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "url": article.get("url"),
                    "publishedAt": article.get("publishedAt")
                })
            cache.set(cache_key, articles)
            return jsonify({"articles": articles})
        else:
            print(f"[ERROR] No news found for {symbol}")
            return jsonify({"error": f"No news found for {symbol}"}), 404

    except Exception as e:
        print(f"[ERROR] Exception fetching symbol news: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/get_stock_data', methods=['POST'])
def get_stock_data():
    print("[DEBUG] Received POST to /get_stock_data")
    start_time = time.time()
    
    try:
        if not request.json:
            print("[ERROR] Request JSON missing")
            return jsonify({"error": "Invalid request format"}), 400

        symbols_str = request.json.get('symbols', '')
        print(f"[DEBUG] Raw symbols input: {symbols_str}")

        if not symbols_str.strip():
            print("[ERROR] No symbols provided")
            return jsonify({"error": "No symbols provided"}), 400

        symbols = list({s.strip().upper() for s in symbols_str.split(',') if s.strip()})
        print(f"[DEBUG] Parsed symbols: {symbols}")

        if len(symbols) > 10:
            print("[ERROR] Too many symbols provided")
            return jsonify({"error": "Too many symbols. Maximum 10 allowed."}), 400

        stock_data = []
        news_data = []
        errors = []

        # Build expanded symbols list for news
        symbols_expanded = []
        for s in symbols:
            symbols_expanded.append(s)
            if '.' in s:
                symbols_expanded.append(s.split('.')[0])  # Handle BRK.A -> BRK

        # Optimized news query
        news_query = f"({' OR '.join(symbols_expanded)}) (stock OR shares OR company OR market OR earnings)"
        news_api_url = (
            f"https://newsapi.org/v2/everything?"
            f"q={news_query}&"
            f"searchIn=title,description&"
            f"language=en&"
            f"sortBy=relevancy&"
            f"pageSize=5&"
            f"apiKey={NEWS_API_KEY}"
        )
        print(f"[DEBUG] News API URL: {news_api_url}")

        # Cache key for news
        news_cache_key = f"combined_news_{'_'.join(sorted(symbols))}"
        if cached_news := cache.get(news_cache_key):
            print("[DEBUG] Using cached news results")
            news_data = cached_news
        else:
            # Fetch news if not cached
            try:
                news_response = session.get(news_api_url, timeout=3).json()
                print(f"[DEBUG] News API response code: {news_response.get('status')}")
                print(f"[DEBUG] News API response: {news_response}")

                if news_response.get("status") == "ok":
                    news_data = [{
                        "title": article.get("title"),
                        "description": article.get("description"),
                        "url": article.get("url")
                    } for article in news_response.get("articles", [])[:5]]
                    cache.set(news_cache_key, news_data)
                else:
                    print(f"[ERROR] News API error message: {news_response.get('message', 'Unknown error')}")
                    errors.append(f"News API Error: {news_response.get('message', 'Unknown error')}")
            except Exception as e:
                print(f"[ERROR] Exception fetching news: {e}")
                errors.append(f"Error fetching news: {e}")

        # Fetch stock data in parallel
        def fetch_stock(symbol):
            cache_key = f"stock_{symbol}"
            if cached := cache.get(cache_key):
                return cached

            try:
                alpha_vantage_url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
                print(f"[DEBUG] Fetching stock data for {symbol} from: {alpha_vantage_url}")
                
                response = session.get(alpha_vantage_url, timeout=3)
                print(f"[DEBUG] Response status for {symbol}: {response.status_code}")
                response.raise_for_status()
                data = response.json()
                print(f"[DEBUG] Response data for {symbol}: {data}")

                if "Global Quote" in data:
                    quote = data["Global Quote"]
                    result = {
                        "symbol": quote.get("01. symbol"),
                        "price": quote.get("05. price"),
                        "change": quote.get("09. change"),
                        "volume": quote.get("06. volume")
                    }
                    cache.set(cache_key, result)
                    return result
                elif "Error Message" in data:
                    print(f"[ERROR] Alpha Vantage error for {symbol}: {data['Error Message']}")
                    errors.append(f"Alpha Vantage Error for {symbol}: {data['Error Message']}")
                else:
                    print(f"[ERROR] No Global Quote found for {symbol}")
                    errors.append(f"No data found for {symbol} from Alpha Vantage.")
            except requests.exceptions.RequestException as e:
                print(f"[ERROR] RequestException fetching stock for {symbol}: {e}")
                errors.append(f"Error fetching stock data for {symbol}: {e}")
            return None

        # Execute stock fetches in parallel
        with ThreadPoolExecutor() as executor:
            stock_results = list(executor.map(fetch_stock, symbols))
            stock_data = [result for result in stock_results if result]

        result = {
            "stock_data": stock_data,
            "news_data": news_data,
            "errors": errors,
            "response_time": f"{(time.time() - start_time):.2f}s"
        }
        print(f"[DEBUG] Final result: {result}")
        return jsonify(result)

    except Exception as e:
        print(f"[ERROR] Exception during request processing: {e}")
        return jsonify({"error": "Server error processing request"}), 500

@app.errorhandler(404)
def not_found(error):
    print(f"[ERROR] 404 - Not Found: {error}")
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    print(f"[ERROR] 500 - Internal Server Error: {error}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    print(f"[DEBUG] Starting app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
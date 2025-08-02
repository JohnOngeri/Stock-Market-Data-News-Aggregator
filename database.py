import sqlite3
import json
from datetime import datetime, timedelta

class StockDataCache:
    def __init__(self, db_path='stock_cache.db'):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS stock_cache (
                    symbol TEXT PRIMARY KEY,
                    data TEXT,
                    timestamp DATETIME
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS news_cache (
                    query TEXT PRIMARY KEY,
                    data TEXT,
                    timestamp DATETIME
                )
            ''')
    
    def get_stock_data(self, symbol):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'SELECT data, timestamp FROM stock_cache WHERE symbol = ?',
                (symbol,)
            )
            row = cursor.fetchone()
            if row:
                timestamp = datetime.fromisoformat(row[1])
                if datetime.now() - timestamp < timedelta(minutes=5):
                    return json.loads(row[0])
        return None
    
    def cache_stock_data(self, symbol, data):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                'INSERT OR REPLACE INTO stock_cache (symbol, data, timestamp) VALUES (?, ?, ?)',
                (symbol, json.dumps(data), datetime.now().isoformat())
            )
    
    def get_news_data(self, query):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'SELECT data, timestamp FROM news_cache WHERE query = ?',
                (query,)
            )
            row = cursor.fetchone()
            if row:
                timestamp = datetime.fromisoformat(row[1])
                if datetime.now() - timestamp < timedelta(minutes=15):
                    return json.loads(row[0])
        return None
    
    def cache_news_data(self, query, data):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                'INSERT OR REPLACE INTO news_cache (query, data, timestamp) VALUES (?, ?, ?)',
                (query, json.dumps(data), datetime.now().isoformat())
            )
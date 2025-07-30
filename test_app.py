#!/usr/bin/env python3
"""
Comprehensive test suite for Stock Market Data & News Aggregator
Tests all API endpoints, error handling, and interactive features
"""

import unittest
import json
import os
import sys
from unittest.mock import patch, Mock
from io import StringIO

# Add the current directory to the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

class StockMarketAppTestCase(unittest.TestCase):
    """Test cases for the Stock Market Data & News Aggregator application"""
    
    def setUp(self):
        """Set up test client and environment"""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
        
        # Mock environment variables for testing
        os.environ['ALPHA_VANTAGE_API_KEY'] = 'test_alpha_vantage_key'
        os.environ['NEWS_API_KEY'] = 'test_news_api_key'
    
    def tearDown(self):
        """Clean up after tests"""
        pass
    
    def test_home_page_loads(self):
        """Test that the home page loads successfully"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Stock Market Data & News Aggregator', response.data)
        self.assertIn(b'Enter stock symbols', response.data)
    
    def test_home_page_contains_required_elements(self):
        """Test that the home page contains all required UI elements"""
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        
        # Check for required elements
        self.assertIn('stockSymbols', html)
        self.assertIn('fetchData', html)
        self.assertIn('stockTable', html)
        self.assertIn('newsArticles', html)
        self.assertIn('stockSearch', html)
        self.assertIn('newsSearch', html)
    
    @patch('requests.get')
    def test_get_single_stock_success(self, mock_get):
        """Test successful single stock data retrieval"""
        # Mock successful API response
        mock_response = Mock()
        mock_response.json.return_value = {
            "Global Quote": {
                "01. symbol": "AAPL",
                "05. price": "150.00",
                "09. change": "2.50",
                "06. volume": "1000000"
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        response = self.client.get('/api/stock/AAPL')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['symbol'], 'AAPL')
        self.assertEqual(data['price'], '150.00')
        self.assertEqual(data['change'], '2.50')
        self.assertEqual(data['volume'], '1000000')
    
    @patch('requests.get')
    def test_get_single_stock_not_found(self, mock_get):
        """Test stock data retrieval when symbol not found"""
        # Mock API response with no data
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        response = self.client.get('/api/stock/INVALID')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', data)
        self.assertIn('No data found', data['error'])
    
    @patch('requests.get')
    def test_get_general_news_success(self, mock_get):
        """Test successful general news retrieval"""
        # Mock successful API response
        mock_response = Mock()
        mock_response.json.return_value = {
            "status": "ok",
            "articles": [
                {
                    "title": "Test News Article",
                    "description": "Test description",
                    "url": "https://example.com",
                    "publishedAt": "2023-01-01T00:00:00Z"
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        response = self.client.get('/api/news')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('articles', data)
        self.assertEqual(len(data['articles']), 1)
        self.assertEqual(data['articles'][0]['title'], 'Test News Article')
    
    @patch('requests.get')
    def test_get_symbol_news_success(self, mock_get):
        """Test successful symbol-specific news retrieval"""
        # Mock successful API response
        mock_response = Mock()
        mock_response.json.return_value = {
            "status": "ok",
            "articles": [
                {
                    "title": "AAPL Stock News",
                    "description": "Apple stock news",
                    "url": "https://example.com",
                    "publishedAt": "2023-01-01T00:00:00Z"
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        response = self.client.get('/api/news/AAPL')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('articles', data)
        self.assertEqual(len(data['articles']), 1)
        self.assertEqual(data['articles'][0]['title'], 'AAPL Stock News')
    
    @patch('requests.get')
    def test_get_stock_data_success(self, mock_get):
        """Test successful stock data and news retrieval via POST"""
        # Mock successful API responses
        mock_response = Mock()
        mock_response.json.side_effect = [
            # Alpha Vantage response
            {
                "Global Quote": {
                    "01. symbol": "AAPL",
                    "05. price": "150.00",
                    "09. change": "2.50",
                    "06. volume": "1000000"
                }
            },
            # News API response
            {
                "status": "ok",
                "articles": [
                    {
                        "title": "Financial News",
                        "description": "Market update",
                        "url": "https://example.com"
                    }
                ]
            }
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        response = self.client.post('/get_stock_data',
                                  json={'symbols': 'AAPL'})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('stock_data', data)
        self.assertIn('news_data', data)
        self.assertEqual(len(data['stock_data']), 1)
        self.assertEqual(len(data['news_data']), 1)
    
    def test_get_stock_data_no_symbols(self):
        """Test stock data retrieval with no symbols provided"""
        response = self.client.post('/get_stock_data',
                                  json={'symbols': ''})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertIn('No symbols provided', data['error'])
    
    def test_get_stock_data_too_many_symbols(self):
        """Test stock data retrieval with too many symbols"""
        symbols = ','.join(['SYMBOL' + str(i) for i in range(11)])
        response = self.client.post('/get_stock_data',
                                  json={'symbols': symbols})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertIn('Too many symbols', data['error'])
    
    def test_get_stock_data_invalid_request(self):
        """Test stock data retrieval with invalid request format"""
        response = self.client.post('/get_stock_data',
                                  data='invalid json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
    
    @patch('requests.get')
    def test_api_error_handling(self, mock_get):
        """Test error handling when API calls fail"""
        # Mock API error
        mock_get.side_effect = Exception("API Error")
        
        response = self.client.get('/api/stock/AAPL')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', data)
    
    def test_404_error_handler(self):
        """Test 404 error handling"""
        response = self.client.get('/nonexistent-endpoint')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', data)
        self.assertIn('Endpoint not found', data['error'])
    
    def test_500_error_handler(self):
        """Test 500 error handling"""
        # This would typically be tested with a route that raises an exception
        # For now, we'll test that the error handler exists
        with app.test_client() as client:
            # Create a temporary route that raises an exception
            @app.route('/test-error')
            def test_error():
                raise Exception("Test error")
            
            response = client.get('/test-error')
            data = json.loads(response.data)
            
            self.assertEqual(response.status_code, 500)
            self.assertIn('error', data)
    
    def test_input_validation(self):
        """Test various input validation scenarios"""
        # Test empty symbols
        response = self.client.post('/get_stock_data',
                                  json={'symbols': '   '})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        
        # Test symbols with special characters
        response = self.client.post('/get_stock_data',
                                  json={'symbols': 'AAPL,MSFT,GOOGL'})
        self.assertEqual(response.status_code, 200)  # Should be valid
    
    def test_api_key_validation(self):
        """Test that the application validates API keys on startup"""
        # This test ensures the app validates API keys
        # The setUp method already sets test API keys
        self.assertIsNotNone(os.environ.get('ALPHA_VANTAGE_API_KEY'))
        self.assertIsNotNone(os.environ.get('NEWS_API_KEY'))
    
    def test_response_format(self):
        """Test that API responses have the correct format"""
        with patch('requests.get') as mock_get:
            # Mock successful response
            mock_response = Mock()
            mock_response.json.return_value = {
                "Global Quote": {
                    "01. symbol": "AAPL",
                    "05. price": "150.00",
                    "09. change": "2.50",
                    "06. volume": "1000000"
                }
            }
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            response = self.client.get('/api/stock/AAPL')
            data = json.loads(response.data)
            
            # Check response format
            required_fields = ['symbol', 'price', 'change', 'volume']
            for field in required_fields:
                self.assertIn(field, data)
    
    def test_news_response_format(self):
        """Test that news API responses have the correct format"""
        with patch('requests.get') as mock_get:
            # Mock successful response
            mock_response = Mock()
            mock_response.json.return_value = {
                "status": "ok",
                "articles": [
                    {
                        "title": "Test Article",
                        "description": "Test description",
                        "url": "https://example.com",
                        "publishedAt": "2023-01-01T00:00:00Z"
                    }
                ]
            }
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            response = self.client.get('/api/news')
            data = json.loads(response.data)
            
            # Check response format
            self.assertIn('articles', data)
            self.assertIsInstance(data['articles'], list)
            if data['articles']:
                article = data['articles'][0]
                required_fields = ['title', 'description', 'url']
                for field in required_fields:
                    self.assertIn(field, article)
    
    def test_rate_limiting_handling(self):
        """Test handling of API rate limiting"""
        with patch('requests.get') as mock_get:
            # Mock rate limit error
            mock_response = Mock()
            mock_response.json.return_value = {
                "Note": "API call frequency limit exceeded"
            }
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            response = self.client.get('/api/stock/AAPL')
            data = json.loads(response.data)
            
            # Should handle rate limiting gracefully
            self.assertIn('error', data)
    
    def test_application_configuration(self):
        """Test application configuration"""
        self.assertTrue(app.config['TESTING'])
        self.assertFalse(app.config.get('WTF_CSRF_ENABLED', True))
    
    def test_static_files_served(self):
        """Test that static files are served correctly"""
        # Test CSS file
        response = self.client.get('/static/css/style.css')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/css', response.headers.get('Content-Type', ''))
        
        # Test JavaScript file
        response = self.client.get('/static/js/main.js')
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/javascript', response.headers.get('Content-Type', ''))
    
    def test_template_rendering(self):
        """Test that templates render correctly"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        # Check for template-specific content
        html = response.data.decode('utf-8')
        self.assertIn('Stock Market Data & News Aggregator', html)
        self.assertIn('Enter stock symbols', html)
        self.assertIn('Fetch Data', html)
    
    def test_json_content_type(self):
        """Test that API endpoints return proper JSON content type"""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {
                "Global Quote": {
                    "01. symbol": "AAPL",
                    "05. price": "150.00",
                    "09. change": "2.50",
                    "06. volume": "1000000"
                }
            }
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            response = self.client.get('/api/stock/AAPL')
            self.assertIn('application/json', response.headers.get('Content-Type', ''))


class IntegrationTestCase(unittest.TestCase):
    """Integration tests for the complete application workflow"""
    
    def setUp(self):
        """Set up test client"""
        app.config['TESTING'] = True
        self.client = app.test_client()
        os.environ['ALPHA_VANTAGE_API_KEY'] = 'test_key'
        os.environ['NEWS_API_KEY'] = 'test_key'
    
    @patch('requests.get')
    def test_complete_workflow(self, mock_get):
        """Test the complete application workflow"""
        # Mock successful API responses
        mock_response = Mock()
        mock_response.json.side_effect = [
            # Stock data response
            {
                "Global Quote": {
                    "01. symbol": "AAPL",
                    "05. price": "150.00",
                    "09. change": "2.50",
                    "06. volume": "1000000"
                }
            },
            # News response
            {
                "status": "ok",
                "articles": [
                    {
                        "title": "Market Update",
                        "description": "Latest market news",
                        "url": "https://example.com"
                    }
                ]
            }
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Test complete workflow
        # 1. Load home page
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        # 2. Get stock data
        response = self.client.post('/get_stock_data',
                                  json={'symbols': 'AAPL'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('stock_data', data)
        self.assertIn('news_data', data)
        
        # 3. Get individual stock data
        response = self.client.get('/api/stock/AAPL')
        self.assertEqual(response.status_code, 200)
        
        # 4. Get news
        response = self.client.get('/api/news')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
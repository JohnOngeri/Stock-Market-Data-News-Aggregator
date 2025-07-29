# Stock Market Data & News Aggregator

A Flask-based web application that provides real-time stock quotes and aggregates relevant financial news articles. This application offers a centralized dashboard for investors to quickly access crucial market information.

## Features

* **Real-time Stock Data**: Fetch current stock prices, changes, and volume for multiple symbols
* **Financial News Aggregation**: Get latest financial news and symbol-specific news articles
* **RESTful API**: Clean API endpoints for programmatic access
* **Web Interface**: User-friendly dashboard for interactive stock and news browsing
* **Error Handling**: Robust error handling for API failures and invalid inputs
* **Docker Support**: Containerized deployment with production-ready configuration
* **Load Balancing**: Nginx configuration for high-availability deployment

## Technologies Used

* **Backend**: Python 3.11, Flask 2.3.2, Gunicorn
* **Frontend**: HTML5, CSS3, JavaScript
* **APIs**: Alpha Vantage (stock data), NewsAPI.org (news articles)
* **Deployment**: Docker, Docker Compose, Nginx
* **Dependencies**: requests, python-dotenv

## Quick Start

### Prerequisites

* Python 3.11+
* API keys from [Alpha Vantage](https://www.alphavantage.co/support/#api-key) and [NewsAPI.org](https://newsapi.org/register)

### Local Setup

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd Stock-Market-Data-News-Aggregator
   ```markdown

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**

   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Run the application:**

   **Windows:**

   ```cmd
   start.bat
   ```

   **Linux/Mac:**

   ```bash
   chmod +x start.sh
   ./start.sh
   ```

   **Or manually:**

   ```bash
   python app.py
   ```

5. **Access the application:**
   Open `http://localhost:8080` in your browser

### Testing

Run the test suite to verify all components:

```bash
python test_app.py
```

## Docker Deployment

### Quick Deploy

**Windows:**

```cmd
deploy.bat
```

**Linux/Mac:**

```bash
chmod +x deploy.sh
./deploy.sh
```

### Manual Docker Commands

1. **Build the image:**

   ```bash
   docker build -t stock-market-aggregator .
   ```

2. **Run locally:**

   ```bash
   docker run -d -p 8080:8080 \
     -e ALPHA_VANTAGE_API_KEY="your_key" \
     -e NEWS_API_KEY="your_key" \
     stock-market-aggregator
   ```

3. **Using Docker Compose:**

   ```bash
   # Development
   docker-compose up -d
   
   # Production
   docker-compose -f docker-compose.prod.yml up -d
   
   # With load balancer
   docker-compose -f docker-compose.loadbalancer.yml up -d
   ```

### Production Deployment

The application includes production-ready configurations:

* **Gunicorn WSGI server** with 4 workers
* **Health checks** for container monitoring
* **Non-root user** for security
* **Nginx load balancer** configuration
* **Multi-stage deployment** scripts

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## API Endpoints

### Web Interface

* `GET /` - Main application dashboard

### Stock Data

* `GET /api/stock/<symbol>` - Get real-time data for specific stock symbol
* `POST /get_stock_data` - Get data for multiple symbols (JSON payload: `{"symbols": "AAPL,MSFT,GOOGL"}`)

### News Data

* `GET /api/news` - Get latest general financial news
* `GET /api/news/<symbol>` - Get news articles for specific stock symbol

### Example API Response

**Stock Data:**

```json
{
  "symbol": "AAPL",
  "price": "150.25",
  "change": "+2.15",
  "volume": "45123456"
}
```

**News Data:**

```json
{
  "articles": [
    {
      "title": "Market Update...",
      "description": "Latest market trends...",
      "url": "https://...",
      "publishedAt": "2024-01-15T10:30:00Z"
    }
  ]
}
```

## Project Structure

Stock-Market-Data-News-Aggregator/
├── static/
│   ├── css/
│   │   └── style.css          # Application styles
│   └── js/
│       └── main.js            # Frontend JavaScript
├── templates/
│   └── index.html             # Main web interface
├── app.py                     # Flask application
├── wsgi.py                    # WSGI entry point
├── test_app.py                # Test suite
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Container configuration
├── docker-compose.yml         # Development compose
├── docker-compose.prod.yml    # Production compose
├── docker-compose.loadbalancer.yml # Load balancer setup
├── nginx.conf                 # Nginx configuration
├── deploy.sh / deploy.bat     # Deployment scripts
├── start.sh / start.bat       # Startup scripts
├── .env.example               # Environment template
├── .dockerignore              # Docker ignore rules
├── DEPLOYMENT.md              # Deployment guide
└── README.md                  # This file

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `ALPHA_VANTAGE_API_KEY` | API key for Alpha Vantage stock data | Yes |
| `NEWS_API_KEY` | API key for NewsAPI.org news articles | Yes |
| `PORT` | Application port (default: 8080) | No |

### Getting API Keys

1. **Alpha Vantage**: Register at [alphavantage.co](https://www.alphavantage.co/support/#api-key)
2. **NewsAPI**: Register at [newsapi.org](https://newsapi.org/register)

Both services offer free tiers suitable for development and testing.

## Development

### Dependencies

* **Flask 2.3.2** - Web framework
* **requests 2.31.0** - HTTP client for API calls
* **python-dotenv 1.0.0** - Environment variable management
* **gunicorn 21.2.0** - WSGI HTTP server for production

### Key Features

* **Rate Limiting**: Built-in protection against API abuse
* **Error Handling**: Comprehensive error responses
* **Health Checks**: Docker health monitoring
* **Security**: Non-root container execution
* **Scalability**: Multi-worker Gunicorn setup
* **Monitoring**: Request logging and error tracking

### Contributing

1. Fork the repository
2. Create a feature branch
3. Run tests: `python test_app.py`
4. Submit a pull request

## Troubleshooting

### Common Issues

* **API Key Errors**: Verify your `.env` file contains valid API keys
* **Port Conflicts**: Change the PORT environment variable if 8080 is in use
* **Docker Issues**: Ensure Docker is running and you have sufficient permissions
* **Network Errors**: Check your internet connection and API service status

### Logs

```bash
# View application logs
docker logs <container_name>

# Follow logs in real-time
docker logs -f <container_name>
```

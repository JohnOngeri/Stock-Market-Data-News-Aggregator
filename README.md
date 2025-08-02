# Stock Market Data & News Aggregator

A comprehensive web application that provides real-time stock market data and financial news aggregation. This application serves a practical purpose by helping users make informed investment decisions through consolidated market information and relevant financial news.

## 🎯 Application Purpose

This application addresses a genuine need in the financial market space by:

- **Consolidating Data**: Combining stock prices and financial news in one interface
- **Real-time Information**: Providing up-to-date market data and breaking financial news
- **User Interaction**: Enabling sorting, filtering, and searching through stock data and news
- **Decision Support**: Helping users make informed investment decisions

## 🚀 Features

### Core Functionality

- **Real-time Stock Data**: Fetch current prices, changes, and volume for multiple stocks
- **Financial News Aggregation**: Latest news from reputable financial sources
- **Interactive Interface**: Sort, filter, and search through data
- **Error Handling**: Graceful handling of API failures and invalid inputs
- **Responsive Design**: Works on desktop and mobile devices

### User Interaction Features

- **Stock Data Sorting**: Sort by symbol, price, change, or volume
- **News Filtering**: Filter news by category (Market, Tech, Finance)
- **Search Functionality**: Search through stocks and news articles
- **Real-time Updates**: Refresh data with a single click

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **APIs**: Alpha Vantage (Stock Data), NewsAPI.org (Financial News)
- **Containerization**: Docker
- **Deployment**: Docker Hub, Load Balancer (HAProxy)

## 📋 Prerequisites

- Python 3.8+
- Docker (for containerized deployment)
- API Keys:
  - [Alpha Vantage API Key](https://www.alphavantage.co/support/#api-key)
  - [NewsAPI.org API Key](https://newsapi.org/register)

## 🔧 Local Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd Stock-Market-Data-News-Aggregator
```

### 2. Set Up Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Keys

Create a `.env` file in the root directory:

```env
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
NEWS_API_KEY=your_news_api_key_here
```

### 4. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:8080`

## 🚀 Simple Server Deployment (No Docker)

### Quick Setup

```bash
# 1. Copy files to server
scp -r Stock-Market-Data-News-Aggregator/ user@server:/home/user/

# 2. SSH to server and deploy
ssh user@server
cd Stock-Market-Data-News-Aggregator
chmod +x simple-deploy.sh
./simple-deploy.sh

# 3. Start the application
./start-app.sh
```

### Alternative: Systemd Service

```bash
# For production deployment with auto-restart
chmod +x systemd-deploy.sh
sudo ./systemd-deploy.sh
```

## 🌐 Simple Lab Deployment

### Step-by-Step Lab Setup

#### 1. Deploy on Web Servers

**Both web-01 and web-02:**

```bash
# Copy project files
scp -r Stock-Market-Data-News-Aggregator/ user@server:/home/user/

# SSH to each server
ssh user@server
cd Stock-Market-Data-News-Aggregator

# Quick deployment
chmod +x simple-deploy.sh
./simple-deploy.sh
./start-app.sh
```

#### 2. Load Balancer Setup (Nginx)

**On lb-01:**

```bash
# Copy and run load balancer setup
scp load-balancer-setup.sh user@lb-01:/home/user/
ssh user@lb-01
chmod +x load-balancer-setup.sh
sudo ./load-balancer-setup.sh
```

#### 3. Quick Testing

```bash
# Test individual servers
curl http://172.20.0.11:8080  # web-01
curl http://172.20.0.12:8080  # web-02

# Test load balancer (nginx round-robin)
for i in {1..6}; do curl http://your-lb-ip; echo; done
```

### Management Commands

```bash
# Start/Stop application
./start-app.sh   # Start
./stop-app.sh    # Stop

# Or with systemd (if using systemd-deploy.sh)
sudo systemctl start stock-market-app
sudo systemctl stop stock-market-app
sudo systemctl status stock-market-app
```

## 🧪 Testing

### Local Testing

```bash
# Run the test suite
python test_app.py

# Test individual components
python simple_test.py
```

### Load Balancer Testing

```bash
# Test end-to-end functionality
curl http://localhost

# Verify load balancing (should alternate between servers)
for i in {1..6}; do
  curl -s http://localhost | grep "Server:" || echo "Request $i"
  sleep 1
done
```

## 🔒 Security Considerations

### API Key Management

- API keys are stored in environment variables
- Never commit API keys to version control
- Use Docker secrets or Kubernetes secrets in production
- Rotate API keys regularly

### Input Validation

- All user inputs are validated and sanitized
- SQL injection protection through parameterized queries
- XSS protection through proper output encoding

## 📊 API Documentation

### External APIs Used

#### Alpha Vantage API

- **Purpose**: Real-time stock market data
- **Documentation**: [Alpha Vantage API Docs](https://www.alphavantage.co/documentation/)
- **Rate Limits**: 5 API calls per minute, 500 per day (free tier)
- **Endpoints Used**: Global Quote

#### NewsAPI.org

- **Purpose**: Financial news aggregation
- **Documentation**: [NewsAPI Documentation](https://newsapi.org/docs)
- **Rate Limits**: 1,000 requests per day (free tier)
- **Endpoints Used**: Everything endpoint

### Application API Endpoints

#### GET `/`

- **Description**: Main application interface
- **Response**: HTML page with stock and news interface

#### POST `/get_stock_data`

- **Description**: Fetch stock data and news for given symbols
- **Request Body**: `{"symbols": "AAPL,MSFT,GOOGL"}`
- **Response**: JSON with stock data, news, and errors

#### GET `/api/stock/<symbol>`

- **Description**: Get data for a specific stock symbol
- **Response**: JSON with stock information

#### GET `/api/news`

- **Description**: Get general financial news
- **Response**: JSON with news articles

#### GET `/api/news/<symbol>`

- **Description**: Get news for a specific stock symbol
- **Response**: JSON with relevant news articles

## 🐛 Error Handling

The application implements comprehensive error handling:

### API Error Handling

- Network timeout handling
- Invalid API key detection
- Rate limit exceeded handling
- Malformed response handling

### User Input Validation

- Empty input validation
- Symbol format validation
- Maximum symbol limit enforcement
- Special character sanitization

### Graceful Degradation

- Partial data display when some APIs fail
- User-friendly error messages
- Fallback to cached data when available

## 🚀 Performance Optimizations

### Caching Strategy

- API response caching to reduce load
- Static asset caching
- Browser-side caching for better UX

### Load Balancing

- Round-robin distribution across servers
- Health checks for backend services
- Automatic failover capabilities

## 📈 Monitoring and Logging

### Health Checks

- Application health endpoint
- Docker health checks
- Load balancer health monitoring

### Logging

- Request/response logging
- Error logging with stack traces
- Performance metrics logging

## 🔄 CI/CD Pipeline (Bonus Feature)

The project includes automated testing and deployment:

### GitHub Actions Workflow

- Automated testing on pull requests
- Docker image building and pushing
- Deployment to staging environment

### Deployment Pipeline

1. Code commit triggers CI/CD
2. Automated tests run
3. Docker image built and tested
4. Image pushed to Docker Hub
5. Deployment to production servers

## 📝 Development Challenges and Solutions

### Challenge 1: API Rate Limiting

**Problem**: Alpha Vantage free tier has strict rate limits
**Solution**: Implemented request caching and user-friendly error messages

### Challenge 2: Cross-Origin Resource Sharing (CORS)

**Problem**: Frontend JavaScript couldn't access API endpoints
**Solution**: Configured Flask-CORS for proper CORS headers

### Challenge 3: Load Balancer Configuration

**Problem**: HAProxy wasn't properly distributing traffic
**Solution**: Added health checks and proper backend configuration

### Challenge 4: Environment Variable Management

**Problem**: API keys exposed in Docker images
**Solution**: Implemented environment variable injection at runtime

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Alpha Vantage](https://www.alphavantage.co/) for providing stock market data
- [NewsAPI.org](https://newsapi.org/) for financial news aggregation
- Flask community for the excellent web framework
- Docker community for containerization tools

## 📞 Support

For issues and questions:

- Create an issue in the GitHub repository
- Check the troubleshooting section in this README
- Review the API documentation links above

---

**Note**: This application is designed for educational purposes and should not be used for actual investment decisions without proper financial advice.

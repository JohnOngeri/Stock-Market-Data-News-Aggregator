# Stock-Market-Data-News-Aggregator

# Stock & News Aggregator

This application provides real-time stock quotes for user-specified symbols and aggregates relevant financial news articles. It aims to offer a centralized view for investors and individuals to quickly access crucial market information.

## Part One: Local Implementation

### Features
* Fetch real-time stock prices for multiple symbols.
* Aggregate news articles related to financial markets or specific stock symbols.
* User-friendly web interface.
* Error handling for API issues or invalid input.

### Technologies Used
* **Backend:** Python (Flask)
* **Frontend:** HTML, CSS, JavaScript
* **External APIs:**
    * [Alpha Vantage](https://www.alphavantage.co/) for stock market data.
    * [NewsAPI.org](https://newsapi.org/) for news articles.

### Setup and Running Locally

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/stock-app.git](https://github.com/your-username/stock-app.git)
    cd stock-app
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Obtain API Keys:**
    * Register for a free API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key).
    * Register for a free API key from [NewsAPI.org](https://newsapi.org/register).

4.  **Create a `.env` file:**
    In the root of your `stock-app` directory, create a file named `.env` and add your API keys:
    ```
    ALPHA_VANTAGE_API_KEY="YOUR_ALPHA_VANTAGE_KEY_HERE"
    NEWS_API_KEY="YOUR_NEWS_API_KEY_HERE"
    ```
    **Important:** Do not commit this `.env` file to your public repository! It's already included in `.gitignore`.

5.  **Run the application:**
    ```bash
    python app.py
    ```
    The application will be accessible at `http://localhost:8080`.

## Part Two A: Deployment (Docker Containers + Docker Hub)

This section details how the application is containerized, published to Docker Hub, and deployed on the lab's three-server setup (Web01, Web02, Lb01) with HAProxy for load balancing.

### Image Details
* **Docker Hub Repo URL:** `https://hub.docker.com/r/yourdockerhubusername/stock-app`
* **Image Name:** `yourdockerhubusername/stock-app`
* **Tags:** `v1`, `latest`

### Build Instructions

To build the Docker image locally:

```bash
docker build -t yourdockerhubusername/stock-app:v1 .
docker tag yourdockerhubusername/stock-app:v1 yourdockerhubusername/stock-app:latest
```

### Push to Docker Hub

```bash
docker login
docker push yourdockerhubusername/stock-app:v1
docker push yourdockerhubusername/stock-app:latest
```

### Deployment on Lab Servers

#### Server Configuration
* **Web01 & Web02:** Application servers running the containerized stock app
* **Lb01:** Load balancer server running HAProxy

#### Deploy on Web Servers (Web01 & Web02)

1. **Pull and run the container:**
   ```bash
   docker pull yourdockerhubusername/stock-app:latest
   docker run -d --name stock-app -p 8080:8080 \
     -e ALPHA_VANTAGE_API_KEY="YOUR_ALPHA_VANTAGE_KEY" \
     -e NEWS_API_KEY="YOUR_NEWS_API_KEY" \
     yourdockerhubusername/stock-app:latest
   ```

#### HAProxy Configuration (Lb01)

Create `/etc/haproxy/haproxy.cfg`:

```
global
    daemon
    maxconn 4096

defaults
    mode http
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms

frontend stock_app_frontend
    bind *:80
    default_backend stock_app_servers

backend stock_app_servers
    balance roundrobin
    server web01 WEB01_IP:8080 check
    server web02 WEB02_IP:8080 check
```

Restart HAProxy:
```bash
sudo systemctl restart haproxy
```

## Part Two B: AWS Deployment

### Architecture Overview
* **ECS Fargate:** Container orchestration
* **Application Load Balancer:** Traffic distribution
* **ECR:** Container registry
* **VPC:** Network isolation

### Deployment Steps

1. **Push image to ECR:**
   ```bash
   aws ecr create-repository --repository-name stock-app
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
   docker tag yourdockerhubusername/stock-app:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/stock-app:latest
   docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/stock-app:latest
   ```

2. **Create ECS cluster and service**
3. **Configure Application Load Balancer**
4. **Set up environment variables in ECS task definition**

## API Endpoints

* `GET /` - Main application interface
* `GET /api/stock/<symbol>` - Get stock data for specific symbol
* `GET /api/news` - Get latest financial news
* `GET /api/news/<symbol>` - Get news for specific stock symbol

## Project Structure

```
Stock-Market-Data-News-Aggregator/
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── templates/
│   └── index.html
├── .env.example
├── .gitignore
├── app.py
├── Dockerfile
├── README.md
└── requirements.txt
```

## Environment Variables

* `ALPHA_VANTAGE_API_KEY` - API key for Alpha Vantage stock data
* `NEWS_API_KEY` - API key for NewsAPI.org
* `FLASK_ENV` - Flask environment (development/production)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.
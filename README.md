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
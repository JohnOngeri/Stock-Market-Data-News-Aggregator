# Stock Market Data & News Aggregator - Deployment Guide

## Prerequisites

- Docker and Docker Compose installed
- API keys from Alpha Vantage and NewsAPI
- Docker Hub account (for production deployment)

## Quick Deployment Options

### Option 1: Local Development

```bash
# 1. Setup environment
cp .env.example .env
# Edit .env with your API keys

# 2. Run locally
python app.py
# Access: http://localhost:8080
```

### Option 2: Docker Local

```bash
# 1. Build and run with Docker Compose
docker-compose up -d

# 2. Access application
# http://localhost:8080
```

### Option 3: Production Docker

```bash
# 1. Deploy to production
docker-compose -f docker-compose.prod.yml up -d
```

## Step-by-Step Deployment

### Step 1: Environment Setup

1. **Get API Keys:**
   - Alpha Vantage: <https://www.alphavantage.co/support/#api-key>
   - NewsAPI: <https://newsapi.org/register>

2. **Configure Environment:**

   ```bash
   cp .env.example .env
   ```

   Edit `.env`:

   ```env
   ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
   NEWS_API_KEY=your_news_api_key_here
   ```

### Step 2: Choose Deployment Method

#### A. Local Python Deployment

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python app.py

# Or use the startup script
# Windows: start.bat
# Linux/Mac: ./start.sh
```

**Access:** <http://localhost:8080>

#### B. Docker Development Deployment

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

#### C. Docker Production Deployment

```bash
# Production deployment
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Step 3: Docker Hub Deployment (Optional)

1. **Update deployment scripts:**
   - Edit `deploy.sh` or `deploy.bat`
   - Replace `your-dockerhub-username` with your Docker Hub username

2. **Login to Docker Hub:**

   ```bash
   docker login
   ```

3. **Deploy:**

   ```bash
   # Windows
   deploy.bat
   
   # Linux/Mac
   chmod +x deploy.sh
   ./deploy.sh
   ```

### Step 4: Multi-Server Production Setup

#### Server Architecture

- **Web01 & Web02:** Application servers
- **Load Balancer:** Nginx reverse proxy

#### Deploy on Application Servers (Web01, Web02)

1. **Pull and run:**

   ```bash
   docker pull your-dockerhub-username/stock-market-aggregator:latest
   
   docker run -d \
     --name stock-app \
     -p 8080:8080 \
     -e ALPHA_VANTAGE_API_KEY="your_key" \
     -e NEWS_API_KEY="your_key" \
     --restart unless-stopped \
     your-dockerhub-username/stock-market-aggregator:latest
   ```

#### Setup Load Balancer

1. **Install Nginx:**

   ```bash
   sudo apt update
   sudo apt install nginx
   ```

2. **Configure Nginx:**

   ```bash
   sudo cp nginx.conf /etc/nginx/sites-available/stock-app
   sudo ln -s /etc/nginx/sites-available/stock-app /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   ```

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ALPHA_VANTAGE_API_KEY` | Stock data API key | Required |
| `NEWS_API_KEY` | News API key | Required |
| `PORT` | Application port | 8080 |
| `FLASK_ENV` | Flask environment | production |

### Docker Compose Override

Create `docker-compose.override.yml` for custom settings:

```yaml
services:
  stock-app:
    ports:
      - "9000:8080"  # Custom port
    environment:
      - PORT=8080
```

## 🧪 Testing Deployment

### Health Check

```bash
curl http://localhost:8080/
```

### API Testing

```bash
# Test stock endpoint
curl http://localhost:8080/api/stock/AAPL

# Test news endpoint
curl http://localhost:8080/api/news

# Run test suite
python test_app.py
```

## 📊 Monitoring & Maintenance

### View Logs

```bash
# Docker Compose
docker-compose logs -f

# Single container
docker logs -f <container_name>
```

### Container Stats

```bash
docker stats
```

### Update Application

```bash
# Pull latest image
docker-compose pull

# Restart with new image
docker-compose up -d
```

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use:**

   ```bash
   # Change port in docker-compose.yml
   ports:
     - "9000:8080"
   ```

2. **API Key Errors:**
   - Verify `.env` file exists and contains valid keys
   - Check API key quotas and limits

3. **Docker Permission Issues:**

   ```bash
   # Add user to docker group (Linux)
   sudo usermod -aG docker $USER
   # Logout and login again
   ```

4. **Container Won't Start:**

   ```bash
   # Check logs
   docker logs <container_name>
   
   # Check container status
   docker ps -a
   ```

### Debug Mode

```bash
# Run in debug mode
docker run -it --rm \
  -p 8080:8080 \
  -e ALPHA_VANTAGE_API_KEY="your_key" \
  -e NEWS_API_KEY="your_key" \
  stock-market-aggregator python app.py
```

## 🔒 Security Considerations

1. **Environment Variables:**
   - Never commit `.env` files
   - Use Docker secrets in production
   - Rotate API keys regularly

2. **Network Security:**
   - Use HTTPS in production
   - Configure firewall rules
   - Limit API access

3. **Container Security:**
   - Run as non-root user (already configured)
   - Keep base images updated
   - Scan for vulnerabilities

## 📈 Scaling Options

### Horizontal Scaling

```bash
# Scale with Docker Compose
docker-compose up -d --scale stock-app=3
```

### Load Balancer Setup

```bash
# Use the load balancer compose file
docker-compose -f docker-compose.loadbalancer.yml up -d
```

## 🎯 Production Checklist

- [ ] API keys configured
- [ ] Environment variables set
- [ ] Health checks working
- [ ] Logs accessible
- [ ] Monitoring setup
- [ ] Backup strategy
- [ ] SSL certificates (if applicable)
- [ ] Firewall configured
- [ ] Load balancer tested
- [ ] Disaster recovery plan

## 📞 Support

If you encounter issues:

1. Check the logs first
2. Verify API keys and quotas
3. Test individual components
4. Review the troubleshooting section
5. Run the test suite: `python test_app.py`

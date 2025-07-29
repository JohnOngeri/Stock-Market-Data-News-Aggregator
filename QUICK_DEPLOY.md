# Quick Deployment Guide

## 🚀 5-Minute Setup

### Prerequisites

- Docker installed
- API keys ready

### Steps

1. **Clone & Setup**

   ```bash
   git clone <your-repo>
   cd Stock-Market-Data-News-Aggregator
   cp .env.example .env
   ```

2. **Add API Keys to .env**

   ```env
   ALPHA_VANTAGE_API_KEY=your_key_here
   NEWS_API_KEY=your_key_here
   ```

3. **Deploy**

   ```bash
   # Option A: Local Python
   pip install -r requirements.txt && python app.py
   
   # Option B: Docker
   docker-compose up -d
   
   # Option C: Production Docker
   docker-compose -f docker-compose.prod.yml up -d
   ```

4. **Access**
   - Open: <http://localhost:8080>
   - Test: `python test_app.py`

## 🔧 Commands Reference

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Logs
docker-compose logs -f

# Update
docker-compose pull && docker-compose up -d

# Test
python test_app.py
```

## 🚨 Troubleshooting

- **Port in use**: Change port in docker-compose.yml
- **API errors**: Check .env file and API quotas
- **Container issues**: Run `docker logs <container_name>`

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

# Docker Deployment Guide

## Prerequisites

1. Docker and Docker Compose installed on all servers
2. Docker Hub account
3. Access to Web01, Web02, and Load Balancer servers

## Step 1: Prepare for Deployment

1. **Update deployment scripts** with your Docker Hub username:
   - Edit `deploy.sh` and `deploy.bat`
   - Replace `your-dockerhub-username` with your actual Docker Hub username

2. **Login to Docker Hub**:

   ```bash
   docker login
   ```

## Step 2: Build and Push to Docker Hub

**On Windows:**

```cmd
deploy.bat
```

**On Linux/Mac:**

```bash
chmod +x deploy.sh
./deploy.sh
```

## Step 3: Deploy on Web Servers

**On Web01 and Web02:**

1. **Pull the image:**

   ```bash
   docker pull your-dockerhub-username/stock-market-aggregator:latest
   ```

2. **Create .env file** with your API keys:

   ```bash
   ALPHA_VANTAGE_API_KEY=your_key_here
   NEWS_API_KEY=your_key_here
   ```

3. **Deploy the container:**

   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

## Step 4: Configure Load Balancer

1. **Install Nginx** on load balancer server
2. **Copy nginx.conf** to `/etc/nginx/sites-available/stock-app`
3. **Enable the site:**

   ```bash
   sudo ln -s /etc/nginx/sites-available/stock-app /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   ```

## Step 5: Verify Deployment

1. **Check container health:**

   ```bash
   docker ps
   docker logs <container_id>
   ```

2. **Test endpoints:**
   - [http://web01:8080/](http://web01:8080/)
   - [http://web02:8080/](http://web02:8080/)
   - [http://load-balancer/](http://load-balancer/)

## Monitoring Commands

```bash
# View logs
docker logs -f <container_name>

# Check resource usage
docker stats

# Health check
curl http://localhost:8080/
```

## Updating the Application

1. Make code changes
2. Run deployment script to build and push new image
3. On each server: `docker-compose -f docker-compose.prod.yml pull && docker-compose -f docker-compose.prod.yml up -d`

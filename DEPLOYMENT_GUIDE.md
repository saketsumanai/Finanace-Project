# 🚀 Deployment Guide

Complete guide for deploying the Oil & Gas M&A Valuation Platform to production.

## 📋 Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Environment Setup](#environment-setup)
3. [Deployment Options](#deployment-options)
4. [Post-Deployment](#post-deployment)
5. [Monitoring & Maintenance](#monitoring--maintenance)

---

## ✅ Pre-Deployment Checklist

### Security
- [ ] Change all default passwords
- [ ] Generate strong SECRET_KEY
- [ ] Configure CORS for production domain
- [ ] Enable HTTPS/SSL
- [ ] Set up firewall rules
- [ ] Review API rate limits
- [ ] Enable security headers

### Configuration
- [ ] Set ENVIRONMENT=production
- [ ] Configure production database
- [ ] Set up Redis for production
- [ ] Add production API keys (Gemini, Alpha Vantage)
- [ ] Configure Firebase for production domain
- [ ] Set up email service (optional)
- [ ] Configure backup strategy

### Testing
- [ ] Run all backend tests
- [ ] Run all frontend tests
- [ ] Test authentication flows
- [ ] Test file uploads
- [ ] Test AI features
- [ ] Load testing completed
- [ ] Security audit completed

### Infrastructure
- [ ] Domain name registered
- [ ] SSL certificate obtained
- [ ] Cloud provider account set up
- [ ] Database provisioned
- [ ] Redis instance provisioned
- [ ] Storage for uploads configured
- [ ] CDN configured (optional)

---

## 🔧 Environment Setup

### 1. Production Environment Variables

Create `.env.production`:

```bash
# Database (Use managed PostgreSQL)
DATABASE_URL=postgresql://user:password@your-db-host:5432/valuation_db

# Redis (Use managed Redis)
REDIS_URL=redis://your-redis-host:6379/0

# Security
SECRET_KEY=generate-a-very-long-random-string-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Application
ENVIRONMENT=production
PROJECT_NAME=Oil & Gas M&A Valuation Platform
VERSION=1.0.0
API_V1_PREFIX=/api/v1

# CORS (Your production domain)
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Firebase
FIREBASE_PROJECT_ID=your-production-project-id
FIREBASE_API_KEY=your-production-api-key
FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
FIREBASE_STORAGE_BUCKET=your-project.appspot.com
FIREBASE_MESSAGING_SENDER_ID=your-sender-id
FIREBASE_APP_ID=your-app-id

# AI Services
GEMINI_API_KEY=your-production-gemini-key
ALPHA_VANTAGE_API_KEY=your-production-alpha-vantage-key

# File Upload
MAX_UPLOAD_SIZE=52428800
UPLOAD_DIR=/var/uploads

# Celery
CELERY_BROKER_URL=redis://your-redis-host:6379/0
CELERY_RESULT_BACKEND=redis://your-redis-host:6379/0
```

### 2. Generate Secure SECRET_KEY

```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

---

## 🌐 Deployment Options

### Option 1: Docker Compose on VPS (Recommended for Small-Medium Scale)

**Best for**: DigitalOcean, Linode, AWS EC2, Google Compute Engine

#### Step 1: Provision Server

```bash
# Minimum requirements:
# - 2 CPU cores
# - 4GB RAM
# - 50GB SSD
# - Ubuntu 22.04 LTS

# SSH into your server
ssh root@your-server-ip
```

#### Step 2: Install Dependencies

```bash
# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt install docker-compose -y

# Install Nginx
apt install nginx -y

# Install Certbot for SSL
apt install certbot python3-certbot-nginx -y
```

#### Step 3: Clone Repository

```bash
# Create app directory
mkdir -p /opt/valuation-platform
cd /opt/valuation-platform

# Clone your repository
git clone https://github.com/yourusername/oil-gas-valuation-platform.git .

# Copy and configure environment
cp .env.example .env
nano .env  # Edit with production values
```

#### Step 4: Create Production Docker Compose

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: valuation_postgres_prod
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: valuation_redis_prod
    restart: always
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: valuation_backend_prod
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - SECRET_KEY=${SECRET_KEY}
      - ENVIRONMENT=production
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - ALPHA_VANTAGE_API_KEY=${ALPHA_VANTAGE_API_KEY}
    volumes:
      - ./uploads:/app/uploads
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: always

  celery_worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: valuation_celery_prod
    command: celery -A app.tasks.celery_app worker --loglevel=info
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - CELERY_BROKER_URL=${CELERY_BROKER_URL}
    depends_on:
      - redis
      - postgres
    restart: always

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      args:
        - VITE_API_URL=https://yourdomain.com/api
    container_name: valuation_frontend_prod
    restart: always

volumes:
  postgres_data:
```

#### Step 5: Configure Nginx

Create `/etc/nginx/sites-available/valuation-platform`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:5173;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Increase timeouts for long-running requests
        proxy_connect_timeout 600;
        proxy_send_timeout 600;
        proxy_read_timeout 600;
        send_timeout 600;
    }

    # File uploads
    client_max_body_size 50M;
}
```

Enable the site:

```bash
ln -s /etc/nginx/sites-available/valuation-platform /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

#### Step 6: Set Up SSL

```bash
certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

#### Step 7: Deploy

```bash
# Build and start services
docker-compose -f docker-compose.prod.yml up -d --build

# Run database migrations
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head

# Check logs
docker-compose -f docker-compose.prod.yml logs -f
```

#### Step 8: Set Up Auto-Restart

Create `/etc/systemd/system/valuation-platform.service`:

```ini
[Unit]
Description=Valuation Platform
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/valuation-platform
ExecStart=/usr/bin/docker-compose -f docker-compose.prod.yml up -d
ExecStop=/usr/bin/docker-compose -f docker-compose.prod.yml down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
systemctl enable valuation-platform
systemctl start valuation-platform
```

---

### Option 2: AWS Deployment

#### Using AWS ECS/Fargate

1. **Create ECR Repositories**
```bash
aws ecr create-repository --repository-name valuation-backend
aws ecr create-repository --repository-name valuation-frontend
```

2. **Build and Push Images**
```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com

# Build and push backend
docker build -t valuation-backend ./backend
docker tag valuation-backend:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/valuation-backend:latest
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/valuation-backend:latest

# Build and push frontend
docker build -t valuation-frontend ./frontend
docker tag valuation-frontend:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/valuation-frontend:latest
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/valuation-frontend:latest
```

3. **Create RDS PostgreSQL Instance**
4. **Create ElastiCache Redis Cluster**
5. **Create ECS Cluster and Task Definitions**
6. **Set up Application Load Balancer**
7. **Configure Route 53 for DNS**

---

### Option 3: Google Cloud Run

```bash
# Build and deploy backend
gcloud builds submit --tag gcr.io/PROJECT_ID/valuation-backend ./backend
gcloud run deploy valuation-backend --image gcr.io/PROJECT_ID/valuation-backend --platform managed

# Build and deploy frontend
gcloud builds submit --tag gcr.io/PROJECT_ID/valuation-frontend ./frontend
gcloud run deploy valuation-frontend --image gcr.io/PROJECT_ID/valuation-frontend --platform managed
```

---

### Option 4: Heroku

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Add Redis
heroku addons:create heroku-redis:hobby-dev

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set GEMINI_API_KEY=your-key
heroku config:set ALPHA_VANTAGE_API_KEY=your-key

# Deploy
git push heroku main
```

---

## 🔍 Post-Deployment

### 1. Verify Deployment

```bash
# Check backend health
curl https://yourdomain.com/health

# Check API docs
curl https://yourdomain.com/api/v1/docs

# Test authentication
curl -X POST https://yourdomain.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!","full_name":"Test User"}'
```

### 2. Set Up Monitoring

#### Install Monitoring Tools

```bash
# Prometheus + Grafana
docker-compose -f monitoring/docker-compose.yml up -d

# Or use cloud services:
# - AWS CloudWatch
# - Google Cloud Monitoring
# - Datadog
# - New Relic
```

### 3. Configure Backups

```bash
# Database backup script
cat > /opt/backup-db.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker exec valuation_postgres_prod pg_dump -U postgres valuation_db > /backups/db_$DATE.sql
# Keep only last 30 days
find /backups -name "db_*.sql" -mtime +30 -delete
EOF

chmod +x /opt/backup-db.sh

# Add to crontab (daily at 2 AM)
echo "0 2 * * * /opt/backup-db.sh" | crontab -
```

### 4. Set Up Log Rotation

```bash
cat > /etc/logrotate.d/valuation-platform << 'EOF'
/var/log/valuation-platform/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 root root
    sharedscripts
}
EOF
```

---

## 📊 Monitoring & Maintenance

### Health Checks

```bash
# Backend health
curl https://yourdomain.com/health

# Database connection
docker exec valuation_postgres_prod pg_isready

# Redis connection
docker exec valuation_redis_prod redis-cli ping
```

### View Logs

```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f backend

# Last 100 lines
docker-compose -f docker-compose.prod.yml logs --tail=100 backend
```

### Update Deployment

```bash
# Pull latest code
cd /opt/valuation-platform
git pull origin main

# Rebuild and restart
docker-compose -f docker-compose.prod.yml up -d --build

# Run migrations
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

### Database Migrations

```bash
# Create new migration
docker-compose -f docker-compose.prod.yml exec backend alembic revision --autogenerate -m "description"

# Apply migrations
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head

# Rollback migration
docker-compose -f docker-compose.prod.yml exec backend alembic downgrade -1
```

---

## 🔒 Security Best Practices

1. **Keep secrets secure** - Use environment variables, never commit secrets
2. **Enable HTTPS** - Always use SSL/TLS in production
3. **Regular updates** - Keep dependencies and OS updated
4. **Firewall rules** - Only expose necessary ports (80, 443)
5. **Database security** - Use strong passwords, enable SSL connections
6. **Rate limiting** - Implement API rate limiting
7. **Monitoring** - Set up alerts for suspicious activity
8. **Backups** - Regular automated backups with tested restore procedures
9. **Access control** - Limit SSH access, use key-based authentication
10. **Security headers** - Enable HSTS, CSP, X-Frame-Options

---

## 🆘 Troubleshooting

### Service Won't Start

```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs backend

# Check container status
docker ps -a

# Restart service
docker-compose -f docker-compose.prod.yml restart backend
```

### Database Connection Issues

```bash
# Test database connection
docker exec valuation_postgres_prod psql -U postgres -d valuation_db -c "SELECT 1"

# Check DATABASE_URL
docker-compose -f docker-compose.prod.yml exec backend env | grep DATABASE_URL
```

### High Memory Usage

```bash
# Check resource usage
docker stats

# Restart services
docker-compose -f docker-compose.prod.yml restart
```

### SSL Certificate Issues

```bash
# Renew certificate
certbot renew

# Test renewal
certbot renew --dry-run
```

---

## 📞 Support

For deployment issues:
- Check logs first
- Review this guide
- Open GitHub issue
- Contact support team

---

**🎉 Congratulations! Your platform is now deployed!**

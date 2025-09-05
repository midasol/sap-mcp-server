# SAP Gateway MCP Server - Deployment Guide

This guide covers deployment strategies for the SAP Gateway MCP Server across different environments.

## 🎯 Deployment Overview

The SAP Gateway MCP Server supports multiple deployment options:

1. **Google Cloud Run** - Serverless, auto-scaling (Recommended for production)
2. **Docker/Container** - Portable containerized deployment
3. **Virtual Machine** - Traditional VM deployment with systemd
4. **Kubernetes** - Container orchestration for enterprise scale
5. **Local Development** - Local development and testing

## ☁️ Google Cloud Run Deployment

### Prerequisites

- Google Cloud Platform account with billing enabled
- Google Cloud SDK installed (`gcloud`)
- Docker installed locally
- Project with appropriate permissions

### Step 1: Setup and Configuration

```bash
# Authenticate with Google Cloud
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### Step 2: Build and Push Container

```bash
# Build the container image
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/sap-mcp-server:latest

# Or build locally and push
docker build -t gcr.io/YOUR_PROJECT_ID/sap-mcp-server:latest .
docker push gcr.io/YOUR_PROJECT_ID/sap-mcp-server:latest
```

### Step 3: Create Secret Manager Secrets

```bash
# Create secrets for sensitive data
gcloud secrets create sap-host --data-file=<(echo \"your-sap-host.com\")
gcloud secrets create sap-username --data-file=<(echo \"your-username\")
gcloud secrets create sap-password --data-file=<(echo \"your-password\")
```

### Step 4: Deploy to Cloud Run

```bash
# Deploy with environment variables
gcloud run deploy sap-mcp-server \\
  --image gcr.io/YOUR_PROJECT_ID/sap-mcp-server:latest \\
  --platform managed \\
  --region us-central1 \\
  --allow-unauthenticated \\
  --memory 1Gi \\
  --cpu 1 \\
  --max-instances 10 \\
  --min-instances 1 \\
  --port 8000 \\
  --timeout 300 \\
  --set-env-vars \"MCP_HOST=0.0.0.0,MCP_PORT=8000,LOG_LEVEL=INFO\" \\
  --set-secrets \"SAP_HOST=sap-host:latest,SAP_USERNAME=sap-username:latest,SAP_PASSWORD=sap-password:latest\"
```

### Step 5: Configure Custom Domain (Optional)

```bash
# Map custom domain
gcloud run domain-mappings create \\
  --service sap-mcp-server \\
  --domain api.yourcompany.com \\
  --region us-central1
```

### Cloud Run Configuration Template

Create `cloudrun.yaml`:

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: sap-mcp-server
  annotations:
    run.googleapis.com/ingress: all
    run.googleapis.com/execution-environment: gen2
spec:
  template:
    metadata:
      annotations:
        # Scaling
        autoscaling.knative.dev/maxScale: \"10\"
        autoscaling.knative.dev/minScale: \"1\"
        
        # Resources
        run.googleapis.com/memory: \"1Gi\"
        run.googleapis.com/cpu: \"1\"
        run.googleapis.com/cpu-throttling: \"false\"
        
        # Networking
        run.googleapis.com/vpc-access-connector: projects/YOUR_PROJECT_ID/locations/us-central1/connectors/YOUR_CONNECTOR
        
        # Security
        run.googleapis.com/service-account: sap-mcp-service@YOUR_PROJECT_ID.iam.gserviceaccount.com
    spec:
      containerConcurrency: 100
      timeoutSeconds: 300
      containers:
      - image: gcr.io/YOUR_PROJECT_ID/sap-mcp-server:latest
        ports:
        - name: http1
          containerPort: 8000
        env:
        - name: MCP_HOST
          value: \"0.0.0.0\"
        - name: MCP_PORT
          value: \"8000\"
        - name: LOG_LEVEL
          value: \"INFO\"
        - name: SAP_HOST
          valueFrom:
            secretKeyRef:
              name: sap-host
              key: latest
        - name: SAP_USERNAME
          valueFrom:
            secretKeyRef:
              name: sap-username
              key: latest
        - name: SAP_PASSWORD
          valueFrom:
            secretKeyRef:
              name: sap-password
              key: latest
        resources:
          limits:
            memory: \"1Gi\"
            cpu: \"1000m\"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 30
          timeoutSeconds: 5
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
```

Deploy with YAML:
```bash
gcloud run services replace cloudrun.yaml --region us-central1
```

## 🐳 Docker/Container Deployment

### Single Container

```bash
# Build image
docker build -t sap-mcp-server:latest .

# Run container
docker run -d \\
  --name sap-mcp-server \\
  --restart unless-stopped \\
  -p 8000:8000 \\
  --env-file .env \\
  --health-cmd=\"curl -f http://localhost:8000/health || exit 1\" \\
  --health-interval=30s \\
  --health-timeout=10s \\
  --health-retries=3 \\
  sap-mcp-server:latest
```

### Docker Compose Production

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  sap-mcp-server:
    build:
      context: .
      dockerfile: Dockerfile
    image: sap-mcp-server:latest
    container_name: sap-mcp-server
    restart: unless-stopped
    ports:
      - \"8000:8000\"
    environment:
      - SAP_HOST=${SAP_HOST}
      - SAP_USERNAME=${SAP_USERNAME}
      - SAP_PASSWORD=${SAP_PASSWORD}
      - MCP_HOST=0.0.0.0
      - MCP_PORT=8000
      - LOG_LEVEL=INFO
    volumes:
      - ./logs:/app/logs
      - ./config:/app/config:ro
    networks:
      - sap-mcp-network
    healthcheck:
      test: [\"CMD\", \"curl\", \"-f\", \"http://localhost:8000/health\"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    logging:
      driver: \"json-file\"
      options:
        max-size: \"100m\"
        max-file: \"5\"

  # Reverse proxy with SSL termination
  nginx:
    image: nginx:alpine
    container_name: sap-mcp-nginx
    restart: unless-stopped
    ports:
      - \"80:80\"
      - \"443:443\"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    networks:
      - sap-mcp-network
    depends_on:
      - sap-mcp-server

  # Monitoring
  prometheus:
    image: prom/prometheus:latest
    container_name: sap-mcp-prometheus
    restart: unless-stopped
    ports:
      - \"9090:9090\"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    networks:
      - sap-mcp-network

  grafana:
    image: grafana/grafana:latest
    container_name: sap-mcp-grafana
    restart: unless-stopped
    ports:
      - \"3000:3000\"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana:/etc/grafana/provisioning:ro
    networks:
      - sap-mcp-network
    depends_on:
      - prometheus

networks:
  sap-mcp-network:
    driver: bridge

volumes:
  prometheus_data:
  grafana_data:
```

Deploy:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 🖥️ Virtual Machine Deployment

### System Requirements

- **OS**: Ubuntu 20.04+ / CentOS 8+ / RHEL 8+
- **CPU**: 2+ cores
- **Memory**: 4GB+ RAM
- **Storage**: 20GB+ available space
- **Network**: Outbound HTTPS (443) to SAP servers

### Installation Script

Create `install.sh`:

```bash
#!/bin/bash
set -e

# Configuration
APP_USER=\"sapmcp\"
APP_DIR=\"/opt/sap-mcp\"
SERVICE_NAME=\"sap-mcp\"
PYTHON_VERSION=\"3.11\"

echo \"Installing SAP MCP Server...\"

# Update system
apt-get update && apt-get upgrade -y

# Install system dependencies
apt-get install -y \\
    python${PYTHON_VERSION} \\
    python${PYTHON_VERSION}-venv \\
    python${PYTHON_VERSION}-dev \\
    build-essential \\
    curl \\
    nginx \\
    certbot \\
    python3-certbot-nginx \\
    supervisor

# Create application user
if ! id \"$APP_USER\" &>/dev/null; then
    useradd --system --home $APP_DIR --shell /bin/false $APP_USER
fi

# Create application directory
mkdir -p $APP_DIR
cd $APP_DIR

# Download and extract application
curl -L https://github.com/company/sap-mcp/archive/main.tar.gz | tar xz --strip-components=1

# Create virtual environment
python${PYTHON_VERSION} -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create configuration
cp .env.example .env
echo \"Please edit $APP_DIR/.env with your SAP configuration\"

# Set permissions
chown -R $APP_USER:$APP_USER $APP_DIR
chmod +x $APP_DIR/venv/bin/*

# Create systemd service
cat > /etc/systemd/system/${SERVICE_NAME}.service << EOF
[Unit]
Description=SAP Gateway MCP Server
After=network.target

[Service]
Type=simple
User=$APP_USER
Group=$APP_USER
WorkingDirectory=$APP_DIR
Environment=PATH=$APP_DIR/venv/bin
EnvironmentFile=$APP_DIR/.env
ExecStart=$APP_DIR/venv/bin/python -m sap_mcp.server
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=$APP_DIR/logs

[Install]
WantedBy=multi-user.target
EOF

# Create log directory
mkdir -p $APP_DIR/logs
chown $APP_USER:$APP_USER $APP_DIR/logs

# Configure nginx
cat > /etc/nginx/sites-available/${SERVICE_NAME} << EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \\$host;
        proxy_set_header X-Real-IP \\$remote_addr;
        proxy_set_header X-Forwarded-For \\$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \\$scheme;
        
        # Health check optimization
        location /health {
            proxy_pass http://127.0.0.1:8000/health;
            access_log off;
        }
    }
}
EOF

# Enable nginx site
ln -sf /etc/nginx/sites-available/${SERVICE_NAME} /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl restart nginx

# Enable and start service
systemctl daemon-reload
systemctl enable ${SERVICE_NAME}
systemctl enable nginx

echo \"Installation complete!\"
echo \"1. Edit configuration: $APP_DIR/.env\"
echo \"2. Start service: systemctl start ${SERVICE_NAME}\"
echo \"3. Check status: systemctl status ${SERVICE_NAME}\"
echo \"4. View logs: journalctl -u ${SERVICE_NAME} -f\"
```

Run installation:
```bash
chmod +x install.sh
sudo ./install.sh
```

### Configuration and Startup

```bash
# Edit configuration
sudo nano /opt/sap-mcp/.env

# Start services
sudo systemctl start sap-mcp
sudo systemctl start nginx

# Enable auto-start
sudo systemctl enable sap-mcp
sudo systemctl enable nginx

# Check status
sudo systemctl status sap-mcp
sudo systemctl status nginx
```

### SSL Certificate Setup

```bash
# Install SSL certificate
sudo certbot --nginx -d api.yourcompany.com

# Auto-renewal test
sudo certbot renew --dry-run
```

## ⚙️ Kubernetes Deployment

### Namespace and ConfigMap

```yaml
# kubernetes/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: sap-mcp

---
# kubernetes/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: sap-mcp-config
  namespace: sap-mcp
data:
  MCP_HOST: \"0.0.0.0\"
  MCP_PORT: \"8000\"
  LOG_LEVEL: \"INFO\"
  SAP_PORT: \"44300\"
  SAP_CLIENT: \"100\"
  SAP_VERIFY_SSL: \"true\"
```

### Secrets

```yaml
# kubernetes/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: sap-mcp-secrets
  namespace: sap-mcp
type: Opaque
data:
  sap-host: <base64-encoded-host>
  sap-username: <base64-encoded-username>
  sap-password: <base64-encoded-password>
```

### Deployment

```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sap-mcp-server
  namespace: sap-mcp
  labels:
    app: sap-mcp-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: sap-mcp-server
  template:
    metadata:
      labels:
        app: sap-mcp-server
    spec:
      containers:
      - name: sap-mcp-server
        image: gcr.io/YOUR_PROJECT_ID/sap-mcp-server:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: sap-mcp-config
        env:
        - name: SAP_HOST
          valueFrom:
            secretKeyRef:
              name: sap-mcp-secrets
              key: sap-host
        - name: SAP_USERNAME
          valueFrom:
            secretKeyRef:
              name: sap-mcp-secrets
              key: sap-username
        - name: SAP_PASSWORD
          valueFrom:
            secretKeyRef:
              name: sap-mcp-secrets
              key: sap-password
        resources:
          requests:
            memory: \"512Mi\"
            cpu: \"500m\"
          limits:
            memory: \"1Gi\"
            cpu: \"1000m\"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
```

### Service and Ingress

```yaml
# kubernetes/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: sap-mcp-service
  namespace: sap-mcp
spec:
  selector:
    app: sap-mcp-server
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: ClusterIP

---
# kubernetes/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: sap-mcp-ingress
  namespace: sap-mcp
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    cert-manager.io/cluster-issuer: \"letsencrypt-prod\"
spec:
  tls:
  - hosts:
    - api.yourcompany.com
    secretName: sap-mcp-tls
  rules:
  - host: api.yourcompany.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: sap-mcp-service
            port:
              number: 80
```

Deploy to Kubernetes:
```bash
kubectl apply -f kubernetes/
```

## 🎛️ Configuration Management

### Environment-Specific Configuration

Create environment-specific configuration files:

```bash
# environments/development/.env
SAP_HOST=dev-sap.company.com
LOG_LEVEL=DEBUG
MCP_DEBUG=true

# environments/staging/.env
SAP_HOST=staging-sap.company.com
LOG_LEVEL=INFO
MCP_DEBUG=false

# environments/production/.env
SAP_HOST=prod-sap.company.com
LOG_LEVEL=WARNING
MCP_DEBUG=false
SECURITY_RATE_LIMIT_PER_MINUTE=30
```

### Configuration Validation

Create validation script:

```bash
#!/bin/bash
# validate-config.sh

echo \"Validating configuration...\"

# Check required environment variables
required_vars=(\"SAP_HOST\" \"SAP_USERNAME\" \"SAP_PASSWORD\")
for var in \"${required_vars[@]}\"; do
    if [[ -z \"${!var}\" ]]; then
        echo \"ERROR: $var is not set\"
        exit 1
    fi
done

# Test SAP connectivity
python3 -c \"
import os
import sys
from src.sap_mcp.sap.client import SAPClient
import asyncio

async def test_connection():
    try:
        client = SAPClient()
        result = await client.test_connection()
        print('SAP connection test: PASSED')
        return True
    except Exception as e:
        print(f'SAP connection test: FAILED - {e}')
        return False

if not asyncio.run(test_connection()):
    sys.exit(1)
\"

echo \"Configuration validation: PASSED\"
```

## 📊 Monitoring and Observability

### Health Checks

```bash
# Basic health check
curl -f http://localhost:8000/health

# Detailed health check
curl -f http://localhost:8000/health/detailed

# Readiness check
curl -f http://localhost:8000/ready
```

### Prometheus Configuration

Create `monitoring/prometheus.yml`:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'sap-mcp-server'
    static_configs:
      - targets: ['sap-mcp-server:8000']
    metrics_path: '/metrics'
    scrape_interval: 5s
```

### Grafana Dashboard

Create monitoring dashboard with key metrics:

- Request rate and error rate
- Response time percentiles
- Active connections and sessions
- Memory and CPU usage
- SAP-specific metrics

## 🚨 Troubleshooting

### Common Issues

1. **Connection Refused**
   ```bash
   # Check if service is running
   systemctl status sap-mcp
   
   # Check logs
   journalctl -u sap-mcp -f
   
   # Check port binding
   netstat -tlnp | grep 8000
   ```

2. **SAP Authentication Failed**
   ```bash
   # Verify credentials
   echo $SAP_USERNAME
   echo $SAP_PASSWORD
   
   # Test SAP connectivity
   curl -k https://$SAP_HOST:$SAP_PORT/sap/opu/odata/
   ```

3. **High Memory Usage**
   ```bash
   # Check memory usage
   docker stats sap-mcp-server
   
   # Restart with memory limit
   docker update --memory=1g sap-mcp-server
   ```

### Log Analysis

```bash
# View application logs
docker logs -f sap-mcp-server

# Filter error logs
docker logs sap-mcp-server 2>&1 | grep ERROR

# View system logs
journalctl -u sap-mcp -f --since \"1 hour ago\"
```

This deployment guide provides comprehensive coverage for deploying the SAP Gateway MCP Server across various environments with proper configuration, monitoring, and troubleshooting procedures.
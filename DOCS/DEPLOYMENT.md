# DATA_SCOUT — Deployment Guide

**Version:** 1.0 | **Last Updated:** 2026-02-20

---

## 1. Docker Setup

### 1.1 Service Architecture

```
docker-compose.yml
├── frontend        (React via Nginx)       :3000
├── backend         (FastAPI + Uvicorn)      :8000
├── celery-worker   (ML + Data workers)      —
├── celery-beat     (Scheduled tasks)        —
├── redis           (Broker + Cache)         :6379
├── postgres        (Metadata DB)            :5432
├── minio           (Object storage)         :9000
└── nginx           (Reverse proxy)          :80/:443
```

### 1.2 docker-compose.yml

```yaml
version: "3.9"

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    environment:
      - VITE_API_URL=http://localhost/api/v1
    depends_on:
      - backend

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
    environment:
      - DATABASE_URL=postgresql://ds_user:ds_pass@postgres:5432/datascout
      - REDIS_URL=redis://redis:6379/0
      - MINIO_ENDPOINT=minio:9000
      - MINIO_ACCESS_KEY=${MINIO_ACCESS_KEY}
      - MINIO_SECRET_KEY=${MINIO_SECRET_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - JWT_SECRET=${JWT_SECRET}
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - model_storage:/app/storage

  celery-worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: >
      celery -A app.workers.celery_app worker
      --queues=ml_queue,data_queue,report_queue
      --concurrency=4 --loglevel=info
    environment:
      - DATABASE_URL=postgresql://ds_user:ds_pass@postgres:5432/datascout
      - REDIS_URL=redis://redis:6379/0
      - MINIO_ENDPOINT=minio:9000
    depends_on:
      - redis
      - postgres
    volumes:
      - model_storage:/app/storage

  redis:
    image: redis:7-alpine
    command: redis-server --maxmemory 512mb --maxmemory-policy allkeys-lru
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      retries: 3
    volumes:
      - redis_data:/data

  postgres:
    image: postgres:16-alpine
    environment:
      - POSTGRES_DB=datascout
      - POSTGRES_USER=ds_user
      - POSTGRES_PASSWORD=ds_pass
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ds_user -d datascout"]
      interval: 10s
      retries: 5
    volumes:
      - pg_data:/var/lib/postgresql/data

  minio:
    image: minio/minio:latest
    command: server /data --console-address ":9001"
    environment:
      - MINIO_ROOT_USER=${MINIO_ACCESS_KEY}
      - MINIO_ROOT_PASSWORD=${MINIO_SECRET_KEY}
    volumes:
      - minio_data:/data

  nginx:
    image: nginx:1.25-alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/certs:/etc/nginx/certs:ro
    depends_on:
      - frontend
      - backend

volumes:
  pg_data:
  redis_data:
  minio_data:
  model_storage:
```

### 1.3 Backend Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 1.4 Frontend Dockerfile

```dockerfile
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:1.25-alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 3000
```

---

## 2. CI/CD Pipeline

### 2.1 GitHub Actions — CI

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint-and-test-backend:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_pass
        ports: ["5432:5432"]
      redis:
        image: redis:7-alpine
        ports: ["6379:6379"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install -r backend/requirements.txt
      - run: cd backend && ruff check . && ruff format --check .
      - run: cd backend && pytest tests/ -v --cov=app --cov-report=xml
      - uses: codecov/codecov-action@v4

  lint-and-test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: "20" }
      - run: cd frontend && npm ci
      - run: cd frontend && npm run lint
      - run: cd frontend && npm test -- --coverage

  build-images:
    needs: [lint-and-test-backend, lint-and-test-frontend]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - run: docker compose build
```

### 2.2 GitHub Actions — Deploy

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - run: |
          docker compose build
          docker compose push
      - name: Deploy to server
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /opt/datascout
            docker compose pull
            docker compose up -d --remove-orphans
            docker system prune -f
```

---

## 3. Cloud Architecture (AWS)

```
                   ┌───────────────┐
                   │   Route 53    │
                   │   (DNS)       │
                   └───────┬───────┘
                           │
                   ┌───────▼───────┐
                   │  CloudFront   │
                   │  (CDN)        │
                   └───────┬───────┘
                           │
              ┌────────────┼────────────┐
              │                         │
    ┌─────────▼─────────┐   ┌──────────▼──────────┐
    │    S3 Bucket       │   │    ALB               │
    │  (React static)   │   │  (API load balancer) │
    └───────────────────┘   └──────────┬──────────┘
                                       │
                            ┌──────────▼──────────┐
                            │   ECS Fargate        │
                            │  ┌────────────────┐  │
                            │  │  FastAPI (x3)  │  │
                            │  ├────────────────┤  │
                            │  │  Celery (x3)   │  │
                            │  └────────────────┘  │
                            └──────────────────────┘
                                       │
              ┌────────────┬───────────┼───────────┐
              │            │                       │
    ┌─────────▼──┐  ┌──────▼──────┐  ┌────────────▼─┐
    │   RDS      │  │ ElastiCache │  │     S3       │
    │ PostgreSQL │  │   Redis     │  │ (files,      │
    │            │  │             │  │  models)     │
    └────────────┘  └─────────────┘  └──────────────┘
```

### 3.1 AWS Resource Estimates (MVP)

| Service | Spec | Estimated Monthly Cost |
|---|---|---|
| ECS Fargate (API) | 3 × 1 vCPU, 2GB | ~$90 |
| ECS Fargate (Workers) | 3 × 2 vCPU, 4GB | ~$180 |
| RDS PostgreSQL | db.t3.medium, 100GB | ~$70 |
| ElastiCache Redis | cache.t3.small | ~$25 |
| S3 | 500GB storage | ~$12 |
| ALB | 1 instance | ~$25 |
| CloudFront | 100GB transfer | ~$10 |
| **Total** | | **~$412/month** |

---

## 4. Monitoring & Logging

### 4.1 Logging Stack

```
Application → Structured JSON logs → stdout → Docker log driver
    → CloudWatch Logs (AWS) / Loki (self-hosted)
    → Grafana dashboards
```

**Log format:**
```json
{
  "timestamp": "2026-02-20T12:05:30Z",
  "level": "INFO",
  "service": "backend",
  "request_id": "req_d4e5f6",
  "user_id": "usr_abc123",
  "message": "Dataset cleaned successfully",
  "extra": { "dataset_id": "ds_7f3a2b", "duration_ms": 4520 }
}
```

### 4.2 Metrics

| Metric | Source | Alert Threshold |
|---|---|---|
| API response time (p95) | FastAPI middleware | > 3s |
| Error rate (5xx) | Nginx access log | > 5% over 5 min |
| Celery queue depth | Redis `llen` | > 20 tasks |
| Worker task failure rate | Celery events | > 10% |
| CPU utilization | Container metrics | > 85% for 10 min |
| Memory utilization | Container metrics | > 90% |
| Disk usage (S3/MinIO) | Storage metrics | > 80% capacity |
| LLM API latency | RAGService timing | > 10s (p95) |

### 4.3 Health Checks

```python
# backend/app/api/v1/routers/health.py
@router.get("/health")
async def health_check():
    checks = {
        "database": await check_postgres(),
        "redis": await check_redis(),
        "storage": await check_minio(),
    }
    status = "healthy" if all(checks.values()) else "degraded"
    return {"status": status, "checks": checks, "version": settings.APP_VERSION}
```

### 4.4 Alerting

| Channel | When |
|---|---|
| Slack/Discord | Warning-level alerts (queue depth, high latency) |
| PagerDuty/Email | Critical alerts (service down, error rate spike) |
| Dashboard | All metrics visible in Grafana |

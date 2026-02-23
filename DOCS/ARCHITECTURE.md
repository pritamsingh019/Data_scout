# DATA_SCOUT — System Architecture

**Version:** 1.0 | **Last Updated:** 2026-02-20

---

## 1. High-Level Architecture

```
┌────────────────────────────────────────────────────────────┐
│                     CLIENT TIER                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                React SPA (Vite)                       │  │
│  │  Upload │ Data Preview │ ML Dashboard │ Chat │ Report │  │
│  └──────────────────────┬───────────────────────────────┘  │
└─────────────────────────┼──────────────────────────────────┘
                          │  HTTPS / WebSocket
┌─────────────────────────┼──────────────────────────────────┐
│                    API GATEWAY                              │
│            Nginx (SSL, Rate Limiting)                       │
└─────────────────────────┼──────────────────────────────────┘
                          │
┌─────────────────────────┼──────────────────────────────────┐
│                  APPLICATION TIER                           │
│  ┌──────────────────────▼───────────────────────────────┐  │
│  │              FastAPI Application                      │  │
│  │  Routers: upload │ data │ ml │ chat │ report │ auth   │  │
│  │  Services: DataService │ MLService │ RAGService       │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
         │                    │                    │
┌────────▼────────┐ ┌────────▼────────┐ ┌────────▼────────┐
│  STORAGE TIER   │ │  WORKER TIER    │ │ EXTERNAL APIs   │
│ PostgreSQL (meta)│ │ Celery Workers  │ │ OpenAI API      │
│ Redis (cache)   │ │  - ML Training  │ │ Anthropic API   │
│ FAISS (vectors) │ │  - Data Clean   │ │ Google AI API   │
│ MinIO/S3 (files)│ │  - Reports      │ │                 │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

---

## 2. Component Breakdown

### 2.1 Frontend — React SPA

| Component | Responsibility | Key Libraries |
|---|---|---|
| **Upload Module** | Drag-and-drop file upload with progress, file validation | `react-dropzone`, `axios` |
| **Data Preview** | Interactive table with sorting/filtering; before/after comparison | `@tanstack/react-table`, `recharts` |
| **ML Dashboard** | Training progress; model comparison; recommendation + feature importance | `recharts`, `framer-motion` |
| **Chat Panel** | RAG chatbot UI; LLM provider selector; message history | Custom WebSocket hook |
| **Report Viewer** | Report preview with section toggles; PDF/HTML export | `react-pdf`, `html2canvas` |

### 2.2 Backend — FastAPI

#### Routers

| Router | Base Path | Purpose |
|---|---|---|
| `upload_router` | `/api/v1/upload` | File upload, status, deletion |
| `data_router` | `/api/v1/data` | Preview, cleaning, quality metrics |
| `ml_router` | `/api/v1/ml` | Train, status, results, model download |
| `chat_router` | `/api/v1/chat` | Send message, history, set LLM |
| `report_router` | `/api/v1/report` | Generate, download, list reports |
| `auth_router` | `/api/v1/auth` | Login, register, token refresh |

#### Services

| Service | Responsibility |
|---|---|
| `DataService` | Ingestion → validation → cleaning → feature engineering |
| `MLService` | Task detection → training → evaluation → recommendation |
| `RAGService` | Embedding → FAISS indexing → retrieval → LLM prompting |
| `ReportService` | Template → data aggregation → chart generation → export |
| `AuthService` | JWT issuance, validation, permissions |

### 2.3 Worker Tier — Celery

| Worker | Queue | Concurrency | Timeout |
|---|---|---|---|
| `ml_training_worker` | `ml_queue` | 2/node | 30 min |
| `data_cleaning_worker` | `data_queue` | 4/node | 10 min |
| `report_worker` | `report_queue` | 4/node | 5 min |

### 2.4 Storage Tier

| Store | Technology | Purpose |
|---|---|---|
| **Metadata DB** | PostgreSQL 16 | Users, dataset metadata, job status |
| **Cache / Broker** | Redis 7 | Celery broker, session cache |
| **Vector Store** | FAISS | Embedding vectors for RAG |
| **Object Store** | MinIO / S3 | Uploaded files, models, reports |

---

## 3. Data Flow

### 3.1 Primary Flow: Upload → Clean → Train → Report

```
User               API Server          Celery Worker        Storage
 │ POST /upload      │                      │                  │
 │──────────────────>│  store raw file      │                  │
 │                   │─────────────────────────────────────────>│
 │                   │  dispatch: clean     │                  │
 │                   │─────────────────────>│ read + clean     │
 │                   │                      │─────────────────>│
 │ WS: clean done    │<─── status update   │                  │
 │<──────────────────│                      │                  │
 │ POST /ml/train    │                      │                  │
 │──────────────────>│  dispatch: train     │                  │
 │                   │─────────────────────>│ AutoML (5-15)    │
 │ WS: progress      │<─── progress        │                  │
 │<──────────────────│                      │ save artifacts   │
 │                   │                      │─────────────────>│
 │ GET /ml/results   │                      │                  │
 │──────────────────>│  read results        │                  │
 │<── comparison +   │<────────────────────────────────────────│
 │    recommendation │                      │                  │
```

### 3.2 RAG Chatbot Flow

```
User Question → embed(question) → FAISS top-k search → build prompt
→ call LLM (GPT/Claude/Gemini) → validate citations → return grounded answer
```

1. User posts question + selected LLM provider
2. `RAGService` embeds the question using `all-MiniLM-L6-v2`
3. FAISS returns top-5 most similar data chunks
4. Prompt is constructed: `system_prompt + retrieved_context + user_question`
5. Selected LLM generates response
6. Response is validated against source chunks; ungrounded claims are stripped
7. Final answer with citations is returned

---

## 4. Async Job Handling

### 4.1 Job States

| State | Description | Transitions |
|---|---|---|
| `PENDING` | Queued, awaiting worker | → `RUNNING` |
| `RUNNING` | Worker executing | → `SUCCESS` / `FAILURE` / `REVOKED` |
| `PROGRESS` | Sub-state with `{percent, message}` | → `SUCCESS` / `FAILURE` |
| `SUCCESS` | Completed; result stored | Terminal |
| `FAILURE` | Failed; error stored | → `PENDING` (retry) |
| `REVOKED` | User cancelled | Terminal |

### 4.2 WebSocket Progress

```json
// ws://api.datascout.io/ws/jobs/{job_id}
{
  "type": "progress",
  "data": {
    "job_id": "abc-123",
    "state": "PROGRESS",
    "percent": 45,
    "message": "Training model 3/8: RandomForest"
  }
}
```

### 4.3 Implementation Pattern

```python
@celery_app.task(bind=True, max_retries=2, soft_time_limit=1800)
def train_models_task(self, dataset_id: str, config: dict):
    self.update_state(state="PROGRESS", meta={"percent": 0, "message": "Loading data"})
    df = load_cleaned_dataset(dataset_id)
    task_type = detect_task_type(df, config["target_column"])
    self.update_state(state="PROGRESS", meta={"percent": 10, "message": f"Detected: {task_type}"})
    results = run_automl(df, task_type, config)
    self.update_state(state="PROGRESS", meta={"percent": 90, "message": "Saving models"})
    save_model_artifacts(dataset_id, results)
    return {"status": "complete", "best_model": results.best_model_name}
```

---

## 5. Scaling Considerations

### 5.1 Horizontal Scaling

```
          Load Balancer (Nginx / ALB)
          ┌─────────┼─────────┐
    FastAPI-1   FastAPI-2   FastAPI-3
          └─────────┼─────────┘
          ┌─────────┼─────────┐
    Worker-1    Worker-2    Worker-3
    (ML)        (ML)        (Data)
```

### 5.2 Scaling Rules

| Component | Trigger | Strategy |
|---|---|---|
| FastAPI | CPU > 70% for 5 min | Add instance (max 10) |
| ML Workers | Queue depth > 5 | Add worker (max 8) |
| PostgreSQL | Connections > 80% | Read replicas |
| Redis | Memory > 80% | Cluster mode |
| FAISS | Index > 10GB | Shard by dataset_id |

### 5.3 Bottleneck Mitigation

| Bottleneck | Mitigation |
|---|---|
| AutoML training (CPU-bound, 5-30 min) | Dedicated ML worker pool; FLAML `time_budget` cap |
| Large file uploads (I/O-bound) | Chunked uploads; stream to S3/MinIO |
| FAISS search (>1M vectors) | Per-dataset indexes; IVF for >100K vectors |
| LLM API rate limits | Exponential backoff; provider fallback chain |

---

## 6. Technology Stack

| Layer | Technology | Justification |
|---|---|---|
| Frontend | React 18 + Vite 5 | Fast HMR, wide ecosystem |
| State | Zustand 4 | Lightweight, no boilerplate |
| Backend | FastAPI 0.110+ | Async-native, auto-docs, Pydantic |
| Task Queue | Celery 5.3+ | Battle-tested async workers |
| AutoML | FLAML 2.1+ | Fast, lightweight tabular AutoML |
| ML Toolkit | scikit-learn 1.4+ | Industry-standard algorithms |
| Vector DB | FAISS 1.7.4+ | High-performance similarity search |
| Embeddings | sentence-transformers | `all-MiniLM-L6-v2` |
| Metadata DB | PostgreSQL 16 | ACID, JSON support |
| Cache/Broker | Redis 7 | In-memory speed, Celery broker |
| Object Store | MinIO / S3 | S3-compatible local + cloud |
| Containers | Docker + Compose | Reproducible environments |
| Proxy | Nginx 1.25+ | SSL, rate limiting |
| CI/CD | GitHub Actions | Native GitHub integration |

---

## 7. Directory Structure

```
data_scout/
├── frontend/
│   └── src/
│       ├── components/        # Upload, DataPreview, MLDashboard, ChatPanel, ReportViewer
│       ├── pages/             # Route-level pages
│       ├── hooks/             # Custom hooks (useWebSocket, useUpload, etc.)
│       ├── services/          # API client functions
│       ├── store/             # Zustand stores
│       └── utils/
├── backend/
│   └── app/
│       ├── api/v1/routers/    # upload, data, ml, chat, report
│       ├── core/              # config, security, logging
│       ├── models/            # SQLAlchemy ORM
│       ├── schemas/           # Pydantic schemas
│       ├── services/          # DataService, MLService, RAGService, ReportService
│       ├── workers/           # Celery tasks
│       ├── pipelines/         # cleaning, feature_eng, task_detection, training, eval
│       └── main.py
├── docker-compose.yml
├── nginx/nginx.conf
├── .github/workflows/
├── DOCS/
└── README.md
```

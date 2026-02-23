# DATA_SCOUT — MVP Implementation Plan

**Version:** 1.0 | **Last Updated:** 2026-02-21  
**Sprint Duration:** 4 Weeks (Feb 24 — Mar 23, 2026)  
**Team Size:** 5 Engineers  
**Goal:** Ship a working end-to-end flow: Upload → Clean → Train → Chat → Report

---

## Team Roster

| # | Role | Name Alias | Primary Responsibility | Secondary Responsibility |
|---|---|---|---|---|
| 🔵 P1 | **Backend Engineer** | Backend Lead | Data & ML pipelines, Celery workers, business logic | Database models, service layer |
| 🟢 P2 | **Frontend Engineer** | Frontend Lead | React SPA, component library, state management, UX | API integration, WebSocket client |
| 🟡 P3 | **API & Integration Engineer** | API Lead | FastAPI routers, Pydantic schemas, auth, WebSocket server | LLM integration, RAG chatbot |
| 🟠 P4 | **DevOps Engineer** | DevOps Lead | Docker, CI/CD, database setup, infra, monitoring | Security hardening, deployment |
| 🟣 P5 | **QA & Documentation Engineer** | QA Lead | Test suites, load testing, documentation, validation | Data fixtures, integration tests |

---

## Sprint Overview

```
Week 1: Foundation          Week 2: Core Pipelines       Week 3: Intelligence        Week 4: Polish & Ship
(Feb 24 — Feb 28)           (Mar 3 — Mar 7)              (Mar 10 — Mar 14)           (Mar 17 — Mar 21)
                                                                                      + Buffer (Mar 22-23)
│                           │                             │                            │
├─ Project scaffolding      ├─ Data cleaning pipeline     ├─ RAG chatbot (FAISS+LLM)  ├─ Integration testing
├─ Docker environment       ├─ AutoML training pipeline   ├─ Report generation engine  ├─ Bug fixes
├─ DB models & migrations   ├─ Upload + Preview UI        ├─ Chat UI                  ├─ Performance tuning
├─ Auth system              ├─ Data cleaning UI           ├─ Results dashboard UI     ├─ Documentation final
├─ Component library        ├─ Training endpoints         ├─ Explainability (SHAP)    ├─ Demo preparation
└─ CI pipeline              └─ WebSocket progress         └─ Report UI               └─ MVP release
```

---

## Week 1: Foundation (Feb 24 — Feb 28)

> **Goal:** Every team member has a working local environment. Backend skeleton, database, auth, Docker, CI, and base React app are all functional.

---

### 🔵 P1 — Backend Engineer

| Day | Task | Deliverables | Dependencies | Definition of Done |
|---|---|---|---|---|
| **Mon** | Set up backend project structure | `backend/app/` skeleton: `main.py`, `core/`, `models/`, `schemas/`, `services/`, `pipelines/`, `workers/` folders with `__init__.py` | None | `uvicorn app.main:app` starts without error |
| **Mon** | Configure settings with pydantic-settings | `core/config.py` with `DATABASE_URL`, `REDIS_URL`, `MINIO_ENDPOINT`, `JWT_SECRET`, all LLM API keys | `.env.example` from P4 | Settings load from `.env`; missing vars raise clear error |
| **Tue** | Create SQLAlchemy ORM models | `models/user.py`, `dataset.py`, `job.py`, `model_result.py`, `conversation.py`, `report.py` with relationships | PostgreSQL running (P4) | All models importable; relationships defined |
| **Tue** | Set up Alembic migrations | `alembic/` directory, `env.py` configured for async | DB models | `alembic upgrade head` creates all tables |
| **Wed** | Implement database session management | `db/session.py` — async session factory, `get_db` dependency | DB running | Dependency injection works in test route |
| **Wed** | Build `AuthService` | `services/auth_service.py` — register, login, hash password (bcrypt), generate/verify JWT | models, session | Register → Login → get access token works |
| **Thu** | Build data ingestion pipeline (Phase 1) | `pipelines/ingestion.py` — parse CSV/XLSX, chunked reading, metadata extraction | `pandas`, `openpyxl` | Correctly parses 5 test files of varying formats |
| **Thu** | Build column type detection | `pipelines/type_detection.py` — multi-heuristic detection (numeric, categorical, datetime, boolean, identifier) | `ingestion.py` | ≥95% accuracy on test fixtures |
| **Fri** | Set up Celery app + Redis broker | `core/celery_app.py` — Celery instance, queue config, result backend | Redis running (P4) | Basic task submits and completes; result retrievable |
| **Fri** | Write data cleaning task skeleton | `workers/data_tasks.py` — `clean_dataset_task` with progress updates via `self.update_state()` | Celery app | Task submittable; progress states visible in Redis |

**Blockers to Watch:**
- Needs P4 to have PostgreSQL + Redis running by Tuesday morning
- Coordinate with P3 on Pydantic schema shapes for auth endpoints

**Key Decisions:**
- Use `asyncpg` driver for async PostgreSQL
- `bcrypt` cost factor = 12
- JWT algorithm = HS256, access TTL = 30 min, refresh TTL = 7 days

---

### 🟢 P2 — Frontend Engineer

| Day | Task | Deliverables | Dependencies | Definition of Done |
|---|---|---|---|---|
| **Mon** | Initialize React + Vite project | `frontend/` with Vite 5, React 18, folder structure (`components/`, `pages/`, `hooks/`, `services/`, `store/`, `styles/`) | None | `npm run dev` serves blank app at localhost:3000 |
| **Mon** | Set up design system: CSS variables + globals | `styles/variables.css` (all tokens from FRONTEND_DESIGN.md), `styles/globals.css` (reset, base typography), `styles/animations.css` | None | All tokens importable; dark theme toggle-ready |
| **Mon** | Set up ESLint + Prettier | `.eslintrc.cjs`, `.prettierrc` | None | `npm run lint` passes on initial codebase |
| **Tue** | Build atomic UI components (Batch 1) | `Button.jsx`, `Input.jsx`, `Card.jsx`, `Badge.jsx`, `Spinner.jsx` + CSS Modules | Design tokens | Components render correctly with all variants |
| **Tue** | Build atomic UI components (Batch 2) | `Modal.jsx`, `Toast.jsx`, `ProgressBar.jsx`, `Skeleton.jsx`, `Tabs.jsx`, `Toggle.jsx`, `Dropdown.jsx`, `Tooltip.jsx` | Design tokens | All components render + keyboard accessible |
| **Wed** | Build layout components | `Header.jsx` (logo, nav links, user menu), `Sidebar.jsx` (collapsible), `PageContainer.jsx`, `Footer.jsx`, `ProtectedLayout.jsx` | UI components | App has visible working layout at all breakpoints |
| **Wed** | Set up React Router | `App.jsx` with all routes defined; `ProtectedLayout` wraps authenticated routes | Layout components | Navigation between pages works; unauthenticated redirects to `/login` |
| **Thu** | Build auth pages | `LoginPage.jsx`, `RegisterPage.jsx` with form validation (React Hook Form + Zod) | UI components, router | Forms validate input; submit button triggers API call (mock for now) |
| **Thu** | Set up Zustand stores | `useAuthStore.js` (tokens, user, login/logout), `useToastStore.js` (global notifications), `useDatasetStore.js`, `useJobStore.js` | None | Stores work in isolation; auth state persists in localStorage |
| **Fri** | Build Axios API client + interceptors | `services/api.js` — base URL, auth header injection, 401 auto-refresh, error handling | `useAuthStore` | API calls include token; 401 triggers refresh flow |
| **Fri** | Build `HomePage.jsx` (Landing) | Hero section, "How it Works" 4-step section, feature cards, footer | UI components, layout | Visually polished landing page; responsive |

**Blockers to Watch:**
- Coordinate with P3 on API response shapes for auth endpoints
- Need design tokens finalized Day 1 (from FRONTEND_DESIGN.md — already done ✅)

**Key Decisions:**
- Zustand over Redux (no boilerplate)
- CSS Modules over Tailwind (full control, no extra dependency)
- React Hook Form + Zod for form validation

---

### 🟡 P3 — API & Integration Engineer

| Day | Task | Deliverables | Dependencies | Definition of Done |
|---|---|---|---|---|
| **Mon** | Set up FastAPI app factory | `main.py` — `create_app()`, CORS middleware, exception handlers, router mounting | None | `GET /health` returns `{"status": "healthy"}` |
| **Mon** | Define Pydantic schemas (auth) | `schemas/auth.py` — `LoginRequest`, `RegisterRequest`, `TokenResponse`, `UserResponse` | None | Schemas validate correct/incorrect payloads |
| **Tue** | Build auth router | `routers/auth.py` — `POST /register`, `POST /login`, `POST /refresh` | `AuthService` (P1) | Full auth flow works via Swagger docs |
| **Tue** | Build auth dependencies | `dependencies.py` — `get_current_user`, `get_db`, `require_auth` | Auth router, JWT | Protected endpoints reject invalid tokens |
| **Wed** | Define Pydantic schemas (upload, data) | `schemas/upload.py` — `UploadResponse`, `DatasetInfo`; `schemas/data.py` — `PreviewResponse`, `CleanRequest`, `QualityReport`; `schemas/common.py` — `ErrorResponse`, `JobStatus` | Coordinate with P1 on models | All schemas documented in Swagger |
| **Wed** | Build upload router | `routers/upload.py` — `POST /upload` (multipart), `GET /upload/{id}`, `DELETE /upload/{id}` | Pydantic schemas, MinIO (P4) | File uploads to MinIO; metadata stored in DB |
| **Thu** | Build data router | `routers/data.py` — `GET /data/{id}/preview`, `POST /data/{id}/clean`, `GET /data/{id}/quality` | Data schemas, cleaning task (P1) | Preview returns first 20 rows; clean dispatches Celery task |
| **Thu** | Build job status router | `routers/jobs.py` — `GET /jobs/{id}`, `DELETE /jobs/{id}` | Job model (P1) | Job status polling works; cancel revokes Celery task |
| **Fri** | Build WebSocket endpoint for job progress | `websocket/job_progress.py` — `/ws/jobs/{job_id}` | Celery progress events | Client receives real-time progress updates |
| **Fri** | End-to-end test: upload → clean → quality | Manual test through Swagger | All above | Full flow works from API; documented |

**Blockers to Watch:**
- P1 must deliver `AuthService` by Tuesday EOD
- P4 must have MinIO running by Wednesday morning
- Coordinate schema shapes with P2 for frontend integration

**Key Decisions:**
- All async endpoints (`async def`)
- Consistent error format: `{"error": {"code": "...", "message": "...", "details": {...}}}`
- API versioning: `/api/v1/` prefix on all routes
- Rate limiting: handled by Nginx (P4), not application-level for MVP

---

### 🟠 P4 — DevOps Engineer

| Day | Task | Deliverables | Dependencies | Definition of Done |
|---|---|---|---|---|
| **Mon** | Create repository structure | Root `data_scout/` with `frontend/`, `backend/`, `nginx/`, `scripts/`, `DOCS/`, `.github/`, `.env.example`, `.gitignore`, `Makefile` | None | `git init` + initial commit with structure |
| **Mon** | Write `docker-compose.yml` (dev) | Services: `postgres`, `redis`, `minio` with health checks, volumes, ports | None | `docker compose up` starts all 3 services; health checks pass |
| **Tue** | Write backend `Dockerfile` | Multi-stage: Python 3.11-slim, install deps, copy app | `requirements.txt` (P1) | `docker build` succeeds; backend starts in container |
| **Tue** | Write frontend `Dockerfile` | Multi-stage: Node 20 build → Nginx serve | `package.json` (P2) | `docker build` succeeds; frontend serves from Nginx |
| **Tue** | Add backend + frontend to docker-compose | `backend`, `celery-worker` services with env vars, `frontend` service | Dockerfiles | `docker compose up` starts full stack |
| **Wed** | Write Nginx reverse proxy config | `nginx/nginx.conf` — `/` → frontend, `/api/` → backend:8000, `/ws/` → backend WebSocket, SSL placeholder, rate limiting, security headers | Docker Compose | Requests routed correctly through Nginx |
| **Wed** | Create MinIO bucket initialization script | `scripts/init_minio.sh` — create `datasets`, `models`, `reports` buckets on first run | MinIO running | Buckets exist after script runs |
| **Thu** | Set up GitHub Actions CI | `.github/workflows/ci.yml` — lint backend (ruff), test backend (pytest), lint frontend (eslint), test frontend (vitest), build Docker images | Tests exist (P5) | CI passes on push to `main` and `develop` |
| **Thu** | Write `Makefile` with common commands | Targets: `dev`, `build`, `test`, `lint`, `migrate`, `seed`, `logs`, `clean` | Docker Compose | `make dev` starts everything; `make test` runs all tests |
| **Fri** | Write `docker-compose.dev.yml` (overrides) | Hot-reload for backend (uvicorn --reload), frontend (vite dev server), exposed debug ports, no SSL | Base compose | `docker compose -f docker-compose.yml -f docker-compose.dev.yml up` enables hot-reload |
| **Fri** | Validate full local dev environment | Run full stack locally; verify all services connect; document any setup quirks | All above | New developer can `make dev` and have everything running in <5 minutes |

**Blockers to Watch:**
- Needs `requirements.txt` from P1 by Tuesday morning
- Needs `package.json` from P2 by Tuesday morning
- CI depends on test files from P5

**Key Decisions:**
- PostgreSQL 16, Redis 7, MinIO latest
- Dev mode: volumes mount source code for hot-reload
- `.env.example` includes all required vars with placeholder values
- Makefile as single entry point for all commands

---

### 🟣 P5 — QA & Documentation Engineer

| Day | Task | Deliverables | Dependencies | Definition of Done |
|---|---|---|---|---|
| **Mon** | Set up pytest infrastructure | `backend/tests/conftest.py` — async test client, test DB fixture (SQLite or test PostgreSQL), auth fixture, temp file fixtures | P1 project structure | `pytest` runs with 0 tests collected (no errors) |
| **Mon** | Create test data fixtures | `tests/fixtures/sample_clean.csv`, `sample_messy.csv` (nulls, outliers, duplicates, mixed types), `sample_imbalanced.csv` | None | 4 fixture files with realistic data; documented column descriptions |
| **Tue** | Write unit tests: type detection | `tests/unit/test_type_detection.py` — numeric, categorical, datetime, boolean, identifier, mixed-type columns | `type_detection.py` (P1) | ≥10 test cases; all pass |
| **Tue** | Write unit tests: auth service | `tests/unit/test_auth.py` — register, login, JWT validity, expired token, wrong password | `auth_service.py` (P1) | ≥8 test cases; all pass |
| **Wed** | Write unit tests: Pydantic schemas | `tests/unit/test_schemas.py` — valid/invalid payloads for all schemas | Schemas (P3) | ≥15 test cases covering edge cases |
| **Wed** | Set up Vitest for frontend | `frontend/vitest.config.js`, sample component test | P2 project structure | `npm test` runs without error |
| **Thu** | Write frontend component tests | `Button.test.jsx`, `FileDropzone.test.jsx`, `DataTable.test.jsx` — render, interaction, accessibility | Components (P2) | ≥10 test cases; all pass |
| **Thu** | Write integration test: auth flow | `tests/integration/test_auth_flow.py` — register → login → access protected → refresh → invalid token | Auth system (P1+P3) | Full flow passes end-to-end |
| **Fri** | Update README.md | Getting started, prerequisites, installation, dev workflow, project structure overview, contributing guide | All above | New developer can set up in <10 minutes following README |
| **Fri** | Review & validate all documentation | Cross-check DOCS/ folder against actual implementation; flag any discrepancies; add missing details | All DOCS/ files | All docs reflect actual state of codebase |

**Blockers to Watch:**
- Test writing depends on P1/P3 delivering implementations
- If implementations are delayed, write tests against planned interfaces (TDD approach)

**Key Decisions:**
- pytest + pytest-asyncio + httpx for backend tests
- Vitest + React Testing Library for frontend tests
- Test fixtures committed to repo (small, synthetic data)
- Coverage target: ≥70% for MVP (stretch: 80%)

---

## Week 2: Core Pipelines (Mar 3 — Mar 7)

> **Goal:** Data cleaning and ML training pipelines work end-to-end. Frontend shows upload, data preview, cleaning, and training progress.

---

### 🔵 P1 — Backend Engineer

| Day | Task | Deliverables | Depends On | Done When |
|---|---|---|---|---|
| **Mon** | Build missing value imputation | `pipelines/cleaning.py` — strategy matrix: mean/median/mode/drop per column type + missingness % | `type_detection.py` | Correct imputation on `sample_messy.csv`; 0 nulls remaining |
| **Mon** | Build outlier detection + treatment | `pipelines/cleaning.py` — IQR method (default), Z-score (optional); cap/remove/flag modes | Cleaning module | Outliers detected and treated; counts match manual check |
| **Tue** | Build deduplication + type correction | `pipelines/cleaning.py` — remove exact dupes; coerce string-numbers/dates | Cleaning module | Duplicates removed; type corrections logged |
| **Tue** | Build feature engineering | `pipelines/feature_engineering.py` — datetime features, frequency encoding, interaction terms, variance filter, correlation filter | Cleaning output | Generated features pass validation; no constant/duplicate features |
| **Wed** | Build data validation (pre+post) | `pipelines/validation.py` — pre-checks (min rows/cols, encoding), post-checks (no nulls, no dupes, row loss <30%), quality score | All cleaning steps | Quality score computed correctly for test datasets |
| **Wed** | Build full `DataService` orchestration | `services/data_service.py` — orchestrate: ingest → validate → clean → feature_eng → validate → store cleaned | All pipeline modules | `DataService.process(dataset_id)` returns quality report |
| **Thu** | Build task detection | `pipelines/task_detection.py` — classification/regression/clustering detection with confidence score | Cleaned data | ≥95% correct on 10+ test datasets |
| **Thu** | Build AutoML training pipeline | `pipelines/model_training.py` — FLAML wrapper, model pool filtering by dataset size, time budget enforcement | Task detection | FLAML trains and returns results within time budget |
| **Fri** | Build evaluation pipeline | `pipelines/evaluation.py` — metrics per task type, overfitting detection, cross-validation | Model training | Metrics computed; overfitting flag works |
| **Fri** | Build model recommendation engine | `services/ml_service.py` — rank models, generate justification text, extract feature importance | Evaluation | Recommendation includes: model name, justification, top-3 features |

**End of Week Milestone:** `MLService.train_and_evaluate(dataset_id, target_col)` runs end-to-end and returns ranked models with recommendation.

---

### 🟢 P2 — Frontend Engineer

| Day | Task | Deliverables | Depends On | Done When |
|---|---|---|---|---|
| **Mon** | Build `FileDropzone` component | `Upload/FileDropzone.jsx` — drag-and-drop, file validation (type + size), visual feedback | UI components | Accepts valid files; rejects invalid ones with error |
| **Mon** | Build `UploadProgress` component | `Upload/UploadProgress.jsx` — per-file progress bar, cancel button | ProgressBar component | Shows real upload progress |
| **Tue** | Build `UploadPage.jsx` | Full upload page with dropzone + recent uploads table | FileDropzone, UploadProgress | File uploads work; recent files listed |
| **Tue** | Integrate upload with API | `services/uploadService.js` — POST /upload with FormData; `useUpload.js` hook | Upload API (P3) | Files upload to backend; response shown |
| **Wed** | Build `DataTable` component | `DataPreview/DataTable.jsx` — sorting, pagination, column type badges, alternating rows | UI components | 50K rows renders smoothly with pagination |
| **Wed** | Build `QualityPanel` component | `DataPreview/QualityPanel.jsx` — quality score meter, null/outlier/duplicate counts | Card, Badge | Shows all quality metrics |
| **Thu** | Build `DataPage.jsx` | Preview tab (DataTable) + Quality panel + Clean button + Before/After toggle | DataTable, QualityPanel | Full data preview + cleaning trigger works |
| **Thu** | Build `CleaningActionLog` component | `DataPreview/CleaningActionLog.jsx` — list of actions with affected rows, icons | Card component | Displays cleaning actions after clean completes |
| **Fri** | Build `TrainingProgress` component | `MLDashboard/TrainingProgress.jsx` — animated progress bar, model list with status icons, ETA | ProgressBar, WebSocket | Real-time progress updates from WebSocket |
| **Fri** | Build `useWebSocket` hook + `useJobPolling` | `hooks/useWebSocket.js` (auto-reconnect), `hooks/useJobPolling.js` (WS + HTTP fallback) | WebSocket endpoint (P3) | Progress updates received in real-time |

**End of Week Milestone:** User can upload a file → see preview → trigger cleaning → see before/after → start training → see live progress.

---

### 🟡 P3 — API & Integration Engineer

| Day | Task | Deliverables | Depends On | Done When |
|---|---|---|---|---|
| **Mon** | Build ML schemas | `schemas/ml.py` — `TrainRequest`, `TrainStatus`, `MLResults`, `ModelMetrics`, `Recommendation`, `FeatureImportance` | Coordinate with P1 | Schemas match ML pipeline output |
| **Mon** | Build ML router | `routers/ml.py` — `POST /ml/train`, `GET /ml/status/{job_id}`, `GET /ml/results/{dataset_id}`, `GET /ml/download/{dataset_id}/{model}` | ML schemas, ML task (P1) | Training dispatches task; results retrievable |
| **Tue** | Build ML training Celery task | `workers/ml_tasks.py` — `train_models_task` with progress updates at each model | MLService (P1), Celery | Task reports progress; stores results |
| **Tue** | Build data cleaning Celery task (full) | `workers/data_tasks.py` — `clean_dataset_task` calling `DataService`, progress at each step | DataService (P1), Celery | Full cleaning runs async with progress |
| **Wed** | Enhance WebSocket with proper error handling | Error messages, reconnection guidance, auth check on WS connect | WS endpoint | Client gets clear errors on failure |
| **Wed** | Build file storage abstraction | `services/storage_service.py` — upload/download/delete files to MinIO; presigned download URLs | MinIO (P4) | Files stored and retrievable; URLs work |
| **Thu** | End-to-end API test: upload → clean → train → results | Full flow through Swagger / httpx | All endpoints | Screenshot/recording of full flow |
| **Thu** | Performance tune: pagination, query optimization | Add pagination to list endpoints; optimize DB queries with `.options(selectinload)` | All routers | List endpoints respond <200ms for 100 items |
| **Fri** | Write API documentation (OpenAPI enrichment) | Add descriptions, examples, tags to all endpoints; verify Swagger docs are complete | All routers | Swagger at `/docs` is fully documented and usable |
| **Fri** | Coordinate with P2 on frontend integration | Joint session: verify API shapes match frontend expectations; fix any mismatches | P2 frontend | No contract mismatches remaining |

**End of Week Milestone:** Full API surface (upload, data, ML, jobs) working and documented in Swagger.

---

### 🟠 P4 — DevOps Engineer

| Day | Task | Deliverables | Depends On | Done When |
|---|---|---|---|---|
| **Mon** | Set up database backup script | `scripts/backup_db.sh` — pg_dump to timestamped file | PostgreSQL running | Backup file created; restore tested |
| **Mon** | Configure logging (structured JSON) | `core/logging.py` — structlog setup; middleware logs request_id, duration, status | Backend running | All requests logged in JSON format to stdout |
| **Tue** | Set up health check endpoint enhancement | `routers/health.py` — check DB, Redis, MinIO; return `healthy` / `degraded` | All services | `/health` accurately reflects service state |
| **Tue** | Add Alembic migration to CI | CI step: `alembic upgrade head` runs against test DB in CI | CI pipeline, migrations | CI fails if migration is broken |
| **Wed** | Configure Celery monitoring | Add Flower dashboard to docker-compose (dev); port 5555 | Celery running | Flower shows workers, queues, task history |
| **Wed** | Write seed script | `scripts/seed_db.py` — create test user, upload sample dataset, create initial data | Backend, DB | `make seed` creates usable test data |
| **Thu** | Optimize Docker images | Multi-stage builds; `.dockerignore`; layer caching; reduce image sizes | Dockerfiles | Backend image <500MB; Frontend image <50MB |
| **Thu** | Set up pre-commit hooks | `.pre-commit-config.yaml` — ruff (format + lint), eslint, prettier, trailing whitespace | None | `pre-commit run --all-files` passes |
| **Fri** | Write deployment script (staging) | `scripts/deploy.sh` — SSH to server, pull images, compose up, health check | Docker images | Script deploys to staging server (or local mimic) |
| **Fri** | Environment documentation | Document all env vars in `.env.example` with descriptions, defaults, and required/optional flags | All services | Every env var documented |

**End of Week Milestone:** Full Docker stack is optimized, monitored (Flower), seeded, and deployable.

---

### 🟣 P5 — QA & Documentation Engineer

| Day | Task | Deliverables | Depends On | Done When |
|---|---|---|---|---|
| **Mon** | Write unit tests: cleaning pipeline | `test_imputation.py`, `test_outliers.py` — strategy matrix, edge cases (all-null, single-value, all-outlier) | `cleaning.py` (P1) | ≥15 test cases; all pass |
| **Tue** | Write unit tests: feature engineering | `test_features.py` — datetime extraction, frequency encoding, variance filter, correlation filter | `feature_engineering.py` | ≥10 test cases; all pass |
| **Tue** | Write unit tests: task detection | `test_task_detection.py` — binary, multiclass, regression, clustering, constant target, ID column | `task_detection.py` | ≥12 test cases; all pass |
| **Wed** | Write integration test: upload → clean → quality | `test_cleaning_flow.py` — upload messy file → trigger clean → poll job → verify quality report | Upload + data APIs | End-to-end flow passes |
| **Wed** | Write integration test: train → results | `test_training_flow.py` — upload → clean → train → poll → verify model results | ML APIs | End-to-end ML flow passes |
| **Thu** | Write frontend tests: UploadPage, DataPage | Test file selection, validation errors, API integration mocks, table rendering | Frontend pages (P2) | ≥8 test cases per page |
| **Thu** | Measure code coverage | Configure `pytest-cov` + Vitest coverage; generate reports | All tests | Backend ≥70%, Frontend ≥60% |
| **Fri** | Update test plan documentation | Update `TEST_PLAN.md` with actual test results, coverage numbers, known gaps | Test results | Test plan reflects ground truth |
| **Fri** | Manual QA: full user flow | Manually test upload → clean → train → results through UI; file bug reports | Running system | Bug list with severity (P0/P1/P2) created |

**End of Week Milestone:** ≥70% backend coverage; integration tests for both core pipelines; manual QA report.

---

## Week 3: Intelligence Layer (Mar 10 — Mar 14)

> **Goal:** RAG chatbot, report generation, SHAP explainability, and all remaining UI pages are functional.

---

### 🔵 P1 — Backend Engineer

| Day | Task | Deliverables | Depends On | Done When |
|---|---|---|---|---|
| **Mon** | Build row-to-text conversion | `pipelines/` — convert dataframe rows to text chunks; generate statistical summary chunks; create schema description chunk | Cleaned data | Chunks are semantic and retrievable |
| **Mon** | Build FAISS indexing pipeline | `services/rag_service.py` — embed chunks with `all-MiniLM-L6-v2`, build FAISS FlatIP index, persist index | sentence-transformers, FAISS | Index built for test dataset; search returns relevant results |
| **Tue** | Build retrieval pipeline | `services/rag_service.py` — embed query, FAISS top-k search, quality gate (threshold=0.3), chunk filtering | FAISS index | Correct chunks retrieved for test questions |
| **Tue** | Build prompt construction | `services/rag_service.py` — system prompt + context chunks + conversation history + user question | Retrieval pipeline | Prompt fits within context window; grounding instructions present |
| **Wed** | Build post-response validation | `services/rag_service.py` — extract numerical claims, check against source chunks, compute grounding ratio | LLM response | Hallucinated claims detected; grounding ratio computed |
| **Wed** | Build SHAP explainability | `pipelines/explainability.py` — TreeExplainer/KernelExplainer, summary plot, feature importance plot, save as images | Trained models | SHAP plots generated and saved to storage |
| **Thu** | Build report generation engine | `services/report_service.py` — template-based report: summary, data quality, model comparison, feature importance, recommendations sections | All pipeline outputs | HTML report generated with real data + charts |
| **Thu** | Build report Celery task | `workers/report_tasks.py` — `generate_report_task` with section selection | ReportService | Async report generation works |
| **Fri** | Build model card generation | `pipelines/explainability.py` — structured model card: type, hyperparams, training shape, CV scores, overfitting report | ML pipeline | Model card JSON generated for every trained model |
| **Fri** | Performance optimization: caching | Add Redis caching for: dataset preview (5 min TTL), quality reports (until re-clean), embedding models (singleton) | Redis, all services | Repeated API calls are 10x faster |

---

### 🟢 P2 — Frontend Engineer

| Day | Task | Deliverables | Depends On | Done When |
|---|---|---|---|---|
| **Mon** | Build `ResultsPage.jsx` | Full results dashboard: RecommendationCard + ComparisonTable + FeatureImportance + OverfitIndicator | ML components | All ML results displayed correctly |
| **Mon** | Build `RecommendationCard` component | Highlighted best-model card with justification text, download button, SHAP link | Card component | Recommendation renders with real data |
| **Tue** | Build `ComparisonTable` component | Multi-model table with sort-by-metric, highlight best, colored performance bars | DataTable variant | All models compared side-by-side |
| **Tue** | Build `FeatureImportance` + `OverfitIndicator` | Horizontal bar chart (Recharts), train-test gap visual indicator | Recharts | Charts render with correct data |
| **Wed** | Build `ChatContainer` + `ChatMessage` | Full chat layout: scrollable message list, user/assistant bubbles, citation cards inline | UI components | Chat appearance matches wireframe |
| **Wed** | Build `ChatInput` + `ProviderSelector` | Text input with send, LLM provider dropdown, suggested question chips | Dropdown, Button | Input works; provider switchable |
| **Thu** | Build `ChatPage.jsx` | Full chat page: ChatContainer + sidebar with dataset stats | Chat components | Chat page is functional (with mock data if API not ready) |
| **Thu** | Integrate chat with API | Connect to `POST /chat/message`, display response with citations, handle loading/error | Chat API (P3) | Real LLM responses shown with citations |
| **Fri** | Build `ReportPage.jsx` | Report config (section checkboxes, format selector, title input) + preview panel + download buttons | Report components | Reports generate and display correctly |
| **Fri** | Build `DashboardPage.jsx` | User dashboard: dataset list, job history, quick actions | All previous | Dashboard shows all user data |

---

### 🟡 P3 — API & Integration Engineer

| Day | Task | Deliverables | Depends On | Done When |
|---|---|---|---|---|
| **Mon** | Build LLM provider abstraction | `llm/base.py`, `openai_provider.py`, `anthropic_provider.py`, `google_provider.py`, `factory.py` | API keys configured | All 3 providers callable through factory |
| **Mon** | Build LLM fallback chain | `factory.py` — retry with backoff, fallback to next provider on failure | Provider implementations | Fallback activates on provider error |
| **Tue** | Build chat schemas | `schemas/chat.py` — `ChatMessageRequest`, `ChatResponse`, `Citation`, `ChatSettings` | Coordinate with P1 | Schemas match RAG service output |
| **Tue** | Build chat router | `routers/chat.py` — `POST /chat/message`, `GET /chat/history/{conversation_id}`, `PUT /chat/settings` | RAGService (P1), LLM providers | Chat endpoint returns grounded answers |
| **Wed** | Build report schemas | `schemas/report.py` — `ReportRequest`, `ReportResponse`, section list | Coordinate with P1 | Schemas match report service output |
| **Wed** | Build report router | `routers/report.py` — `POST /report/generate`, `GET /report/{id}`, `GET /report/download/{id}` | ReportService (P1) | Reports generate async; downloadable |
| **Thu** | Build SHAP/explainability endpoints | Add `GET /ml/shap/{dataset_id}` — return SHAP plot URLs; `GET /ml/model-card/{dataset_id}` | Explainability (P1) | SHAP plots and model cards accessible via API |
| **Thu** | PII detection middleware | Middleware to scan uploaded data for PII patterns (email, phone, SSN); warn user, don't block | Ingestion pipeline | PII warnings returned in upload response |
| **Fri** | End-to-end test: upload → clean → train → chat → report | Full flow through API; verify all pieces connect | All endpoints | Complete flow documented with screenshots |
| **Fri** | API rate limiting (per user) | Add rate limit headers; track via Redis; return 429 with Retry-After header | Redis, all routers | Rate limits enforced per endpoint group |

---

### 🟠 P4 — DevOps Engineer

| Day | Task | Deliverables | Depends On | Done When |
|---|---|---|---|---|
| **Mon** | Add sentence-transformers + FAISS to backend image | Update `requirements.txt` + Dockerfile; ensure model downloads cached in Docker layer | P1 requirements | Backend image builds with ML dependencies |
| **Tue** | Set up model caching in Docker | Download `all-MiniLM-L6-v2` during Docker build; mount as volume | sentence-transformers | Model loads from cache, not downloaded at runtime |
| **Wed** | Configure Celery queue separation | Separate ML queue (2 workers) from data/report queue (4 workers) in docker-compose | Celery tasks | Workers consume from correct queues |
| **Thu** | Set up staging deployment | Deploy to cloud VM or VPS: docker compose up with production config, SSL via Let's Encrypt | Deploy script | Staging accessible via HTTPS |
| **Fri** | Monitoring: add Prometheus + Grafana (basic) | `docker-compose.monitoring.yml` — Prometheus scrapes FastAPI metrics; Grafana dashboard | Docker stack | Basic dashboard: request rate, latency, error rate |

---

### 🟣 P5 — QA & Documentation Engineer

| Day | Task | Deliverables | Depends On | Done When |
|---|---|---|---|---|
| **Mon** | Write unit tests: RAG service | `test_rag_service.py` — chunk generation, retrieval quality gate, prompt construction, grounding validation | RAGService (P1) | ≥10 test cases |
| **Tue** | Write unit tests: LLM providers | `test_llm_providers.py` — factory creation, fallback chain, error handling (mocked APIs) | LLM providers (P3) | ≥8 test cases |
| **Wed** | Write integration test: chat flow | `test_chat_flow.py` — upload → index → ask question → verify citations | Chat API (P3) | Full chat flow passes |
| **Thu** | Write ML validation tests | `test_classification.py` (Iris ≥95% acc), `test_regression.py` (R² ≥0.80), `test_clustering.py` (silhouette ≥0.70) | ML pipeline (P1) | Baselines met on standard datasets |
| **Fri** | Manual QA: full flow with 5 different datasets | Test with: clean CSV, messy Excel, imbalanced data, high-cardinality, small dataset | Full system | Bug list with severity; UX feedback notes |

---

## Week 4: Polish & Ship (Mar 17 — Mar 21)

> **Goal:** Fix all P0 bugs, integration testing, performance tuning, final documentation, and MVP demo.

---

### 🔵 P1 — Backend Engineer

| Day | Task |
|---|---|
| **Mon** | Fix all P0 bugs from QA reports; handle edge cases discovered in testing |
| **Tue** | Performance tuning: optimize slow queries, reduce memory usage in cleaning pipeline, add streaming for large files |
| **Wed** | Add error recovery: graceful handling of OOM, timeout, corrupted files; meaningful error messages |
| **Thu** | Code review all backend code; refactor any tech debt; add docstrings to all public functions |
| **Fri** | Support demo preparation; fix any last-minute issues; tag v0.1.0 release |

### 🟢 P2 — Frontend Engineer

| Day | Task |
|---|---|
| **Mon** | Fix all UI bugs; polish responsive design; dark theme verification |
| **Tue** | Add empty states, error boundaries, and loading skeletons to all pages |
| **Wed** | Accessibility audit: keyboard navigation, screen reader, color contrast; fix issues |
| **Thu** | Performance: lazy-load pages (React.lazy), optimize bundle size, add page transitions |
| **Fri** | Final visual polish; demo preparation; record walkthrough video |

### 🟡 P3 — API & Integration Engineer

| Day | Task |
|---|---|
| **Mon** | Fix all API bugs; verify all error codes and messages are correct |
| **Tue** | Add request validation edge cases: empty files, invalid JSON, oversized payloads |
| **Wed** | Write API usage guide: curl examples for every endpoint; add to documentation |
| **Thu** | Security review: verify auth on all endpoints, check for unprotected routes, sanitize inputs |
| **Fri** | Swagger docs final review; support demo; tag v0.1.0 |

### 🟠 P4 — DevOps Engineer

| Day | Task |
|---|---|
| **Mon** | Production Docker compose: no dev overrides, secrets via env, restart policies |
| **Tue** | Load test: Locust with 50 concurrent users; identify and fix bottlenecks |
| **Wed** | Set up production deployment (cloud): SSL, domain, DNS, auto-restart |
| **Thu** | Configure alerts: error rate, latency, disk space; Slack notification integration |
| **Fri** | Final deployment; smoke test; support demo |

### 🟣 P5 — QA & Documentation Engineer

| Day | Task |
|---|---|
| **Mon** | Regression testing: re-run all test suites after bug fixes; verify coverage ≥70% |
| **Tue** | Write user-facing README.md: badges, features, screenshots, quickstart, contributing |
| **Wed** | Update all DOCS/ files to match actual implementation; fix any discrepancies |
| **Thu** | Write CHANGELOG.md for v0.1.0; create release notes |
| **Fri** | Final manual QA pass; prepare demo script; support demo |

---

## Communication & Coordination

### Daily Standup (15 min, 10:00 AM)

Each person answers:
1. What I completed yesterday
2. What I'm working on today
3. Any blockers

### Coordination Points

| When | Who | What |
|---|---|---|
| **Mon W1** | All | Kick-off: align on architecture, schemas, conventions |
| **Fri W1** | All | Demo: each person shows working piece; integration check |
| **Wed W2** | P1 + P3 | API contract review: verify schemas match implementations |
| **Wed W2** | P2 + P3 | Frontend integration session: verify API shapes match components |
| **Fri W2** | All | Demo: upload → clean → train → results (end-to-end) |
| **Fri W3** | All | Demo: full flow including chat + reports |
| **Wed W4** | All | Code freeze: no new features; bug fixes only |
| **Fri W4** | All | MVP demo + retrospective |

### Git Workflow

```
main ──────────────────────────────────────────────────── (production)
  │
  └── develop ─────────────────────────────────────────── (integration)
        │
        ├── feature/p1-data-pipeline ──── (P1 branches)
        ├── feature/p2-upload-page ────── (P2 branches)
        ├── feature/p3-ml-router ──────── (P3 branches)
        ├── feature/p4-docker-setup ───── (P4 branches)
        └── feature/p5-unit-tests ─────── (P5 branches)
```

- **Branch naming:** `feature/{person}-{short-description}`
- **PR required:** All merges to `develop` require 1 review
- **CI must pass** before merge
- **`develop` → `main`** only on Friday demos (after QA sign-off)

---

## Risk Mitigation

| Risk | Probability | Impact | Mitigation | Owner |
|---|---|---|---|---|
| LLM API keys not provisioned | Low | Blocks chatbot (Week 3) | Provision keys in Week 1; test connectivity | P3 |
| FLAML training exceeds memory | Medium | Breaks ML pipeline | `time_budget=300`, memory monitoring, smaller model pool | P1 |
| Frontend-backend schema mismatch | Medium | Integration delays | Joint schema review Wed W2; TypeScript-like Zod schemas on frontend | P2 + P3 |
| CI pipeline flaky | Medium | Blocks merges | Fix flakes immediately; use `pytest-rerunfailures` | P4 |
| Scope creep | High | Delays MVP | Strict feature freeze; anything not in plan goes to backlog | All |
| Team member unavailable | Low | Delays their track | Cross-training in Week 1; documented handoff procedures | All |

---

## MVP Definition of Done

### Must-Have for v0.1.0 Release

- [ ] User can register and log in
- [ ] User can upload CSV/XLSX files (≤200MB)
- [ ] System auto-detects column types with ≥95% accuracy
- [ ] Data cleaning pipeline handles nulls, outliers, duplicates
- [ ] Before/after data quality comparison shown
- [ ] Task type (classification/regression) auto-detected
- [ ] ≥5 ML models trained via FLAML
- [ ] Best model recommended with justification and feature importance
- [ ] RAG chatbot answers questions with citations using GPT-4
- [ ] Chatbot says "I don't know" instead of hallucinating
- [ ] Basic HTML report generated with data quality + model results
- [ ] All pages responsive (mobile, tablet, desktop)
- [ ] Docker Compose runs full stack with single command
- [ ] CI pipeline passes: lint + tests + build
- [ ] ≥70% backend test coverage
- [ ] README with setup instructions

### Nice-to-Have (if time permits)

- [ ] Claude + Gemini support (multi-LLM)
- [ ] PDF report export
- [ ] SHAP plots in dashboard
- [ ] Dark theme
- [ ] Clustering support

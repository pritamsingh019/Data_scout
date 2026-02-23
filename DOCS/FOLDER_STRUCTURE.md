# DATA_SCOUT — Folder Structure

**Version:** 1.0 | **Last Updated:** 2026-02-21

---

## Complete Project Tree

```
data_scout/
│
├── 📂 frontend/                          # React SPA (Vite)
│   ├── 📂 public/
│   │   ├── favicon.ico                   # App favicon
│   │   ├── logo.svg                      # DATA_SCOUT logo asset
│   │   └── manifest.json                 # PWA manifest
│   │
│   ├── 📂 src/
│   │   ├── 📂 assets/                    # Static assets (images, fonts, icons)
│   │   │   ├── 📂 images/                # Illustrations, backgrounds
│   │   │   ├── 📂 icons/                 # Custom SVG icons
│   │   │   └── 📂 fonts/                 # Self-hosted fonts (if any)
│   │   │
│   │   ├── 📂 components/                # Reusable UI components
│   │   │   ├── 📂 ui/                    # Atomic design primitives
│   │   │   │   ├── Button.jsx            # Primary, secondary, ghost, danger variants
│   │   │   │   ├── Button.module.css
│   │   │   │   ├── Input.jsx             # Text, number, search input field
│   │   │   │   ├── Input.module.css
│   │   │   │   ├── Modal.jsx             # Overlay dialog with backdrop
│   │   │   │   ├── Modal.module.css
│   │   │   │   ├── Badge.jsx             # Status badges (success, warning, error)
│   │   │   │   ├── Card.jsx              # Content container with shadow & border
│   │   │   │   ├── Card.module.css
│   │   │   │   ├── Spinner.jsx           # Loading spinner animation
│   │   │   │   ├── Toast.jsx             # Notification toasts (auto-dismiss)
│   │   │   │   ├── Tooltip.jsx           # Hover tooltip
│   │   │   │   ├── Dropdown.jsx          # Select dropdown menu
│   │   │   │   ├── ProgressBar.jsx       # Determinate & indeterminate progress
│   │   │   │   ├── Skeleton.jsx          # Skeleton loading placeholder
│   │   │   │   ├── Tabs.jsx              # Tab switcher component
│   │   │   │   └── Toggle.jsx            # Boolean toggle switch
│   │   │   │
│   │   │   ├── 📂 layout/               # Page layout wrappers
│   │   │   │   ├── Header.jsx            # Top nav bar with logo, nav links, user menu
│   │   │   │   ├── Header.module.css
│   │   │   │   ├── Sidebar.jsx           # Collapsible side navigation
│   │   │   │   ├── Sidebar.module.css
│   │   │   │   ├── PageContainer.jsx     # Max-width wrapper with padding
│   │   │   │   ├── Footer.jsx            # Footer with links and copyright
│   │   │   │   └── ProtectedLayout.jsx   # Auth guard wrapper; redirects unauthenticated
│   │   │   │
│   │   │   ├── 📂 Upload/               # File upload feature
│   │   │   │   ├── FileDropzone.jsx      # Drag-and-drop area with validation
│   │   │   │   ├── FileDropzone.module.css
│   │   │   │   ├── UploadProgress.jsx    # Per-file upload progress bar
│   │   │   │   └── FileList.jsx          # List of uploaded files with status & actions
│   │   │   │
│   │   │   ├── 📂 DataPreview/           # Data exploration widgets
│   │   │   │   ├── DataTable.jsx         # Interactive table (sort, filter, paginate)
│   │   │   │   ├── DataTable.module.css
│   │   │   │   ├── ColumnTypeTag.jsx     # Inline dtype badge (numeric, categorical, etc.)
│   │   │   │   ├── QualityPanel.jsx      # Data quality score card (nulls, outliers, etc.)
│   │   │   │   ├── BeforeAfterView.jsx   # Side-by-side raw vs cleaned comparison
│   │   │   │   ├── NullHeatmap.jsx       # Visual null-value heatmap per column
│   │   │   │   └── CleaningActionLog.jsx # List of cleaning actions taken by the system
│   │   │   │
│   │   │   ├── 📂 MLDashboard/           # ML training & results
│   │   │   │   ├── TrainingProgress.jsx  # Animated progress with model name + ETA
│   │   │   │   ├── ModelCard.jsx         # Single model metrics card (expandable)
│   │   │   │   ├── ModelCard.module.css
│   │   │   │   ├── ComparisonTable.jsx   # Multi-model metrics comparison table
│   │   │   │   ├── RecommendationCard.jsx# Highlighted best-model card with justification
│   │   │   │   ├── FeatureImportance.jsx # Horizontal bar chart of feature importances
│   │   │   │   ├── ShapPlot.jsx          # SHAP beeswarm plot (rendered from image)
│   │   │   │   ├── OverfitIndicator.jsx  # Train-test gap visual indicator
│   │   │   │   └── TaskTypeDetector.jsx  # Task type result with confidence meter
│   │   │   │
│   │   │   ├── 📂 ChatPanel/             # RAG chatbot interface
│   │   │   │   ├── ChatContainer.jsx     # Full chat layout (messages + input)
│   │   │   │   ├── ChatContainer.module.css
│   │   │   │   ├── ChatMessage.jsx       # Single message bubble (user or assistant)
│   │   │   │   ├── ChatInput.jsx         # Text input with send button
│   │   │   │   ├── CitationCard.jsx      # Expandable citation reference
│   │   │   │   ├── ProviderSelector.jsx  # LLM provider dropdown (GPT/Claude/Gemini)
│   │   │   │   ├── TypingIndicator.jsx   # Three-dot typing animation
│   │   │   │   └── SuggestedQuestions.jsx# Pre-set question chips for empty state
│   │   │   │
│   │   │   └── 📂 ReportViewer/          # Report generation & viewing
│   │   │       ├── ReportPreview.jsx     # Full report preview with scroll
│   │   │       ├── ReportPreview.module.css
│   │   │       ├── SectionToggle.jsx     # Checkbox list to include/exclude sections
│   │   │       ├── ExportButton.jsx      # Download button (HTML/PDF format picker)
│   │   │       └── ReportChart.jsx       # Chart wrapper used inside reports
│   │   │
│   │   ├── 📂 pages/                     # Route-level page components
│   │   │   ├── HomePage.jsx              # Landing page with hero, features, CTA
│   │   │   ├── HomePage.module.css
│   │   │   ├── LoginPage.jsx             # Email/password login form
│   │   │   ├── RegisterPage.jsx          # Registration form
│   │   │   ├── UploadPage.jsx            # File upload workflow page
│   │   │   ├── DataPage.jsx              # Data preview + cleaning trigger + quality
│   │   │   ├── TrainingPage.jsx          # ML config form + training progress
│   │   │   ├── ResultsPage.jsx           # Model comparison + recommendation
│   │   │   ├── ChatPage.jsx              # Full-page chatbot experience
│   │   │   ├── ReportPage.jsx            # Report configuration + preview
│   │   │   ├── DashboardPage.jsx         # User dashboard (datasets, jobs, history)
│   │   │   └── NotFoundPage.jsx          # 404 error page
│   │   │
│   │   ├── 📂 hooks/                     # Custom React hooks
│   │   │   ├── useWebSocket.js           # WebSocket connection with auto-reconnect
│   │   │   ├── useUpload.js              # File upload with progress tracking
│   │   │   ├── useJobPolling.js          # Poll async job status (WS + HTTP fallback)
│   │   │   ├── useAuth.js               # Login, logout, token refresh logic
│   │   │   ├── useDebounce.js            # Debounced value for search inputs
│   │   │   └── useMediaQuery.js          # Responsive breakpoint detection
│   │   │
│   │   ├── 📂 services/                  # API client layer
│   │   │   ├── api.js                    # Axios instance with interceptors (auth, retry)
│   │   │   ├── uploadService.js          # POST /upload, GET /upload/:id
│   │   │   ├── dataService.js            # GET /data/preview, POST /data/clean
│   │   │   ├── mlService.js              # POST /ml/train, GET /ml/results
│   │   │   ├── chatService.js            # POST /chat/message, GET /chat/history
│   │   │   └── reportService.js          # POST /report/generate, GET /report/:id
│   │   │
│   │   ├── 📂 store/                     # Zustand state stores
│   │   │   ├── useAuthStore.js           # User session, access/refresh tokens
│   │   │   ├── useDatasetStore.js        # Dataset list, active dataset, quality
│   │   │   ├── useJobStore.js            # Running jobs, progress percentages
│   │   │   ├── useChatStore.js           # Conversation history, LLM provider
│   │   │   └── useToastStore.js          # Global toast notification queue
│   │   │
│   │   ├── 📂 utils/                     # Utility functions
│   │   │   ├── formatters.js             # formatBytes(), formatDate(), formatPercent()
│   │   │   ├── constants.js              # API_URL, WS_URL, MAX_FILE_SIZE, SUPPORTED_FORMATS
│   │   │   └── validators.js             # validateEmail(), validateFileType()
│   │   │
│   │   ├── 📂 styles/                    # Global styles & design tokens
│   │   │   ├── globals.css               # CSS reset, base typography, CSS variables
│   │   │   ├── variables.css             # Design tokens: colors, spacing, radii, shadows
│   │   │   └── animations.css            # Keyframes: fadeIn, slideUp, pulse, shimmer
│   │   │
│   │   ├── App.jsx                       # Root component: router + layout + providers
│   │   └── main.jsx                      # Entry point: ReactDOM.createRoot()
│   │
│   ├── .eslintrc.cjs                     # ESLint config (Airbnb + React rules)
│   ├── vite.config.js                    # Vite config: proxy, aliases, build options
│   ├── package.json                      # Dependencies & scripts
│   ├── package-lock.json
│   └── Dockerfile                        # Multi-stage: build → Nginx
│
├── 📂 backend/                           # FastAPI application
│   ├── 📂 app/
│   │   ├── 📂 api/
│   │   │   ├── 📂 v1/
│   │   │   │   ├── 📂 routers/           # HTTP route handlers
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── upload.py         # POST /upload, GET/DELETE /upload/:id
│   │   │   │   │   ├── data.py           # GET /data/preview, POST /data/clean, GET /data/quality
│   │   │   │   │   ├── ml.py             # POST /ml/train, GET /ml/status, GET /ml/results
│   │   │   │   │   ├── chat.py           # POST /chat/message, GET /chat/history, PUT /chat/settings
│   │   │   │   │   ├── report.py         # POST /report/generate, GET /report/:id, GET /report/download
│   │   │   │   │   ├── auth.py           # POST /auth/register, POST /auth/login, POST /auth/refresh
│   │   │   │   │   ├── jobs.py           # GET /jobs/:id, DELETE /jobs/:id (cancel)
│   │   │   │   │   └── health.py         # GET /health (readiness + liveness probe)
│   │   │   │   └── dependencies.py       # Shared FastAPI dependencies (get_db, get_user, etc.)
│   │   │   └── __init__.py
│   │   │
│   │   ├── 📂 core/                      # Application configuration & cross-cutting
│   │   │   ├── __init__.py
│   │   │   ├── config.py                 # Pydantic Settings: DB_URL, REDIS_URL, API keys, limits
│   │   │   ├── security.py               # JWT encode/decode, password hashing (bcrypt)
│   │   │   ├── logging.py                # Structured JSON logger setup (structlog)
│   │   │   ├── exceptions.py             # Custom exception classes + handlers
│   │   │   └── celery_app.py             # Celery app initialization + configuration
│   │   │
│   │   ├── 📂 models/                    # SQLAlchemy ORM models
│   │   │   ├── __init__.py
│   │   │   ├── base.py                   # DeclarativeBase + common mixins (timestamps)
│   │   │   ├── user.py                   # User model (id, email, hashed_password, role)
│   │   │   ├── dataset.py                # Dataset model (id, owner, filename, status, metadata)
│   │   │   ├── job.py                    # Job model (id, type, status, progress, result)
│   │   │   ├── model_result.py           # TrainedModel (id, dataset, name, metrics, path)
│   │   │   ├── conversation.py           # Conversation (id, dataset, messages, provider)
│   │   │   └── report.py                 # Report (id, dataset, sections, format, path)
│   │   │
│   │   ├── 📂 schemas/                   # Pydantic request/response schemas
│   │   │   ├── __init__.py
│   │   │   ├── auth.py                   # LoginRequest, RegisterRequest, TokenResponse
│   │   │   ├── upload.py                 # UploadResponse, DatasetInfo
│   │   │   ├── data.py                   # PreviewResponse, CleanRequest, QualityReport
│   │   │   ├── ml.py                     # TrainRequest, TrainStatus, MLResults, ModelMetrics
│   │   │   ├── chat.py                   # ChatMessage, ChatResponse, Citation, ChatSettings
│   │   │   ├── report.py                 # ReportRequest, ReportResponse
│   │   │   └── common.py                 # ErrorResponse, JobStatus, PaginationParams
│   │   │
│   │   ├── 📂 services/                  # Business logic layer
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py           # Register, login, verify JWT, refresh token
│   │   │   ├── data_service.py           # Ingest file, trigger cleaning, return quality report
│   │   │   ├── ml_service.py             # Orchestrate: task detection → train → evaluate → recommend
│   │   │   ├── rag_service.py            # Embed chunks, FAISS index, retrieve, call LLM, validate
│   │   │   └── report_service.py         # Build report from template + data + charts
│   │   │
│   │   ├── 📂 workers/                   # Celery async task definitions
│   │   │   ├── __init__.py
│   │   │   ├── data_tasks.py             # clean_dataset_task: ingest → validate → clean → store
│   │   │   ├── ml_tasks.py               # train_models_task: detect → FLAML → evaluate → save
│   │   │   └── report_tasks.py           # generate_report_task: aggregate → chart → export
│   │   │
│   │   ├── 📂 pipelines/                 # Data & ML processing logic
│   │   │   ├── __init__.py
│   │   │   ├── ingestion.py              # File parsing (CSV, XLSX, TSV, JSON); chunked reading
│   │   │   ├── type_detection.py         # Multi-heuristic column type inference
│   │   │   ├── cleaning.py               # Missing values, dedup, outliers, encoding
│   │   │   ├── feature_engineering.py    # Datetime features, interactions, frequency encoding
│   │   │   ├── validation.py             # Pre/post cleaning validation; data quality score
│   │   │   ├── task_detection.py         # Classification / regression / clustering detection
│   │   │   ├── model_training.py         # FLAML AutoML wrapper; model pool selection
│   │   │   ├── evaluation.py             # Metrics computation, overfitting check
│   │   │   └── explainability.py         # SHAP values, feature importance, model card
│   │   │
│   │   ├── 📂 llm/                       # LLM provider abstraction
│   │   │   ├── __init__.py
│   │   │   ├── base.py                   # Abstract LLMProvider class
│   │   │   ├── openai_provider.py        # OpenAI GPT-4 implementation
│   │   │   ├── anthropic_provider.py     # Anthropic Claude implementation
│   │   │   ├── google_provider.py        # Google Gemini implementation
│   │   │   └── factory.py               # LLMFactory: create provider by name + fallback chain
│   │   │
│   │   ├── 📂 db/                        # Database utilities
│   │   │   ├── __init__.py
│   │   │   ├── session.py                # AsyncSession factory, get_db dependency
│   │   │   └── init_db.py               # Create tables, seed initial data
│   │   │
│   │   ├── 📂 websocket/                 # WebSocket handlers
│   │   │   ├── __init__.py
│   │   │   └── job_progress.py           # WS endpoint: stream job progress to client
│   │   │
│   │   └── main.py                       # FastAPI app factory: create_app(), CORS, routers
│   │
│   ├── 📂 alembic/                       # Database migrations
│   │   ├── env.py                        # Alembic environment config
│   │   ├── alembic.ini                   # Migration settings
│   │   └── 📂 versions/                  # Auto-generated migration scripts
│   │       ├── 001_initial_tables.py     # Users, datasets, jobs, conversations
│   │       └── 002_add_reports.py        # Reports table
│   │
│   ├── 📂 tests/                         # Test suite
│   │   ├── 📂 unit/                      # Unit tests (no external dependencies)
│   │   │   ├── test_type_detection.py    # Column type inference tests
│   │   │   ├── test_task_detection.py    # ML task detection tests
│   │   │   ├── test_imputation.py        # Missing value strategies
│   │   │   ├── test_outliers.py          # Outlier detection methods
│   │   │   ├── test_features.py          # Feature engineering logic
│   │   │   ├── test_schemas.py           # Pydantic schema validation
│   │   │   ├── test_auth.py              # JWT + password hashing
│   │   │   └── test_llm_providers.py     # LLM abstraction (mocked)
│   │   │
│   │   ├── 📂 integration/              # Integration tests (with DB, Redis)
│   │   │   ├── test_upload_flow.py       # Upload → preview
│   │   │   ├── test_cleaning_flow.py     # Upload → clean → quality
│   │   │   ├── test_training_flow.py     # Upload → clean → train → results
│   │   │   ├── test_chat_flow.py         # Upload → index → chat
│   │   │   ├── test_report_flow.py       # Full report generation pipeline
│   │   │   └── test_auth_flow.py         # Register → login → access → refresh
│   │   │
│   │   ├── 📂 ml_validation/            # ML model quality tests
│   │   │   ├── test_classification.py    # Iris, imbalanced datasets
│   │   │   ├── test_regression.py        # Boston Housing, continuous targets
│   │   │   └── test_clustering.py        # Synthetic blobs
│   │   │
│   │   ├── 📂 fixtures/                  # Test data files
│   │   │   ├── sample_clean.csv          # Clean CSV for quick tests
│   │   │   ├── sample_messy.csv          # CSV with nulls, outliers, mixed types
│   │   │   ├── sample_large.csv          # 100K rows for performance tests
│   │   │   └── sample_imbalanced.csv     # 95/5 class imbalance
│   │   │
│   │   ├── conftest.py                   # Shared fixtures: test DB, client, auth
│   │   └── locustfile.py                 # Load testing scripts
│   │
│   ├── requirements.txt                  # Python dependencies (pinned versions)
│   ├── requirements-dev.txt              # Dev-only: pytest, ruff, pre-commit
│   └── Dockerfile                        # Python 3.11-slim + dependencies
│
├── 📂 nginx/                             # Reverse proxy configuration
│   ├── nginx.conf                        # SSL, rate limiting, proxy_pass rules
│   └── 📂 certs/                         # SSL certificates (not committed)
│       ├── fullchain.pem
│       └── privkey.pem
│
├── 📂 scripts/                           # Utility & deploy scripts
│   ├── seed_db.py                        # Seed database with test users + sample dataset
│   ├── create_superuser.py               # CLI to create admin user
│   ├── migrate.sh                        # Run Alembic upgrade head
│   └── healthcheck.sh                    # Verify all services are healthy
│
├── 📂 DOCS/                              # Project documentation
│   ├── PRD.md                            # Product Requirements Document
│   ├── ARCHITECTURE.md                   # System architecture & diagrams
│   ├── API_SPEC.md                       # REST API specification
│   ├── DATA_PIPELINE.md                  # Data ingestion & cleaning pipeline
│   ├── ML_PIPELINE.md                    # ML task detection, training, evaluation
│   ├── RAG_CHATBOT.md                    # RAG retrieval, prompts, hallucination
│   ├── FRONTEND_SPEC.md                  # React architecture & state management
│   ├── FRONTEND_DESIGN.md               # Visual design system & page layouts
│   ├── DEPLOYMENT.md                     # Docker, CI/CD, cloud architecture
│   ├── SECURITY.md                       # Privacy, auth, encryption, LLM policy
│   ├── TEST_PLAN.md                      # Unit, integration, ML, load tests
│   ├── ROADMAP.md                        # Phased milestones & future features
│   ├── RISKS.md                          # Technical, ethical risks & mitigations
│   └── FOLDER_STRUCTURE.md              # This file
│
├── 📂 .github/                           # GitHub configuration
│   ├── 📂 workflows/
│   │   ├── ci.yml                        # Lint + test on push/PR
│   │   └── deploy.yml                    # Build + push images + SSH deploy
│   ├── PULL_REQUEST_TEMPLATE.md          # PR checklist template
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md                 # Bug report template
│       └── feature_request.md            # Feature request template
│
├── docker-compose.yml                    # All services: frontend, backend, workers, DB, Redis, MinIO, Nginx
├── docker-compose.dev.yml                # Dev overrides: hot-reload, debug ports, no SSL
├── .env.example                          # Template for environment variables
├── .gitignore                            # Ignore: __pycache__, .env, node_modules, *.pkl, uploads/
├── .pre-commit-config.yaml               # Pre-commit hooks: ruff, eslint, prettier
├── Makefile                              # Common commands: make dev, make test, make build, make deploy
├── LICENSE                               # Project license (MIT)
└── README.md                             # Getting started guide
```

---

## Module Summary

| Module | Files | Purpose |
|---|---|---|
| `frontend/src/components/ui/` | 15 | Atomic UI primitives (Button, Input, Modal, etc.) |
| `frontend/src/components/` (feature) | 22 | Feature-specific components (Upload, DataPreview, ML, Chat, Report) |
| `frontend/src/pages/` | 11 | Route-level page components |
| `frontend/src/hooks/` | 6 | Custom React hooks |
| `frontend/src/services/` | 6 | API client functions |
| `frontend/src/store/` | 5 | Zustand state stores |
| `backend/app/api/v1/routers/` | 8 | REST API route handlers |
| `backend/app/core/` | 5 | Config, security, logging, exceptions, Celery |
| `backend/app/models/` | 7 | SQLAlchemy ORM models |
| `backend/app/schemas/` | 7 | Pydantic request/response schemas |
| `backend/app/services/` | 5 | Business logic layer |
| `backend/app/workers/` | 3 | Celery async tasks |
| `backend/app/pipelines/` | 9 | Data & ML processing logic |
| `backend/app/llm/` | 5 | Multi-LLM provider abstraction |
| `backend/tests/` | 17 | Unit, integration, ML validation tests |
| Total | **~130 files** | |

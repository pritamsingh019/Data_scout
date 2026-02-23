# 🔍 DATA_SCOUT

> **AI-Powered Data Analysis Platform** — Upload → Clean → Train → Chat → Report

DATA_SCOUT automates the entire data-to-insight pipeline: intelligent data cleaning, AutoML model training with explainability, RAG-powered chatbot for natural-language data exploration, and customizable report generation.

---

## ✨ Features

- **Smart Data Cleaning** — Auto-detect column types, handle missing values, remove outliers
- **AutoML Training** — Train & compare 5+ models via FLAML with one click
- **Model Explainability** — SHAP plots, feature importance, overfitting detection
- **RAG Chatbot** — Ask questions about your data with cited, grounded answers
- **Multi-LLM Support** — GPT-4, Claude, Gemini with automatic fallback
- **Report Generation** — Customizable HTML/PDF reports with charts
- **Real-time Progress** — WebSocket-based live training updates

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 20+ (for local frontend dev)
- Python 3.11+ (for local backend dev)

### Setup

```bash
# Clone the repository
git clone https://github.com/your-org/data_scout.git
cd data_scout

# Copy environment variables
cp .env.example .env
# Edit .env with your API keys and settings

# Start all services
make dev
```

The app will be available at:
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000/docs
- **MinIO Console:** http://localhost:9001

---

## 📁 Project Structure

```
data_scout/
├── frontend/          # React SPA (Vite)
├── backend/           # FastAPI application
├── nginx/             # Reverse proxy configuration
├── scripts/           # Utility & deploy scripts
├── DOCS/              # Project documentation
├── .github/           # CI/CD workflows
├── docker-compose.yml # Production services
└── Makefile           # Common commands
```

See [DOCS/FOLDER_STRUCTURE.md](DOCS/FOLDER_STRUCTURE.md) for the complete project tree.

---

## 🛠 Development

```bash
make dev          # Start dev environment with hot-reload
make test         # Run all tests
make lint         # Lint all code
make migrate      # Run database migrations
make seed         # Seed database with test data
make help         # Show all available commands
```

---

## 📖 Documentation

| Document | Description |
|---|---|
| [PRD](DOCS/PRD.md) | Product Requirements |
| [Architecture](DOCS/ARCHITECTURE.md) | System Architecture |
| [API Spec](DOCS/API_SPEC.md) | REST API Specification |
| [Data Pipeline](DOCS/DATA_PIPELINE.md) | Data Processing Pipeline |
| [ML Pipeline](DOCS/ML_PIPELINE.md) | ML Training Pipeline |
| [Frontend Design](DOCS/FRONTEND_DESIGN.md) | Visual Design System |
| [Deployment](DOCS/DEPLOYMENT.md) | Docker & CI/CD |
| [Security](DOCS/SECURITY.md) | Security & Privacy |

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

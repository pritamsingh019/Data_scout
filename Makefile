# ═══════════════════════════════════════════════
# DATA_SCOUT — Makefile
# ═══════════════════════════════════════════════

.PHONY: dev build test lint migrate seed logs clean help

# ── Development ───────────────────────────────
dev: ## Start all services in development mode
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build

up: ## Start all services in production mode
	docker compose up -d --build

down: ## Stop all services
	docker compose down

# ── Build ─────────────────────────────────────
build: ## Build all Docker images
	docker compose build

# ── Testing ───────────────────────────────────
test: ## Run all tests (backend + frontend)
	docker compose exec backend pytest --cov=app --cov-report=term-missing
	docker compose exec frontend npm test

test-backend: ## Run backend tests only
	docker compose exec backend pytest --cov=app --cov-report=term-missing -v

test-frontend: ## Run frontend tests only
	docker compose exec frontend npm test

# ── Linting ───────────────────────────────────
lint: ## Lint all code
	docker compose exec backend ruff check .
	docker compose exec frontend npm run lint

fmt: ## Format all code
	docker compose exec backend ruff format .

# ── Database ──────────────────────────────────
migrate: ## Run database migrations
	docker compose exec backend alembic upgrade head

seed: ## Seed database with test data
	docker compose exec backend python -m scripts.seed_db

# ── Logs ──────────────────────────────────────
logs: ## Tail logs for all services
	docker compose logs -f

logs-backend: ## Tail backend logs
	docker compose logs -f backend

logs-worker: ## Tail celery worker logs
	docker compose logs -f celery-worker

# ── Cleanup ───────────────────────────────────
clean: ## Remove all containers, volumes, and images
	docker compose down -v --rmi local
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true

# ── Help ──────────────────────────────────────
help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help

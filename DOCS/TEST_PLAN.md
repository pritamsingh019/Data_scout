# DATA_SCOUT — Test Plan

**Version:** 1.0 | **Last Updated:** 2026-02-20

---

## 1. Unit Tests

### 1.1 Backend Unit Tests

| Module | Test File | Key Test Cases | Framework |
|---|---|---|---|
| **Data type detection** | `test_type_detection.py` | Numeric, categorical, datetime, boolean, mixed-type columns | pytest |
| **Missing value imputation** | `test_imputation.py` | Mean/median/mode strategies; edge cases (all-null, single-value) | pytest |
| **Outlier detection** | `test_outliers.py` | IQR/Z-score methods; edge: no outliers, all outliers | pytest |
| **Task detection** | `test_task_detection.py` | Classification (binary/multi), regression, clustering detection | pytest |
| **Feature engineering** | `test_features.py` | Datetime extraction, frequency encoding, interaction terms | pytest |
| **Pydantic schemas** | `test_schemas.py` | Valid/invalid request bodies; boundary values | pytest |
| **Auth service** | `test_auth.py` | Registration, login, JWT validation, refresh, expiry | pytest |
| **LLM abstraction** | `test_llm_providers.py` | Provider factory, fallback chain, error handling | pytest + unittest.mock |

#### Example: Task Detection Unit Test

```python
# tests/unit/test_task_detection.py
import pandas as pd
import pytest
from app.pipelines.task_detection import detect_task_type

class TestTaskDetection:
    def test_binary_classification(self):
        df = pd.DataFrame({"feature": [1, 2, 3, 4], "target": [0, 1, 0, 1]})
        result = detect_task_type(df, "target")
        assert result.task_type == "classification"
        assert result.confidence >= 0.90

    def test_regression_float_target(self):
        df = pd.DataFrame({"feature": range(100), "target": [x * 1.5 for x in range(100)]})
        result = detect_task_type(df, "target")
        assert result.task_type == "regression"

    def test_clustering_no_target(self):
        df = pd.DataFrame({"f1": range(50), "f2": range(50)})
        result = detect_task_type(df, target_column=None)
        assert result.task_type == "clustering"

    def test_multiclass_string_target(self):
        df = pd.DataFrame({"f1": range(90), "target": ["A"] * 30 + ["B"] * 30 + ["C"] * 30})
        result = detect_task_type(df, "target")
        assert result.task_type == "classification"

    def test_constant_target_raises_error(self):
        df = pd.DataFrame({"f1": range(10), "target": [1] * 10})
        with pytest.raises(ValueError, match="no variance"):
            detect_task_type(df, "target")
```

### 1.2 Frontend Unit Tests

| Component | Test File | Key Test Cases | Framework |
|---|---|---|---|
| `FileDropzone` | `FileDropzone.test.jsx` | Valid file accepted, oversized rejected, wrong type rejected | Vitest + React Testing Library |
| `DataTable` | `DataTable.test.jsx` | Renders columns/rows, sorting, pagination | Vitest + RTL |
| `ModelCard` | `ModelCard.test.jsx` | Displays metrics, recommendation badge, download link | Vitest + RTL |
| `ChatMessage` | `ChatMessage.test.jsx` | User/assistant messages, citation links, loading state | Vitest + RTL |
| `useWebSocket` | `useWebSocket.test.js` | Connect, receive message, auto-reconnect, cleanup | Vitest |
| Zustand stores | `stores.test.js` | State mutations, computed values, reset | Vitest |

---

## 2. Integration Tests

### 2.1 API Integration Tests

| Flow | Test File | Steps | Expected |
|---|---|---|---|
| **Upload → Preview** | `test_upload_flow.py` | Upload CSV → GET preview | 201 → 200 with correct row/col counts |
| **Upload → Clean → Quality** | `test_cleaning_flow.py` | Upload → POST clean → poll job → GET quality | Quality report shows 0 nulls |
| **Upload → Train → Results** | `test_training_flow.py` | Upload → Clean → POST train → poll → GET results | ≥5 models evaluated; recommendation present |
| **Chat flow** | `test_chat_flow.py` | Upload → Index → POST message → validate response | Response contains citations |
| **Report generation** | `test_report_flow.py` | Upload → Clean → Train → POST report → download | Valid HTML/PDF file |
| **Auth flow** | `test_auth_flow.py` | Register → Login → Access protected → Refresh → Logout | Tokens work correctly |

#### Example: Upload → Clean Integration Test

```python
# tests/integration/test_cleaning_flow.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_upload_and_clean(client, auth_headers, sample_csv_with_nulls):
    # Step 1: Upload
    response = await client.post(
        "/api/v1/upload",
        files={"file": ("test.csv", sample_csv_with_nulls, "text/csv")},
        headers=auth_headers,
    )
    assert response.status_code == 201
    dataset_id = response.json()["dataset_id"]

    # Step 2: Trigger cleaning
    response = await client.post(
        f"/api/v1/data/{dataset_id}/clean",
        json={"missing_strategy": "auto"},
        headers=auth_headers,
    )
    assert response.status_code == 202
    job_id = response.json()["job_id"]

    # Step 3: Poll until complete
    for _ in range(30):
        response = await client.get(f"/api/v1/jobs/{job_id}", headers=auth_headers)
        if response.json()["status"] == "SUCCESS":
            break
        await asyncio.sleep(1)

    # Step 4: Verify quality
    response = await client.get(f"/api/v1/data/{dataset_id}/quality", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["after"]["null_percentage"] == 0.0
```

### 2.2 Database Integration Tests

| Test | Description |
|---|---|
| Migration test | Run all Alembic migrations up/down; verify schema |
| Concurrent access | 10 parallel dataset uploads; no deadlocks |
| Cascade delete | Delete user → verify all datasets, models, reports removed |

---

## 3. ML Validation Tests

### 3.1 Model Quality Tests

| Test | Dataset | Pass Criteria |
|---|---|---|
| **Classification baseline** | Iris (150 rows, 4 features) | Best model accuracy ≥ 0.95 |
| **Regression baseline** | Boston Housing (506 rows) | Best model R² ≥ 0.80 |
| **Clustering baseline** | Blobs (300 rows, 3 clusters) | Silhouette ≥ 0.70 |
| **Messy data handling** | Iris + 20% injected nulls + 5% outliers | Pipeline completes; accuracy ≥ 0.85 |
| **High cardinality** | 50 features, 10K rows, mixed types | FLAML completes within time budget |
| **Imbalanced classes** | 95/5 split binary dataset | F1 ≥ 0.60 on minority class |

### 3.2 Overfitting Detection Tests

```python
def test_overfitting_detected():
    """Verify overfitting is flagged when train >> test."""
    result = detect_overfitting(train_score=0.99, test_score=0.72)
    assert result["is_overfitting"] is True
    assert result["severity"] == "high"

def test_no_overfitting():
    result = detect_overfitting(train_score=0.93, test_score=0.91)
    assert result["is_overfitting"] is False
    assert result["severity"] == "none"
```

### 3.3 RAG Quality Tests

| Test | Input | Expected |
|---|---|---|
| **Grounded answer** | Question about existing column | Answer cites specific rows/values |
| **Out-of-scope question** | "What's the weather today?" | "This question doesn't relate to your dataset" |
| **No retrieval match** | Obscure question with no matching data | "I don't have enough data to answer" |
| **Numerical accuracy** | "What is the average revenue?" | Answer matches `df['revenue'].mean()` ± 1% |
| **Hallucination detection** | Force low-quality retrieval | Response flagged as low-confidence |

---

## 4. Load Testing

### 4.1 Tool

[Locust](https://locust.io/) for HTTP load testing.

### 4.2 Scenarios

```python
# locustfile.py
from locust import HttpUser, task, between

class DataScoutUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        response = self.client.post("/api/v1/auth/login", json={
            "email": "loadtest@example.com", "password": "TestPass123!"
        })
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    @task(3)
    def upload_file(self):
        with open("test_data/small.csv", "rb") as f:
            self.client.post("/api/v1/upload",
                files={"file": ("test.csv", f, "text/csv")},
                headers=self.headers)

    @task(5)
    def preview_data(self):
        self.client.get("/api/v1/data/ds_test/preview?rows=20",
            headers=self.headers)

    @task(2)
    def chat_message(self):
        self.client.post("/api/v1/chat/message", json={
            "dataset_id": "ds_test",
            "message": "What is the average revenue?",
            "llm_provider": "openai"
        }, headers=self.headers)
```

### 4.3 Performance Targets

| Metric | Target | Test Configuration |
|---|---|---|
| API response time (p95) | ≤ 500ms (non-ML endpoints) | 50 concurrent users, 5 min |
| Upload throughput | ≥ 10 files/min (10MB each) | 20 concurrent users |
| Chat response time (p95) | ≤ 5s | 30 concurrent users |
| Concurrent training jobs | ≥ 5 without degradation | 5 simultaneous trains |
| Error rate under load | ≤ 1% | 100 concurrent users, 10 min |
| System recovery | Return to normal within 30s after spike | Spike to 200 users → back to 50 |

### 4.4 Run Commands

```bash
# Standard load test
locust -f locustfile.py --host http://localhost --users 50 --spawn-rate 5 --run-time 5m

# Stress test
locust -f locustfile.py --host http://localhost --users 200 --spawn-rate 20 --run-time 10m

# Headless with CSV report
locust -f locustfile.py --host http://localhost --users 50 --spawn-rate 5 \
  --run-time 5m --headless --csv=results/load_test
```

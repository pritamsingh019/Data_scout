# DATA_SCOUT — API Specification

**Version:** 1.0 | **Base URL:** `/api/v1` | **Auth:** Bearer JWT

---

## 1. Authentication

### Strategy

- **JWT-based authentication** with access + refresh tokens
- Access token: 30 min TTL, sent in `Authorization: Bearer <token>` header
- Refresh token: 7 day TTL, stored in HTTP-only cookie
- API key auth supported for programmatic access

### Endpoints

#### `POST /auth/register`
```json
// Request
{ "email": "user@example.com", "password": "Str0ng!Pass", "name": "Jane Doe" }

// Response 201
{ "id": "usr_abc123", "email": "user@example.com", "name": "Jane Doe", "created_at": "2026-02-20T12:00:00Z" }
```

#### `POST /auth/login`
```json
// Request
{ "email": "user@example.com", "password": "Str0ng!Pass" }

// Response 200
{ "access_token": "eyJ...", "token_type": "bearer", "expires_in": 1800 }
// Set-Cookie: refresh_token=eyJ...; HttpOnly; Secure; SameSite=Strict
```

#### `POST /auth/refresh`
```json
// Response 200 (uses refresh_token from cookie)
{ "access_token": "eyJ...", "token_type": "bearer", "expires_in": 1800 }
```

---

## 2. File Upload

#### `POST /upload`
Upload a dataset file (CSV, XLSX, TSV, JSON).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file` | `multipart/form-data` | Yes | Dataset file (max 200MB) |
| `name` | `string` | No | Display name (defaults to filename) |

```json
// Response 201
{
  "dataset_id": "ds_7f3a2b",
  "filename": "sales_2025.csv",
  "size_bytes": 15728640,
  "format": "csv",
  "status": "uploaded",
  "created_at": "2026-02-20T12:05:00Z"
}
```

#### `GET /upload/{dataset_id}`
```json
// Response 200
{
  "dataset_id": "ds_7f3a2b",
  "filename": "sales_2025.csv",
  "size_bytes": 15728640,
  "format": "csv",
  "status": "cleaned",        // uploaded | cleaning | cleaned | failed
  "row_count": 50000,
  "column_count": 18,
  "created_at": "2026-02-20T12:05:00Z"
}
```

#### `DELETE /upload/{dataset_id}`
```json
// Response 200
{ "message": "Dataset ds_7f3a2b deleted", "files_removed": ["raw", "cleaned", "vectors"] }
```

---

## 3. Data Pipeline

#### `GET /data/{dataset_id}/preview`
Returns first N rows of the dataset.

| Query Param | Type | Default | Description |
|---|---|---|---|
| `rows` | `int` | 20 | Number of rows (max 100) |
| `stage` | `string` | `raw` | `raw` or `cleaned` |

```json
// Response 200
{
  "columns": ["id", "name", "revenue", "date"],
  "dtypes": {"id": "int64", "name": "object", "revenue": "float64", "date": "datetime64"},
  "data": [
    {"id": 1, "name": "Widget A", "revenue": 1250.50, "date": "2025-01-15"},
    ...
  ],
  "total_rows": 50000
}
```

#### `POST /data/{dataset_id}/clean`
Triggers async data cleaning pipeline.

```json
// Request (optional overrides)
{
  "missing_strategy": "auto",          // auto | drop | mean | median | mode
  "outlier_method": "iqr",            // iqr | zscore | none
  "remove_duplicates": true,
  "encode_categoricals": true
}

// Response 202
{
  "job_id": "job_c4d5e6",
  "dataset_id": "ds_7f3a2b",
  "status": "PENDING",
  "message": "Data cleaning job queued"
}
```

#### `GET /data/{dataset_id}/quality`
```json
// Response 200
{
  "before": {
    "row_count": 50200, "null_percentage": 12.3, "duplicate_rows": 200,
    "columns_with_nulls": ["revenue", "region", "date"],
    "outlier_count": 145
  },
  "after": {
    "row_count": 49800, "null_percentage": 0.0, "duplicate_rows": 0,
    "columns_with_nulls": [],
    "outlier_count": 0
  },
  "actions_taken": [
    {"column": "revenue", "action": "median_imputation", "affected_rows": 3200},
    {"column": "region", "action": "mode_imputation", "affected_rows": 1500},
    {"column": "date", "action": "drop_rows", "affected_rows": 340},
    {"action": "remove_duplicates", "affected_rows": 200},
    {"action": "outlier_removal_iqr", "affected_rows": 145}
  ]
}
```

---

## 4. ML Pipeline

#### `POST /ml/train`
Starts async AutoML training.

```json
// Request
{
  "dataset_id": "ds_7f3a2b",
  "target_column": "churn",
  "time_budget_seconds": 300,
  "task_type": "auto",                 // auto | classification | regression | clustering
  "exclude_columns": ["customer_id"]
}

// Response 202
{
  "job_id": "job_m1n2o3",
  "dataset_id": "ds_7f3a2b",
  "status": "PENDING",
  "estimated_duration_seconds": 300
}
```

#### `GET /ml/status/{job_id}`
```json
// Response 200
{
  "job_id": "job_m1n2o3",
  "status": "PROGRESS",               // PENDING | PROGRESS | SUCCESS | FAILURE | REVOKED
  "percent": 45,
  "message": "Training model 3/8: RandomForest",
  "started_at": "2026-02-20T12:10:00Z"
}
```

#### `GET /ml/results/{dataset_id}`
```json
// Response 200
{
  "dataset_id": "ds_7f3a2b",
  "task_type": "classification",
  "task_confidence": 0.97,
  "models": [
    {
      "rank": 1,
      "name": "LGBMClassifier",
      "metrics": {"accuracy": 0.934, "f1": 0.921, "precision": 0.928, "recall": 0.915, "roc_auc": 0.962},
      "training_time_seconds": 42.3,
      "is_recommended": true
    },
    {
      "rank": 2,
      "name": "RandomForestClassifier",
      "metrics": {"accuracy": 0.918, "f1": 0.905, "precision": 0.912, "recall": 0.898, "roc_auc": 0.948},
      "training_time_seconds": 38.1,
      "is_recommended": false
    }
  ],
  "recommendation": {
    "model": "LGBMClassifier",
    "justification": "Highest F1 score (0.921) with fast training time. Strong performance across all metrics with no signs of overfitting (train-test gap < 2%).",
    "feature_importance": [
      {"feature": "monthly_charges", "importance": 0.234},
      {"feature": "tenure", "importance": 0.198},
      {"feature": "contract_type", "importance": 0.156}
    ]
  },
  "overfitting_check": {
    "train_score": 0.948,
    "test_score": 0.934,
    "gap": 0.014,
    "is_overfitting": false
  }
}
```

#### `GET /ml/download/{dataset_id}/{model_name}`
Downloads trained model as `.pkl` file.
- **Response:** `application/octet-stream` (binary pickle file)
- **Content-Disposition:** `attachment; filename="LGBMClassifier_ds_7f3a2b.pkl"`

---

## 5. RAG Chatbot

#### `POST /chat/message`
```json
// Request
{
  "dataset_id": "ds_7f3a2b",
  "message": "What are the top 3 factors driving customer churn?",
  "llm_provider": "openai",           // openai | anthropic | google
  "conversation_id": "conv_x1y2z3"    // optional, for multi-turn
}

// Response 200
{
  "conversation_id": "conv_x1y2z3",
  "message_id": "msg_a1b2c3",
  "response": "Based on the dataset, the top 3 factors driving churn are:\n1. **Monthly charges** — customers paying >$70/month churn at 2.3x the rate [rows with monthly_charges > 70, churn_rate = 42%]\n2. **Contract type** — month-to-month contracts have 3.5x higher churn [contract_type = 'Month-to-month', churn_rate = 48%]\n3. **Tenure** — customers with <12 months tenure are 2.1x more likely to churn [tenure < 12, churn_rate = 38%]",
  "citations": [
    {"source": "column: monthly_charges", "rows_referenced": "12,450 rows > $70", "confidence": 0.92},
    {"source": "column: contract_type", "rows_referenced": "3,420 month-to-month", "confidence": 0.95},
    {"source": "column: tenure", "rows_referenced": "8,230 rows < 12 months", "confidence": 0.89}
  ],
  "confidence": 0.91,
  "llm_provider_used": "openai"
}
```

#### `GET /chat/history/{conversation_id}`
```json
// Response 200
{
  "conversation_id": "conv_x1y2z3",
  "dataset_id": "ds_7f3a2b",
  "messages": [
    {"role": "user", "content": "What are the...", "timestamp": "..."},
    {"role": "assistant", "content": "Based on...", "timestamp": "...", "citations": [...]}
  ]
}
```

#### `PUT /chat/settings`
```json
// Request
{ "llm_provider": "anthropic", "temperature": 0.1, "max_tokens": 1024 }

// Response 200
{ "message": "Chat settings updated", "active_provider": "anthropic" }
```

---

## 6. Reports

#### `POST /report/generate`
```json
// Request
{
  "dataset_id": "ds_7f3a2b",
  "sections": ["summary", "data_quality", "model_comparison", "feature_importance", "recommendations"],
  "format": "html",                    // html | pdf
  "title": "Q4 Churn Analysis Report"
}

// Response 202
{ "job_id": "job_r1s2t3", "status": "PENDING", "message": "Report generation queued" }
```

#### `GET /report/{report_id}`
```json
// Response 200
{
  "report_id": "rpt_v4w5x6",
  "dataset_id": "ds_7f3a2b",
  "title": "Q4 Churn Analysis Report",
  "format": "html",
  "status": "ready",
  "download_url": "/api/v1/report/download/rpt_v4w5x6",
  "created_at": "2026-02-20T12:30:00Z",
  "size_bytes": 245760
}
```

#### `GET /report/download/{report_id}`
- **Response:** Binary file (`text/html` or `application/pdf`)

---

## 7. Jobs

#### `GET /jobs/{job_id}`
Universal job status endpoint.
```json
// Response 200
{
  "job_id": "job_c4d5e6",
  "type": "data_cleaning",            // data_cleaning | ml_training | report_generation
  "status": "SUCCESS",
  "percent": 100,
  "message": "Completed successfully",
  "started_at": "2026-02-20T12:05:30Z",
  "completed_at": "2026-02-20T12:06:15Z",
  "result": { ... }
}
```

#### `DELETE /jobs/{job_id}`
Cancel a running or pending job.
```json
// Response 200
{ "job_id": "job_c4d5e6", "status": "REVOKED", "message": "Job cancelled" }
```

---

## 8. Error Handling

### Standard Error Response

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Target column 'churn_label' not found in dataset",
    "details": {
      "available_columns": ["id", "name", "revenue", "churn"],
      "suggestion": "Did you mean 'churn'?"
    },
    "request_id": "req_d4e5f6"
  }
}
```

### Error Codes

| HTTP Status | Code | Description |
|---|---|---|
| 400 | `VALIDATION_ERROR` | Invalid input, missing fields |
| 400 | `UNSUPPORTED_FORMAT` | File type not supported |
| 400 | `FILE_TOO_LARGE` | Exceeds 200MB limit |
| 401 | `UNAUTHORIZED` | Missing or invalid token |
| 403 | `FORBIDDEN` | Insufficient permissions |
| 404 | `NOT_FOUND` | Resource not found |
| 409 | `CONFLICT` | Job already running for this dataset |
| 422 | `PROCESSING_ERROR` | Data processing failed |
| 429 | `RATE_LIMITED` | Too many requests (100/min per user) |
| 500 | `INTERNAL_ERROR` | Unexpected server error |
| 502 | `LLM_PROVIDER_ERROR` | External LLM API failure |
| 503 | `SERVICE_UNAVAILABLE` | System overloaded |

### Rate Limits

| Endpoint Group | Limit | Window |
|---|---|---|
| `/auth/*` | 10 requests | 1 minute |
| `/upload` | 5 requests | 1 minute |
| `/chat/message` | 30 requests | 1 minute |
| All other endpoints | 100 requests | 1 minute |

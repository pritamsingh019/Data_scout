# DATA_SCOUT — Risk Assessment

**Version:** 1.0 | **Last Updated:** 2026-02-20

---

## 1. Technical Risks

| # | Risk | Probability | Impact | Severity | Mitigation |
|---|---|---|---|---|---|
| T1 | **AutoML exceeds time budget** on large/complex datasets, causing timeouts | Medium | High | 🔴 High | Enforce FLAML `time_budget`; kill after `soft_time_limit`; return partial results |
| T2 | **FAISS index corruption** on concurrent write/read during dataset updates | Low | High | 🟡 Medium | Per-dataset index isolation; read-write locks; rebuild on failure |
| T3 | **Memory exhaustion** on datasets approaching 200MB with many features | Medium | High | 🔴 High | Chunked loading; streaming feature engineering; enforce memory limits per worker |
| T4 | **Data cleaning produces invalid output** (e.g., all rows dropped, wrong imputation) | Medium | Medium | 🟡 Medium | Row-loss cap (30%); validation gates after each cleaning step; rollback capability |
| T5 | **WebSocket connections drop** under load, losing training progress updates | Medium | Low | 🟢 Low | Automatic reconnection with exponential backoff; fallback to HTTP polling |
| T6 | **Task type misdetection** (e.g., treating ID column as regression target) | Low | Medium | 🟡 Medium | ID column detection heuristics; user override option; confidence threshold warnings |
| T7 | **Database migration failures** in production deploys | Low | High | 🟡 Medium | Pre-deploy migration dry-run; automated rollback scripts; staging environment |
| T8 | **Model serialization incompatibility** across scikit-learn versions | Low | Medium | 🟡 Medium | Pin exact library versions; include version metadata in `.pkl` files |

---

## 2. Ethical Risks

| # | Risk | Probability | Impact | Severity | Mitigation |
|---|---|---|---|---|---|
| E1 | **Chatbot hallucination** — generating fabricated statistics or trends | Medium | High | 🔴 High | RAG grounding; retrieval quality gate; post-response validation; confidence scoring |
| E2 | **Biased model recommendations** — AutoML picks model that amplifies dataset bias | Medium | High | 🔴 High | Fairness metrics (demographic parity, equalized odds) in evaluation report; bias warnings |
| E3 | **PII exposure through chatbot** — LLM leaks personal data in responses | Low | Critical | 🔴 High | PII detection before indexing; strip PII from context chunks; data masking |
| E4 | **Over-reliance on AutoML** — users treat recommendations as ground truth without validation | High | Medium | 🟡 Medium | Display confidence intervals; overfitting warnings; "This is a suggestion, not a guarantee" disclaimer |
| E5 | **Unintended data retention** — user data persists after deletion request | Low | High | 🟡 Medium | Hard delete across all stores (DB, S3, FAISS, Redis); deletion audit log |
| E6 | **LLM provider data usage** — user data used for LLM training without consent | Low | Critical | 🔴 High | Use API endpoints with data usage opt-out; user disclosure; audit provider policies quarterly |

---

## 3. Failure Scenarios

### Scenario 1: Large File Causes Backend OOM

```
Trigger: User uploads 200MB CSV with 500 columns
Impact: Worker process killed; other users' jobs affected
Timeline: Immediate (during cleaning)
```

**Recovery:**
1. Celery worker auto-restarts (Docker `restart: unless-stopped`)
2. Job marked as `FAILURE` with error: "Dataset too large for current memory allocation"
3. User notified via WebSocket with suggestion: "Try reducing columns or file size"
4. **Prevention**: Pre-upload estimation of memory requirements; reject if > 80% of worker memory

### Scenario 2: LLM Provider Outage During Chat

```
Trigger: OpenAI API returns 503 for >5 minutes
Impact: Chatbot non-functional for users on OpenAI
Timeline: Duration of outage
```

**Recovery:**
1. After 2 failed retries (with exponential backoff), activate fallback chain
2. Switch to Anthropic → Google → error message
3. Log incident; alert ops team
4. User sees: "Switched to alternative AI provider for this response"

### Scenario 3: Corrupted Dataset Passes Validation

```
Trigger: CSV with mismatched column counts across rows (malformed)
Impact: Pandas reads with NaN fill; cleaning produces misleading results
Timeline: Not detected until user reviews results
```

**Recovery:**
1. Pre-processing: count columns per row; reject if variance > 0
2. If slips through: anomaly detection on null patterns post-parse
3. User shown: "Warning: dataset may have structural issues — {X} rows had inconsistent column counts"

### Scenario 4: Database Connection Pool Exhaustion

```
Trigger: 100+ concurrent users with long-running queries
Impact: New API requests fail with 500 errors
Timeline: Seconds to minutes
```

**Recovery:**
1. Connection pool configured with `pool_size=20, max_overflow=10, pool_timeout=30`
2. Health check detects; alert fires
3. Auto-scale API instances to distribute load
4. Implement query timeouts (`statement_timeout = 30s`)

### Scenario 5: Model Training Produces Nonsensical Results

```
Trigger: Dataset has target leakage (feature derived from target)
Impact: Model shows 99.9% accuracy; useless in production
Timeline: User sees inflated results
```

**Recovery:**
1. Target leakage detection: if any feature has correlation > 0.98 with target, flag warning
2. Overfitting check: train-test gap analysis
3. Display warning: "Feature '{name}' has suspiciously high correlation with the target. This may indicate data leakage."

---

## 4. Mitigation Strategy Summary

### Risk Matrix Visualization

```
              Impact
              Low        Medium       High        Critical
         ┌──────────┬──────────┬──────────┬──────────┐
  High   │          │   E4     │   T1     │          │
         ├──────────┼──────────┼──────────┼──────────┤
  Medium │   T5     │   T4,T6  │ E1,E2,T3 │          │
Prob.    ├──────────┼──────────┼──────────┼──────────┤
  Low    │          │   T8     │ T2,T7,E5 │  E3,E6   │
         └──────────┴──────────┴──────────┴──────────┘
```

### Top-5 Risks by Severity

| Rank | Risk | Category | Key Mitigation |
|---|---|---|---|
| 1 | Chatbot hallucination (E1) | Ethical | Multi-layer RAG grounding + post-validation |
| 2 | PII exposure (E3) | Ethical | PII detection + stripping before LLM calls |
| 3 | LLM data usage (E6) | Ethical | Provider policy audit + user disclosure |
| 4 | Memory exhaustion (T3) | Technical | Chunked processing + memory limits per worker |
| 5 | AutoML timeout (T1) | Technical | Time budgets + partial result return |

### Monitoring & Response Plan

| Risk Category | Monitoring | Alert Channel | Response SLA |
|---|---|---|---|
| Service outage | Health checks (30s interval) | PagerDuty | 15 min |
| Error rate spike | 5xx rate > 5% over 5 min | Slack + PagerDuty | 30 min |
| Data privacy incident | Audit log review | Email to DPO + Engineering lead | 1 hour |
| Model quality regression | Automated benchmark tests in CI | Slack | 24 hours |
| LLM provider issue | API latency/error monitoring | Slack | Automatic fallback |

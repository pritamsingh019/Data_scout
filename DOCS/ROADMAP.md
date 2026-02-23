# DATA_SCOUT — Product Roadmap

**Version:** 1.0 | **Last Updated:** 2026-02-20

---

## Phase Overview

```
Phase 1: MVP          Phase 2: Growth       Phase 3: Scale        Phase 4: Enterprise
(Months 1-3)          (Months 4-6)          (Months 7-9)          (Months 10-12)
│                     │                     │                     │
├─ Upload + Clean     ├─ Multi-LLM (full)   ├─ Scheduled training  ├─ Multi-tenant
├─ AutoML (FLAML)     ├─ PDF export         ├─ Dataset history     ├─ SSO / OAuth
├─ RAG chatbot (GPT)  ├─ Claude + Gemini    ├─ Template reports    ├─ Admin dashboard
├─ Basic reports      ├─ SHAP explainability├─ API rate tiers      ├─ Audit logging
├─ Docker deployment  ├─ User dashboard     ├─ GPU worker support  ├─ On-premise deploy
└─ JWT auth           └─ Improved chat UX   └─ Caching layer       └─ Custom integrations
```

---

## Phase 1: MVP (Months 1–3)

### Goals
Ship a working end-to-end flow: upload → clean → train → chat → basic report.

### Milestones

| Week | Milestone | Deliverables |
|---|---|---|
| 1–2 | **Project setup** | Repo scaffolding, Docker Compose, CI pipeline, DB migrations |
| 3–4 | **Data pipeline** | CSV/XLSX upload, type detection, cleaning (imputation + dedup + outliers) |
| 5–6 | **ML pipeline** | Task detection, FLAML AutoML, model comparison, recommendation engine |
| 7–8 | **RAG chatbot** | FAISS indexing, embeddings, GPT-4 integration, citation system |
| 9–10 | **Frontend v1** | Upload, data preview, ML dashboard, chat panel |
| 11–12 | **Auth + Reports + Deploy** | JWT auth, basic HTML report generation, Docker production build |

### Exit Criteria
- [ ] User can upload a CSV, auto-clean it, train models, get a recommendation, and ask questions
- [ ] Chatbot provides cited answers with <5% hallucination rate on test set
- [ ] System handles 50 concurrent users without degradation
- [ ] All CI tests pass; ≥80% code coverage

---

## Phase 2: Growth (Months 4–6)

### Goals
Expand LLM support, improve explainability, and polish user experience.

### Features

| Feature | Details | Priority |
|---|---|---|
| **Claude + Gemini support** | Full multi-LLM abstraction with fallback chain | P0 |
| **PDF report export** | Generate reports as PDF with charts and tables | P0 |
| **SHAP explainability** | Summary, waterfall, and dependence plots for top model | P0 |
| **User dashboard** | List datasets, view job history, manage account | P1 |
| **Improved chat UX** | Multi-turn context, suggested questions, export chat | P1 |
| **TSV + JSON support** | Expand file format support | P1 |
| **Performance optimization** | Redis caching for frequent queries; query optimization | P2 |

### Exit Criteria
- [ ] Users can switch between GPT-4, Claude, and Gemini in the chatbot
- [ ] SHAP plots generated for every recommended model
- [ ] Reports exportable as both HTML and PDF
- [ ] User satisfaction (SUS) ≥ 72

---

## Phase 3: Scale (Months 7–9)

### Goals
Enable production-grade scalability, advanced features, and operational maturity.

### Features

| Feature | Details | Priority |
|---|---|---|
| **Scheduled re-training** | Users can schedule periodic model re-training on updated data | P0 |
| **Dataset versioning** | Track dataset changes over time; compare model performance | P0 |
| **Custom report templates** | Users define report sections, branding, and layout | P1 |
| **API rate tiers** | Free, Pro, Enterprise tiers with different rate limits | P1 |
| **GPU worker support** | Optional GPU workers for larger FLAML budgets | P1 |
| **Caching layer** | Redis caching for embeddings, frequently asked questions | P2 |
| **Webhook notifications** | Notify external systems when training completes | P2 |

### Exit Criteria
- [ ] System handles 200+ concurrent users with auto-scaling
- [ ] Re-training jobs execute on schedule without manual intervention
- [ ] API rate limiting enforced per tier

---

## Phase 4: Enterprise (Months 10–12)

### Goals
Enterprise-ready features for organizational deployment.

### Features

| Feature | Details | Priority |
|---|---|---|
| **Multi-tenant architecture** | Organization workspaces with isolated data | P0 |
| **SSO / OAuth 2.0** | Google, Microsoft, SAML integration | P0 |
| **Admin dashboard** | User management, usage analytics, system health | P0 |
| **Audit logging** | Immutable log of all data access and model operations | P1 |
| **On-premise deployment** | Helm charts for Kubernetes; air-gapped mode (no external LLM calls) | P1 |
| **Custom LLM integration** | Support for self-hosted LLMs (Ollama, vLLM) | P2 |
| **Collaborative workspaces** | Share datasets, models, and reports within teams | P2 |

### Exit Criteria
- [ ] SOC 2 readiness assessment passed
- [ ] Multi-tenant isolation verified via security audit
- [ ] On-premise deployment tested in air-gapped environment

---

## Future Enhancements (Beyond v1.0)

| Enhancement | Description | Estimated Effort |
|---|---|---|
| **Deep Learning support** | PyTorch/TensorFlow for tabular deep learning (TabNet, FT-Transformer) | 3 months |
| **Time-series forecasting** | ARIMA, Prophet, LSTM for time-series datasets | 2 months |
| **NLP pipeline** | Text classification, sentiment analysis for text-heavy datasets | 2 months |
| **Image classification** | Upload image datasets; train CNNs via transfer learning | 3 months |
| **Streaming data** | Kafka/Flink integration for real-time data ingestion | 4 months |
| **AutoML ensemble** | Stacking and blending of top-N models | 1 month |
| **Model serving** | Deploy trained models as REST APIs with one click | 2 months |
| **Mobile app** | React Native companion app for dashboards | 3 months |
| **Marketplace** | Share and discover pre-trained models and report templates | 4 months |

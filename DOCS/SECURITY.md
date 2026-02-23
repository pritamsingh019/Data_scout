# DATA_SCOUT — Security Specification

**Version:** 1.0 | **Last Updated:** 2026-02-20

---

## 1. Data Privacy Controls

### 1.1 Data Lifecycle

```
Upload → Process → Store → Access → Delete
   │         │        │       │        │
   ▼         ▼        ▼       ▼        ▼
 Encrypt   Isolate  Encrypt  AuthZ   Purge all
 in-trans  by user  at-rest  check   copies
```

### 1.2 Privacy Principles

| Principle | Implementation |
|---|---|
| **Data minimization** | Only store what's needed; strip PII if not Required |
| **User isolation** | Each user's data stored under unique prefix; no cross-user access |
| **Consent-based** | Data is never shared with third parties without explicit opt-in |
| **Right to delete** | One-click dataset deletion removes raw + cleaned + vectors + models |
| **Retention policy** | Inactive datasets auto-deleted after 90 days (configurable) |

### 1.3 PII Detection

Automatically scan uploaded datasets for potential PII:

```python
PII_PATTERNS = {
    "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
    "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
    "credit_card": r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",
    "ip_address": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
}

# On detection: warn user, offer to mask/drop columns
```

---

## 2. Access Control

### 2.1 Authentication Flow

```
Client                    API                     Database
  │  POST /auth/login       │                          │
  │  {email, password}      │                          │
  │────────────────────────>│  bcrypt.verify(password) │
  │                         │─────────────────────────>│
  │                         │  ◄── user record         │
  │  ◄── access_token (JWT) │                          │
  │      + refresh_token    │                          │
  │      (HTTP-only cookie) │                          │
```

### 2.2 JWT Structure

```json
{
  "header": { "alg": "HS256", "typ": "JWT" },
  "payload": {
    "sub": "usr_abc123",
    "email": "user@example.com",
    "role": "user",
    "iat": 1708430400,
    "exp": 1708432200
  }
}
```

### 2.3 Role-Based Access

| Role | Permissions |
|---|---|
| `user` | Upload, clean, train, chat, report — own data only |
| `admin` | All user permissions + manage users + system config |

### 2.4 Resource Authorization

```python
async def verify_dataset_ownership(dataset_id: str, user_id: str):
    dataset = await db.get_dataset(dataset_id)
    if dataset is None:
        raise HTTPException(404, "Dataset not found")
    if dataset.owner_id != user_id:
        raise HTTPException(403, "Access denied")
    return dataset
```

---

## 3. Secure Storage

### 3.1 Encryption

| Layer | Method | Details |
|---|---|---|
| **In transit** | TLS 1.3 | Nginx terminates SSL; internal traffic over Docker network |
| **At rest (DB)** | AES-256 | PostgreSQL TDE or application-level encryption for sensitive fields |
| **At rest (files)** | S3 SSE-S3 / MinIO encryption | Server-side encryption for all objects |
| **Passwords** | bcrypt (cost=12) | Salted hash; never stored in plaintext |
| **API keys** | SHA-256 hash | Only hash stored; original shown once on creation |

### 3.2 Secrets Management

| Secret | Storage | Access |
|---|---|---|
| JWT signing key | Environment variable | Backend only |
| DB credentials | Environment variable | Backend + workers |
| LLM API keys | Environment variable | Backend service layer |
| MinIO credentials | Environment variable | Backend + workers |

**Production:** Use AWS Secrets Manager, HashiCorp Vault, or similar. Never commit secrets to Git.

### 3.3 Database Security

- **Connection**: SSL-enforced (`sslmode=require`)
- **User**: Dedicated service account with minimal privileges
- **Backups**: Encrypted daily backups with 30-day retention
- **Migrations**: Audited via Alembic; no raw SQL in production

---

## 4. LLM Data Handling Policy

### 4.1 Data Sent to LLM Providers

| Data Type | Sent to LLM? | Mitigation |
|---|---|---|
| Raw user data | **No** | Only chunked context (top-k retrieved rows) |
| Full dataset | **Never** | Only relevant slices via RAG retrieval |
| Column names | Yes (in context) | Non-sensitive by nature |
| Statistical summaries | Yes (in context) | Aggregated, non-PII |
| User questions | Yes | Necessary for response generation |
| Model artifacts | **Never** | Processed locally only |

### 4.2 Provider-Specific Policies

| Provider | Data Retention | Training on Data | Compliance |
|---|---|---|---|
| OpenAI (API) | 30 days (abuse monitoring) | Opt-out available | SOC 2 |
| Anthropic (API) | 30 days | Not used for training | SOC 2 |
| Google AI (API) | 30 days | Not used for training | SOC 2 |

### 4.3 Safeguards

1. **PII stripping**: Run PII detection before sending context to LLM
2. **Context minimization**: Send only top-k relevant chunks, not entire dataset
3. **No file uploads to LLM**: All processing happens locally; only text prompts go external
4. **Audit log**: Every LLM call logged with: timestamp, provider, token count, user_id (no prompt content stored)
5. **User disclosure**: UI shows "Data will be sent to {provider}" before first chat message

---

## 5. Network Security

### 5.1 Nginx Configuration

```nginx
server {
    listen 443 ssl http2;
    server_name datascout.io;

    ssl_certificate /etc/nginx/certs/fullchain.pem;
    ssl_certificate_key /etc/nginx/certs/privkey.pem;
    ssl_protocols TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=100r/m;

    # Security headers
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Content-Security-Policy "default-src 'self';" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    location /api/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://backend:8000;
    }
}
```

### 5.2 CORS Policy

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://datascout.io"],  # No wildcards in production
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
    allow_credentials=True,
    max_age=86400,
)
```

### 5.3 Input Validation

| Vector | Protection |
|---|---|
| SQL injection | SQLAlchemy ORM (parameterized queries); no raw SQL |
| XSS | React auto-escapes; CSP headers |
| File upload attacks | Validate MIME type + extension; scan with `python-magic` |
| Path traversal | Sanitize filenames; store with UUID keys |
| Denial of Service | Rate limiting; file size limits; training timeouts |
| Prompt injection | System prompt isolation; context-only responses |

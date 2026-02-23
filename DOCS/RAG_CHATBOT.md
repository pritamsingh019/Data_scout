# DATA_SCOUT — RAG Chatbot

**Version:** 1.0 | **Last Updated:** 2026-02-20

---

## 1. Retrieval Pipeline

### 1.1 Architecture

```
User Question
    │
    ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  Embed       │──>│  FAISS       │──>│  Build       │──>│  LLM Call    │
│  Question    │   │  Similarity  │   │  Prompt      │   │  (selected   │
│  (MiniLM)    │   │  Search      │   │  w/ Context  │   │   provider)  │
└──────────────┘   │  (top-k=5)   │   └──────────────┘   └──────┬───────┘
                   └──────────────┘                              │
                                                                 ▼
                                                    ┌──────────────────┐
                                                    │  Validate &      │
                                                    │  Return w/       │
                                                    │  Citations       │
                                                    └──────────────────┘
```

### 1.2 Indexing Pipeline (runs on dataset upload)

1. **Load cleaned dataset** from storage
2. **Chunk data** into semantically meaningful text blocks:
   - Each row is converted to a natural-language sentence
   - Column statistics are summarized as separate chunks
   - Schema description is added as a chunk
3. **Generate embeddings** for all chunks
4. **Build FAISS index** (FlatIP for <50K vectors; IVF for >50K)
5. **Store index** alongside dataset metadata

### 1.3 Row-to-Text Conversion

```python
def row_to_text(row: pd.Series, columns: list) -> str:
    """Convert a dataframe row to a natural language description."""
    parts = []
    for col in columns:
        parts.append(f"{col} is {row[col]}")
    return f"Row {row.name}: " + ", ".join(parts) + "."

# Example output:
# "Row 42: customer_id is C1023, monthly_charges is 72.50,
#  tenure is 8, churn is Yes."
```

### 1.4 Statistical Summary Chunks

In addition to row-level chunks, the system generates summary chunks:

```python
summary_chunks = [
    f"The dataset has {len(df)} rows and {len(df.columns)} columns.",
    f"Column '{col}' has mean={mean:.2f}, median={median:.2f}, std={std:.2f}.",
    f"Column '{col}' has {nunique} unique values: {top_values}.",
    f"The target column '{target}' has class distribution: {dist}.",
]
```

---

## 2. Embeddings Strategy

### 2.1 Model Selection

| Model | Dim | Speed | Quality | Use Case |
|---|---|---|---|---|
| `all-MiniLM-L6-v2` | 384 | Fast | Good | **Default** — best speed/quality trade-off |
| `all-mpnet-base-v2` | 768 | Medium | Best | Large datasets needing higher retrieval quality |

### 2.2 Embedding Pipeline

```python
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def build_index(chunks: list[str]) -> tuple[faiss.Index, np.ndarray]:
    embeddings = model.encode(chunks, batch_size=256, show_progress_bar=True)
    embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
    
    dim = embeddings.shape[1]
    if len(chunks) < 50_000:
        index = faiss.IndexFlatIP(dim)        # Exact search
    else:
        nlist = int(np.sqrt(len(chunks)))
        quantizer = faiss.IndexFlatIP(dim)
        index = faiss.IndexIVFFlat(quantizer, dim, nlist)
        index.train(embeddings)
    
    index.add(embeddings)
    return index, embeddings
```

### 2.3 Chunking Strategy

| Content Type | Chunk Size | Overlap |
|---|---|---|
| Individual rows | 1 row = 1 chunk | None |
| Column statistics | 1 column summary = 1 chunk | None |
| Schema description | Full schema = 1 chunk | None |
| Large text columns | 256 tokens per chunk | 50 tokens |

---

## 3. Prompt Construction

### 3.1 System Prompt

```
You are DATA_SCOUT AI, an analytical assistant that answers questions
about a user's uploaded dataset. You MUST follow these rules:

1. ONLY use information from the provided context chunks below.
2. ALWAYS cite your sources using [Row X, Column: Y] format.
3. If the context does not contain enough information to answer,
   say: "I don't have enough data in the current dataset to answer this."
4. Never make up statistics, values, or trends not in the context.
5. When providing numbers, state exact values from the data.
6. If asked about predictions or causation, clarify that you are
   reporting correlations and patterns, not causal relationships.
```

### 3.2 Prompt Template

```
SYSTEM: {system_prompt}

CONTEXT (retrieved from user's dataset):
---
Chunk 1: {chunk_text_1}
Chunk 2: {chunk_text_2}
Chunk 3: {chunk_text_3}
Chunk 4: {chunk_text_4}
Chunk 5: {chunk_text_5}
---

CONVERSATION HISTORY:
{previous_messages if multi-turn}

USER QUESTION: {user_question}

INSTRUCTIONS:
- Answer using ONLY the context above
- Cite specific rows, columns, or statistics
- If unsure, say "I don't have enough data to answer this"
```

### 3.3 Dynamic Context Window Management

| LLM Provider | Max Context | Reserved for Response | Available for Context |
|---|---|---|---|
| GPT-4 Turbo | 128K tokens | 2K | 126K |
| Claude 3 Sonnet | 200K tokens | 2K | 198K |
| Gemini 1.5 Pro | 1M tokens | 2K | ~998K |

Context is filled greedily: top-k chunks ranked by similarity, truncated to fit.

---

## 4. Hallucination Mitigation

### 4.1 Multi-Layer Defense

```
Layer 1: Retrieval Quality Gate
    │  Discard chunks with similarity < 0.3
    │
Layer 2: Prompt Engineering
    │  Explicit grounding instructions in system prompt
    │
Layer 3: Low Temperature
    │  temperature=0.1 to reduce creative generation
    │
Layer 4: Post-Response Validation
    │  Verify claims against source chunks
    │
Layer 5: Confidence Scoring
    │  Return confidence score; flag low-confidence answers
```

### 4.2 Retrieval Quality Gate

```python
def filter_chunks(query_embedding, index, chunks, threshold=0.3, top_k=5):
    scores, indices = index.search(query_embedding, top_k * 2)  # over-retrieve
    
    filtered = []
    for score, idx in zip(scores[0], indices[0]):
        if score >= threshold:
            filtered.append({"text": chunks[idx], "score": float(score), "index": int(idx)})
    
    if len(filtered) == 0:
        return None  # triggers "I don't know" response
    
    return filtered[:top_k]
```

### 4.3 Post-Response Validation

```python
def validate_response(response: str, source_chunks: list[dict]) -> dict:
    """Check if claims in the response are grounded in source chunks."""
    
    # Extract numerical claims from response
    numbers_in_response = re.findall(r'\b\d+\.?\d*\b', response)
    
    # Check each number against source chunks
    source_text = " ".join([c["text"] for c in source_chunks])
    grounded_count = sum(1 for n in numbers_in_response if n in source_text)
    
    grounding_ratio = grounded_count / len(numbers_in_response) if numbers_in_response else 1.0
    
    return {
        "is_grounded": grounding_ratio >= 0.7,
        "grounding_ratio": grounding_ratio,
        "total_claims": len(numbers_in_response),
        "grounded_claims": grounded_count
    }
```

### 4.4 Fallback Responses

| Condition | Response |
|---|---|
| No chunks pass quality gate | "I don't have enough data in the current dataset to answer this question." |
| Low grounding ratio (<0.7) | "Based on the available data, I can partially answer: {partial}. However, I cannot confirm all details." |
| Question is off-topic | "This question doesn't seem related to your uploaded dataset. I can only answer questions about the data you've provided." |
| LLM API error | "I'm having trouble processing your question right now. Please try again shortly." |

---

## 5. Multi-LLM Abstraction

### 5.1 Provider Interface

```python
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, messages: list[dict], **kwargs) -> str:
        """Generate a response from the LLM."""
        pass
    
    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """Count tokens for context management."""
        pass
    
    @abstractmethod
    def get_max_context_length(self) -> int:
        """Return max context window size."""
        pass
```

### 5.2 Provider Implementations

```python
class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "gpt-4-turbo"):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
    
    async def generate(self, messages, temperature=0.1, max_tokens=1024):
        response = await self.client.chat.completions.create(
            model=self.model, messages=messages,
            temperature=temperature, max_tokens=max_tokens
        )
        return response.choices[0].message.content

class AnthropicProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "claude-3-sonnet-20240229"):
        self.client = AsyncAnthropic(api_key=api_key)
        self.model = model
    
    async def generate(self, messages, temperature=0.1, max_tokens=1024):
        response = await self.client.messages.create(
            model=self.model, messages=messages,
            temperature=temperature, max_tokens=max_tokens
        )
        return response.content[0].text

class GoogleProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "gemini-1.5-pro"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)
    
    async def generate(self, messages, temperature=0.1, max_tokens=1024):
        response = await self.model.generate_content_async(
            contents=messages,
            generation_config={"temperature": temperature, "max_output_tokens": max_tokens}
        )
        return response.text
```

### 5.3 Provider Factory

```python
class LLMFactory:
    _providers = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "google": GoogleProvider,
    }
    
    @classmethod
    def create(cls, provider: str, api_key: str) -> LLMProvider:
        if provider not in cls._providers:
            raise ValueError(f"Unsupported provider: {provider}")
        return cls._providers[provider](api_key=api_key)
```

### 5.4 Fallback Chain

If the primary provider fails (rate limit, timeout, error):

```
Primary Provider (user-selected)
    │ failure
    ▼
Fallback 1: Next available provider
    │ failure
    ▼
Fallback 2: Third provider
    │ failure
    ▼
Error response to user with retry suggestion
```

Configuration:
```python
FALLBACK_ORDER = {
    "openai": ["anthropic", "google"],
    "anthropic": ["openai", "google"],
    "google": ["openai", "anthropic"],
}
MAX_RETRIES_PER_PROVIDER = 2
RETRY_DELAY_SECONDS = 1
```

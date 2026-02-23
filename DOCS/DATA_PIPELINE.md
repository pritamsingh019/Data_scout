# DATA_SCOUT — Data Pipeline

**Version:** 1.0 | **Last Updated:** 2026-02-20

---

## 1. Data Ingestion

### 1.1 Supported Formats

| Format | Extension | Parser | Max Size |
|---|---|---|---|
| CSV | `.csv` | `pandas.read_csv` | 200MB |
| Excel | `.xlsx`, `.xls` | `openpyxl` / `xlrd` | 200MB |
| TSV | `.tsv` | `pandas.read_csv(sep='\t')` | 200MB |
| JSON | `.json` | `pandas.read_json` (records/table) | 200MB |

### 1.2 Ingestion Flow

```
File Upload
    │
    ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Validate    │───>│  Parse &     │───>│  Store Raw   │───>│  Generate    │
│  File Type   │    │  Read File   │    │  to MinIO/S3 │    │  Metadata    │
│  & Size      │    │  (chunked)   │    │              │    │  Record      │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

### 1.3 Chunked Reading Strategy

For files >50MB, the system uses chunked reading to prevent memory exhaustion:

```python
def ingest_large_file(filepath: str, chunk_size: int = 50_000) -> pd.DataFrame:
    chunks = []
    for chunk in pd.read_csv(filepath, chunksize=chunk_size):
        chunks.append(chunk)
    return pd.concat(chunks, ignore_index=True)
```

### 1.4 Initial Metadata Extraction

Upon successful upload, the following metadata is computed:

| Metric | Computation |
|---|---|
| Row count | `len(df)` |
| Column count | `len(df.columns)` |
| Column dtypes | `df.dtypes` inferred by pandas |
| Memory usage | `df.memory_usage(deep=True).sum()` |
| Sample rows | First 5 + last 5 rows |
| Null summary | `df.isnull().sum()` per column |

---

## 2. Automated Data Type Detection

### 2.1 Detection Logic

Standard pandas inference often misclassifies columns. DATA_SCOUT applies a **multi-heuristic detection pipeline**:

```
For each column:
  1. Check if column name contains date keywords → parse as datetime
  2. Attempt pd.to_numeric() → if >90% success → numeric
  3. Attempt pd.to_datetime() → if >80% success → datetime
  4. Count unique values / total values ratio:
     - ratio < 0.05 → categorical (even if numeric)
     - ratio > 0.5 and dtype=object → text/free-form
  5. If column has exactly 2 unique values → boolean
  6. Default → categorical (if <50 unique) or text
```

### 2.2 Type Mapping

| Detected Type | Internal Type | Downstream Treatment |
|---|---|---|
| `integer` | `int64` | Scale/normalize for ML |
| `float` | `float64` | Scale/normalize for ML |
| `boolean` | `bool` | Binary encode (0/1) |
| `categorical_low` (<20 unique) | `category` | One-hot encode |
| `categorical_high` (20-50) | `category` | Target/ordinal encode |
| `datetime` | `datetime64` | Extract year, month, day, dayofweek, hour |
| `text` | `object` | TF-IDF or drop (configurable) |
| `identifier` | `object` | Drop (e.g., UUIDs, row IDs) |

---

## 3. Data Cleaning Steps

### 3.1 Pipeline Order

```
Raw Data
    │
    ▼
┌──────────────────┐
│ 1. Remove        │  Drop columns with >95% identical values
│    constant cols  │  Drop columns detected as identifiers (UUID patterns)
└────────┬─────────┘
         ▼
┌──────────────────┐
│ 2. Deduplication │  Remove exact duplicate rows
│                  │  Keep first occurrence
└────────┬─────────┘
         ▼
┌──────────────────┐
│ 3. Missing Value │  Strategy selected per-column based on type + missingness %
│    Imputation    │  (see strategy matrix below)
└────────┬─────────┘
         ▼
┌──────────────────┐
│ 4. Outlier       │  IQR method for numeric columns
│    Treatment     │  Option: remove, cap (winsorize), or flag
└────────┬─────────┘
         ▼
┌──────────────────┐
│ 5. Type          │  Convert mistyped columns (e.g., "123" → 123)
│    Correction    │  Parse date strings to datetime
└────────┬─────────┘
         ▼
┌──────────────────┐
│ 6. Encoding      │  One-hot for low-cardinality categoricals
│                  │  Target encoding for high-cardinality
└────────┬─────────┘
         ▼
Cleaned Data
```

### 3.2 Missing Value Strategy Matrix

| Column Type | Missing % < 5% | Missing 5-30% | Missing > 30% |
|---|---|---|---|
| Numeric (normal dist) | Mean | Mean | Drop column |
| Numeric (skewed) | Median | Median | Drop column |
| Categorical | Mode | Mode + "Missing" class | Drop column |
| Datetime | Forward fill | Drop rows | Drop column |
| Boolean | Mode | Mode | Drop column |

### 3.3 Outlier Detection

**IQR Method (default):**
```python
Q1 = df[col].quantile(0.25)
Q3 = df[col].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
outliers = df[(df[col] < lower) | (df[col] > upper)]
```

**Z-Score Method (optional):**
```python
from scipy import stats
z_scores = np.abs(stats.zscore(df[col].dropna()))
outliers = df[z_scores > 3]
```

**Treatment options:**
- `remove`: Delete outlier rows
- `cap`: Winsorize to [Q1 - 1.5*IQR, Q3 + 1.5*IQR]
- `flag`: Add `{col}_is_outlier` boolean column

---

## 4. Feature Engineering

### 4.1 Automated Feature Generation

| Source Type | Generated Features |
|---|---|
| **Datetime** | `year`, `month`, `day`, `day_of_week`, `hour`, `is_weekend`, `quarter` |
| **Numeric pairs** | Interaction terms (top-5 correlated pairs): `col_a * col_b` |
| **Categorical** | Frequency encoding: `{col}_freq = count(value) / total_rows` |
| **Text** (if enabled) | TF-IDF (top 50 terms), text length, word count |

### 4.2 Feature Selection

Post-generation, features are filtered using:

1. **Variance threshold**: Drop features with variance < 0.01
2. **Correlation filter**: If two features have Pearson r > 0.95, drop the one with lower target correlation
3. **Mutual information**: Rank features by MI with target; keep top-N (default: 50)

### 4.3 Scaling

| Method | When Used |
|---|---|
| `StandardScaler` | Default for most algorithms |
| `MinMaxScaler` | When data must be in [0, 1] (e.g., neural networks) |
| `RobustScaler` | When outliers remain in the dataset |

---

## 5. Data Validation

### 5.1 Pre-Processing Validation

| Check | Rule | Action on Failure |
|---|---|---|
| Minimum rows | ≥ 20 rows | Reject with error |
| Minimum columns | ≥ 2 columns | Reject with error |
| File encoding | Auto-detect via `chardet` | Convert to UTF-8 |
| Header detection | First row contains non-numeric values | Flag if ambiguous |
| Empty file | File size > 0 and has parseable content | Reject with error |

### 5.2 Post-Cleaning Validation

| Check | Description |
|---|---|
| No null values remaining | `df.isnull().sum().sum() == 0` |
| No duplicate rows | `df.duplicated().sum() == 0` |
| All columns have correct dtypes | Compare inferred vs expected types |
| Row loss < 30% | If cleaning removed >30% of rows, warn user |
| Feature count reasonable | Total features < 500 after engineering |

### 5.3 Data Quality Score

A composite score (0–100) computed as:

```
quality_score = (
    (1 - null_ratio) * 30 +
    (1 - duplicate_ratio) * 20 +
    (1 - outlier_ratio) * 20 +
    type_consistency_ratio * 15 +
    completeness_ratio * 15
)
```

---

## 6. Handling Edge Cases

### 6.1 Edge Case Matrix

| Edge Case | Detection | Handling |
|---|---|---|
| **Single-column dataset** | `len(df.columns) == 1` | Error: "Need ≥2 columns for analysis" |
| **All-null column** | `df[col].isnull().all()` | Drop column; log warning |
| **Mixed types in column** | `df[col].apply(type).nunique() > 1` | Coerce to most common type; flag failures |
| **Extremely high cardinality** | `nunique > 0.9 * len(df)` | Treat as identifier; exclude from ML |
| **Date in string format** | `dateutil.parser` success rate > 80% | Auto-parse to datetime |
| **Numeric stored as string** | `pd.to_numeric(errors='coerce')` success > 90% | Convert to numeric |
| **Unicode/special chars in headers** | Regex check `[^a-zA-Z0-9_]` | Sanitize: strip, lowercase, replace spaces with `_` |
| **Delimiter mismatch** | `csv.Sniffer` detection | Auto-detect delimiter; fallback to `,` |
| **Large numeric IDs** | Column name contains "id" + all unique integers | Drop column |
| **Imbalanced target** (class ratio > 10:1) | Value counts on target column | Warn user; suggest SMOTE or class weights |
| **Constant target** | `target.nunique() == 1` | Error: "Target has no variance" |
| **Target in wrong format** | Target is text but task is classification | Auto-encode labels with `LabelEncoder` |

### 6.2 Error Recovery

When a cleaning step fails on a column:

1. Log the error with column name and step
2. Skip the column for that step
3. Mark column as `partially_cleaned` in metadata
4. Continue pipeline with remaining columns
5. Report all skipped operations in the quality summary

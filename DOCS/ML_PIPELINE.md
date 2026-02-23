# DATA_SCOUT — ML Pipeline

**Version:** 1.0 | **Last Updated:** 2026-02-20

---

## 1. Task Detection Logic

### 1.1 Detection Algorithm

```
Input: DataFrame (df) + target_column (optional)
                │
                ▼
        ┌───────────────┐
        │ Target column │──── No ───> CLUSTERING
        │  provided?    │
        └───────┬───────┘
                │ Yes
                ▼
        ┌───────────────┐
        │ Target dtype  │
        └───────┬───────┘
                │
    ┌───────────┼───────────┐
    │           │           │
  object/     float       int
  category      │           │
    │           │     ┌─────┴─────┐
    ▼           ▼     │ nunique   │
CLASSIF.    REGRESSION│ ≤ 20?     │
                      └─────┬─────┘
                        Yes │ No
                         ▼    ▼
                    CLASSIF. REGRESSION
```

### 1.2 Decision Rules

| Condition | Detected Task | Confidence |
|---|---|---|
| No target column provided | Clustering | 1.0 |
| Target is `object` or `category` | Classification | 0.95 |
| Target is `bool` | Classification | 1.0 |
| Target is `float64` | Regression | 0.90 |
| Target is `int64` with ≤20 unique values | Classification | 0.85 |
| Target is `int64` with >20 unique values | Regression | 0.80 |
| Target is `int64`, values are 0/1 only | Binary Classification | 0.95 |

### 1.3 Validation

After detection, the system validates:
- **Classification**: target has 2–50 classes; warns if >50
- **Regression**: target has continuous distribution; warns if all integers
- **Clustering**: dataset has ≥2 numeric features after encoding

User can override auto-detection via `task_type` parameter in the training request.

---

## 2. Model Selection Strategy

### 2.1 Model Pools

#### Classification Models

| Model | Library | When Preferred |
|---|---|---|
| LogisticRegression | sklearn | Baseline; linearly separable data |
| RandomForestClassifier | sklearn | Robust default; handles mixed types |
| GradientBoostingClassifier | sklearn | High accuracy; moderately sized data |
| LGBMClassifier | lightgbm | Large datasets; fast training |
| XGBClassifier | xgboost | Structured data with many features |
| ExtraTreesClassifier | sklearn | High-dimensional data; fast |
| KNeighborsClassifier | sklearn | Small datasets; local patterns |
| SVC (RBF kernel) | sklearn | Small-medium datasets; non-linear boundaries |

#### Regression Models

| Model | Library | When Preferred |
|---|---|---|
| LinearRegression | sklearn | Baseline |
| Ridge / Lasso / ElasticNet | sklearn | Regularization for high-dim data |
| RandomForestRegressor | sklearn | Non-linear relationships |
| GradientBoostingRegressor | sklearn | High accuracy |
| LGBMRegressor | lightgbm | Large datasets |
| XGBRegressor | xgboost | Structured data |
| SVR | sklearn | Small-medium datasets |

#### Clustering Algorithms

| Model | Library | When Preferred |
|---|---|---|
| KMeans | sklearn | Spherical clusters; known k |
| DBSCAN | sklearn | Arbitrary shapes; outlier detection |
| AgglomerativeClustering | sklearn | Hierarchical structure |
| GaussianMixture | sklearn | Overlapping clusters |

### 2.2 AutoML Execution (FLAML)

```python
from flaml import AutoML

automl = AutoML()
automl.fit(
    X_train, y_train,
    task=detected_task,           # "classification" or "regression"
    time_budget=time_budget,      # User-defined (default: 300s)
    metric=primary_metric,        # "accuracy" / "f1" / "rmse"
    estimator_list=model_pool,    # Filtered based on dataset size
    eval_method="cv",             # 5-fold cross-validation
    n_splits=5,
    log_file_name="automl.log",
    seed=42
)
```

### 2.3 Dataset-Adaptive Model Pool Filtering

| Dataset Characteristic | Filter Rule |
|---|---|
| Rows < 1,000 | Exclude LGBM, XGBoost (need more data) |
| Rows > 100,000 | Exclude SVC, KNN (too slow) |
| Features > 100 | Prefer tree-based models; add Lasso |
| Binary classification | Add calibrated classifiers |
| Highly imbalanced (>10:1) | Enable `class_weight='balanced'` on all models |

---

## 3. Evaluation Metrics

### 3.1 Metrics by Task Type

#### Classification

| Metric | Formula | Primary When |
|---|---|---|
| **Accuracy** | (TP+TN) / Total | Balanced classes |
| **F1 Score** (macro) | 2·P·R / (P+R) | Imbalanced classes (default primary) |
| **Precision** | TP / (TP+FP) | False positives are costly |
| **Recall** | TP / (TP+FN) | False negatives are costly |
| **ROC AUC** | Area under ROC curve | Binary classification |
| **Log Loss** | -Σ y·log(ŷ) | Probability calibration matters |

#### Regression

| Metric | Formula | Primary When |
|---|---|---|
| **RMSE** | √(Σ(y-ŷ)²/n) | Default primary metric |
| **MAE** | Σ|y-ŷ|/n | Outlier-robust evaluation |
| **R² Score** | 1 - SS_res/SS_tot | Explained variance |
| **MAPE** | Σ|(y-ŷ)/y|/n × 100 | Relative error matters |

#### Clustering

| Metric | Formula | When Used |
|---|---|---|
| **Silhouette Score** | (b-a) / max(a,b) | Always (primary) |
| **Calinski-Harabasz** | Between-cluster / within-cluster variance | Large datasets |
| **Davies-Bouldin** | Average similarity of each cluster | Cluster separation |
| **Inertia** | Sum of squared distances to centroid | KMeans; elbow method |

### 3.2 Cross-Validation Strategy

- **Default**: Stratified 5-fold CV (classification) / 5-fold CV (regression)
- **Small datasets** (<500 rows): 10-fold CV or Leave-One-Out
- **Time-series data** (detected via datetime index): TimeSeriesSplit (5 splits)

---

## 4. Overfitting Detection

### 4.1 Detection Method

```python
def detect_overfitting(train_score, test_score, threshold=0.05):
    gap = train_score - test_score
    relative_gap = gap / train_score if train_score > 0 else 0
    
    return {
        "train_score": train_score,
        "test_score": test_score,
        "absolute_gap": gap,
        "relative_gap": relative_gap,
        "is_overfitting": relative_gap > threshold,
        "severity": "high" if relative_gap > 0.15 else
                    "medium" if relative_gap > 0.08 else
                    "low" if relative_gap > threshold else "none"
    }
```

### 4.2 Severity Levels

| Level | Train-Test Gap | Action |
|---|---|---|
| **None** | < 5% | No action needed |
| **Low** | 5–8% | Warning in results; model still usable |
| **Medium** | 8–15% | Recommend model with lower complexity |
| **High** | > 15% | Flag model; suggest regularization or more data |

### 4.3 Mitigation Strategies (Auto-Applied)

1. **Regularization**: Increase `alpha` for linear models; reduce `max_depth` for trees
2. **Cross-validation**: Use more folds (10-fold) for better estimates
3. **Early stopping**: Enable for LGBM/XGBoost (`early_stopping_rounds=50`)
4. **Feature selection**: Reduce feature count if features > samples

---

## 5. Explainability Methods

### 5.1 Feature Importance

#### Tree-Based Models
```python
# Built-in feature importance (Gini / gain)
importances = model.feature_importances_
```

#### Linear Models
```python
# Coefficient magnitudes (after scaling)
importances = np.abs(model.coef_[0])
```

#### Model-Agnostic (Permutation Importance)
```python
from sklearn.inspection import permutation_importance
result = permutation_importance(model, X_test, y_test, n_repeats=10, random_state=42)
```

### 5.2 SHAP Values

Applied to the top-recommended model:

```python
import shap

explainer = shap.TreeExplainer(model)  # or KernelExplainer for non-tree models
shap_values = explainer.shap_values(X_test[:100])

# Generate:
# 1. Summary plot (global feature importance)
# 2. Waterfall plot (single prediction explanation)
# 3. Dependence plot (feature interaction)
```

### 5.3 Model Recommendation Justification

The recommendation engine generates a natural-language justification:

```
Template:
"{model_name} is recommended because:
1. It achieved the highest {primary_metric} of {score} across 5-fold cross-validation.
2. The train-test gap of {gap}% indicates {no/minimal/moderate} overfitting.
3. Top-3 most influential features: {f1} ({imp1}%), {f2} ({imp2}%), {f3} ({imp3}%).
4. Training completed in {time}s, making it {fast/moderate/slow} relative to alternatives.
{optional: class balance note}
{optional: compared to 2nd-best model}"
```

### 5.4 Explainability Output Structure

```json
{
  "feature_importance": [
    {"feature": "monthly_charges", "importance": 0.234, "rank": 1},
    {"feature": "tenure", "importance": 0.198, "rank": 2}
  ],
  "shap_summary_plot": "/reports/ds_7f3a2b/shap_summary.png",
  "model_card": {
    "model_type": "LGBMClassifier",
    "hyperparameters": {"n_estimators": 200, "max_depth": 6, "learning_rate": 0.1},
    "training_data_shape": [40000, 18],
    "cross_val_scores": [0.931, 0.935, 0.928, 0.940, 0.936],
    "overfitting_report": {"gap": 0.014, "severity": "none"}
  }
}
```

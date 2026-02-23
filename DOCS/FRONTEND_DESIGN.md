# DATA_SCOUT — Frontend Design System & UI Specification

**Version:** 1.0 | **Last Updated:** 2026-02-21

---

## Table of Contents

1. [Design Philosophy](#1-design-philosophy)
2. [Design Tokens](#2-design-tokens)
3. [Typography](#3-typography)
4. [Component Library](#4-component-library)
5. [Page Designs](#5-page-designs)
6. [Responsive Design](#6-responsive-design)
7. [Animations & Micro-Interactions](#7-animations--micro-interactions)
8. [Accessibility](#8-accessibility)
9. [Iconography](#9-iconography)

---

## 1. Design Philosophy

### 1.1 Principles

| Principle | Description | In Practice |
|---|---|---|
| **Clarity over cleverness** | Non-technical users must understand every screen | No jargon without tooltips; plain-English labels |
| **Progressive disclosure** | Show the minimum needed; reveal complexity on demand | Collapsed advanced settings; expandable model details |
| **Trust through transparency** | Users must trust AI recommendations | Always show reasoning, citations, confidence scores |
| **Guided workflow** | Users never wonder "what next?" | Step indicators, CTAs, contextual help |
| **Data-first aesthetics** | Charts and data should be the visual hero, not chrome | Generous whitespace around data; muted UI, vivid data colors |

### 1.2 Visual Identity

| Attribute | Value |
|---|---|
| **Brand Name** | DATA_SCOUT |
| **Tagline** | "From messy data to ML insights — in minutes" |
| **Visual Style** | Clean, modern SaaS with glassmorphism accents |
| **Mood** | Professional, trustworthy, approachable |
| **Inspiration** | Notion (clarity), Linear (polish), Vercel (dark elegance) |

---

## 2. Design Tokens

### 2.1 Color Palette

#### Light Theme

```css
:root {
  /* Primary — Deep Indigo */
  --color-primary-50:  #EEF2FF;
  --color-primary-100: #E0E7FF;
  --color-primary-200: #C7D2FE;
  --color-primary-300: #A5B4FC;
  --color-primary-400: #818CF8;
  --color-primary-500: #6366F1;   /* Main brand color */
  --color-primary-600: #4F46E5;
  --color-primary-700: #4338CA;

  /* Neutral — Slate */
  --color-neutral-50:  #F8FAFC;
  --color-neutral-100: #F1F5F9;
  --color-neutral-200: #E2E8F0;
  --color-neutral-300: #CBD5E1;
  --color-neutral-400: #94A3B8;
  --color-neutral-500: #64748B;
  --color-neutral-600: #475569;
  --color-neutral-700: #334155;
  --color-neutral-800: #1E293B;
  --color-neutral-900: #0F172A;

  /* Semantic */
  --color-success-500: #22C55E;
  --color-warning-500: #F59E0B;
  --color-error-500:   #EF4444;
  --color-info-500:    #3B82F6;

  /* Surface */
  --color-bg:          #FFFFFF;
  --color-bg-subtle:   #F8FAFC;
  --color-bg-card:     #FFFFFF;
  --color-border:      #E2E8F0;
  --color-text:        #0F172A;
  --color-text-muted:  #64748B;
}
```

#### Dark Theme

```css
[data-theme="dark"] {
  --color-bg:          #0B1120;
  --color-bg-subtle:   #111827;
  --color-bg-card:     #1E293B;
  --color-border:      #334155;
  --color-text:        #F1F5F9;
  --color-text-muted:  #94A3B8;

  --color-primary-500: #818CF8;
  --color-primary-600: #6366F1;
}
```

### 2.2 Spacing Scale

```css
:root {
  --space-1:  4px;     /* Tight: icon padding */
  --space-2:  8px;     /* Element gap */
  --space-3:  12px;    /* Input padding */
  --space-4:  16px;    /* Card padding */
  --space-5:  20px;    /* Section gap */
  --space-6:  24px;    /* Component separation */
  --space-8:  32px;    /* Section margin */
  --space-10: 40px;    /* Page section gap */
  --space-12: 48px;    /* Major section separator */
  --space-16: 64px;    /* Page padding top/bottom */
}
```

### 2.3 Borders & Shadows

```css
:root {
  --radius-sm:   4px;
  --radius-md:   8px;
  --radius-lg:   12px;
  --radius-xl:   16px;
  --radius-full: 9999px;

  --shadow-sm:   0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md:   0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
  --shadow-lg:   0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
  --shadow-xl:   0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
  --shadow-glow: 0 0 20px rgba(99, 102, 241, 0.3);   /* Primary glow for CTAs */
}
```

---

## 3. Typography

### 3.1 Font Stack

```css
:root {
  --font-sans:  'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-mono:  'JetBrains Mono', 'Fira Code', monospace;
}
```

**Load via Google Fonts:**
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

### 3.2 Type Scale

| Token | Size | Weight | Line Height | Usage |
|---|---|---|---|---|
| `--text-xs` | 12px | 400 | 1.5 | Captions, metadata, badges |
| `--text-sm` | 14px | 400 | 1.5 | Table cells, helper text |
| `--text-base` | 16px | 400 | 1.6 | Body text, inputs |
| `--text-lg` | 18px | 500 | 1.5 | Section subtitles |
| `--text-xl` | 20px | 600 | 1.4 | Card headings |
| `--text-2xl` | 24px | 600 | 1.3 | Page section titles |
| `--text-3xl` | 30px | 700 | 1.2 | Page headings |
| `--text-4xl` | 36px | 700 | 1.1 | Hero heading |
| `--text-mono` | 14px | 400 | 1.6 | Code, metrics, data values |

---

## 4. Component Library

### 4.1 Buttons

```
┌─────────────────────────────────────────────────┐
│  Primary      Secondary     Ghost      Danger   │
│ ┌──────────┐ ┌──────────┐ ┌────────┐ ┌────────┐│
│ │ Train    │ │ Preview  │ │ Cancel │ │ Delete ││
│ │ Models   │ │ Data     │ │        │ │        ││
│ └──────────┘ └──────────┘ └────────┘ └────────┘│
│  Filled       Outlined     Text only   Red fill │
│  indigo-600   indigo border  gray text  red-500  │
│  white text   indigo text               white    │
└─────────────────────────────────────────────────┘
```

| Variant | Background | Border | Text | Hover |
|---|---|---|---|---|
| **Primary** | `primary-600` | none | `white` | `primary-700` + `shadow-glow` |
| **Secondary** | transparent | `primary-300` | `primary-600` | `primary-50` bg |
| **Ghost** | transparent | none | `neutral-600` | `neutral-100` bg |
| **Danger** | `error-500` | none | `white` | `error-600` |
| **Disabled** | `neutral-200` | none | `neutral-400` | No change; `cursor: not-allowed` |

**Sizes:** `sm` (32px h), `md` (40px h), `lg` (48px h)

### 4.2 Card

```
┌─────────────────────────────────────────┐
│  Card Header                      Icon  │
│─────────────────────────────────────────│
│                                         │
│  Card body content. Can contain text,   │
│  tables, charts, or sub-components.     │
│                                         │
│─────────────────────────────────────────│
│  Footer actions                [Button] │
└─────────────────────────────────────────┘

Style:
  background: var(--color-bg-card)
  border: 1px solid var(--color-border)
  border-radius: var(--radius-lg)
  box-shadow: var(--shadow-sm)
  padding: var(--space-6)
```

### 4.3 Toast Notifications

```
  ┌────────────────────────────────────────┐
  │ ✅  Dataset cleaned successfully       │
  │     50,200 → 49,800 rows (−0.8%)   ✕  │
  └────────────────────────────────────────┘

  ┌────────────────────────────────────────┐
  │ ❌  Upload failed: file exceeds 200MB  │
  │     Try compressing or splitting    ✕  │
  └────────────────────────────────────────┘

Position: top-right, stacked
Duration: success=3s, error=6s, info=4s
Animation: slideInRight → fadeOut
```

### 4.4 Data Table

```
┌──────────────────────────────────────────────────────────┐
│ 🔍 Search columns...                      Rows: 49,800  │
├──────┬──────────────────┬──────────┬────────┬────────────┤
│  #   │ customer_id      │ revenue ↕│ region │ churn ↕    │
│      │ 🏷️ identifier     │ 🔢 float │ 📋 cat │ ✅ bool    │
├──────┼──────────────────┼──────────┼────────┼────────────┤
│  1   │ CUST-001         │ 1,250.50 │ East   │ No         │
│  2   │ CUST-002         │   890.00 │ West   │ Yes        │
│  3   │ CUST-003         │ 2,100.75 │ East   │ No         │
│  ...                                                     │
├──────┴──────────────────┴──────────┴────────┴────────────┤
│  ← 1 2 3 ... 100 →            Showing 1-50 of 49,800    │
└──────────────────────────────────────────────────────────┘

Features:
  - Column type badges (auto-detected dtype)
  - Click header to sort (↑↓)
  - Inline search filter
  - Pagination (50 rows/page)
  - Column resize handles
  - Alternating row backgrounds
```

### 4.5 Progress Bar (Training)

```
┌────────────────────────────────────────────────────────┐
│  Training in progress...                               │
│                                                        │
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░  62%        │
│                                                        │
│  🔄 Model 5/8: GradientBoosting  │  ⏱️ ~2:15 remaining │
│                                                        │
│  Completed:                                            │
│  ✅ LogisticRegression (4.2s)                          │
│  ✅ RandomForest (38.1s)                               │
│  ✅ LGBMClassifier (42.3s)                             │
│  ✅ ExtraTrees (22.8s)                                 │
│  🔄 GradientBoosting (running...)                      │
│  ⏳ XGBClassifier                                      │
│  ⏳ KNeighbors                                         │
│  ⏳ SVC                                                │
│                                                        │
│  [Cancel Training]                                     │
└────────────────────────────────────────────────────────┘

Animation: progress bar has smooth width transition (0.5s ease)
Gradient: linear-gradient(90deg, primary-500, primary-400)
Shimmer: animated highlight sweeping left→right on active bar
```

---

## 5. Page Designs

### 5.1 Home Page (Landing)

```
┌──────────────────────────────────────────────────────────────────┐
│  🔍 DATA_SCOUT              Features  Docs  Pricing    [Login]  │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│                   From Messy Data to                             │
│                 ML Insights — In Minutes                         │
│                                                                  │
│      Upload your dataset. We'll clean it, train models,          │
│      and let you ask questions — no code required.               │
│                                                                  │
│              [ Get Started Free ]    [ Watch Demo ]              │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │         ┌─── Animated product demo / screenshot ───┐     │   │
│  │         │   showing upload → results flow           │     │   │
│  │         └───────────────────────────────────────────┘     │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ─────────────── How It Works (4 Steps) ────────────────────    │
│                                                                  │
│  ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐          │
│  │   📤   │───>│   🧹   │───>│   🤖   │───>│   💬   │          │
│  │ Upload │    │ Clean  │    │ Train  │    │  Chat  │          │
│  │  your  │    │  auto  │    │  auto  │    │  ask   │          │
│  │  data  │    │  clean │    │  ML    │    │ ques-  │          │
│  │        │    │        │    │        │    │ tions  │          │
│  └────────┘    └────────┘    └────────┘    └────────┘          │
│                                                                  │
│  ─────────────── Key Features ──────────────────────────────    │
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌────────────────┐│
│  │ 🧹 Smart Cleaning│  │ 🏆 AutoML        │  │ 💬 AI Chatbot  ││
│  │ Auto-detect and  │  │ Train & compare  │  │ Ask questions  ││
│  │ fix data issues  │  │ 8+ ML models     │  │ in plain       ││
│  │ in seconds       │  │ automatically    │  │ English        ││
│  └──────────────────┘  └──────────────────┘  └────────────────┘│
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌────────────────┐│
│  │ 📊 Explainability│  │ 📋 Custom Reports│  │ 🔒 Privacy     ││
│  │ SHAP, feature    │  │ Generate branded │  │ Your data      ││
│  │ importance, why  │  │ PDF/HTML reports │  │ never leaves   ││
│  │ this model?      │  │ with one click   │  │ your control   ││
│  └──────────────────┘  └──────────────────┘  └────────────────┘│
│                                                                  │
│  ─────────────── Trusted By ────────────────────────────────    │
│  [logo] [logo] [logo] [logo] [logo]                             │
│                                                                  │
│  ─────────────── Footer ────────────────────────────────────    │
│  DATA_SCOUT │ Docs │ GitHub │ Privacy │ Terms  │ © 2026         │
└──────────────────────────────────────────────────────────────────┘
```

### 5.2 Upload Page

```
┌──────────────────────────────────────────────────────────────────┐
│  DATA_SCOUT    📂 Datasets  📊 Results  💬 Chat    [User ▼]     │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Upload Dataset                                Step 1 of 4      │
│  ─────────────                                ● ○ ○ ○           │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │         ┌───────────────────────────────────┐            │   │
│  │         │          📁                       │            │   │
│  │         │                                   │            │   │
│  │         │  Drag & drop your file here       │            │   │
│  │         │  or click to browse               │            │   │
│  │         │                                   │            │   │
│  │         │  CSV, XLSX, TSV, JSON • Max 200MB │            │   │
│  │         └───────────────────────────────────┘            │   │
│  │              Dashed border, subtle bg on drag-over       │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌── Upload Progress (when active) ─────────────────────────┐  │
│  │  📄 sales_q4_2025.csv  (15.2 MB)                        │  │
│  │  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  100%  ✅        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  Recent Uploads                                                  │
│  ┌──────────────────┬──────────┬─────────┬──────┬────────────┐ │
│  │ Dataset          │ Size     │ Rows    │ Cols │ Actions    │ │
│  ├──────────────────┼──────────┼─────────┼──────┼────────────┤ │
│  │ 📄 sales_q4.csv  │ 15.2 MB  │ 50,200  │ 18   │ [→] [🗑️]  │ │
│  │ 📄 customers.xlsx│ 8.4 MB   │ 12,400  │ 24   │ [→] [🗑️]  │ │
│  └──────────────────┴──────────┴─────────┴──────┴────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

### 5.3 Data Cleaning Page

```
┌──────────────────────────────────────────────────────────────────┐
│  DATA_SCOUT     📄 sales_q4.csv                 Step 2 of 4     │
│                                                 ● ● ○ ○         │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─── Data Quality Score ───────────────────────────────────┐   │
│  │                                                          │   │
│  │     📊 Quality Score:  ████████████████░░░░  78/100      │   │
│  │                                                          │   │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────┐│   │
│  │  │ Nulls     │  │ Outliers  │  │ Duplicates│  │ Types ││   │
│  │  │  12.3%    │  │    145    │  │    200    │  │  3 ⚠️ ││   │
│  │  │  ⚠️ 6 cols │  │  ⚠️ 4 cols│  │           │  │ mixed ││   │
│  │  └───────────┘  └───────────┘  └───────────┘  └───────┘│   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Cleaning Settings                                               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Missing values:  [Auto ▼]     Outlier method: [IQR ▼]  │   │
│  │  ☑ Remove duplicates           ☑ Encode categoricals     │   │
│  │                                                          │   │
│  │  [🧹 Clean Dataset]   [⚙️ Advanced Settings]             │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─── Before / After ──────────────────────────────────────┐   │
│  │  [Before]  [After]                                       │   │
│  │  ┌───────────────────────────────────────────────────┐   │   │
│  │  │  (DataTable showing raw or cleaned data preview)  │   │   │
│  │  │  with column type badges and null highlighting    │   │   │
│  │  └───────────────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Cleaning Actions Log                                            │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  ✅ revenue: median imputation (3,200 rows affected)     │   │
│  │  ✅ region: mode imputation (1,500 rows affected)        │   │
│  │  ✅ Removed 200 duplicate rows                           │   │
│  │  ✅ Outlier removal (IQR): 145 rows capped               │   │
│  │  ⚠️ date: 340 rows dropped (unparseable dates)           │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│                                          [Continue to Training →]│
└──────────────────────────────────────────────────────────────────┘
```

### 5.4 ML Training & Results Page

```
┌──────────────────────────────────────────────────────────────────┐
│  DATA_SCOUT     📄 sales_q4.csv                 Step 3 of 4     │
│                                                 ● ● ● ○         │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─── Task Detection ──────────────────────────────────────┐    │
│  │  🎯 Detected: Binary Classification  (confidence: 97%)  │    │
│  │  Target column: churn  │  Classes: Yes (42%), No (58%)   │    │
│  │  ⚠️ Mild class imbalance detected — using balanced mode  │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌─── 🏆 Recommended Model ────────────────────────────────┐    │
│  │                                                          │    │
│  │   LGBMClassifier                               ⭐ Best  │    │
│  │                                                          │    │
│  │   F1: 0.921  │  Accuracy: 93.4%  │  AUC: 0.962         │    │
│  │                                                          │    │
│  │   "Highest F1 (0.921) with fast training. No overfitting │    │
│  │   (train-test gap 1.4%). Excels on mixed feature types." │    │
│  │                                                          │    │
│  │   [📥 Download Model]  [📊 View SHAP]  [📋 Model Card]  │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌─── All Models Comparison ───────────────────────────────┐    │
│  │  Model               │ F1    │ Acc   │ AUC   │ Time    │    │
│  │  ─────────────────────┼───────┼───────┼───────┼─────────│    │
│  │  ⭐ LGBMClassifier    │ 0.921 │ 93.4% │ 0.962 │ 42.3s   │    │
│  │  XGBClassifier       │ 0.912 │ 92.5% │ 0.955 │ 55.1s   │    │
│  │  RandomForest        │ 0.905 │ 91.8% │ 0.948 │ 38.1s   │    │
│  │  GradientBoosting    │ 0.898 │ 91.2% │ 0.941 │ 67.4s   │    │
│  │  ExtraTrees          │ 0.891 │ 90.6% │ 0.935 │ 22.8s   │    │
│  │  LogisticRegression  │ 0.842 │ 87.1% │ 0.903 │  4.2s   │    │
│  │  KNeighbors          │ 0.815 │ 85.3% │ 0.881 │  6.7s   │    │
│  │  SVC                 │ 0.832 │ 86.5% │ 0.895 │ 91.2s   │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌─── Feature Importance ──┐  ┌─── Overfitting Check ──────┐   │
│  │                          │  │                             │   │
│  │ monthly_charges ▓▓▓▓▓▓▓ │  │ Train: 94.8%  Test: 93.4%  │   │
│  │ tenure          ▓▓▓▓▓   │  │ Gap: 1.4%  ✅ No overfitting│   │
│  │ contract_type   ▓▓▓▓    │  │                             │   │
│  │ total_charges   ▓▓▓     │  │ ┌─────────────────────────┐│   │
│  │ internet_svc    ▓▓      │  │ │ ████████████████████░   ││   │
│  │                          │  │ │ Train ▓▓▓  Test ░░░    ││   │
│  │                          │  │ └─────────────────────────┘│   │
│  └──────────────────────────┘  └─────────────────────────────┘   │
│                                                                  │
│                              [💬 Ask Questions]  [📋 Generate Report]│
└──────────────────────────────────────────────────────────────────┘
```

### 5.5 Chat Page

```
┌──────────────────────────────────────────────────────────────────┐
│  DATA_SCOUT     📄 sales_q4.csv     💬 Chat                     │
├─────────────────────────────────┬────────────────────────────────┤
│                                 │  Dataset Info                  │
│  LLM Provider: [GPT-4 ▼]       │  ─────────────                 │
│                                 │  📄 sales_q4.csv               │
│  ┌─ Suggested Questions ─────┐ │  49,800 rows × 18 cols         │
│  │ "Top 3 churn factors?"    │ │  Task: Classification          │
│  │ "Average revenue by       │ │  Best model: LGBM (F1: 0.921) │
│  │  region?"                 │ │                                │
│  │ "Revenue trend over       │ │  Quick Stats                   │
│  │  time?"                   │ │  ─────────────                 │
│  └───────────────────────────┘ │  Avg revenue: $1,420.50        │
│                                 │  Churn rate: 42.3%             │
│  ┌────────────────────────────┐│  Regions: 4                    │
│  │  🧑 What are the top 3    ││                                │
│  │   factors driving churn?  ││                                │
│  └────────────────────────────┘│                                │
│                                 │                                │
│  ┌────────────────────────────┐│                                │
│  │  🤖 Based on the dataset,  ││                                │
│  │  the top 3 factors are:   ││                                │
│  │                            ││                                │
│  │  1. **Monthly charges**    ││                                │
│  │     Customers >$70/month   ││                                │
│  │     churn at 2.3x the rate ││                                │
│  │     [revenue >70: 42% churn]│                                │
│  │                            ││                                │
│  │  2. **Contract type**      ││                                │
│  │     Month-to-month: 3.5x   ││                                │
│  │     [contract: M2M → 48%]  ││                                │
│  │                            ││                                │
│  │  3. **Tenure**             ││                                │
│  │     <12 months: 2.1x       ││                                │
│  │     [tenure <12: 38%]      ││                                │
│  │                            ││                                │
│  │  📎 3 citations │ 91% conf. ││                                │
│  └────────────────────────────┘│                                │
│                                 │                                │
│  ┌──────────────────────────┐  │                                │
│  │ Ask about your data...  🔼│  │                                │
│  └──────────────────────────┘  │                                │
└─────────────────────────────────┴────────────────────────────────┘
```

### 5.6 Report Page

```
┌──────────────────────────────────────────────────────────────────┐
│  DATA_SCOUT     📄 sales_q4.csv     📋 Report                   │
├─────────────────────────────────┬────────────────────────────────┤
│  Report Settings                │  Preview                       │
│  ─────────────                  │  ─────────                     │
│                                 │                                │
│  Title:                         │  ┌────────────────────────────┐│
│  [Q4 Churn Analysis Report  ]   │  │  Q4 CHURN ANALYSIS REPORT ││
│                                 │  │  Generated by DATA_SCOUT   ││
│  Sections:                      │  │  2026-02-21               ││
│  ☑ Executive Summary            │  │                            ││
│  ☑ Data Quality Report          │  │  1. Executive Summary     ││
│  ☑ Model Comparison             │  │  Dataset: sales_q4.csv    ││
│  ☑ Feature Importance           │  │  49,800 rows, 18 cols     ││
│  ☑ Recommendations              │  │  Best model: LGBM...      ││
│  ☐ Raw Data Statistics          │  │                            ││
│  ☐ Model Hyperparameters        │  │  2. Data Quality          ││
│                                 │  │  Score: 78 → 100 after    ││
│  Format:                        │  │  cleaning...              ││
│  (●) HTML  ( ) PDF              │  │                            ││
│                                 │  │  [Charts and tables       ││
│  [📋 Generate Report]           │  │   rendered inline]        ││
│                                 │  └────────────────────────────┘│
│                                 │                                │
│                                 │  [📥 Download HTML] [📥 PDF]   │
└─────────────────────────────────┴────────────────────────────────┘
```

---

## 6. Responsive Design

### 6.1 Breakpoints

| Breakpoint | Width | Layout |
|---|---|---|
| **Mobile** | < 640px | Single column; bottom nav; collapsed sidebar |
| **Tablet** | 640–1024px | Two-column where possible; condensed tables |
| **Desktop** | 1024–1440px | Standard layout; sidebar + content |
| **Wide** | > 1440px | Max-width 1400px; centered content |

### 6.2 Responsive Adjustments

| Component | Mobile | Desktop |
|---|---|---|
| **Header** | Hamburger menu; logo only | Full nav links + user menu |
| **Sidebar** | Slide-in overlay (hidden by default) | Persistent, collapsible (240px / 60px) |
| **Data Table** | Horizontal scroll; priority columns only | Full columns visible |
| **Chat Page** | Full width; side panel as bottom sheet | Two-column (60/40 split) |
| **Model Cards** | Full-width stack | 2-column grid |
| **Charts** | Simplified; fewer labels | Full detail |

---

## 7. Animations & Micro-Interactions

### 7.1 Keyframes

```css
/* Fade in on page mount */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* Skeleton shimmer for loading states */
@keyframes shimmer {
  0%   { background-position: -200px 0; }
  100% { background-position: calc(200px + 100%) 0; }
}

/* Progress bar glow pulse */
@keyframes barPulse {
  0%, 100% { box-shadow: 0 0 8px var(--color-primary-400); }
  50%      { box-shadow: 0 0 20px var(--color-primary-300); }
}

/* Typing indicator dots */
@keyframes typingBounce {
  0%, 80%, 100% { transform: translateY(0); }
  40%           { transform: translateY(-6px); }
}
```

### 7.2 Interaction Map

| Trigger | Animation | Duration | Easing |
|---|---|---|---|
| Page mount | `fadeIn` on content | 300ms | `ease-out` |
| Button hover | Scale 1.02 + shadow | 150ms | `ease` |
| Card hover | Lift (`translateY(-2px)`) + shadow-md | 200ms | `ease` |
| File drop (valid) | Green border flash + checkmark | 400ms | `ease-in-out` |
| File drop (invalid) | Red border shake (3 cycles) | 500ms | `ease` |
| Toast enter | Slide in from right | 300ms | `cubic-bezier(0.4, 0, 0.2, 1)` |
| Toast exit | Fade + slide right | 200ms | `ease-in` |
| Progress update | Width transition (smooth) | 500ms | `ease` |
| Model card expand | Height auto + fade content | 300ms | `ease-out` |
| Tab switch | Content crossfade | 200ms | `ease` |
| Skeleton loading | `shimmer` gradient sweep | 1.5s loop | `linear` |
| Typing indicator | 3 dots bounce staggered | 1.2s loop | `ease-in-out` |

---

## 8. Accessibility

### 8.1 Requirements (WCAG 2.1 AA)

| Requirement | Implementation |
|---|---|
| **Color contrast** | All text ≥ 4.5:1 ratio; large text ≥ 3:1; tested with axe-core |
| **Keyboard navigation** | All interactive elements focusable via Tab; visible focus ring (2px outline, primary-400) |
| **Screen readers** | All images have `alt`; icons have `aria-label`; live regions for progress updates |
| **Focus management** | Modal focuses first element on open; returns focus on close |
| **Error announcements** | Formula errors use `role="alert"`; toasts use `aria-live="polite"` |
| **Reduced motion** | `@media (prefers-reduced-motion)` disables all animations |
| **Form labels** | Every input has associated `<label>` or `aria-label` |
| **Skip navigation** | "Skip to main content" link visible on focus |

---

## 9. Iconography

### 9.1 Icon Set

Using **Lucide React** (open-source, consistent stroke-based icons):

```
npm install lucide-react
```

### 9.2 Icon Usage Map

| Context | Icon | Lucide Name |
|---|---|---|
| Upload file | 📤 | `Upload` |
| Dataset | 📄 | `FileSpreadsheet` |
| Clean data | 🧹 | `Sparkles` |
| Train models | 🤖 | `Bot` |
| Chat | 💬 | `MessageSquare` |
| Report | 📋 | `FileText` |
| Download | 📥 | `Download` |
| Delete | 🗑️ | `Trash2` |
| Settings | ⚙️ | `Settings` |
| Success | ✅ | `CheckCircle` |
| Warning | ⚠️ | `AlertTriangle` |
| Error | ❌ | `XCircle` |
| Info | ℹ️ | `Info` |
| Star/Best | ⭐ | `Star` |
| Charts | 📊 | `BarChart3` |
| User | 👤 | `User` |
| Logout | 🚪 | `LogOut` |
| Search | 🔍 | `Search` |
| Sort | ↕ | `ArrowUpDown` |
| Expand | ▸ | `ChevronRight` |

**Icon size:** 16px (inline), 20px (buttons), 24px (navigation), 32px (empty states)
**Stroke width:** 1.5px (consistent across all icons)

# DATA_SCOUT — Frontend Specification

**Version:** 1.0 | **Last Updated:** 2026-02-20

---

## 1. React Architecture

### 1.1 Technology Choices

| Concern | Technology | Rationale |
|---|---|---|
| Build tool | Vite 5 | Fast HMR, ESBuild-based |
| Router | React Router v6 | Standard; nested routes |
| State | Zustand 4 | Minimal boilerplate, no providers |
| HTTP | Axios | Interceptors, cancel tokens |
| Styling | CSS Modules + design tokens | Scoped styles, theming |
| Charts | Recharts | Declarative, composable |
| Tables | @tanstack/react-table v8 | Headless, performant |
| Animations | Framer Motion | Smooth layout/page transitions |
| Forms | React Hook Form + Zod | Performant validation |

### 1.2 Project Structure

```
src/
├── components/                    # Shared UI components
│   ├── ui/                        # Button, Input, Modal, Badge, Card, Spinner
│   ├── layout/                    # Header, Sidebar, PageContainer
│   ├── Upload/                    # FileDropzone, UploadProgress, FileList
│   ├── DataPreview/               # DataTable, QualityPanel, BeforeAfter
│   ├── MLDashboard/               # TrainingProgress, ModelCard, ComparisonTable
│   ├── ChatPanel/                 # ChatMessage, ChatInput, ProviderSelector
│   └── ReportViewer/              # ReportPreview, SectionToggle, ExportButton
├── pages/
│   ├── HomePage.jsx               # Landing + upload CTA
│   ├── UploadPage.jsx             # File upload workflow
│   ├── DataPage.jsx               # Preview + cleaning
│   ├── TrainingPage.jsx           # ML config + progress
│   ├── ResultsPage.jsx            # Model comparison + recommendation
│   ├── ChatPage.jsx               # RAG chatbot
│   ├── ReportPage.jsx             # Report generation
│   ├── LoginPage.jsx              # Auth
│   └── NotFoundPage.jsx           # 404
├── hooks/
│   ├── useWebSocket.js            # WS connection management
│   ├── useUpload.js               # File upload with progress
│   ├── useJobPolling.js           # Poll job status + WS fallback
│   └── useAuth.js                 # Token management
├── services/
│   ├── api.js                     # Axios instance + interceptors
│   ├── uploadService.js           # POST /upload
│   ├── dataService.js             # GET/POST /data/*
│   ├── mlService.js               # POST /ml/train, GET /ml/results
│   ├── chatService.js             # POST /chat/message
│   └── reportService.js           # POST /report/generate
├── store/
│   ├── useDatasetStore.js         # Active dataset state
│   ├── useJobStore.js             # Running jobs + progress
│   ├── useChatStore.js            # Conversation history
│   └── useAuthStore.js            # User + tokens
├── utils/
│   ├── formatters.js              # Number, date, byte formatting
│   └── constants.js               # API URLs, limits
├── App.jsx
└── main.jsx
```

---

## 2. State Management

### 2.1 Zustand Store Design

```javascript
// store/useDatasetStore.js
import { create } from 'zustand';

const useDatasetStore = create((set) => ({
  datasets: [],
  activeDataset: null,
  cleaningStatus: null,
  qualityReport: null,
  
  setActiveDataset: (dataset) => set({ activeDataset: dataset }),
  setCleaningStatus: (status) => set({ cleaningStatus: status }),
  setQualityReport: (report) => set({ qualityReport: report }),
  
  addDataset: (dataset) => set((state) => ({
    datasets: [...state.datasets, dataset]
  })),
  
  removeDataset: (id) => set((state) => ({
    datasets: state.datasets.filter(d => d.dataset_id !== id),
    activeDataset: state.activeDataset?.dataset_id === id ? null : state.activeDataset
  })),
}));
```

### 2.2 Store Boundaries

| Store | Manages | Persisted? |
|---|---|---|
| `useAuthStore` | User session, tokens | Yes (localStorage) |
| `useDatasetStore` | Dataset list, active dataset, quality | No |
| `useJobStore` | Running jobs, progress % | No |
| `useChatStore` | Conversations, LLM provider | No |

---

## 3. Page Structure & Routing

### 3.1 Route Map

```javascript
<Routes>
  <Route path="/" element={<HomePage />} />
  <Route path="/login" element={<LoginPage />} />
  <Route element={<ProtectedLayout />}>          {/* Auth guard */}
    <Route path="/upload" element={<UploadPage />} />
    <Route path="/data/:datasetId" element={<DataPage />} />
    <Route path="/train/:datasetId" element={<TrainingPage />} />
    <Route path="/results/:datasetId" element={<ResultsPage />} />
    <Route path="/chat/:datasetId" element={<ChatPage />} />
    <Route path="/report/:datasetId" element={<ReportPage />} />
  </Route>
  <Route path="*" element={<NotFoundPage />} />
</Routes>
```

### 3.2 Page Wireframes

#### Upload Page
```
┌────────────────────────────────────────────────┐
│  ┌──────────────────────────────────────────┐  │
│  │                                          │  │
│  │     📁 Drag & drop your dataset here     │  │
│  │         or click to browse               │  │
│  │                                          │  │
│  │     Supported: CSV, XLSX, TSV, JSON      │  │
│  │     Max size: 200MB                      │  │
│  │                                          │  │
│  └──────────────────────────────────────────┘  │
│                                                │
│  Recent Uploads:                               │
│  ┌──────────┬──────────┬────────┬──────────┐  │
│  │ Name     │ Size     │ Status │ Actions  │  │
│  ├──────────┼──────────┼────────┼──────────┤  │
│  │ sales.csv│ 15.2 MB  │ ✅     │ View │ ✕ │  │
│  │ data.xlsx│ 8.4 MB   │ 🔄     │      │ ✕ │  │
│  └──────────┴──────────┴────────┴──────────┘  │
└────────────────────────────────────────────────┘
```

#### ML Results Page
```
┌─────────────────────────────────────────────────┐
│  🏆 Recommended Model                          │
│  ┌───────────────────────────────────────────┐  │
│  │  LGBMClassifier                           │  │
│  │  F1: 0.921 │ Accuracy: 93.4% │ AUC: 0.96│  │
│  │  "Highest F1 with no overfitting..."      │  │
│  │  [Download .pkl]  [View SHAP]             │  │
│  └───────────────────────────────────────────┘  │
│                                                 │
│  Model Comparison                               │
│  ┌────────────┬────────┬──────┬────────┬─────┐ │
│  │ Model      │ F1     │ Acc  │ AUC    │ Time│ │
│  ├────────────┼────────┼──────┼────────┼─────┤ │
│  │ LGBM ⭐    │ 0.921  │ 93.4 │ 0.962  │ 42s │ │
│  │ RF         │ 0.905  │ 91.8 │ 0.948  │ 38s │ │
│  │ XGBoost    │ 0.912  │ 92.5 │ 0.955  │ 55s │ │
│  └────────────┴────────┴──────┴────────┴─────┘ │
│                                                 │
│  Feature Importance          SHAP Summary       │
│  ┌───────────────────┐  ┌───────────────────┐  │
│  │ ▓▓▓▓▓▓▓ charges   │  │  [SHAP beeswarm  │  │
│  │ ▓▓▓▓▓  tenure     │  │   plot rendered   │  │
│  │ ▓▓▓▓  contract    │  │   as image]       │  │
│  └───────────────────┘  └───────────────────┘  │
└─────────────────────────────────────────────────┘
```

---

## 4. API Integration

### 4.1 Axios Instance

```javascript
// services/api.js
import axios from 'axios';
import { useAuthStore } from '../store/useAuthStore';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  timeout: 30000,
});

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().accessToken;
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      const refreshed = await useAuthStore.getState().refreshToken();
      if (refreshed) return api.request(error.config);
      useAuthStore.getState().logout();
    }
    return Promise.reject(error);
  }
);

export default api;
```

### 4.2 WebSocket Hook

```javascript
// hooks/useWebSocket.js
import { useEffect, useRef, useCallback } from 'react';

export function useWebSocket(jobId, onMessage) {
  const ws = useRef(null);

  const connect = useCallback(() => {
    if (!jobId) return;
    const url = `${import.meta.env.VITE_WS_URL}/ws/jobs/${jobId}`;
    ws.current = new WebSocket(url);
    
    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      onMessage(data);
    };
    
    ws.current.onclose = () => {
      setTimeout(connect, 3000); // Auto-reconnect
    };
  }, [jobId, onMessage]);

  useEffect(() => {
    connect();
    return () => ws.current?.close();
  }, [connect]);

  return { isConnected: ws.current?.readyState === WebSocket.OPEN };
}
```

---

## 5. Error & Loading States

### 5.1 Loading States

| State | UI Treatment |
|---|---|
| **Page loading** | Full-page skeleton with pulsing placeholders |
| **Data table loading** | Table skeleton with row placeholders |
| **File uploading** | Progress bar with percentage + estimated time |
| **ML training** | Animated progress bar + current model name |
| **Chart loading** | Chart area skeleton |
| **Chatbot thinking** | Typing indicator (three-dot animation) |

### 5.2 Error States

| Error Type | UI Treatment |
|---|---|
| **Network error** | Toast: "Connection lost. Retrying..." + auto-retry |
| **File too large** | Inline error below dropzone: "File exceeds 200MB limit" |
| **Invalid format** | Inline error: "Unsupported file type. Use CSV, XLSX, TSV, or JSON" |
| **Training failed** | Error card with details + "Retry" button |
| **LLM API error** | Chat bubble: "Unable to process. Trying alternative provider..." |
| **401 Unauthorized** | Redirect to login page |
| **404 Not Found** | Full-page 404 with "Go Home" link |
| **Rate limited** | Toast: "Too many requests. Please wait {X} seconds" |
| **Server error (500)** | Error card: "Something went wrong" + support link |

### 5.3 Empty States

| Context | Message | CTA |
|---|---|---|
| No datasets | "Upload your first dataset to get started" | "Upload Dataset" button |
| No models trained | "Train models to see results" | "Start Training" button |
| No chat history | "Ask a question about your data" | Suggested questions |
| No reports | "Generate your first report" | "Create Report" button |

### 5.4 Toast Notification System

```javascript
// Global toast via Zustand
const useToastStore = create((set) => ({
  toasts: [],
  addToast: (toast) => set((state) => ({
    toasts: [...state.toasts, { id: Date.now(), ...toast }]
  })),
  removeToast: (id) => set((state) => ({
    toasts: state.toasts.filter(t => t.id !== id)
  })),
}));

// Usage: useToastStore.getState().addToast({
//   type: 'error',  // success | error | warning | info
//   message: 'Upload failed: file too large',
//   duration: 5000
// })
```

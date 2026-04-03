# CareerForge — Deterministic Career Intelligence Platform

> Build your path. Track your progress. Get hired.

---

## ⚡ Quick Start

```bash
uvicorn main:app --reload --port 8000 --host 127.0.0.1
```

Then open **http://localhost:8000** in your browser.

---

## 📁 Project Structure

```
careerforge/
├── main.py                  ← FastAPI app (all API endpoints)
├── profiles.py              ← Multi-profile management
├── questions.py             ← Deterministic question selection engine
├── readiness.py             ← Readiness model (0.6×test + 0.4×completion)
├── evaluation.py            ← Score evaluation engine (untouched)
├── gap_detection.py         ← Gap detection engine (untouched)
├── decision.py              ← Decision/recommendation engine (untouched)
├── explainability.py        ← Explainability layer (untouched)
├── generate_data.py         ← Generates question bank + learning content
├── requirements.txt
├── start.sh
├── data/
│   ├── company_map.json     ← Full Category → Company → Role mapping
│   ├── questions.json       ← 110 MCQ questions (DSA + CS + SD)
│   ├── learning_content.json← Striver-style topic groups
│   ├── users.json           ← Auth store (auto-created)
│   ├── profiles.json        ← Profile store (auto-created)
│   └── progress.json        ← Progress store (auto-created)
└── frontend/
    └── index.html           ← Complete SPA (all views, no build step)
```

---

## 🔄 User Flow

```
Login/Signup
    ↓
Profile List (create or continue)
    ↓
Sequential Selection: Category → Company → Role
    ↓
Test Guidelines
    ↓
Initial Assessment (MCQ, deterministic)
    ↓
Results + Adaptive Learning Plan
    ↓
Dashboard (readiness ring, score cards, section cards)
    ↓
Section Detail (Striver A2Z-style topic list with checkboxes)
    ↓
Readiness Analysis (gaps, action plan, explainability)
```

---

## 🧠 Determinism Guarantee

- `profile_id = hash(username + category + company + role)`
- `question_seed = hash(profile_id)` → deterministic Fisher-Yates shuffle
- `readiness_score = 0.6 × test_score + 0.4 × completion_percentage`
- All thresholds generated from Company Intelligence Layer (no calibration)
- **Same input → always same output**

---

## 🏢 Supported Companies

| Category | Companies |
|---|---|
| HFT / Quant | Jane Street, Citadel Securities, Tower Research, Hudson River Trading, Jump Trading |
| Product / FAANG+ | Google, Microsoft, Amazon, Meta, Adobe, Flipkart/Uber |
| AI Labs & FinTech | OpenAI/Anthropic, Goldman Sachs, Bloomberg |
| Service / MNC | TCS, Infosys/Wipro, Accenture, Cognizant/HCL |

---

## 🔌 API Endpoints

| Method | Path | Description |
|---|---|---|
| POST | `/signup` | Create account |
| POST | `/login` | Get session token |
| POST | `/logout` | Invalidate token |
| GET | `/company-map` | Full hierarchy |
| GET | `/profiles` | List user profiles |
| POST | `/profiles` | Create profile |
| GET | `/profiles/{id}` | Get profile |
| GET | `/test/{id}/questions` | Get test questions |
| POST | `/test/{id}/submit` | Submit answers |
| GET | `/dashboard/{id}` | Full dashboard data |
| POST | `/progress/{id}/toggle` | Toggle topic item |
| GET | `/readiness/{id}` | Full analysis |

---

## 🎨 Features

- ✅ Dark / Light theme toggle
- ✅ Multi-profile system
- ✅ Deterministic question selection (hash-based seed)
- ✅ Striver A2Z-style learning dashboard
- ✅ 3-level progress tracking (item → topic → section)
- ✅ Adaptive difficulty recommendation
- ✅ Readiness ring (animated SVG)
- ✅ Gap detection + action plan
- ✅ Full explainability layer
- ✅ Periodic test support
- ✅ No external database (JSON file store)
- ✅ Single HTML file frontend (no build step)

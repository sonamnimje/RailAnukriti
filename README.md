# 👉 Live link: https://rail-anukriti-7u8e.vercel.app/


# 🚆 RailAnukriti – AI-Powered Smart Train Traffic Optimizer
RailAnukriti is an AI-powered decision-support system for Indian Railways section controllers.  
It optimizes train precedence, crossings, and platform allocation to maximize throughput and minimize delays.

The system combines Artificial Intelligence (Reinforcement Learning, Graph Neural Networks) and Operations Research (Constraint Optimization) to make fast, explainable, and adaptive scheduling decisions.

---

## 🎯 Goals
- Enable real-time train scheduling (<1s response)
- Provide explainable recommendations with reasoning
- Simulate disruptions using a digital twin
- Allow human-in-the-loop overrides with adaptive learning
- Improve throughput, reduce congestion, and minimize delays

---

## 🌟 Core Features
- 📍 **Live Dashboard** → Real-time train map, AI suggestions, KPIs
- 🛠 **Simulation Mode** → Test disruption scenarios
- 🧑‍✈️ **Human-in-the-Loop** → Controllers can override AI decisions
- 📊 **Analytics & Reports** → Delay trends, throughput insights
- 🤖 **Adaptive Learning** → Smarter decisions from past delays & overrides

---

## 🏗 Tech Stack

**Backend:**
- Python, FastAPI, Uvicorn
- OR-Tools (Constraint Solver)
- PyTorch + RLlib (Reinforcement Learning)
- Graph Neural Networks (rail network topology learning)

**Frontend:**
- React (Vite)
- TailwindCSS
- Shadcn/UI (compatible)

**Database:**
- SQLite by default (development) – `backend/app/rail.db`
- Optional: PostgreSQL/TimescaleDB for time-series at scale

**Infra/Runtime:**
- WebSockets (real-time updates)
- Local dev via Vite + Uvicorn

---

## 📂 Repository Structure
```text
RailAnukriti/
│── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI app factory + routes mount
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── ingest.py
│   │   │       ├── optimizer.py
│   │   │       ├── simulator.py
│   │   │       ├── overrides.py
│   │   │       ├── users.py
│   │   │       ├── reports.py
│   │   │       └── ws.py
│   │   ├── core/
│   │   │   └── config.py
│   │   ├── db/
│   │   │   ├── models.py
│   │   │   ├── session.py
│   │   │   └── init_timescaledb.sql
│   │   ├── services/
│   │   │   ├── optimizer.py
│   │   │   └── simulator.py
│   │   └── rail.db                 # SQLite dev database
│   ├── requirements.txt
│   └── uvicorn_app.py              # Uvicorn entrypoint
│
│── frontend/
│   ├── index.html
│   ├── package.json
│   ├── src/
│   │   ├── main.tsx
│   │   ├── index.css
│   │   ├── lib/api.ts
│   │   └── pages/
│   │       ├── App.tsx
│   │       ├── Dashboard.tsx
│   │       ├── Home.tsx
│   │       ├── Login.tsx
│   │       ├── Reports.tsx
│   │       ├── Simulation.tsx
│   │       └── Settings.tsx
│   └── vite.config.ts
│
│── README.md
```

---

## 🚀 Getting Started

### 1️⃣ Clone the repo
```bash
git clone https://github.com/sonamnimje/RailAnukriti.git
cd RailAnukriti
```

### 2️⃣ Backend Setup
```bash
cd backend
pip install -r requirements.txt
# Option A: run via module path
uvicorn app.main:app --reload
# Option B: use helper (same effect)
python uvicorn_app.py
```

### 3️⃣ Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 4️⃣ Database Setup
Development defaults to SQLite at `backend/app/rail.db`. No action needed.

For PostgreSQL/TimescaleDB (optional), use `backend/app/db/init_timescaledb.sql` as a starting point.

### 5️⃣ Run order (local)
1. Start backend (see step 2)
2. Start frontend
```bash
cd frontend
npm run dev
```

---

## 📊 Example Use Cases

- ✅ Prioritize express trains over goods during peak hours
- ✅ Simulate track maintenance disruptions in digital twin
- ✅ Allocate platforms optimally at busy junctions
- ✅ Adapt schedules when human controllers override

---

## 🤝 Team RailAnukriti

- 🚆 Backend AI/Optimization: Sonam Nimje, Shreya Saraf
- 🖥 Frontend/UI: Sameeksha Vishwakarma
- 🗄 Database & Infra: Riya Saraf
- 📊 Simulation & Reports: Palak Singh, Richa Singh

---

## 📜 License

MIT License – feel free to use and adapt for research & development.

---


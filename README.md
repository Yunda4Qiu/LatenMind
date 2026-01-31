# LatentMind

LatentMind is a small **frontend–backend separated** interactive experiment.

- **Backend (FastAPI)**: provides a JSON API (default: `http://127.0.0.1:8001`)
- **Frontend (static HTML/JS)**: calls the backend via `fetch()`

## Project layout

- `backend/`: FastAPI app + game logic + logging
- `frontend/`: static UI (`index.html`, `main.js`, `report.html`)
- `requirements.txt`: minimal Python dependencies

## Prerequisites

- Python 3.10+ 
- `fastapi` and `uvicorn`

Install dependencies:

```bash
pip install -r requirements.txt
```

## 1) Start the backend API

From the project root:

```bash
cd backend
uvicorn app:app --reload --port 8001
```

## 2) Start the frontend (static server)

```bash
cd frontend
python3 -m http.server 5500
```

## 3) How to play in the browser

1. Open the UI: `http://127.0.0.1:5500/index.html`
2. Click **Start experiment**
3. Click **Action 0 / Action 1 / Action 2 / Hold** to play rounds
4. After round 20, a **View report** button appears (no forced redirect)
5. On the report page, click **Back to game** to continue the same session

Notes:

- The backend keeps game sessions in memory. If you restart the backend, old sessions are lost.
- The frontend stores the last state in `localStorage` to make “Back to game” smoother.

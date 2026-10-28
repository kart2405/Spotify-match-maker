# Spotify Match Maker

A dating website that matches people based on how similar their music taste is, using data from the Spotify API.

## Tech stack

- **Frontend:** React (Vite) in `frontend/`
- **Backend:** Python (FastAPI) in `backend/`
- **Database:** PostgreSQL (coming in a later step)

## Run it locally

You need Python 3.10+ and Node.js 18+.

### 1. Start the backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Check it at http://localhost:8000/api/health (interactive API docs at http://localhost:8000/docs).

### 2. Start the frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. You should see "Hello from the Spotify Match Maker backend!" on the page.

## Roadmap

1. Project skeleton (this step)
2. Sign up + connect Spotify, store each user's top artists and genres
3. Basic match score (shared artists and genres) + browse / like / match pages
4. Chat, then deploy (frontend on Netlify, backend on Render, database on Supabase)

The matching algorithm will be upgraded step by step: basic overlap, then weighted, then taste vectors, then learning from user behavior.

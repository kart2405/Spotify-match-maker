# Spotify Match Maker

A dating website that matches people by how similar their music taste is, using data from the
Spotify API. See [PLAN.md](PLAN.md) for the plan and the matching algorithm roadmap.

## Tech stack

- **Frontend:** React (Vite) in `frontend/`
- **Backend:** Python (FastAPI + SQLAlchemy) in `backend/`
- **Database:** SQLite for local development; PostgreSQL in production (just change `DATABASE_URL`)

## How it's organised

```
backend/app/
  main.py            app setup
  auth.py            login sessions and your own profile (/api/me)
  dating.py          browse, like/pass, matches
  seed.py            creates fake test users
  music/             the privacy boundary: only this folder touches listening data
    spotify.py       "Log in with Spotify"
    compatibility.py the matching algorithm
frontend/src/
  pages/             Landing, Browse, Matches, Profile
  components/        Avatar, CompatRing, ProfileCard
```

## Run it locally

You need Python 3.10+ and Node.js 18+.

### 1. Start the backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env           # Windows: copy .env.example .env
python -m app.seed             # creates ~50 fake users to match with
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 2. Start the frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open **http://127.0.0.1:5173** and click **Try the demo** to log in as a test user.

## Turn on "Log in with Spotify"

1. Go to https://developer.spotify.com/dashboard and create an app.
2. In the app settings, add this Redirect URI exactly:
   `http://127.0.0.1:5173/api/auth/spotify/callback`
   (Spotify doesn't accept `localhost`, so always open the site at `127.0.0.1`.)
3. Tick **Web API** as the API you'll use, and save.
4. Copy the Client ID and Client Secret into `backend/.env`.
5. In development mode, add each tester's Spotify email under **User Management** (up to 25).
6. Restart the backend. The Spotify button on the home page is now live.

## Privacy

Only `backend/app/music/` reads raw listening data. The rest of the app can only ask for a
compatibility percentage and, if both people opted in, a few shared artists. Spotify access
tokens are used once at login to fetch top artists and are never stored.

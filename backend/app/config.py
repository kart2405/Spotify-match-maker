"""App settings, read from environment variables (or backend/.env)."""

import os

from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")
SPOTIFY_REDIRECT_URI = os.getenv(
    "SPOTIFY_REDIRECT_URI", "http://127.0.0.1:5173/api/auth/spotify/callback"
)
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://127.0.0.1:5173")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./matchmaker.db")
DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"

SPOTIFY_ENABLED = bool(SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET)

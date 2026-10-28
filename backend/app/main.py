"""Spotify Match Maker API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app import auth, config, dating
from app.database import Base, engine
from app.music import models as music_models  # noqa: F401  (registers the music tables)
from app.music import spotify

Base.metadata.create_all(engine)

app = FastAPI(title="Spotify Match Maker API")

app.add_middleware(SessionMiddleware, secret_key=config.SECRET_KEY, same_site="lax", max_age=60 * 60 * 24 * 14)
# In development the React dev server proxies /api to this app, so this only matters
# when the frontend is hosted on a different domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(spotify.router)
app.include_router(dating.router)


@app.get("/api/health")
def health():
    """Simple check that the backend is running."""
    return {"status": "ok", "message": "Hello from the Spotify Match Maker backend!"}

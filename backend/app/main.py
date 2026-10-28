"""Spotify Match Maker API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Spotify Match Maker API")

# Allow the React dev server (Vite runs on port 5173) to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    """Simple check that the backend is running."""
    return {"status": "ok", "message": "Hello from the Spotify Match Maker backend!"}

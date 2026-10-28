"""'Log in with Spotify': creates the account and imports top artists in one step."""

import secrets
from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app import config
from app.database import get_db
from app.models import User
from app.music.store import save_top_artists

router = APIRouter(prefix="/api/auth/spotify")

AUTHORIZE_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_URL = "https://api.spotify.com/v1"
# Only ask for what we need: the user's top artists. No email, no playlists.
SCOPES = "user-top-read"


@router.get("/login")
def login(request: Request):
    if not config.SPOTIFY_ENABLED:
        raise HTTPException(503, "Spotify login isn't set up yet. Add your keys to backend/.env.")
    state = secrets.token_urlsafe(16)
    request.session["spotify_state"] = state
    params = {
        "client_id": config.SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": config.SPOTIFY_REDIRECT_URI,
        "scope": SCOPES,
        "state": state,
    }
    return RedirectResponse(f"{AUTHORIZE_URL}?{urlencode(params)}")


@router.get("/callback")
def callback(request: Request, code: str = "", state: str = "", error: str = "", db: Session = Depends(get_db)):
    if error or not code or state != request.session.pop("spotify_state", None):
        return RedirectResponse(f"{config.FRONTEND_URL}/?error=spotify")

    with httpx.Client(timeout=15) as client:
        token_res = client.post(
            TOKEN_URL,
            data={"grant_type": "authorization_code", "code": code, "redirect_uri": config.SPOTIFY_REDIRECT_URI},
            auth=(config.SPOTIFY_CLIENT_ID, config.SPOTIFY_CLIENT_SECRET),
        )
        if token_res.status_code != 200:
            return RedirectResponse(f"{config.FRONTEND_URL}/?error=spotify")
        headers = {"Authorization": f"Bearer {token_res.json()['access_token']}"}

        me = client.get(f"{API_URL}/me", headers=headers).json()
        top = client.get(
            f"{API_URL}/me/top/artists", headers=headers, params={"limit": 50, "time_range": "medium_term"}
        ).json()

    # The access token is used once and never stored.
    top_artists = [{"name": a["name"], "genres": a.get("genres", [])} for a in top.get("items", [])]

    user = db.query(User).filter(User.spotify_id == me["id"]).first()
    is_new = user is None
    if is_new:
        user = User(spotify_id=me["id"], name=me.get("display_name") or "New listener")
        db.add(user)
        db.commit()
    save_top_artists(db, user.id, top_artists)

    request.session["user_id"] = user.id
    return RedirectResponse(f"{config.FRONTEND_URL}/?welcome=1" if is_new else config.FRONTEND_URL)

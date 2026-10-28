"""Sessions, the current user, and the user's own profile."""

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app import config
from app.database import get_db
from app.models import User
from app.music import get_taste_summary

router = APIRouter(prefix="/api")

DEMO_USER_SPOTIFY_ID = "demo-user"


def current_user(request: Request, db: Session = Depends(get_db)) -> User:
    user_id = request.session.get("user_id")
    user = db.get(User, user_id) if user_id else None
    if user is None:
        raise HTTPException(401, "Please log in.")
    return user


def profile_json(user: User) -> dict:
    return {
        "id": user.id,
        "name": user.name,
        "age": user.age,
        "city": user.city,
        "bio": user.bio,
        "gender": user.gender,
        "interested_in": user.interested_in,
        "share_artists": user.share_artists,
    }


@router.get("/config")
def get_config():
    return {"demo_mode": config.DEMO_MODE, "spotify_enabled": config.SPOTIFY_ENABLED}


@router.post("/auth/demo")
def demo_login(request: Request, db: Session = Depends(get_db)):
    if not config.DEMO_MODE:
        raise HTTPException(404)
    user = db.query(User).filter(User.spotify_id == DEMO_USER_SPOTIFY_ID).first()
    if user is None:
        raise HTTPException(503, "No demo user yet. Run: python -m app.seed")
    request.session["user_id"] = user.id
    return profile_json(user)


@router.post("/auth/logout")
def logout(request: Request):
    request.session.clear()
    return {"ok": True}


@router.get("/me")
def get_me(user: User = Depends(current_user), db: Session = Depends(get_db)):
    return {**profile_json(user), "music": get_taste_summary(db, user.id)}


class ProfileUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    age: int | None = Field(None, ge=18, le=120)
    city: str | None = Field(None, max_length=100)
    bio: str | None = Field(None, max_length=500)
    gender: str | None = Field(None, pattern="^(man|woman|nonbinary)$")
    interested_in: str | None = Field(None, pattern="^(men|women|everyone)$")
    share_artists: bool | None = None


@router.patch("/me")
def update_me(update: ProfileUpdate, user: User = Depends(current_user), db: Session = Depends(get_db)):
    for field, value in update.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    return get_me(user, db)

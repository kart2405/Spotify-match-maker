"""Browse, like/pass, and matches. Uses the music module only through compatibility()."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import current_user
from app.database import get_db
from app.models import Like, User
from app.music import compatibility, shared_artists

router = APIRouter(prefix="/api")

GENDER_FOR_INTEREST = {"men": "man", "women": "woman"}


def is_interested(user: User, other: User) -> bool:
    if user.interested_in == "everyone":
        return True
    return other.gender == GENDER_FOR_INTEREST.get(user.interested_in)


def card_json(db: Session, user: User, other: User, score: int) -> dict:
    card = {
        "id": other.id,
        "name": other.name,
        "age": other.age,
        "city": other.city,
        "bio": other.bio,
        "compatibility": score,
        "shared_artists": [],
    }
    if user.share_artists and other.share_artists:
        card["shared_artists"] = shared_artists(db, user.id, other.id)
    return card


@router.get("/candidates")
def candidates(user: User = Depends(current_user), db: Session = Depends(get_db)):
    """People you haven't liked or passed yet, best music match first."""
    seen = {row.to_user_id for row in db.query(Like.to_user_id).filter(Like.from_user_id == user.id)}
    others = [
        other
        for other in db.query(User).filter(User.id != user.id).all()
        if other.id not in seen and is_interested(user, other) and is_interested(other, user)
    ]
    scores = compatibility(db, user.id, [o.id for o in others])
    others.sort(key=lambda o: scores[o.id], reverse=True)
    return [card_json(db, user, o, scores[o.id]) for o in others[:20]]


def record(db: Session, user: User, other_id: int, liked: bool) -> dict:
    if other_id == user.id or db.get(User, other_id) is None:
        raise HTTPException(404, "User not found.")
    existing = db.query(Like).filter(Like.from_user_id == user.id, Like.to_user_id == other_id).first()
    if existing:
        existing.liked = liked
    else:
        db.add(Like(from_user_id=user.id, to_user_id=other_id, liked=liked))
    db.commit()

    is_match = liked and db.query(Like).filter(
        Like.from_user_id == other_id, Like.to_user_id == user.id, Like.liked.is_(True)
    ).first() is not None
    return {"match": is_match}


@router.post("/candidates/{other_id}/like")
def like(other_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    return record(db, user, other_id, liked=True)


@router.post("/candidates/{other_id}/pass")
def pass_(other_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    return record(db, user, other_id, liked=False)


@router.get("/matches")
def matches(user: User = Depends(current_user), db: Session = Depends(get_db)):
    """People where both of you pressed like, best music match first."""
    i_liked = {r.to_user_id for r in db.query(Like.to_user_id).filter(Like.from_user_id == user.id, Like.liked)}
    liked_me = {r.from_user_id for r in db.query(Like.from_user_id).filter(Like.to_user_id == user.id, Like.liked)}
    others = db.query(User).filter(User.id.in_(i_liked & liked_me)).all()
    scores = compatibility(db, user.id, [o.id for o in others])
    others.sort(key=lambda o: scores[o.id], reverse=True)
    return [card_json(db, user, o, scores[o.id]) for o in others]

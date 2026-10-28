"""Reading and writing music profiles."""

from collections import Counter

from sqlalchemy.orm import Session

from app.models import utcnow
from app.music.models import MusicProfile


def save_top_artists(db: Session, user_id: int, top_artists: list[dict]) -> None:
    profile = db.get(MusicProfile, user_id)
    if profile is None:
        profile = MusicProfile(user_id=user_id)
        db.add(profile)
    profile.top_artists = top_artists
    profile.updated_at = utcnow()
    db.commit()


def load_profiles(db: Session, user_ids: list[int]) -> dict[int, list[dict]]:
    """Return {user_id: top_artists} for the given users."""
    rows = db.query(MusicProfile).filter(MusicProfile.user_id.in_(user_ids)).all()
    return {row.user_id: row.top_artists for row in rows}


def get_taste_summary(db: Session, user_id: int) -> dict:
    """A user's own music summary, shown only to that user on their profile page."""
    artists = load_profiles(db, [user_id]).get(user_id, [])
    genre_counts = Counter(g for artist in artists for g in artist.get("genres", []))
    return {
        "top_artists": [a["name"] for a in artists[:10]],
        "top_genres": [g for g, _ in genre_counts.most_common(8)],
        "artist_count": len(artists),
    }

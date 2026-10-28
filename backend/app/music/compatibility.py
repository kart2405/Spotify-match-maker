"""Music compatibility between two users.

Rung 1 of the algorithm ladder (see PLAN.md): 60% genre overlap + 40% artist overlap,
each measured with Jaccard similarity (shared items / all items either person has).
"""

from sqlalchemy.orm import Session

from app.music.store import load_profiles

GENRE_WEIGHT = 0.6
ARTIST_WEIGHT = 0.4


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def score_profiles(artists_a: list[dict], artists_b: list[dict]) -> int:
    """Compatibility percentage (0-100) between two lists of top artists."""
    names_a = {a["name"].lower() for a in artists_a}
    names_b = {a["name"].lower() for a in artists_b}
    genres_a = {g for a in artists_a for g in a.get("genres", [])}
    genres_b = {g for a in artists_b for g in a.get("genres", [])}

    score = GENRE_WEIGHT * jaccard(genres_a, genres_b) + ARTIST_WEIGHT * jaccard(names_a, names_b)
    return round(score * 100)


def compatibility(db: Session, user_id: int, other_ids: list[int]) -> dict[int, int]:
    """Return {other_id: percentage} for how well user_id matches each of other_ids."""
    profiles = load_profiles(db, [user_id, *other_ids])
    mine = profiles.get(user_id, [])
    return {other: score_profiles(mine, profiles.get(other, [])) for other in other_ids}


def shared_artists(db: Session, user_id: int, other_id: int, limit: int = 3) -> list[str]:
    """Artists both users listen to, in user_id's order of preference."""
    profiles = load_profiles(db, [user_id, other_id])
    theirs = {a["name"].lower() for a in profiles.get(other_id, [])}
    return [a["name"] for a in profiles.get(user_id, []) if a["name"].lower() in theirs][:limit]

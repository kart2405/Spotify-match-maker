"""Create fake test users with realistic music taste.

Run from the backend folder:  python -m app.seed
Running it again wipes the fake users and creates them fresh.
"""

import random

from app.database import Base, SessionLocal, engine
from app.models import Like, User
from app.music.models import MusicProfile
from app.music.compatibility import score_profiles
from app.music.store import save_top_artists
from app.auth import DEMO_USER_SPOTIFY_ID

# Artists grouped by taste "scene", with Spotify-style genres.
SCENES = {
    "indie": [
        ("Phoebe Bridgers", ["indie pop", "indie folk"]),
        ("Arctic Monkeys", ["indie rock", "garage rock"]),
        ("Tame Impala", ["psychedelic rock", "indie rock"]),
        ("Mitski", ["indie pop", "art pop"]),
        ("Bon Iver", ["indie folk", "chamber pop"]),
        ("The Strokes", ["indie rock", "garage rock"]),
        ("Clairo", ["bedroom pop", "indie pop"]),
        ("Fleet Foxes", ["indie folk", "chamber pop"]),
        ("Mac DeMarco", ["slacker rock", "indie pop"]),
        ("boygenius", ["indie rock", "indie folk"]),
    ],
    "hiphop": [
        ("Kendrick Lamar", ["hip hop", "west coast hip hop", "conscious hip hop"]),
        ("J. Cole", ["hip hop", "conscious hip hop"]),
        ("Tyler, The Creator", ["hip hop", "alternative hip hop"]),
        ("Travis Scott", ["rap", "trap"]),
        ("Kanye West", ["hip hop", "rap"]),
        ("Little Simz", ["uk hip hop", "alternative hip hop"]),
        ("Mac Miller", ["hip hop", "alternative hip hop"]),
        ("Doja Cat", ["rap", "dance pop"]),
        ("Dave", ["uk hip hop", "rap"]),
        ("Anderson .Paak", ["hip hop", "neo soul"]),
    ],
    "rnb": [
        ("Frank Ocean", ["r&b", "neo soul"]),
        ("SZA", ["r&b", "pop"]),
        ("Daniel Caesar", ["r&b", "neo soul"]),
        ("H.E.R.", ["r&b"]),
        ("Steve Lacy", ["r&b", "bedroom pop"]),
        ("Jorja Smith", ["uk r&b", "neo soul"]),
        ("Erykah Badu", ["neo soul", "r&b"]),
        ("Brent Faiyaz", ["r&b"]),
        ("Solange", ["r&b", "art pop"]),
    ],
    "pop": [
        ("Taylor Swift", ["pop"]),
        ("Dua Lipa", ["dance pop", "pop"]),
        ("Harry Styles", ["pop"]),
        ("Olivia Rodrigo", ["pop", "pop rock"]),
        ("Billie Eilish", ["pop", "art pop"]),
        ("Sabrina Carpenter", ["pop"]),
        ("Charli xcx", ["dance pop", "hyperpop"]),
        ("Chappell Roan", ["pop", "indie pop"]),
        ("The Weeknd", ["pop", "r&b"]),
    ],
    "electronic": [
        ("Fred again..", ["house", "electronica"]),
        ("Disclosure", ["house", "uk garage"]),
        ("Bonobo", ["downtempo", "electronica"]),
        ("ODESZA", ["electronica", "chillwave"]),
        ("Four Tet", ["electronica", "house"]),
        ("Jamie xx", ["electronica", "uk garage"]),
        ("Kaytranada", ["house", "electronic r&b"]),
        ("Caribou", ["electronica", "indietronica"]),
        ("Daft Punk", ["french house", "electronica"]),
    ],
    "rock": [
        ("Foo Fighters", ["alternative rock", "rock"]),
        ("Radiohead", ["alternative rock", "art rock"]),
        ("Queens of the Stone Age", ["stoner rock", "alternative rock"]),
        ("Fleetwood Mac", ["classic rock", "soft rock"]),
        ("Led Zeppelin", ["classic rock", "hard rock"]),
        ("Paramore", ["pop punk", "alternative rock"]),
        ("Red Hot Chili Peppers", ["alternative rock", "funk rock"]),
        ("Nirvana", ["grunge", "alternative rock"]),
        ("The Black Keys", ["blues rock", "garage rock"]),
    ],
    "jazz": [
        ("Norah Jones", ["vocal jazz", "jazz pop"]),
        ("Kamasi Washington", ["jazz", "spiritual jazz"]),
        ("Miles Davis", ["jazz", "cool jazz"]),
        ("Robert Glasper", ["jazz", "neo soul"]),
        ("Nina Simone", ["vocal jazz", "soul"]),
        ("BADBADNOTGOOD", ["jazz", "instrumental hip hop"]),
        ("Snarky Puppy", ["jazz fusion"]),
        ("Laufey", ["vocal jazz", "bedroom pop"]),
    ],
    "latin": [
        ("Bad Bunny", ["reggaeton", "latin trap"]),
        ("Rosalía", ["flamenco pop", "latin pop"]),
        ("Karol G", ["reggaeton", "latin pop"]),
        ("J Balvin", ["reggaeton"]),
        ("Kali Uchis", ["latin r&b", "neo soul"]),
        ("Peso Pluma", ["corridos tumbados"]),
        ("Rauw Alejandro", ["reggaeton", "latin pop"]),
    ],
}

PEOPLE = [
    ("Maya", "woman"), ("Liam", "man"), ("Aisha", "woman"), ("Noah", "man"), ("Sofia", "woman"),
    ("Ethan", "man"), ("Priya", "woman"), ("Lucas", "man"), ("Zara", "woman"), ("Oliver", "man"),
    ("Chloe", "woman"), ("Mateo", "man"), ("Hana", "woman"), ("Arjun", "man"), ("Isla", "woman"),
    ("Kai", "man"), ("Amara", "woman"), ("Leo", "man"), ("Nina", "woman"), ("Theo", "man"),
    ("Freya", "woman"), ("Omar", "man"), ("Lucia", "woman"), ("Ravi", "man"), ("Ella", "woman"),
    ("Jonah", "man"), ("Mei", "woman"), ("Samir", "man"), ("Ruby", "woman"), ("Diego", "man"),
    ("Ivy", "woman"), ("Felix", "man"), ("Yara", "woman"), ("Hugo", "man"), ("Leila", "woman"),
    ("Finn", "man"), ("Ana", "woman"), ("Kofi", "man"), ("Grace", "woman"), ("Ben", "man"),
    ("Sky", "nonbinary"), ("River", "nonbinary"), ("Alex", "nonbinary"), ("Jules", "nonbinary"),
    ("Nadia", "woman"), ("Marco", "man"), ("Tara", "woman"), ("Sam", "nonbinary"),
]

CITIES = ["London", "Manchester", "Bristol", "Edinburgh", "Brighton", "Leeds", "Glasgow", "Cardiff"]

BIOS = [
    "Will make you a playlist before our second date.",
    "Sunday mornings, long walks, and loud choruses.",
    "Gig regular. Always near the front.",
    "Trying every coffee shop in the city, one album at a time.",
    "Hiking in the day, vinyl at night.",
    "Plant parent. Shower singer. Festival planner.",
    "Ask me about the best album nobody has heard of.",
    "Can cook, can't dance, will try anyway.",
    "Road trips need a good soundtrack, and I've got one.",
    "Looking for someone to share headphones with.",
    "Bookshops, sunsets, and a song for every mood.",
    "My friends call me the aux cord dictator.",
]


def make_taste(rng: random.Random, scenes: list[str]) -> list[dict]:
    """Pick ~15 artists, mostly from the first scene, ordered favourite first."""
    picks = []
    for i, scene in enumerate(scenes):
        pool = SCENES[scene]
        count = min(len(pool), rng.randint(6, 9) if i == 0 else rng.randint(2, 5))
        picks += rng.sample(pool, count)
    rng.shuffle(picks)
    return [{"name": name, "genres": genres} for name, genres in picks]


def interest_for(rng: random.Random, gender: str) -> str:
    if gender == "man":
        return rng.choices(["women", "men", "everyone"], [6, 2, 2])[0]
    if gender == "woman":
        return rng.choices(["men", "women", "everyone"], [6, 2, 2])[0]
    return "everyone"


def seed(rng_seed: int = 7) -> None:
    rng = random.Random(rng_seed)
    Base.metadata.create_all(engine)
    db = SessionLocal()

    # Wipe old fake users (and the demo user), plus their likes and music.
    old_ids = [u.id for u in db.query(User).filter(User.is_fake.is_(True))]
    db.query(Like).filter(Like.from_user_id.in_(old_ids) | Like.to_user_id.in_(old_ids)).delete()
    db.query(MusicProfile).filter(MusicProfile.user_id.in_(old_ids)).delete()
    db.query(User).filter(User.id.in_(old_ids)).delete()
    db.commit()

    scene_names = list(SCENES)
    users, tastes = [], {}

    demo = User(
        spotify_id=DEMO_USER_SPOTIFY_ID, name="You (demo)", age=27, city="London", gender="woman",
        interested_in="everyone", bio="This is the demo account. Edit me on the Profile page!", is_fake=True,
    )
    db.add(demo)
    db.commit()
    tastes[demo.id] = make_taste(rng, ["indie", "rnb", "electronic"])
    users.append(demo)

    for name, gender in PEOPLE:
        user = User(
            name=name, age=rng.randint(21, 36), city=rng.choice(CITIES), gender=gender,
            interested_in=interest_for(rng, gender), bio=rng.choice(BIOS), is_fake=True,
            share_artists=rng.random() > 0.15,
        )
        db.add(user)
        db.commit()
        tastes[user.id] = make_taste(rng, rng.sample(scene_names, rng.choice([1, 2, 2, 3])))
        users.append(user)

    for user in users:
        save_top_artists(db, user.id, tastes[user.id])

    # Fake users like each other, more often when their music matches.
    from app.dating import is_interested

    for user in users[1:]:
        for other in users:
            if other.id == user.id or not is_interested(user, other):
                continue
            chance = 0.2 + score_profiles(tastes[user.id], tastes[other.id]) / 100
            if other is demo:
                chance += 0.2  # so the demo account gets some matches to show
            if rng.random() < chance:
                db.add(Like(from_user_id=user.id, to_user_id=other.id, liked=True))
    db.commit()
    db.close()
    print(f"Created {len(users)} fake users (including the demo account).")


if __name__ == "__main__":
    seed()

"""The music module: the privacy boundary around users' listening data.

Only this package talks to Spotify and reads raw listening data. The rest of the app
should import only what is listed in __all__.
"""

from app.music.compatibility import compatibility, shared_artists
from app.music.store import get_taste_summary

__all__ = ["compatibility", "shared_artists", "get_taste_summary"]

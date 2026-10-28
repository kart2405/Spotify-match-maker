# Plan

## The idea

A dating website where people are matched by how similar their music taste is.

**Privacy rule:** raw listening data (your top artists and genres) lives only inside the
`music` module of the backend. The dating side of the app can only ask
"how compatible are user A and user B?" and gets back a percentage. Shared artists are
shown on a profile card only when both people have opted in.

## Build steps

1. **Spotify login + profile + database.** "Log in with Spotify" creates the account and
   pulls the user's top artists and genres in one go. Users add age, bio and who they're
   interested in.
2. **Fake test users + `compatibility()`.** A seed script creates ~50 realistic fake users
   so matching can be tested without real sign-ups (Spotify allows only 25 testers in
   development mode).
3. **Dating flow.** Browse candidates sorted by compatibility, like or pass, and a mutual
   like becomes a match.
4. **Safety, chat, deploy.** 18+ check, block and report, messaging between matches.
   Then deploy: frontend on Netlify, backend on Render, database on Supabase.

## Algorithm ladder

Each rung only changes the inside of `compatibility()`; nothing else in the app changes.

1. **Basic** (current): 60% genre overlap + 40% artist overlap (Jaccard similarity).
2. **Weighted:** your #1 artist counts more than your #50; rare shared artists count more
   than popular ones.
3. **Taste fingerprint:** compare genre mixes as vectors and use related artists, so people
   with no exact overlap can still match.
4. **Learning:** blend in mutual preferences and learn from who actually likes whom.

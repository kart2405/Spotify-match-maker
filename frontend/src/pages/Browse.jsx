import { useEffect, useState } from 'react'
import { api } from '../api.js'
import Avatar from '../components/Avatar.jsx'
import ProfileCard from '../components/ProfileCard.jsx'

export default function Browse({ onGoToMatches }) {
  const [people, setPeople] = useState(null)
  const [error, setError] = useState('')
  const [newMatch, setNewMatch] = useState(null)
  const [busy, setBusy] = useState(false)

  function load() {
    api('/candidates').then(setPeople).catch((e) => setError(e.message))
  }

  useEffect(load, [])

  async function decide(person, action) {
    setBusy(true)
    try {
      const result = await api(`/candidates/${person.id}/${action}`, { method: 'POST' })
      if (result.match) setNewMatch(person)
      const rest = people.slice(1)
      setPeople(rest)
      if (rest.length === 0) load()
    } catch (e) {
      setError(e.message)
    } finally {
      setBusy(false)
    }
  }

  if (error) return <p className="notice notice--coral">{error}</p>
  if (people === null) return <p className="muted center">Tuning in…</p>

  const person = people[0]

  return (
    <div className="browse">
      <div className="page-head">
        <h1>Discover</h1>
        <p className="muted">Sorted by how well your music matches.</p>
      </div>

      {person ? (
        <ProfileCard key={person.id} person={person}>
          <div className="decide">
            <button className="btn btn--ghost btn--round" disabled={busy} onClick={() => decide(person, 'pass')}>
              ✕ Pass
            </button>
            <button className="btn btn--coral btn--round" disabled={busy} onClick={() => decide(person, 'like')}>
              ♥ Like
            </button>
          </div>
        </ProfileCard>
      ) : (
        <div className="card empty">
          <span className="step__icon">🌱</span>
          <h2>You&rsquo;ve seen everyone for now</h2>
          <p className="muted">New people join all the time. Check back soon, or see your matches.</p>
          <button className="btn btn--leaf" onClick={onGoToMatches}>See my matches</button>
        </div>
      )}

      {newMatch && (
        <div className="modal-backdrop" onClick={() => setNewMatch(null)}>
          <div className="card modal" role="dialog" aria-label="It's a match" onClick={(e) => e.stopPropagation()}>
            <p className="eyebrow">It&rsquo;s a match!</p>
            <Avatar id={newMatch.id} name={newMatch.name} size={110} />
            <h2>You and {newMatch.name} liked each other</h2>
            <p className="muted">{newMatch.compatibility}% music match</p>
            <div className="decide">
              <button className="btn btn--ghost" onClick={() => setNewMatch(null)}>Keep browsing</button>
              <button className="btn btn--leaf" onClick={onGoToMatches}>See matches</button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

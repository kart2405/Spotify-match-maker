import { useEffect, useState } from 'react'
import { api } from '../api.js'
import ProfileCard from '../components/ProfileCard.jsx'

export default function Matches({ onGoToBrowse }) {
  const [matches, setMatches] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    api('/matches').then(setMatches).catch((e) => setError(e.message))
  }, [])

  if (error) return <p className="notice notice--coral">{error}</p>
  if (matches === null) return <p className="muted center">Loading your matches…</p>

  return (
    <div>
      <div className="page-head">
        <h1>Your matches</h1>
        <p className="muted">People who liked you back. Chat is coming soon.</p>
      </div>
      {matches.length === 0 ? (
        <div className="card empty">
          <span className="step__icon">🌼</span>
          <h2>No matches yet</h2>
          <p className="muted">Like a few people and your matches will bloom here.</p>
          <button className="btn btn--leaf" onClick={onGoToBrowse}>Start discovering</button>
        </div>
      ) : (
        <div className="grid">
          {matches.map((person) => (
            <ProfileCard key={person.id} person={person} compact />
          ))}
        </div>
      )}
    </div>
  )
}

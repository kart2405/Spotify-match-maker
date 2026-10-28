import Avatar from './Avatar.jsx'
import { compatLabel } from '../compat.js'
import CompatRing from './CompatRing.jsx'

export default function ProfileCard({ person, compact = false, children }) {
  return (
    <article className={`card profile-card${compact ? ' profile-card--compact' : ''}`}>
      <header className="profile-card__head">
        <Avatar id={person.id} name={person.name} size={compact ? 64 : 96} />
        <div className="profile-card__who">
          <h2>
            {person.name}
            {person.age ? <span className="age">, {person.age}</span> : null}
          </h2>
          {person.city && <p className="city">{person.city}</p>}
          <p className="compat-label">{compatLabel(person.compatibility)}</p>
        </div>
        <CompatRing score={person.compatibility} size={compact ? 64 : 88} />
      </header>

      {person.bio && <p className="bio">{person.bio}</p>}

      {person.shared_artists.length > 0 && (
        <div className="shared">
          <p className="eyebrow">You both love</p>
          <ul className="chips">
            {person.shared_artists.map((artist) => (
              <li key={artist} className="chip chip--green">♪ {artist}</li>
            ))}
          </ul>
        </div>
      )}

      {children}
    </article>
  )
}

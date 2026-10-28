import { useState } from 'react'
import { api } from '../api.js'
import Avatar from '../components/Avatar.jsx'

export default function Profile({ me, onSaved, welcome }) {
  const [form, setForm] = useState({
    name: me.name,
    age: me.age ?? '',
    city: me.city,
    bio: me.bio,
    gender: me.gender,
    interested_in: me.interested_in,
    share_artists: me.share_artists,
  })
  const [status, setStatus] = useState('')

  function set(field) {
    return (e) => setForm({ ...form, [field]: e.target.type === 'checkbox' ? e.target.checked : e.target.value })
  }

  async function save(e) {
    e.preventDefault()
    setStatus('')
    try {
      const updated = await api('/me', { method: 'PATCH', body: { ...form, age: Number(form.age) } })
      onSaved(updated)
      setStatus('saved')
    } catch (err) {
      setStatus(err.status === 422 ? 'Please check your details. You must be 18 or older.' : err.message)
    }
  }

  return (
    <div className="profile">
      <div className="page-head">
        <h1>Your profile</h1>
        {welcome && (
          <p className="notice notice--sun">Welcome! Add a few details so we can start finding your matches.</p>
        )}
      </div>

      <div className="profile__layout">
        <form className="card form" onSubmit={save}>
          <div className="form__avatar">
            <Avatar id={me.id} name={form.name || '?'} size={80} />
          </div>
          <label>
            Name
            <input value={form.name} onChange={set('name')} required maxLength={100} />
          </label>
          <div className="form__row">
            <label>
              Age
              <input type="number" min="18" max="120" value={form.age} onChange={set('age')} required />
            </label>
            <label>
              City
              <input value={form.city} onChange={set('city')} maxLength={100} />
            </label>
          </div>
          <div className="form__row">
            <label>
              I am a
              <select value={form.gender} onChange={set('gender')} required>
                <option value="" disabled>Choose…</option>
                <option value="woman">Woman</option>
                <option value="man">Man</option>
                <option value="nonbinary">Non-binary</option>
              </select>
            </label>
            <label>
              Interested in
              <select value={form.interested_in} onChange={set('interested_in')}>
                <option value="everyone">Everyone</option>
                <option value="women">Women</option>
                <option value="men">Men</option>
              </select>
            </label>
          </div>
          <label>
            About me
            <textarea rows="3" value={form.bio} onChange={set('bio')} maxLength={500} />
          </label>
          <label className="check">
            <input type="checkbox" checked={form.share_artists} onChange={set('share_artists')} />
            Show artists we both love on my card
          </label>
          <div className="form__actions">
            <button className="btn btn--leaf" type="submit">Save profile</button>
            {status === 'saved' ? <span className="saved">✓ Saved</span> : status && <span className="error">{status}</span>}
          </div>
        </form>

        <aside className="card music">
          <p className="eyebrow">Your music · only you can see this</p>
          {me.music.artist_count === 0 ? (
            <p className="muted">No music data yet. Log in with Spotify to import your top artists.</p>
          ) : (
            <>
              <h3>Top artists</h3>
              <ol className="artists">
                {me.music.top_artists.map((a) => (
                  <li key={a}>{a}</li>
                ))}
              </ol>
              <h3>Top genres</h3>
              <ul className="chips">
                {me.music.top_genres.map((g, i) => (
                  <li key={g} className={`chip chip--${['sky', 'sun', 'coral', 'lavender', 'leaf'][i % 5]}`}>{g}</li>
                ))}
              </ul>
            </>
          )}
        </aside>
      </div>
    </div>
  )
}

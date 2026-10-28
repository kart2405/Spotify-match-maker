import { useEffect, useState } from 'react'
import { api } from './api.js'
import Browse from './pages/Browse.jsx'
import Landing from './pages/Landing.jsx'
import Matches from './pages/Matches.jsx'
import Profile from './pages/Profile.jsx'

const params = new URLSearchParams(window.location.search)
const START_ERROR = params.get('error') === 'spotify' ? 'Spotify login didn’t go through. Please try again.' : ''
const WELCOME = params.has('welcome')
if (window.location.search) window.history.replaceState(null, '', window.location.pathname)

const TABS = [
  ['browse', 'Discover'],
  ['matches', 'Matches'],
  ['profile', 'Profile'],
]

function App() {
  const [config, setConfig] = useState(null)
  const [me, setMe] = useState(undefined) // undefined = loading, null = logged out
  const [page, setPage] = useState('browse')
  const [error, setError] = useState(START_ERROR)

  useEffect(() => {
    api('/config')
      .then(setConfig)
      .catch(() => setError('Can’t reach the backend. Is it running on port 8000?'))
    api('/me')
      .then((user) => {
        setMe(user)
        if (!user.age || !user.gender) setPage('profile')
      })
      .catch(() => setMe(null))
  }, [])

  async function startDemo() {
    try {
      await api('/auth/demo', { method: 'POST' })
      setMe(await api('/me'))
      setPage('browse')
    } catch (e) {
      setError(e.message)
    }
  }

  async function logout() {
    await api('/auth/logout', { method: 'POST' })
    setMe(null)
  }

  return (
    <div className="app">
      <nav className="nav">
        <span className="logo">
          <span className="logo__mark">🌿</span> Match Maker
        </span>
        {me && (
          <div className="nav__tabs">
            {TABS.map(([key, label]) => (
              <button
                key={key}
                className={`nav__tab${page === key ? ' nav__tab--active' : ''}`}
                onClick={() => setPage(key)}
              >
                {label}
              </button>
            ))}
            <button className="nav__tab nav__tab--quiet" onClick={logout}>Log out</button>
          </div>
        )}
      </nav>

      <main className="main">
        {me === undefined || (!me && !config && !error) ? (
          <p className="muted center">Tuning in…</p>
        ) : !me ? (
          <Landing config={config ?? {}} onDemo={startDemo} error={error} />
        ) : page === 'browse' ? (
          <Browse onGoToMatches={() => setPage('matches')} />
        ) : page === 'matches' ? (
          <Matches onGoToBrowse={() => setPage('browse')} />
        ) : (
          <Profile me={me} onSaved={setMe} welcome={WELCOME || !me.age} />
        )}
      </main>

      <footer className="footer muted">Made with music 🎶 · Your listening data is never shown to other people.</footer>
    </div>
  )
}

export default App

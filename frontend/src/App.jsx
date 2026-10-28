import { useEffect, useState } from 'react'

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

function App() {
  const [backendMessage, setBackendMessage] = useState('Connecting to backend...')

  useEffect(() => {
    fetch(`${API_URL}/api/health`)
      .then((res) => res.json())
      .then((data) => setBackendMessage(data.message))
      .catch(() => setBackendMessage('Could not reach the backend. Is it running on port 8000?'))
  }, [])

  return (
    <main>
      <h1>Spotify Match Maker</h1>
      <p>Find people who share your music taste.</p>
      <p className="status">{backendMessage}</p>
    </main>
  )
}

export default App

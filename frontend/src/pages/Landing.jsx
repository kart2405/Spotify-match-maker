import { spotifyLoginUrl } from '../api.js'

export default function Landing({ config, onDemo, error }) {
  return (
    <div className="landing">
      <section className="hero">
        <p className="eyebrow">Music-matched dating</p>
        <h1>
          Find someone who <em>hears the world</em> the way you do.
        </h1>
        <p className="lead">
          Connect your Spotify, and we&rsquo;ll introduce you to people whose music taste
          harmonises with yours, scored from 0 to 100%.
        </p>

        {error && <p className="notice notice--coral">{error}</p>}

        <div className="hero__actions">
          {config.spotify_enabled ? (
            <a className="btn btn--leaf btn--lg" href={spotifyLoginUrl}>
              Log in with Spotify
            </a>
          ) : (
            <span className="btn btn--leaf btn--lg btn--disabled" title="Add Spotify keys to backend/.env to turn this on">
              Log in with Spotify (coming soon)
            </span>
          )}
          {config.demo_mode && (
            <button className="btn btn--ghost btn--lg" onClick={onDemo}>
              Try the demo
            </button>
          )}
        </div>
      </section>

      <section className="steps">
        <div className="card step step--sky">
          <span className="step__icon">🎧</span>
          <h3>Connect your music</h3>
          <p>One Spotify login creates your account and reads your top artists. No passwords.</p>
        </div>
        <div className="card step step--sun">
          <span className="step__icon">🌻</span>
          <h3>We compare, privately</h3>
          <p>Your listening data stays in our music engine. Others only see a match percentage.</p>
        </div>
        <div className="card step step--coral">
          <span className="step__icon">💌</span>
          <h3>Match and meet</h3>
          <p>Like the people you vibe with. When it&rsquo;s mutual, it&rsquo;s a match.</p>
        </div>
      </section>
    </div>
  )
}

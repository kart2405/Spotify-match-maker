import { spotifyLoginUrl } from '../api.js'

export default function Landing({ config, onDemo, error }) {
  return (
    <div className="landing">
      <section className="hero">
        <p className="eyebrow">Music-matched dating</p>
        <p className="ornament" aria-hidden="true">❦</p>
        <h1>
          Find someone who <em>hears the world</em> the way you do.
        </h1>
        <p className="lead">
          Connect your Spotify, and we&rsquo;ll introduce you to people whose music taste
          harmonises with yours, scored from 0 to 100%.
        </p>

        {error && <p className="notice notice--error">{error}</p>}

        <div className="hero__actions">
          {config.spotify_enabled ? (
            <a className="btn btn--primary btn--lg" href={spotifyLoginUrl}>
              Log in with Spotify
            </a>
          ) : (
            <span className="btn btn--primary btn--lg btn--disabled" title="Add Spotify keys to backend/.env to turn this on">
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

      <section className="steps" aria-label="How it works">
        <div className="card step">
          <span className="step__num">I</span>
          <h3>Connect your music</h3>
          <p>One Spotify login creates your account and reads your top artists. No passwords.</p>
        </div>
        <div className="card step">
          <span className="step__num">II</span>
          <h3>We compare, privately</h3>
          <p>Your listening data stays in our music engine. Others only see a match percentage.</p>
        </div>
        <div className="card step">
          <span className="step__num">III</span>
          <h3>Match and meet</h3>
          <p>Like the people you vibe with. When it&rsquo;s mutual, it&rsquo;s a match.</p>
        </div>
      </section>
    </div>
  )
}

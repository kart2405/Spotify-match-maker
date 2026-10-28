import { compatLabel } from '../compat.js'

export default function CompatRing({ score, size = 88 }) {
  return (
    <div
      className="compat-ring"
      style={{ width: size, height: size, '--score': score }}
      title={`${score}% music match: ${compatLabel(score)}`}
    >
      <div className="compat-ring__inner">
        <strong>{score}%</strong>
        <span>match</span>
      </div>
    </div>
  )
}

// Cameo portrait tones: sepia, Bordeaux, verdigris, zinc, dusty rose, gilt.
const GRADIENTS = [
  ['#ead7b6', '#a07548'], // sepia
  ['#e9bdb7', '#7b2233'], // Bordeaux
  ['#c9dccf', '#3f6b5c'], // verdigris
  ['#d5dbe3', '#56667a'], // zinc rooftops
  ['#f0d3cb', '#b9746b'], // dusty rose
  ['#efe0b2', '#a8842f'], // gilt
]

export default function Avatar({ id, name, size = 96 }) {
  const [from, to] = GRADIENTS[id % GRADIENTS.length]
  return (
    <div
      className="avatar"
      style={{
        width: size,
        height: Math.round(size * 1.18),
        fontSize: size * 0.4,
        background: `linear-gradient(135deg, ${from}, ${to})`,
      }}
      aria-hidden="true"
    >
      {name.charAt(0)}
    </div>
  )
}

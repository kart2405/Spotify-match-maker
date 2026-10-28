// Soft nature gradients; each person gets one based on their id.
const GRADIENTS = [
  ['#9fd8b5', '#4c9a6a'], // meadow
  ['#ffd88a', '#f4a259'], // sunflower
  ['#a9d4ef', '#5b9fd0'], // sky
  ['#ffb8a1', '#ec7b5c'], // coral
  ['#cdbdf0', '#8f78cf'], // lavender
  ['#b8e3d9', '#3f9c8c'], // lagoon
]

export default function Avatar({ id, name, size = 96 }) {
  const [from, to] = GRADIENTS[id % GRADIENTS.length]
  return (
    <div
      className="avatar"
      style={{
        width: size,
        height: size,
        fontSize: size * 0.4,
        background: `linear-gradient(135deg, ${from}, ${to})`,
      }}
      aria-hidden="true"
    >
      {name.charAt(0)}
    </div>
  )
}

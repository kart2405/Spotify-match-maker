export function compatLabel(score) {
  if (score >= 40) return 'In perfect tune'
  if (score >= 25) return 'Great harmony'
  if (score >= 12) return 'Some shared notes'
  return 'Different playlists'
}

import type { Container, Cylinder } from '../types'

export interface ParsedInstance {
  container: Container
  cylinders: Cylinder[]
}

export function parseInstanceFile(text: string): ParsedInstance | null {
  const lines = text.split('\n').filter(line => {
    const trimmed = line.trim()
    return trimmed && !trimmed.startsWith('#')
  })

  let container: Container | null = null
  const cylinders: Cylinder[] = []

  for (const line of lines) {
    const parts = line.trim().split(/\s+/)

    if (parts[0] === 'container') {
      container = {
        width: parseFloat(parts[1]),
        depth: parseFloat(parts[2]),
        max_weight: parseFloat(parts[3])
      }
    } else if (parts[0] === 'cylinder') {
      cylinders.push({
        diameter: parseFloat(parts[1]),
        weight: parseFloat(parts[2])
      })
    }
  }

  if (!container || cylinders.length === 0) {
    return null
  }

  return { container, cylinders }
}
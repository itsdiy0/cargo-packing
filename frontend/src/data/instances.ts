import type { Container, Cylinder } from '../types'

export interface PresetInstance {
  id: string
  name: string
  container: Container
  cylinders: Cylinder[]
  difficulty: 'easy' | 'medium' | 'hard'
}

export const PRESET_INSTANCES: PresetInstance[] = [
  {
    id: 'simple-4',
    name: 'Simple (4 cylinders)',
    difficulty: 'easy',
    container: { width: 20, depth: 15, max_weight: 1000 },
    cylinders: [
      { diameter: 2.0, weight: 100 },
      { diameter: 2.0, weight: 100 },
      { diameter: 2.0, weight: 100 },
      { diameter: 2.0, weight: 100 }
    ]
  },
  {
    id: 'medium-6',
    name: 'Medium (6 cylinders)',
    difficulty: 'medium',
    container: { width: 20, depth: 15, max_weight: 1500 },
    cylinders: [
      { diameter: 3.0, weight: 200 },
      { diameter: 2.5, weight: 150 },
      { diameter: 2.0, weight: 100 },
      { diameter: 2.0, weight: 100 },
      { diameter: 1.5, weight: 80 },
      { diameter: 1.5, weight: 80 }
    ]
  },
  {
    id: 'challenging-8',
    name: 'Challenging (8 cylinders)',
    difficulty: 'hard',
    container: { width: 15, depth: 12, max_weight: 2000 },
    cylinders: [
      { diameter: 3.0, weight: 200 },
      { diameter: 2.5, weight: 150 },
      { diameter: 2.5, weight: 150 },
      { diameter: 2.0, weight: 100 },
      { diameter: 2.0, weight: 100 },
      { diameter: 2.0, weight: 100 },
      { diameter: 1.5, weight: 80 },
      { diameter: 1.5, weight: 80 }
    ]
  },
  {
    id: 'challenging-10',
    name: 'Challenging (10 cylinders)',
    difficulty: 'hard',
    container: { width: 15, depth: 12, max_weight: 1800 },
    cylinders: [
      { diameter: 2.5, weight: 150 },
      { diameter: 2.2, weight: 120 },
      { diameter: 2.0, weight: 100 },
      { diameter: 2.0, weight: 100 },
      { diameter: 1.8, weight: 90 },
      { diameter: 1.8, weight: 90 },
      { diameter: 1.5, weight: 80 },
      { diameter: 1.5, weight: 80 },
      { diameter: 1.2, weight: 60 },
      { diameter: 1.0, weight: 50 }
    ]
  },
  {
    id: 'very-tight-12',
    name: 'Very Tight (12 cylinders)',
    difficulty: 'hard',
    container: { width: 12, depth: 10, max_weight: 1500 },
    cylinders: [
      { diameter: 2.5, weight: 140 },
      { diameter: 2.2, weight: 120 },
      { diameter: 2.0, weight: 100 },
      { diameter: 2.0, weight: 100 },
      { diameter: 1.8, weight: 90 },
      { diameter: 1.8, weight: 90 },
      { diameter: 1.5, weight: 75 },
      { diameter: 1.5, weight: 75 },
      { diameter: 1.2, weight: 60 },
      { diameter: 1.0, weight: 50 },
      { diameter: 1.0, weight: 50 },
      { diameter: 1.0, weight: 50 }
    ]
  },
  {
    id: 'large-mix-10',
    name: 'Large & Small Mix (10 cylinders)',
    difficulty: 'hard',
    container: { width: 16, depth: 12, max_weight: 2200 },
    cylinders: [
      { diameter: 4.0, weight: 300 },
      { diameter: 3.5, weight: 250 },
      { diameter: 3.0, weight: 200 },
      { diameter: 2.5, weight: 150 },
      { diameter: 2.0, weight: 100 },
      { diameter: 2.0, weight: 100 },
      { diameter: 1.5, weight: 80 },
      { diameter: 1.5, weight: 80 },
      { diameter: 1.0, weight: 50 },
      { diameter: 1.0, weight: 50 }
    ]
  }
]
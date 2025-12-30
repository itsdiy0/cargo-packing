export interface Container {
    width: number
    depth: number
    max_weight: number
  }
  
  export interface Cylinder {
    diameter: number
    weight: number
  }
  
  export interface PlacedCylinder {
    id: number
    x: number
    y: number
    diameter: number
    radius: number
    weight: number
  }
  
  export interface SolutionDetails {
    valid: boolean
    center_of_mass: [number, number]
    packing_density: number
    cylinders: PlacedCylinder[]
  }
  
  export interface Solution {
    algorithm: string
    solution: number[]
    fitness: number
    details: SolutionDetails
    generation_history?: GenerationStats[]
  }
  
  export interface GenerationStats {
    generation: number
    best: number
    avg: number
    worst?: number
  }
  
  export interface ProgressUpdate {
    generation: number
    best_fitness: number
    avg_fitness: number
    worst_fitness?: number
    solution?: {
      placement_order: number[]
      cylinders: PlacedCylinder[]
      center_of_mass: [number, number]
      packing_density: number
    }
  }
  
  export type Algorithm = 'genetic' | 'greedy' | 'random'
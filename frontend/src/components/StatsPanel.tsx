import type { Solution } from '../types'

interface StatsPanelProps {
  solution: Solution
}

export default function StatsPanel({ solution }: StatsPanelProps) {
  return (
    <section className="solution-stats">
      <h2>Solution Statistics</h2>
      <div className="stats-grid">
        <div className="stat-item">
          <span className="stat-label">Algorithm:</span>
          <span className="stat-value">{solution.algorithm}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Fitness:</span>
          <span className="stat-value">{solution.fitness.toFixed(2)}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Valid:</span>
          <span className={`stat-value ${solution.details.valid ? 'valid' : 'invalid'}`}>
            {solution.details.valid ? '✓ Yes' : '✗ No'}
          </span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Packing Density:</span>
          <span className="stat-value">
            {(solution.details.packing_density * 100).toFixed(2)}%
          </span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Center of Mass:</span>
          <span className="stat-value">
            ({solution.details.center_of_mass[0].toFixed(2)}, {solution.details.center_of_mass[1].toFixed(2)})
          </span>
        </div>
        <div className="stat-item full-width">
          <span className="stat-label">Placement Order:</span>
          <span className="stat-value order">
            {solution.solution.join(' → ')}
          </span>
        </div>
      </div>
    </section>
  )
}
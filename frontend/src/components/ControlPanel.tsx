import type { Container, Cylinder, Algorithm } from '../types'

interface ControlPanelProps {
  container: Container
  cylinders: Cylinder[]
  algorithm: Algorithm
  solving: boolean
  onUpdateContainer: (field: keyof Container, value: string) => void
  onAddCylinder: () => void
  onRemoveCylinder: (index: number) => void
  onUpdateCylinder: (index: number, field: keyof Cylinder, value: string) => void
  onAlgorithmChange: (algo: Algorithm) => void
  onSolve: () => void
}

export default function ControlPanel({
  container,
  cylinders,
  algorithm,
  solving,
  onUpdateContainer,
  onAddCylinder,
  onRemoveCylinder,
  onUpdateCylinder,
  onAlgorithmChange,
  onSolve
}: ControlPanelProps) {
  return (
    <>
      <section className="container-config">
        <h2>Container Configuration</h2>
        <div className="input-group">
          <label>Width (m):</label>
          <input
            type="number"
            value={container.width}
            onChange={(e) => onUpdateContainer('width', e.target.value)}
            step="0.5"
            min="1"
          />
        </div>
        <div className="input-group">
          <label>Depth (m):</label>
          <input
            type="number"
            value={container.depth}
            onChange={(e) => onUpdateContainer('depth', e.target.value)}
            step="0.5"
            min="1"
          />
        </div>
        <div className="input-group">
          <label>Max Weight (kg):</label>
          <input
            type="number"
            value={container.max_weight}
            onChange={(e) => onUpdateContainer('max_weight', e.target.value)}
            step="100"
            min="100"
          />
        </div>
      </section>

      <section className="cylinders-config">
        <div className="section-header">
          <h2>Cylinders ({cylinders.length})</h2>
          <button onClick={onAddCylinder} className="add-button">
            + Add Cylinder
          </button>
        </div>
        
        <div className="cylinders-list">
          {cylinders.map((cyl, index) => (
            <div key={index} className="cylinder-item">
              <span className="cylinder-id">#{index}</span>
              <div className="cylinder-inputs">
                <input
                  type="number"
                  value={cyl.diameter}
                  onChange={(e) => onUpdateCylinder(index, 'diameter', e.target.value)}
                  placeholder="Diameter (m)"
                  step="0.1"
                  min="0.1"
                />
                <input
                  type="number"
                  value={cyl.weight}
                  onChange={(e) => onUpdateCylinder(index, 'weight', e.target.value)}
                  placeholder="Weight (kg)"
                  step="10"
                  min="1"
                />
              </div>
              <button
                onClick={() => onRemoveCylinder(index)}
                className="remove-button"
                disabled={cylinders.length <= 1}
              >
                ×
              </button>
            </div>
          ))}
        </div>
      </section>

      <section className="algorithm-config">
        <h2>Algorithm</h2>
        <select 
          value={algorithm} 
          onChange={(e) => onAlgorithmChange(e.target.value as Algorithm)}
          className="algorithm-select"
        >
          <option value="genetic">Genetic Algorithm</option>
          <option value="greedy">Greedy Algorithm</option>
          <option value="random">Random Search</option>
        </select>

        <button
          onClick={onSolve}
          disabled={solving || cylinders.length === 0}
          className="solve-button"
        >
          {solving ? 'Solving...' : 'Run Algorithm'}
        </button>
      </section>
    </>
  )
}
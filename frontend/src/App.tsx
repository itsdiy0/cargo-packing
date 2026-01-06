import { useState } from 'react'
import axios from 'axios'
import './App.css'
import type { Container, Cylinder, Solution, ProgressUpdate, Algorithm } from './types'
import SolutionVisualization from './components/SolutionVisualization'
import PresetSelector from './components/PresetSelector'

const API_URL = 'http://127.0.0.1:5000/api'

function App() {
  const [container, setContainer] = useState<Container>({
    width: 20,
    depth: 15,
    max_weight: 1000
  })

  const [cylinders, setCylinders] = useState<Cylinder[]>([
    { diameter: 2.0, weight: 100 },
    { diameter: 2.0, weight: 100 },
    { diameter: 2.0, weight: 100 }
  ])

  const [algorithm, setAlgorithm] = useState<Algorithm>('genetic')
  const [solving, setSolving] = useState(false)
  const [solution, setSolution] = useState<Solution | null>(null)
  const [logs, setLogs] = useState<string[]>([])
  const [progress, setProgress] = useState<ProgressUpdate | null>(null)
  const [selectedPreset, setSelectedPreset] = useState<string>('custom')

  const addCylinder = () => {
    setCylinders([...cylinders, { diameter: 2.0, weight: 100 }])
  }

  const removeCylinder = (index: number) => {
    setCylinders(cylinders.filter((_, i) => i !== index))
  }

  const updateCylinder = (index: number, field: keyof Cylinder, value: string) => {
    const updated = [...cylinders]
    updated[index][field] = parseFloat(value) || 0
    setCylinders(updated)
  }

  const updateContainer = (field: keyof Container, value: string) => {
    setContainer({ ...container, [field]: parseFloat(value) || 0 })
  }

  const addLog = (message: string) => {
    setLogs(prev => [...prev, `[${new Date().toLocaleTimeString()}] ${message}`])
  }

  const loadPreset = (presetContainer: Container, presetCylinders: Cylinder[], name: string) => {
    setContainer(presetContainer)
    setCylinders(presetCylinders)
    setSolution(null)
    setLogs([])
    setProgress(null)
    setSelectedPreset(name)
    addLog(`Loaded preset: ${name}`)
  }

  const handleFileUpload = (fileContainer: Container, fileCylinders: Cylinder[]) => {
    setContainer(fileContainer)
    setCylinders(fileCylinders)
    setSolution(null)
    setLogs([])
    setProgress(null)
    setSelectedPreset('custom')
    addLog(`Loaded instance from file`)
    addLog(`Container: ${fileContainer.width}m × ${fileContainer.depth}m`)
    addLog(`Cylinders: ${fileCylinders.length}`)
  }

  const solveProblem = async () => {
    if (algorithm === 'genetic') {
      solveWithStreaming()
    } else {
      solveStandard()
    }
  }

  const solveStandard = async () => {
    setSolving(true)
    setSolution(null)
    setLogs([])
    setProgress(null)
    addLog(`Starting ${algorithm} algorithm...`)
    addLog(`Container: ${container.width}m × ${container.depth}m`)
    addLog(`Cylinders: ${cylinders.length}`)

    try {
      const response = await axios.post(`${API_URL}/solve`, {
        container,
        cylinders,
        algorithm,
        params: {
          population_size: 100,
          mutation_rate: 0.05,
          step_size: 0.3,
          max_generations: 200,
          strategy: 'largest_first',
          num_trials: 1000,
          use_local_search: true
        }
      })

      if (response.data.success) {
        setSolution(response.data.result)
        addLog(`Solution found! Fitness: ${response.data.result.fitness.toFixed(2)}`)
        addLog(`Valid: ${response.data.result.details.valid ? 'Yes' : 'No'}`)
        addLog(`Packing density: ${(response.data.result.details.packing_density * 100).toFixed(2)}%`)
      }
    } catch (error) {
      console.error('Error solving:', error)
      addLog('ERROR: Failed to solve problem')
    } finally {
      setSolving(false)
    }
  }

  const solveWithStreaming = async () => {
    setSolving(true)
    setSolution(null)
    setProgress(null)
    setLogs([])
    addLog('Starting Genetic Algorithm with live visualization...')
    addLog(`Container: ${container.width}m × ${container.depth}m, Max: ${container.max_weight}kg`)
    addLog(`Cylinders: ${cylinders.length}`)

    try {
      const response = await fetch(`${API_URL}/solve-stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          container,
          cylinders,
          params: {
            population_size: 100,
            mutation_rate: 0.05,
            step_size: 0.3,
            max_generations: 200,
            animation_delay: 0.05
          }
        })
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      if (!response.body) {
        throw new Error('No response body')
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      const processChunk = async (): Promise<void> => {
        const { done, value } = await reader.read()
        
        if (done) {
          setSolving(false)
          addLog('Evolution complete!')
          return
        }

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6))

              if (data.type === 'start') {
                addLog(`Evolution starting: ${data.total_generations} generations`)
              }
              else if (data.type === 'progress') {
                setProgress({
                  generation: data.generation,
                  best_fitness: data.best_fitness,
                  avg_fitness: data.avg_fitness,
                  worst_fitness: data.worst_fitness
                })

                if (data.solution && data.solution.cylinders && data.solution.cylinders.length > 0) {
                  setSolution({
                    algorithm: `Genetic Algorithm (Gen ${data.generation})`,
                    solution: data.solution.placement_order,
                    fitness: data.best_fitness,
                    details: {
                      valid: data.best_fitness > 0,
                      center_of_mass: data.solution.center_of_mass,
                      packing_density: data.solution.packing_density,
                      cylinders: data.solution.cylinders
                    }
                  })
                }

                if (data.generation % 50 === 0) {
                  addLog(`Gen ${data.generation}: best=${data.best_fitness.toFixed(2)}, avg=${data.avg_fitness.toFixed(2)}`)
                }
              }
              else if (data.type === 'complete') {
                setSolution({
                  algorithm: 'Genetic Algorithm (Final)',
                  solution: data.solution.placement_order,
                  fitness: data.solution.fitness,
                  details: data.solution
                })
                addLog(`Final solution! Fitness: ${data.solution.fitness.toFixed(2)}`)
                addLog(`Valid: ${data.solution.valid ? 'Yes' : 'No'}`)
                addLog(`Packing density: ${(data.solution.packing_density * 100).toFixed(2)}%`)
                setSolving(false)
                return
              }
            } catch (e) {
              console.error('Error parsing SSE:', e)
            }
          }
        }

        return processChunk()
      }

      await processChunk()
    } catch (error) {
      console.error('Stream error:', error)
      addLog('ERROR: Streaming failed')
      setSolving(false)
    }
  }

  return (
    <div className="app">
      <div className="top-section">
        <div className="algorithm-panel">
          <h2>Algorithm Selection</h2>
          <select
            value={algorithm}
            onChange={(e) => setAlgorithm(e.target.value as Algorithm)}
            className="algorithm-select"
          >
            <option value="genetic">Genetic Algorithm</option>
            <option value="greedy">Greedy Algorithm</option>
            <option value="random">Random Search</option>
          </select>

          <PresetSelector
            selectedPreset={selectedPreset}
            onLoadPreset={loadPreset}
            onFileUpload={handleFileUpload}
          />
        </div>

        <div className="start-panel">
          <button
            onClick={solveProblem}
            disabled={solving || cylinders.length === 0}
            className="start-button"
          >
            {solving ? 'Solving...' : 'Start'}
          </button>
        </div>

        <div className="container-config-panel">
          <h2>Container Configuration</h2>
          <div className="config-grid">
            <div className="config-item">
              <label>Width (m)</label>
              <input
                type="number"
                value={container.width}
                onChange={(e) => updateContainer('width', e.target.value)}
                step="0.5"
                min="1"
              />
            </div>
            <div className="config-item">
              <label>Depth (m)</label>
              <input
                type="number"
                value={container.depth}
                onChange={(e) => updateContainer('depth', e.target.value)}
                step="0.5"
                min="1"
              />
            </div>
            <div className="config-item">
              <label>Max Weight (kg)</label>
              <input
                type="number"
                value={container.max_weight}
                onChange={(e) => updateContainer('max_weight', e.target.value)}
                step="100"
                min="100"
              />
            </div>
          </div>
        </div>
      </div>

      <div className="middle-section">
        <div className="visualizer-panel">
          <div className="visualizer-header">
            <h2>Visualiser</h2>
            {progress && (
              <div className="generation-badge">
                Generation {progress.generation}/200 | Fitness: {progress.best_fitness.toFixed(2)}
              </div>
            )}
          </div>
          <div className="visualizer-content">
            {solution ? (
              <SolutionVisualization
                container={container}
                cylinders={solution.details.cylinders}
                centerOfMass={solution.details.center_of_mass}
              />
            ) : (
              <div className="visualizer-placeholder">
                <p>Solution will appear here</p>
              </div>
            )}
          </div>
        </div>

        <div className="cylinders-panel">
          <div className="cylinders-header">
            <h2>Cylinders ({cylinders.length})</h2>
            <button onClick={addCylinder} className="add-cylinder-btn">
              + Add
            </button>
          </div>
          <div className="cylinders-grid">
            {cylinders.map((cyl, index) => (
              <div key={index} className="cylinder-card">
                <div className="cylinder-card-header">
                  <span className="cylinder-title">Cylinder {index + 1}</span>
                  <button
                    onClick={() => removeCylinder(index)}
                    className="remove-cylinder-btn"
                    disabled={cylinders.length <= 1}
                  >
                    ×
                  </button>
                </div>
                <div className="cylinder-card-body">
                  <div className="cylinder-input-group">
                    <label>Diameter (m)</label>
                    <input
                      type="number"
                      value={cyl.diameter}
                      onChange={(e) => updateCylinder(index, 'diameter', e.target.value)}
                      step="0.1"
                      min="0.1"
                    />
                  </div>
                  <div className="cylinder-input-group">
                    <label>Weight (kg)</label>
                    <input
                      type="number"
                      value={cyl.weight}
                      onChange={(e) => updateCylinder(index, 'weight', e.target.value)}
                      step="10"
                      min="1"
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="bottom-section">
        <div className="logs-panel">
          <h2>Results / Logs</h2>
          <div className="logs-content">
            {logs.length === 0 ? (
              <p className="logs-placeholder">Logs will appear here...</p>
            ) : (
              logs.map((log, idx) => (
                <div key={idx} className="log-entry">{log}</div>
              ))
            )}
            {solution && (
              <div className="solution-summary">
                <div className="summary-item">
                  <strong>Placement Order:</strong> {solution.solution.join(' → ')}
                </div>
                <div className="summary-item">
                  <strong>Fitness:</strong> {solution.fitness.toFixed(2)}
                </div>
                <div className="summary-item">
                  <strong>Valid:</strong> {solution.details.valid ? '✓ Yes' : '✗ No'}
                </div>
                <div className="summary-item">
                  <strong>Packing Density:</strong> {(solution.details.packing_density * 100).toFixed(2)}%
                </div>
                <div className="summary-item">
                  <strong>Center of Mass:</strong> ({solution.details.center_of_mass[0].toFixed(2)}, {solution.details.center_of_mass[1].toFixed(2)})
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
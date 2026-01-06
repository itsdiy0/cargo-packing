import { PRESET_INSTANCES } from '../data/instances'
import type { Container, Cylinder } from '../types'
import { parseInstanceFile } from '../utils/fileParser'

interface PresetSelectorProps {
  selectedPreset: string
  onLoadPreset: (container: Container, cylinders: Cylinder[], name: string) => void
  onFileUpload: (container: Container, cylinders: Cylinder[]) => void
}

export default function PresetSelector({ 
  selectedPreset, 
  onLoadPreset,
  onFileUpload 
}: PresetSelectorProps) {
  const handlePresetChange = (value: string) => {
    if (value === 'custom') return

    const preset = PRESET_INSTANCES.find(p => p.id === value)
    if (preset) {
      onLoadPreset(preset.container, preset.cylinders, preset.name)
    }
  }

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return

    const reader = new FileReader()
    reader.onload = (e) => {
      const text = e.target?.result as string
      const parsed = parseInstanceFile(text)
      
      if (parsed) {
        onFileUpload(parsed.container, parsed.cylinders)
      } else {
        alert('Failed to parse instance file. Check format.')
      }
    }
    reader.readAsText(file)
    
    event.target.value = ''
  }

  return (
    <div className="preset-selector">
      <div className="preset-dropdown">
        <label>Select Problem</label>
        <select 
          value={selectedPreset}
          onChange={(e) => handlePresetChange(e.target.value)}
          className="preset-select"
        >
          <option value="custom">Custom Configuration</option>
          <optgroup label="Reference Instances">
            {PRESET_INSTANCES.filter(p => p.difficulty === 'easy').map(preset => (
              <option key={preset.id} value={preset.id}>{preset.name}</option>
            ))}
          </optgroup>
          <optgroup label="Challenging Instances">
            {PRESET_INSTANCES.filter(p => p.difficulty === 'medium' || p.difficulty === 'hard').map(preset => (
              <option key={preset.id} value={preset.id}>{preset.name}</option>
            ))}
          </optgroup>
        </select>
      </div>

      <div className="file-upload">
        <label htmlFor="file-input" className="file-upload-label">
          Upload Instance File
        </label>
        <input
          id="file-input"
          type="file"
          accept=".txt"
          onChange={handleFileChange}
          className="file-input"
        />
      </div>
    </div>
  )
}
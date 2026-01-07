import type { Container, PlacedCylinder } from '../types'

interface SolutionVisualizationProps {
  container: Container
  cylinders: PlacedCylinder[]
  centerOfMass: [number, number]
}

export default function SolutionVisualization({
  container,
  cylinders,
  centerOfMass
}: SolutionVisualizationProps) {
  const padding = 40
  
  const toScreenX = (x: number, width: number, scale: number, offsetX: number) => offsetX + x * scale
  const toScreenY = (y: number, scale: number, offsetY: number) => offsetY + y * scale
  const toScreenDist = (d: number, scale: number) => d * scale
  
  const colors = [
    '#FFB6C1', '#87CEEB', '#98FB98', '#DDA0DD', '#F0E68C',
    '#FFB347', '#B0E0E6', '#DEB887', '#F08080', '#E6E6FA',
    '#FFDAB9', '#C1FFC1', '#FFE4B5', '#B0C4DE', '#FFDEAD'
  ]

  return (
    <svg 
      width="100%" 
      height="100%" 
      viewBox="0 0 800 600"
      preserveAspectRatio="xMidYMid meet"
      style={{ maxWidth: '100%', maxHeight: '100%' }}
    >
      <SVGContent
        container={container}
        cylinders={cylinders}
        centerOfMass={centerOfMass}
        colors={colors}
        padding={padding}
      />
    </svg>
  )
}

function SVGContent({ container, cylinders, centerOfMass, colors, padding }: any) {
  const canvasWidth = 800
  const canvasHeight = 600
  
  const availableWidth = canvasWidth - 2 * padding
  const availableHeight = canvasHeight - 2 * padding
  
  const scaleX = availableWidth / container.width
  const scaleY = availableHeight / container.depth
  const scale = Math.min(scaleX, scaleY)
  
  const containerWidth = container.width * scale
  const containerHeight = container.depth * scale
  
  const offsetX = padding + (availableWidth - containerWidth) / 2
  const offsetY = padding + (availableHeight - containerHeight) / 2
  
  const toScreenX = (x: number) => offsetX + x * scale
  const toScreenY = (y: number) => offsetY + y * scale
  const toScreenDist = (d: number) => d * scale
  
  const safeZone = {
    x: toScreenX(container.width * 0.2),
    y: toScreenY(container.depth * 0.2),
    width: toScreenDist(container.width * 0.6),
    height: toScreenDist(container.depth * 0.6)
  }

  return (
    <g>
      <rect
        x={offsetX}
        y={offsetY}
        width={containerWidth}
        height={containerHeight}
        fill="#0a0a0a"
        stroke="#888"
        strokeWidth="2"
      />
      
      <rect
        x={safeZone.x}
        y={safeZone.y}
        width={safeZone.width}
        height={safeZone.height}
        fill="rgba(0, 255, 0, 0.08)"
        stroke="#48bb78"
        strokeWidth="1.5"
        strokeDasharray="5,5"
      />
      
      <text x={safeZone.x + 5} y={safeZone.y + 15} fontSize="11" fill="#48bb78">
        Safe zone (60%)
      </text>

      {cylinders.map((cyl, idx) => {
        const cx = toScreenX(cyl.x)
        const cy = toScreenY(cyl.y)
        const r = toScreenDist(cyl.radius)
        const color = colors[idx % colors.length]

        return (
          <g key={idx}>
            <circle
              cx={cx}
              cy={cy}
              r={r}
              fill={color}
              stroke="#4a5568"
              strokeWidth="2"
              opacity="0.85"
            />
            <text
              x={cx}
              y={cy - 5}
              textAnchor="middle"
              fontSize="13"
              fontWeight="bold"
              fill="#000"
            >
              {cyl.id}
            </text>
            <text
              x={cx}
              y={cy + 8}
              textAnchor="middle"
              fontSize="9"
              fill="#000"
            >
              ø{cyl.diameter}m
            </text>
            <text
              x={cx}
              y={cy + 18}
              textAnchor="middle"
              fontSize="8"
              fill="#000"
            >
              {cyl.weight}kg
            </text>
          </g>
        )
      })}

      {centerOfMass && (
        <g>
          <line
            x1={toScreenX(centerOfMass[0]) - 12}
            y1={toScreenY(centerOfMass[1])}
            x2={toScreenX(centerOfMass[0]) + 12}
            y2={toScreenY(centerOfMass[1])}
            stroke="#f56565"
            strokeWidth="2.5"
          />
          <line
            x1={toScreenX(centerOfMass[0])}
            y1={toScreenY(centerOfMass[1]) - 12}
            x2={toScreenX(centerOfMass[0])}
            y2={toScreenY(centerOfMass[1]) + 12}
            stroke="#f56565"
            strokeWidth="2.5"
          />
          <circle
            cx={toScreenX(centerOfMass[0])}
            cy={toScreenY(centerOfMass[1])}
            r="16"
            fill="none"
            stroke="#f56565"
            strokeWidth="2"
          />
        </g>
      )}

      <text x={offsetX} y={offsetY - 15} fontSize="12" fontWeight="bold" fill="#aaa">
        {container.width}m × {container.depth}m (Max: {container.max_weight}kg)
      </text>
    </g>
  )
}
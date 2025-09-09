import React, { useEffect, useState } from 'react'

type Train = {
  id: string
  name: string
  departureStation: string
  departure: string
  arrivalStation: string
  arrival: string
  status: 'On Time' | 'Delayed' | string
}

const trainsData: Train[] = [
  {
    id: '12345',
    name: 'Rajdhani Express',
    departureStation: 'Delhi',
    departure: '2025-09-10T21:00:00',
    arrivalStation: 'Bhopal',
    arrival: '2025-09-10T23:00:00',
    status: 'On Time'
  },
  {
    id: '54321',
    name: 'Duronto Express',
    departureStation: 'Mumbai',
    departure: '2025-09-10T20:30:00',
    arrivalStation: 'Nagpur',
    arrival: '2025-09-10T23:30:00',
    status: 'Delayed'
  }
]

export default function TrainTimeline(): JSX.Element {
  const [progress, setProgress] = useState<Record<string, number>>({})

  useEffect(() => {
    const updateProgress = () => {
      const newProgress: Record<string, number> = {}
      trainsData.forEach(train => {
        const now = new Date().getTime()
        const dep = new Date(train.departure).getTime()
        const arr = new Date(train.arrival).getTime()
        let pct = ((now - dep) / (arr - dep)) * 100
        if (pct < 0) pct = 0
        if (pct > 100) pct = 100
        newProgress[train.id] = pct
      })
      setProgress(newProgress)
    }

    updateProgress()
    const interval = setInterval(updateProgress, 1000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-gray-800">Train Movement Timeline (Demo)</h3>
      {trainsData.map(train => (
        <div key={train.id} className="">
          <div className="flex items-center justify-between text-sm font-medium text-gray-700 mb-1">
            <span>{train.departureStation}</span>
            <span>{train.arrivalStation}</span>
          </div>
          <div className="relative w-full h-2 bg-gray-300 rounded-full overflow-hidden mb-2">
            <div
              className="absolute -top-3 text-2xl transition-all duration-1000 ease-linear"
              style={{ left: `${progress[train.id] || 0}%`, transform: 'translateX(-50%)' }}
            >
              🚆
            </div>
          </div>
          <div className="text-sm text-gray-700">
            <span className="font-semibold">{train.name}</span> ({train.id}) – {train.status} – {Math.round(progress[train.id] || 0)}% completed
          </div>
        </div>
      ))}
    </div>
  )
}



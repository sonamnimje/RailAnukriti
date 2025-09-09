import { useMemo } from 'react'
import type { TimelineData } from '../lib/api'

interface TimelineChartProps {
	data: TimelineData
	height?: number
}

export default function TimelineChart({ data, height = 400 }: TimelineChartProps) {
	const chartData = useMemo(() => {
		const trains = Object.keys(data.timeline)
		const timeRange = {
			start: new Date(data.time_range.start).getTime(),
			end: new Date(data.time_range.end).getTime()
		}
		const totalDuration = timeRange.end - timeRange.start

		return trains.map(trainId => {
			const events = data.timeline[trainId]
			return {
				trainId,
				events: events.map(event => ({
					...event,
					startTime: event.planned_time ? new Date(event.planned_time).getTime() : null,
					actualTime: event.actual_time ? new Date(event.actual_time).getTime() : null,
					position: event.planned_time 
						? ((new Date(event.planned_time).getTime() - timeRange.start) / totalDuration) * 100
						: 0,
					actualPosition: event.actual_time 
						? ((new Date(event.actual_time).getTime() - timeRange.start) / totalDuration) * 100
						: null
				}))
			}
		})
	}, [data])

	const formatTime = (timeStr: string) => {
		return new Date(timeStr).toLocaleTimeString()
	}

	const getEventColor = (eventType: string, delay?: number) => {
		if (delay && delay > 0) return 'bg-red-500'
		switch (eventType) {
			case 'arrival': return 'bg-green-500'
			case 'departure': return 'bg-blue-500'
			case 'delay': return 'bg-red-500'
			case 'status_change': return 'bg-yellow-500'
			default: return 'bg-gray-500'
		}
	}

	return (
		<div className="w-full bg-white border border-gray-300 rounded-lg p-4 shadow-sm">
			<div className="mb-4">
				<h3 className="text-lg font-semibold text-gray-800 mb-2">Train Movement Timeline</h3>
				<div className="text-sm text-gray-600">
					Time Range: {formatTime(data.time_range.start)} - {formatTime(data.time_range.end)}
				</div>
			</div>
			
			<div className="relative" style={{ height: `${height}px` }}>
				{/* Time axis */}
				<div className="absolute top-0 left-0 right-0 h-8 bg-gray-100 border-b border-gray-300 rounded-t flex items-center px-2">
					<div className="text-xs text-gray-600">Time →</div>
				</div>
				
				{/* Train rows */}
				<div className="pt-8 space-y-2">
					{chartData.map((train, trainIndex) => (
						<div key={train.trainId} className="relative h-12 bg-gray-100 border border-gray-300 rounded flex items-center">
							{/* Train ID label */}
							<div className="absolute left-2 text-sm font-medium text-blue-600 z-10">
								🚂 {train.trainId}
							</div>
							
							{/* Timeline events */}
							<div className="absolute inset-0 flex items-center">
								{train.events.map((event, eventIndex) => (
									<div key={eventIndex} className="relative">
										{/* Planned time marker */}
										{event.startTime && (
											<div 
												className="absolute w-2 h-2 bg-gray-600 rounded-full border border-gray-800"
												style={{ left: `${event.position}%` }}
												title={`Planned: ${formatTime(event.planned_time!)}`}
											/>
										)}
										
										{/* Actual time marker */}
										{event.actualTime && (
											<div 
												className={`absolute w-3 h-3 rounded-full ${getEventColor(event.event_type, event.delay_minutes)}`}
												style={{ left: `${event.actualPosition!}%` }}
												title={`Actual: ${formatTime(event.actual_time!)} (${event.delay_minutes || 0} min delay)`}
											/>
										)}
										
										{/* Connection line */}
										{event.startTime && event.actualTime && (
											<div 
												className="absolute h-0.5 bg-gray-400"
												style={{ 
													left: `${Math.min(event.position, event.actualPosition!)}%`,
													width: `${Math.abs(event.actualPosition! - event.position)}%`
												}}
											/>
										)}
									</div>
								))}
							</div>
						</div>
					))}
				</div>
				
				{/* Legend */}
				<div className="absolute bottom-0 left-0 right-0 h-16 bg-gray-100 border-t border-gray-300 rounded-b p-2">
					<div className="flex items-center gap-4 text-xs">
						<div className="flex items-center gap-1">
							<div className="w-2 h-2 bg-gray-600 rounded-full border border-gray-800"></div>
							<span className="text-gray-700">Planned</span>
						</div>
						<div className="flex items-center gap-1">
							<div className="w-3 h-3 bg-green-500 rounded-full"></div>
							<span className="text-gray-700">Arrival</span>
						</div>
						<div className="flex items-center gap-1">
							<div className="w-3 h-3 bg-blue-500 rounded-full"></div>
							<span className="text-gray-700">Departure</span>
						</div>
						<div className="flex items-center gap-1">
							<div className="w-3 h-3 bg-red-500 rounded-full"></div>
							<span className="text-gray-700">Delay</span>
						</div>
						<div className="flex items-center gap-1">
							<div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
							<span className="text-gray-700">Status Change</span>
						</div>
					</div>
				</div>
			</div>
		</div>
	)
}

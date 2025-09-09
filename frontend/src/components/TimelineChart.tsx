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
		<div className="w-full rounded-2xl border border-slate-200 bg-white shadow-sm p-5">
			{/* Header */}
			<div className="flex items-center justify-between mb-4">
				<div>
					<h3 className="text-xl font-semibold text-slate-800">Train Movement Timeline</h3>
					<p className="text-xs text-slate-500">Visualizing planned vs actual events</p>
				</div>
				<div className="text-sm text-slate-600 bg-slate-100 px-3 py-1 rounded-full">
					{formatTime(data.time_range.start)} – {formatTime(data.time_range.end)}
				</div>
			</div>

			{/* Timeline */}
			<div className="relative rounded-xl border border-slate-200 bg-slate-50" style={{ height: `${height}px` }}>
				{/* Time axis with ticks */}
				<div className="absolute top-0 left-0 right-0 h-10 rounded-t-xl bg-white/70 border-b border-slate-200 flex items-center px-3">
					<div className="text-xs text-slate-600">Time →</div>
					<div className="flex-1 h-px bg-gradient-to-r from-transparent via-slate-200 to-transparent ml-3 relative">
						{Array.from({ length: 6 }).map((_, i) => (
							<div key={i} className="absolute top-[-6px] h-3 w-px bg-slate-300" style={{ left: `${(i + 1) * (100 / 7)}%` }} />
						))}
					</div>
				</div>

				{/* Rows */}
				<div className="pt-10 space-y-3 p-3">
					{chartData.length === 0 && (
						<div className="h-[160px] flex items-center justify-center text-sm text-slate-500">No timeline data</div>
					)}
					{chartData.map(train => (
						<div key={train.trainId} className="relative h-14 rounded-xl bg-white border border-slate-200 shadow-xs overflow-hidden">
							{/* Train label */}
							<div className="absolute left-3 top-1/2 -translate-y-1/2 text-sm font-medium text-blue-600 z-10">
								🚂 {train.trainId}
							</div>
							{/* Events layer */}
							<div className="absolute inset-0 flex items-center pl-24 pr-3">
								<div className="relative w-full h-1 bg-slate-200 rounded">
									{train.events.map((event, idx) => (
										<div key={idx} className="absolute">
											{event.startTime && (
												<div
													className="w-2 h-2 -mt-0.5 rounded-full bg-slate-600 border border-slate-800"
													style={{ left: `calc(${event.position}% - 1px)` }}
													title={`Planned: ${formatTime(event.planned_time!)}`}
												/>
											)}
											{event.actualTime && (
												<div
													className={`w-3 h-3 -mt-1 rounded-full ${getEventColor(event.event_type, event.delay_minutes)} shadow`}
													style={{ left: `calc(${event.actualPosition!}% - 2px)` }}
													title={`Actual: ${formatTime(event.actual_time!)} (${event.delay_minutes || 0} min delay)`}
												/>
											)}
											{event.startTime && event.actualTime && (
												<div
													className="absolute top-1/2 -translate-y-1/2 h-0.5 bg-slate-400"
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
						</div>
					))}
				</div>

				{/* Legend */}
				<div className="absolute bottom-0 left-0 right-0 h-14 bg-white/70 border-t border-slate-200 rounded-b-xl px-3 flex items-center gap-3 text-xs">
					<span className="inline-flex items-center gap-2 px-2 py-1 rounded-full bg-slate-100 text-slate-700"><span className="w-2 h-2 rounded-full bg-gray-600 border border-gray-800"/>Planned</span>
					<span className="inline-flex items-center gap-2 px-2 py-1 rounded-full bg-green-100 text-green-700"><span className="w-3 h-3 rounded-full bg-green-500"/>Arrival</span>
					<span className="inline-flex items-center gap-2 px-2 py-1 rounded-full bg-blue-100 text-blue-700"><span className="w-3 h-3 rounded-full bg-blue-500"/>Departure</span>
					<span className="inline-flex items-center gap-2 px-2 py-1 rounded-full bg-red-100 text-red-700"><span className="w-3 h-3 rounded-full bg-red-500"/>Delay</span>
					<span className="inline-flex items-center gap-2 px-2 py-1 rounded-full bg-yellow-100 text-yellow-700"><span className="w-3 h-3 rounded-full bg-yellow-500"/>Status Change</span>
				</div>
			</div>
		</div>
	)
}

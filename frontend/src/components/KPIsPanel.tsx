import React from 'react';

interface KPIs {
	throughput_per_hour?: number;
	avg_delay_minutes?: number;
	congestion_index?: number;
	on_time_percentage?: number;
}

export default function KPIsPanel({ kpis }: { kpis: KPIs | null }) {
	return (
		<div className="bg-indigo-100 rounded-2xl p-6 shadow min-w-[300px]">
			<div className="text-lg font-semibold text-indigo-700 mb-2">Key Performance</div>
			<ul className="space-y-2">
				<li className="flex items-center gap-2 text-gray-700"><span>📊</span> Section Throughput: <span className="font-bold">{kpis?.throughput_per_hour !== undefined ? `${kpis.throughput_per_hour}%` : '--'}</span></li>
				<li className="flex items-center gap-2 text-gray-700"><span>⏱️</span> Avg Delay: <span className="font-bold">{kpis?.avg_delay_minutes !== undefined ? `${kpis.avg_delay_minutes} mins` : '--'}</span></li>
				<li className="flex items-center gap-2 text-gray-700"><span>✅</span> On-time Trains: <span className="font-bold">{kpis?.on_time_percentage !== undefined ? `${kpis.on_time_percentage}%` : '--'}</span></li>
			</ul>
		</div>
	);
}



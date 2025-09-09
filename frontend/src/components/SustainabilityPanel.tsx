import React from 'react';

export default function SustainabilityPanel({ todayKg = 15, totalKg }: { todayKg?: number; totalKg?: number }) {
	return (
		<div className="bg-emerald-50 rounded-2xl p-6 shadow w-full">
			<div className="text-lg font-semibold text-emerald-800 mb-1">Sustainability Tracker</div>
			<div className="text-sm text-emerald-900">Emissions saved by AI decisions</div>
			<div className="mt-3 flex items-center gap-6">
				<div className="text-2xl font-bold text-emerald-700">~{todayKg} kg CO₂</div>
				{typeof totalKg === 'number' && (
					<div className="text-xs text-emerald-900">MTD: {totalKg.toFixed(0)} kg</div>
				)}
			</div>
		</div>
	);
}



import React from 'react';

interface Forecast {
	icon: string;
	message: string;
}

export default function ForecastsPanel({ forecasts }: { forecasts?: Forecast[] }) {
	const items: Forecast[] = forecasts && forecasts.length > 0 ? forecasts : [
		{ icon: '⚠️', message: 'High chance of bottleneck at Section B (3 trains converging).' },
		{ icon: '⚡', message: 'Possible signal congestion near Station C.' }
	];
	return (
		<div className="bg-yellow-50 rounded-2xl p-6 shadow w-full">
			<div className="text-lg font-semibold text-yellow-800 mb-2">Disruption Prediction (next 30 mins)</div>
			<ul className="space-y-2">
				{items.map((f, i) => (
					<li key={i} className="text-sm text-yellow-900 flex items-start gap-2">
						<span>{f.icon}</span>
						<span>{f.message}</span>
					</li>
				))}
			</ul>
		</div>
	);
}



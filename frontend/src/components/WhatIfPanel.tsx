import React, { useMemo, useState } from 'react';

export default function WhatIfPanel() {
	const [delayMins, setDelayMins] = useState(5);
	const congestionDrop = useMemo(() => Math.min(40, Math.max(5, delayMins * 4)), [delayMins]);
	return (
		<div className="bg-slate-50 rounded-2xl p-6 shadow w-full">
			<div className="text-lg font-semibold text-slate-800 mb-1">What-If Scenario</div>
			<div className="text-sm text-slate-900">If you delay Train 120 by <b>{delayMins} mins</b> → Station B congestion drops <b>{congestionDrop}%</b>.</div>
			<div className="mt-3 flex items-center gap-3">
				<input type="range" min={0} max={15} value={delayMins} onChange={(e) => setDelayMins(parseInt(e.target.value))} className="w-48" />
				<div className="text-xs text-slate-700">Adjust delay</div>
			</div>
		</div>
	);
}



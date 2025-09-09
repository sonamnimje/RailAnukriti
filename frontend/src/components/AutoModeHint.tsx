import React, { useState } from 'react';

export default function AutoModeHint({ onEnable }: { onEnable?: (minutes: number) => void }) {
	const [enabled, setEnabled] = useState(false);
	const [mins, setMins] = useState(15);
	function handleEnable() {
		setEnabled(true);
		onEnable?.(mins);
	}
	return (
		<div className="bg-blue-50 rounded-2xl p-6 shadow w-full">
			<div className="text-lg font-semibold text-blue-800 mb-1">Controller Stress Reduction</div>
			<div className="text-sm text-blue-900">System can auto-manage low-priority freight. Enable auto-mode?</div>
			<div className="mt-3 flex items-center gap-3">
				<input type="range" min={5} max={30} value={mins} onChange={(e) => setMins(parseInt(e.target.value))} className="w-40" />
				<div className="text-xs text-blue-900">{mins} mins</div>
				<button className="px-3 py-1 text-xs rounded-lg bg-blue-600 text-white hover:bg-blue-700" onClick={handleEnable} disabled={enabled}>{enabled ? 'Enabled' : 'Enable'}</button>
			</div>
		</div>
	);
}



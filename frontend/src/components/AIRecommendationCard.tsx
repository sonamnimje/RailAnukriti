import React from 'react';
import type { Recommendation } from '../lib/api';

export default function AIRecommendationCard({ recommendation, onAccept, onOverride }: {
	recommendation: Recommendation | null;
	onAccept: (rec: Recommendation) => void;
	onOverride: (rec: Recommendation) => void;
}) {
	if (!recommendation) return null;

	function buildDecision(rec: Recommendation) {
		const mins = rec.eta_change_seconds ? Math.round(Math.abs(rec.eta_change_seconds) / 60) : undefined;
		const base = rec.action && rec.action.trim().length > 0 ? rec.action : `Prioritize Train ${rec.train_id}${rec.platform ? ` at platform ${rec.platform}` : ''}`;
		if (mins && mins > 0) return `${base} → saves ~${mins} min` + (mins > 1 ? 's' : '');
		return base;
	}

	function buildReason(rec: Recommendation) {
		if (rec.reason && rec.reason.trim().length > 0) return rec.reason;
		if (/platform/i.test(rec.action) || rec.platform) return 'Avoid platform conflict and reduce dwell time.';
		if (/cross|precedence|priority/i.test(rec.action)) return 'Passenger load higher; reduces network idle time.';
		return 'Mitigates upcoming congestion and improves section throughput.';
	}
	return (
		<div className="bg-green-100 rounded-2xl p-6 mt-6 shadow flex flex-col gap-3">
			<div className="text-lg font-semibold text-green-700 mb-1">AI Recommendation</div>
			<div className="text-base"><b>Decision:</b> <span className="font-semibold text-green-900">{buildDecision(recommendation)}</span></div>
			<div className="text-base"><b>Reason:</b> <span className="font-semibold text-gray-900">{buildReason(recommendation)}</span></div>
			<div className="flex gap-4 mt-2">
				<button className="bg-green-600 hover:bg-green-700 text-white font-bold px-6 py-2 rounded-lg text-lg" onClick={() => onAccept(recommendation)}>Accept</button>
				<button className="bg-red-600 hover:bg-red-700 text-white font-bold px-6 py-2 rounded-lg text-lg" onClick={() => onOverride(recommendation)}>Override</button>
			</div>
		</div>
	);
}



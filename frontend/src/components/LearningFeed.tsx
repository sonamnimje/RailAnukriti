import React from 'react';

export default function LearningFeed({ notes }: { notes?: string[] }) {
	const items = notes && notes.length > 0 ? notes : [
		'We learned from your last override: You prioritized Train 101 over Train 109 during peak hour. This pattern will be used in future suggestions.'
	];
	return (
		<div className="bg-violet-50 rounded-2xl p-6 shadow w-full">
			<div className="text-lg font-semibold text-violet-800 mb-2">Adaptive Learning Feed</div>
			<ul className="list-disc pl-6 text-sm text-violet-900">
				{items.map((n, i) => (<li key={i}>{n}</li>))}
			</ul>
		</div>
	);
}



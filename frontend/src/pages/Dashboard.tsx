import React, { useEffect, useState } from 'react';


import {
	fetchMe,
	fetchPositions,
	fetchRecommendations,
	applyOverride,
	fetchKpis,
	type Recommendation
} from '../lib/api';

// Section ID for demo (could be dynamic)
const SECTION_ID = 'SEC-001';

// Header with dashboard icon and title
function Header() {
	return (
		<div className="flex items-center gap-3 px-6 pt-6 pb-2">
			<h1 className="text-4xl font-extrabold text-gray-800">📊 Dashboard</h1>
		</div>
	);
}

// Map panel styled as in screenshot
function MapPanel({ positions }: { positions: Array<{ train_id: string; location_km: number; speed_kmph: number }> }) {
	// Demo stations and train icons/colors
	const stations = [
		{ name: 'Station X', pos: 0 },
		{ name: 'Station Y', pos: 100 },
	];
	// Place trains between 0-100 (km or %)
	const trainIcons: Record<string, string> = {
		'Local': '🚆',
		'Freight': '🚄',
	};
	const getTrainIcon = (id: string) => {
		if (/freight/i.test(id)) return '🚄';
		if (/local/i.test(id)) return '🚆';
		return '🚆';
	};
	const getTrainColor = (id: string) => {
		if (/freight/i.test(id)) return 'bg-purple-500';
		if (/local/i.test(id)) return 'bg-green-500';
		return 'bg-blue-500';
	};
	return (
		<div className="bg-white rounded-2xl p-6 shadow flex-1 min-w-[400px]">
			<div className="text-xl font-semibold text-violet-700 mb-2">Digital Twin: Live Train Map</div>
			<div className="relative h-48 flex flex-col justify-center items-center border rounded-xl bg-white">
				{/* Track line */}
				<div className="absolute left-10 right-10 top-1/2 h-1 bg-black" style={{ zIndex: 0 }} />
				{/* Stations */}
				<div className="absolute left-10 top-1/2 -translate-y-1/2 flex flex-col items-center" style={{zIndex:1}}>
					<div className="w-5 h-5 rounded-full bg-blue-700" />
					<span className="text-xs mt-1 font-semibold">Station X</span>
				</div>
				<div className="absolute right-10 top-1/2 -translate-y-1/2 flex flex-col items-center" style={{zIndex:1}}>
					<div className="w-5 h-5 rounded-full bg-blue-700" />
					<span className="text-xs mt-1 font-semibold">Station Y</span>
				</div>
				{/* Trains */}
				{positions.map((pos, idx) => (
					<div
						key={pos.train_id}
						className="absolute flex flex-col items-center"
						style={{ left: `calc(${10 + (pos.location_km ?? 0)}% - 18px)`, top: '40%' }}
					>
						<div className={`w-9 h-9 rounded-lg ${getTrainColor(pos.train_id)} flex items-center justify-center text-white text-2xl border-2 border-white shadow`}>
							{getTrainIcon(pos.train_id)}
						</div>
						<span className="text-xs mt-1 font-semibold" style={{color: getTrainColor(pos.train_id) === 'bg-green-500' ? '#22c55e' : '#a21caf'}}>
							{pos.train_id} ({Math.round(pos.location_km)}m)
						</span>
					</div>
				))}
			</div>
		</div>
	);
}

// KPIs panel styled as in screenshot
function KPIsPanel({ kpis }: {
	kpis: { throughput_per_hour?: number; avg_delay_minutes?: number; congestion_index?: number; on_time_percentage?: number } | null
}) {
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

// AI Recommendation card styled as in screenshot
function AIRecommendationCard({ recommendation, onAccept, onOverride }: {
	recommendation: Recommendation | null;
	onAccept: (rec: Recommendation) => void;
	onOverride: (rec: Recommendation) => void;
}) {
	if (!recommendation) return null;
	return (
		<div className="bg-green-100 rounded-2xl p-6 mt-6 shadow flex flex-col gap-3">
			<div className="text-lg font-semibold text-green-700 mb-1">AI Recommendation</div>
			<div className="text-base"><b>Decision:</b> <span className="font-semibold text-green-900">{recommendation.action}</span></div>
			<div className="text-base"><b>Reason:</b> <span className="font-semibold text-gray-900">{recommendation.reason}</span></div>
			<div className="flex gap-4 mt-2">
				<button className="bg-green-600 hover:bg-green-700 text-white font-bold px-6 py-2 rounded-lg text-lg" onClick={() => onAccept(recommendation)}>Accept</button>
				<button className="bg-red-600 hover:bg-red-700 text-white font-bold px-6 py-2 rounded-lg text-lg" onClick={() => onOverride(recommendation)}>Override</button>
			</div>
		</div>
	);
}



export default function Dashboard() {
	// User info
	const [user, setUser] = useState<{ username: string; role: string } | null>(null);
	// Train positions
	const [positions, setPositions] = useState<Array<{ train_id: string; location_km: number; speed_kmph: number }>>([]);
	// Recommendations
	const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
	const [recLoading, setRecLoading] = useState(false);
	const [recError, setRecError] = useState<string | null>(null);
	// KPIs
	const [kpis, setKpis] = useState<any>(null);
	// Accept/Override feedback
	const [actionMsg, setActionMsg] = useState<string | null>(null);

	// Fetch user info
	useEffect(() => {
		fetchMe().then(setUser).catch(() => setUser(null));
	}, []);

	// Fetch train positions every 5s
	useEffect(() => {
		let mounted = true;
		async function loadPositions() {
			try {
				const data = await fetchPositions();
				if (mounted) setPositions(data);
			} catch {}
		}
		loadPositions();
		const interval = setInterval(loadPositions, 5000);
		return () => { mounted = false; clearInterval(interval); };
	}, []);

	// Fetch recommendations
	async function loadRecommendations() {
		setRecLoading(true);
		setRecError(null);
		try {
			const data = await fetchRecommendations({ section_id: SECTION_ID, lookahead_minutes: 30 });
			setRecommendations(data.recommendations);
		} catch (e: any) {
			setRecError(e.message);
		} finally {
			setRecLoading(false);
		}
	}
	useEffect(() => { loadRecommendations(); }, []);

	// Fetch KPIs every 10s
	useEffect(() => {
		let mounted = true;
		async function loadKpis() {
			try {
				const data = await fetchKpis();
				if (mounted) setKpis(data);
			} catch {}
		}
		loadKpis();
		const interval = setInterval(loadKpis, 10000);
		return () => { mounted = false; clearInterval(interval); };
	}, []);

	// Accept recommendation
	async function handleAccept(rec: Recommendation) {
		setActionMsg(null);
		try {
			await applyOverride({
				controller_id: user?.username || 'ctrl-1',
				train_id: rec.train_id,
				action: rec.action,
				ai_action: rec.action,
				reason: rec.reason,
				timestamp: Date.now() / 1000
			});
			setActionMsg('Accepted!');
			loadRecommendations();
		} catch (e: any) {
			setActionMsg('Failed: ' + e.message);
		}
	}
	// Override recommendation (for demo, just re-apply with reason 'Manual override')
	async function handleOverride(rec: Recommendation) {
		setActionMsg(null);
		try {
			await applyOverride({
				controller_id: user?.username || 'ctrl-1',
				train_id: rec.train_id,
				action: rec.action,
				ai_action: rec.action,
				reason: 'Manual override',
				timestamp: Date.now() / 1000
			});
			setActionMsg('Override applied!');
			loadRecommendations();
		} catch (e: any) {
			setActionMsg('Failed: ' + e.message);
		}
	}

	// Use only the first recommendation for the AI card (screenshot style)
	const mainRecommendation = recommendations.length > 0 ? recommendations[0] : null;

	return (
		<div className="min-h-screen bg-gray-50">
			<Header />
			<div className="flex flex-row gap-6 px-8 mt-4">
				<div className="flex-1">
					<MapPanel positions={positions} />
				</div>
				<div className="w-[350px]">
					<KPIsPanel kpis={kpis} />
				</div>
			</div>
			<div className="px-8">
				<AIRecommendationCard
					recommendation={mainRecommendation}
					onAccept={handleAccept}
					onOverride={handleOverride}
				/>
				{actionMsg && <div className="text-center text-sm text-green-600 mt-2">{actionMsg}</div>}
			</div>
		</div>
	);
}



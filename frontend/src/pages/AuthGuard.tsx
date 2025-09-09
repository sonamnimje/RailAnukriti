import { useEffect, useState } from 'react'
import { Navigate } from 'react-router-dom'
import { fetchMe } from '../lib/api'

export default function AuthGuard({ children }: { children: JSX.Element }) {
	const [status, setStatus] = useState<'checking' | 'ok' | 'nope'>('checking')
	useEffect(() => {
		fetchMe().then(() => setStatus('ok')).catch(() => setStatus('nope'))
	}, [])
	if (status === 'checking') return <div className="p-6">Checking session...</div>
	if (status === 'nope') return <Navigate to="/login" replace />
	return children
}



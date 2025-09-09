import React, { useEffect, useState } from 'react'
import { fetchMe } from '../lib/api'

export default function RoleGuard({ allow, children }: { allow: Array<'controller' | 'admin'>; children: JSX.Element }) {
	const [status, setStatus] = useState<'checking' | 'ok' | 'nope'>('checking')
	useEffect(() => {
		fetchMe()
			.then((me) => setStatus(allow.includes(me.role as any) ? 'ok' : 'nope'))
			.catch(() => setStatus('nope'))
	}, [allow])
	if (status === 'checking') return <div className="p-6">Checking permissions...</div>
	if (status === 'nope') return <div className="p-6">You do not have access to this page.</div>
	return children
}



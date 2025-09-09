import React, { useState } from 'react';
import { signup, login, fetchMe } from '../lib/api';


export default function SignupPage({ onSuccess }: { onSuccess: () => void }) {
	const [form, setForm] = useState({ name: '', email: '', password: '', confirm: '', role: 'controller' as 'controller' | 'admin' });
	const [error, setError] = useState<string | null>(null);
	const [loading, setLoading] = useState(false);
// Removed agree state for Terms & Conditions

	async function handleSubmit(e: React.FormEvent) {
		e.preventDefault();
		setError(null);
		if (form.password !== form.confirm) {
			setError('Passwords do not match');
			return;
		}
		setLoading(true);
		try {
			   await signup(form.email, form.password, form.role);
			   await login(form.email, form.password);
			   await fetchMe();
			   onSuccess();
		   } catch (e: any) {
			   // Show a friendly message if user already exists
			   if (typeof e.message === 'string' && e.message.includes('Username already exists')) {
				   setError('User already registered');
			   } else {
				   setError(e.message);
			   }
		   } finally {
			   setLoading(false);
		   }
	}

	return (
		<div className="min-h-screen flex items-center justify-center relative auth-bg">
			<div className="absolute inset-0 auth-overlay" />
			<div className="relative z-10 w-full max-w-md mx-auto p-8 sm:p-10 glass-card rounded-2xl">
				<form onSubmit={handleSubmit} className="w-full flex flex-col gap-6">
					<h2 className="text-3xl font-bold text-white tracking-tight text-center">Create your account</h2>
					<div className="flex flex-col gap-2">
						<label className="text-sm text-white/90 font-medium">NAME</label>
						<input
							className="rounded-lg px-4 py-3 border border-white/20 focus:border-white/40 focus:ring-2 focus:ring-white/20 outline-none bg-white/90 text-gray-900 placeholder:text-gray-500"
							placeholder="Enter your name"
							type="text"
							value={form.name}
							onChange={e => setForm({ ...form, name: e.target.value })}
							autoComplete="name"
							required
						/>
					</div>
					<div className="flex flex-col gap-2">
						<label className="text-sm text-white/90 font-medium">E-MAIL ADDRESS</label>
						<input
							className="rounded-lg px-4 py-3 border border-white/20 focus:border-white/40 focus:ring-2 focus:ring-white/20 outline-none bg-white/90 text-gray-900 placeholder:text-gray-500"
							placeholder="Enter your email"
							type="email"
							value={form.email}
							onChange={e => setForm({ ...form, email: e.target.value })}
							autoComplete="email"
							required
						/>
					</div>
					<div className="flex flex-col gap-2">
						<label className="text-sm text-white/90 font-medium">PASSWORD</label>
						<input
							type="password"
							className="rounded-lg px-4 py-3 border border-white/20 focus:border-white/40 focus:ring-2 focus:ring-white/20 outline-none bg-white/90 text-gray-900 placeholder:text-gray-500"
							placeholder="Enter your password"
							value={form.password}
							onChange={e => setForm({ ...form, password: e.target.value })}
							autoComplete="new-password"
							required
						/>
					</div>
					<div className="flex flex-col gap-2">
						<label className="text-sm text-white/90 font-medium">CONFIRM PASSWORD</label>
						<input
							type="password"
							className="rounded-lg px-4 py-3 border border-white/20 focus:border-white/40 focus:ring-2 focus:ring-white/20 outline-none bg-white/90 text-gray-900 placeholder:text-gray-500"
							placeholder="Confirm your password"
							value={form.confirm}
							onChange={e => setForm({ ...form, confirm: e.target.value })}
							autoComplete="new-password"
							required
						/>
					</div>
					<div className="flex flex-col gap-2">
						<label className="text-sm text-white/90 font-medium">ROLE</label>
						<select
							className="rounded-lg px-4 py-3 border border-white/20 focus:border-white/40 focus:ring-2 focus:ring-white/20 outline-none bg-white/90 text-gray-900"
							value={form.role}
							onChange={e => setForm({ ...form, role: e.target.value as 'controller' | 'admin' })}
						>
							<option value="controller">Controller</option>
							<option value="admin">Admin</option>
						</select>
					</div>
					<button
						className="w-full rounded-lg px-4 py-3 bg-blue-600 text-white font-semibold hover:bg-blue-700 transition disabled:opacity-60 shadow-md"
						disabled={loading}
						type="submit"
					>
						{loading ? 'Signing up…' : 'Sign Up'}
					</button>
					{error && <div className="text-red-300 text-center text-sm">{error}</div>}
					<div className="text-center mt-2">
						<a className="text-white/90 text-sm hover:underline" href="/login">Already have an account?</a>
					</div>
				</form>
			</div>
		</div>
	);
	}

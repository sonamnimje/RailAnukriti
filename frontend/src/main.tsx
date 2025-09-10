import React from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import { BrowserRouter, Route, Routes } from 'react-router-dom'

import Layout from './pages/Layout';
import AuthGuard from './pages/AuthGuard';
import LoginPage from './pages/Login';
import SignupPage from './pages/Signup';
import ForgotPasswordPage from './pages/ForgotPassword';
import RoleGuard from './pages/RoleGuard';
import LogsPage from './pages/Logs';
import SimulationPage from './pages/Simulation';
import OverridesPage from './pages/Overrides';
import ReportsPage from './pages/Reports';
import SettingsPage from './pages/Settings';
import HomePage from './pages/Home';
import DashboardPage from './pages/Dashboard';

import { Navigate } from 'react-router-dom';

const root = createRoot(document.getElementById('root')!)


root.render(
	<React.StrictMode>
		<BrowserRouter>
			<Routes>
				<Route path="/login" element={<LoginPage onSuccess={() => location.replace('/app/dashboard')} />} />
				<Route path="/signup" element={<SignupPage onSuccess={() => location.replace('/')} />} />
				<Route path="/forgot-password" element={<ForgotPasswordPage />} />
				{/* All other pages (including Home) use Layout */}
				<Route element={<Layout />}>
					<Route path="/" element={<HomePage />} />
					<Route path="/app/dashboard" element={<DashboardPage />} />
					
					<Route path="/app/logs" element={<LogsPage />} />
					<Route path="/app/simulation" element={<SimulationPage />} />
					<Route path="/app/overrides" element={<OverridesPage />} />
					<Route path="/app/reports" element={<ReportsPage />} />
					<Route
						path="/app/settings"
						element={
							<RoleGuard allow={['admin']}>
								<SettingsPage />
							</RoleGuard>
						}
					/>
				</Route>
				{/* Catch-all route to redirect unknown paths to Home */}
				<Route path="*" element={<Navigate to="/" replace />} />
			</Routes>
		</BrowserRouter>
	</React.StrictMode>
)



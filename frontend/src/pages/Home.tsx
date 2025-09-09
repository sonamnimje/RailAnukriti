import React, { useState } from 'react';

function Home() {
  const [showModal, setShowModal] = useState(false);

  const handleNavigate = (path: string) => {
    window.location.href = path;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100 relative overflow-hidden">
      {/* Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        {/* City Skyline Background */}
        <div className="absolute bottom-0 left-0 w-full h-32 bg-gradient-to-t from-blue-200 to-transparent">
          <div className="absolute bottom-0 left-0 w-full h-24 bg-blue-300 opacity-30">
            {/* Simple city skyline shapes */}
            <div className="absolute bottom-0 left-0 w-8 h-16 bg-blue-400"></div>
            <div className="absolute bottom-0 left-12 w-6 h-20 bg-blue-400"></div>
            <div className="absolute bottom-0 left-24 w-10 h-12 bg-blue-400"></div>
            <div className="absolute bottom-0 left-40 w-7 h-18 bg-blue-400"></div>
            <div className="absolute bottom-0 left-56 w-9 h-14 bg-blue-400"></div>
            <div className="absolute bottom-0 left-72 w-6 h-22 bg-blue-400"></div>
            <div className="absolute bottom-0 left-84 w-8 h-16 bg-blue-400"></div>
            <div className="absolute bottom-0 left-96 w-5 h-20 bg-blue-400"></div>
            <div className="absolute bottom-0 right-0 w-12 h-10 bg-blue-400"></div>
          </div>
        </div>
        
        {/* Train in background */}
        <div className="absolute bottom-8 left-1/4 w-32 h-8 bg-gray-300 rounded-lg opacity-40">
          <div className="absolute top-1 left-2 w-6 h-6 bg-gray-400 rounded-full"></div>
          <div className="absolute top-1 right-2 w-6 h-6 bg-gray-400 rounded-full"></div>
        </div>
        
        {/* Clouds */}
        <div className="absolute top-20 right-20 w-16 h-8 bg-white rounded-full opacity-60"></div>
        <div className="absolute top-32 left-20 w-12 h-6 bg-white rounded-full opacity-60"></div>
        <div className="absolute top-16 left-1/2 w-20 h-10 bg-white rounded-full opacity-60"></div>
      </div>

      {/* Main Hero Section */}
      <main className="relative z-10 flex items-center justify-between px-6 py-12 max-w-7xl mx-auto">
        {/* Left Side - Text Content */}
        <div className="flex-1 max-w-2xl">
          <h1 className="text-6xl font-bold text-teal-700 mb-2">RailAnukriti</h1>
          <p className="text-2xl text-teal-500 mb-6">AI-Powered Smart Train Traffic Optimizer</p>
          <p className="text-gray-600 text-lg mb-8 leading-relaxed">
            Maximize section throughput using AI-powered precise train traffic control. 
            Our intelligent system optimizes train precedence, crossings, and platform allocation 
            to minimize delays and improve efficiency across Indian Railways.
          </p>
          <button
            className="px-8 py-4 bg-orange-500 text-white font-bold text-lg rounded-lg hover:bg-orange-600 transition shadow-lg"
            onClick={() => setShowModal(true)}
          >
            GET STARTED
          </button>
        </div>

        {/* Right Side - Mobile App Illustration */}
        <div className="flex-1 flex justify-center items-center relative">
          {/* Mobile Phone Mockup */}
          <div className="relative">
            <div className="w-80 h-96 bg-blue-200 rounded-3xl p-4 shadow-2xl transform rotate-6">
              <div className="w-full h-full bg-white rounded-2xl overflow-hidden">
                {/* Phone Header */}
                <div className="bg-blue-100 px-4 py-2 flex justify-between items-center">
                  <span className="text-sm font-mono">00:00</span>
                  <span className="text-sm font-bold">Ticket</span>
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                    <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  </div>
                </div>
                
                {/* Ticket Display */}
                <div className="p-4">
                  <div className="bg-green-100 rounded-lg p-3 mb-4 flex items-center justify-between">
                    <div className="w-8 h-8 bg-teal-500 rounded flex items-center justify-center">
                      <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M2 6a2 2 0 012-2h6l2 2h6a2 2 0 012 2v6a2 2 0 01-2 2H4a2 2 0 01-2-2V6zM14.553 7.106A1 1 0 0014 8v4a1 1 0 00.553.894l2 1A1 1 0 0018 13V7a1 1 0 00-1.447-.894l-2 1z"/>
                      </svg>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-bold">Express Train</div>
                      <div className="text-xs text-gray-600">Delhi → Mumbai</div>
                    </div>
                  </div>
                  
                  {/* Map Section */}
                  <div className="bg-gray-100 rounded-lg h-32 relative">
                    <div className="absolute inset-0 flex items-center justify-center">
                      <div className="w-full h-16 bg-green-200 rounded relative">
                        <div className="absolute top-2 left-2 w-3 h-3 bg-black rounded-full"></div>
                        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-1 h-8 bg-green-500"></div>
                      </div>
                    </div>
                  </div>
                  
                  {/* Bottom Actions */}
                  <div className="flex items-center justify-between mt-4">
                    <button className="w-12 h-12 bg-blue-500 rounded-lg flex items-center justify-center">
                      <span className="text-white font-bold">₹</span>
                    </button>
                    <div className="w-16 h-8 bg-white border border-gray-300 rounded flex items-center justify-center">
                      <div className="w-12 h-4 bg-black"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            {/* Character Illustration */}
            <div className="absolute -right-8 top-16">
              <div className="w-16 h-20 bg-yellow-400 rounded-t-full relative">
                {/* Head */}
                <div className="absolute -top-2 left-1/2 transform -translate-x-1/2 w-6 h-6 bg-yellow-300 rounded-full"></div>
                {/* Body */}
                <div className="absolute top-2 left-1/2 transform -translate-x-1/2 w-8 h-12 bg-yellow-400"></div>
                {/* Pants */}
                <div className="absolute top-10 left-1/2 transform -translate-x-1/2 w-8 h-8 bg-teal-500"></div>
                {/* Arms */}
                <div className="absolute top-4 -left-1 w-2 h-6 bg-yellow-300 rounded"></div>
                <div className="absolute top-4 -right-1 w-2 h-6 bg-yellow-300 rounded"></div>
                {/* Ticket in hand */}
                <div className="absolute top-6 -left-3 w-3 h-4 bg-green-200 rounded"></div>
                {/* Suitcase */}
                <div className="absolute top-12 -right-4 w-6 h-4 bg-blue-500 rounded"></div>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Features Section */}
      <section className="relative z-10 px-6 py-16 bg-white/80 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-gray-800 mb-12">Core Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <FeatureCard
              title="AI-Powered Optimization"
              description="Advanced algorithms optimize train schedules and routes for maximum efficiency and minimal delays."
              icon={<svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" /></svg>}
            />
            <FeatureCard
              title="Real-time Simulation"
              description="Test scenarios and disruptions using our digital twin technology for better planning."
              icon={<svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" /><path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6l4 2" /></svg>}
            />
            <FeatureCard
              title="Live Monitoring"
              description="Monitor train status and network health in real-time with intuitive dashboards."
              icon={<svg className="w-8 h-8 text-yellow-500" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="2" /><path strokeLinecap="round" strokeLinejoin="round" d="M8 9h8M8 13h6M8 17h4" /></svg>}
            />
            <FeatureCard
              title="Human-in-the-Loop"
              description="Controllers can override AI decisions with adaptive learning from past interactions."
              icon={<svg className="w-8 h-8 text-purple-500" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><circle cx="12" cy="8" r="4" /><path strokeLinecap="round" strokeLinejoin="round" d="M6 20v-2a4 4 0 018 0v2" /></svg>}
            />
            <FeatureCard
              title="Comprehensive Reports"
              description="Generate detailed analytics on performance, delays, and resource utilization."
              icon={<svg className="w-8 h-8 text-pink-500" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>}
            />
            <FeatureCard
              title="Adaptive Learning"
              description="System learns from delays and overrides to make smarter decisions over time."
              icon={<svg className="w-8 h-8 text-red-500" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>}
            />
          </div>
        </div>
      </section>

      {/* Modal Popup */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40">
          <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-sm flex flex-col items-center relative">
            <button
              className="absolute top-2 right-2 text-gray-400 hover:text-gray-600 text-2xl"
              onClick={() => setShowModal(false)}
              aria-label="Close"
            >
              &times;
            </button>
            <h3 className="text-2xl font-bold text-gray-900 mb-4">Get Started</h3>
            <p className="text-gray-600 mb-6 text-center">Sign in or create an account to access all features.</p>
            <div className="flex gap-4 w-full">
              <button
                className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition"
                onClick={() => handleNavigate('/login')}
              >
                Login
              </button>
              <button
                className="flex-1 px-4 py-2 bg-gray-200 text-blue-700 rounded-lg font-semibold hover:bg-blue-100 transition"
                onClick={() => handleNavigate('/signup')}
              >
                Sign Up
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// FeatureCard component
function FeatureCard({ title, description, icon }: { title: string; description: string; icon: React.ReactNode }) {
  return (
    <div className="flex flex-col items-center bg-white rounded-xl p-6 border border-gray-200 hover:border-blue-300 transition">
      <div className="mb-3">{icon}</div>
      <h3 className="text-lg font-semibold text-gray-900 mb-1 text-center">{title}</h3>
      <p className="text-gray-600 text-center text-sm">{description}</p>
    </div>
  );
}

export default Home;

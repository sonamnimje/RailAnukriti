import React, { useState } from 'react';

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    // Simulate API call
    if (!email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
      setError('Please enter a valid email address.');
      return;
    }
    setSubmitted(true);
  }

  return (
    <div className="min-h-screen flex items-center justify-center relative auth-bg">
      <div className="absolute inset-0 auth-overlay" />
      <div className="relative z-10 w-full max-w-md mx-auto p-8 sm:p-10 glass-card rounded-2xl">
        <form onSubmit={handleSubmit} className="w-full flex flex-col gap-6">
          <h2 className="text-3xl font-bold text-white tracking-tight text-center">Forgot Password</h2>
          {submitted ? (
            <div className="text-green-300 text-center text-lg">If an account exists for this email, a reset link has been sent.</div>
          ) : (
            <>
              <div className="flex flex-col gap-2">
                <label className="text-sm text-white/90 font-medium">E-MAIL ADDRESS</label>
                <input
                  className="rounded-lg px-4 py-3 border border-white/20 focus:border-white/40 focus:ring-2 focus:ring-white/20 outline-none bg-white/90 text-gray-900 placeholder:text-gray-500"
                  placeholder="Enter your email"
                  value={email}
                  onChange={e => setEmail(e.target.value)}
                  autoComplete="email"
                  type="email"
                  required
                />
              </div>
              <button
                className="w-full rounded-lg px-4 py-3 bg-blue-600 text-white font-semibold hover:bg-blue-700 transition disabled:opacity-60 shadow-md"
                type="submit"
              >
                Send Reset Link
              </button>
              {error && <div className="text-red-300 text-center text-sm">{error}</div>}
            </>
          )}
          <div className="text-center mt-2">
            <a className="text-white/90 text-sm hover:underline" href="/login">Back to login</a>
          </div>
        </form>
      </div>
    </div>
  );
}

import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { API_BASE_URL } from '../services/api';

const SignIn: React.FC = () => {
  const location = useLocation();
  const [error, setError] = useState('');

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    if (params.get('error') === 'oauth_timeout') {
      setError('Google OAuth request timed out due to network connection. Please retry.');
    }
  }, [location.search]);

  const handleGoogleLogin = () => {
    window.location.href = `${API_BASE_URL}/auth/google/start`;
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-6">
      <div className="bg-white p-10 rounded-3xl border-2 border-gray-200 shadow-xl max-w-md w-full text-center">
        <div className="w-16 h-16 rounded-2xl bg-green-500 text-white font-black text-4xl flex items-center justify-center mx-auto mb-4 border-b-4 border-green-700 shadow-md">
          C
        </div>
        <h1 className="text-3xl font-black text-gray-900 mb-2">Welcome to CLARIO</h1>
        <p className="text-gray-500 text-sm font-medium mb-8">Sign in to continue your personal learning journey</p>

        {error && <div className="p-3 mb-6 bg-red-50 text-red-600 rounded-xl text-sm font-bold border border-red-200">{error}</div>}

        <div className="space-y-4">
          <button
            onClick={handleGoogleLogin}
            className="w-full bg-white hover:bg-gray-50 text-gray-700 font-extrabold py-4 px-6 rounded-2xl border-2 border-gray-300 shadow-sm flex items-center justify-center gap-3 transition-all cursor-pointer"
          >
            <svg className="w-6 h-6" viewBox="0 0 24 24">
              <path
                fill="#4285F4"
                d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
              />
              <path
                fill="#34A853"
                d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
              />
              <path
                fill="#FBBC05"
                d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"
              />
              <path
                fill="#EA4335"
                d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"
              />
            </svg>
            Continue with Google
          </button>
        </div>
      </div>
    </div>
  );
};

export default SignIn;

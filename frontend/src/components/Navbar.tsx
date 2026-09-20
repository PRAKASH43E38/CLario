import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../services/api';

interface UserStats {
  xp: number;
  clarity: number;
  clarity_streak: number;
  level: number;
  title: string;
}

const Navbar: React.FC = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState<UserStats | null>(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await api.get('/user/stats');
        setStats(res.data);
      } catch (err) {
        // Silently handle if unauthenticated
      }
    };
    fetchStats();
  }, []);

  const handleLogout = async () => {
    try {
      await api.post('/auth/logout');
    } catch (e) {
      // Ignore
    }
    navigate('/signin');
  };

  return (
    <nav className="bg-white border-b-2 border-green-100 sticky top-0 z-50 px-6 py-3 shadow-xs" role="navigation" aria-label="Main navigation">
      <div className="max-w-6xl mx-auto flex items-center justify-between">
        <Link to="/home" className="flex items-center gap-2 group" aria-label="Go to home">
          <div className="w-10 h-10 rounded-xl bg-green-500 text-white font-black text-2xl flex items-center justify-center shadow-md group-hover:scale-105 transition-transform" aria-hidden="true">
            C
          </div>
          <div>
            <span className="font-extrabold text-2xl tracking-wider text-green-900">CLARIO</span>
            <span className="block text-[10px] font-bold text-green-600 tracking-widest uppercase">Conceptual Clarity</span>
          </div>
        </Link>

        {stats && (
          <div className="flex items-center gap-4" aria-hidden="true">
            <div className="flex items-center gap-2 bg-yellow-50 px-3 py-1.5 rounded-xl border border-yellow-200">
              <span className="text-lg">⚡</span>
              <div>
                <div className="text-[10px] font-bold uppercase text-yellow-700">XP</div>
                <div className="font-extrabold text-sm text-yellow-800">{stats.xp}</div>
              </div>
            </div>

            <div className="flex items-center gap-2 bg-blue-50 px-3 py-1.5 rounded-xl border border-blue-200">
              <span className="text-lg">🎯</span>
              <div>
                <div className="text-[10px] font-bold uppercase text-blue-700">Clarity</div>
                <div className="font-extrabold text-sm text-blue-800">{stats.clarity}%</div>
              </div>
            </div>

            <div className="flex items-center gap-2 bg-orange-50 px-3 py-1.5 rounded-xl border border-orange-200">
              <span className="text-lg">🔥</span>
              <div>
                <div className="text-[10px] font-bold uppercase text-orange-700">Streak</div>
                <div className="font-extrabold text-sm text-orange-800">{stats.clarity_streak} days</div>
              </div>
            </div>
          </div>
        )}

        <div className="flex items-center gap-4">
          <Link to="/home" className="font-bold text-green-800 hover:text-green-600 transition-colors" aria-label="Home link">
            Home
          </Link>
          <Link to="/insights" className="font-bold text-green-800 hover:text-green-600 transition-colors" aria-label="Insights link">
            Insights
          </Link>
          <button
            onClick={handleLogout}
            aria-label="Sign out"
            title="Sign out"
            className="text-xs font-bold text-red-600 hover:text-red-800 bg-red-50 hover:bg-red-100 px-3 py-2 rounded-xl transition-colors border border-red-200 cursor-pointer"
          >
            Sign Out
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;

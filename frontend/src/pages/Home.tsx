import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import api from '../services/api';

interface LearningSession {
  id: number;
  task: string;
  goal: string;
  status: string;
  created_at: string;
}

interface UserStats {
  xp: number;
  clarity: number;
  clarity_streak: number;
  level: number;
  title: string;
}

interface Achievement {
  id: number;
  code: string;
  title: string;
  icon: string;
  unlocked: boolean;
}

interface LearnerInsight {
  id: number;
  insight_text: string;
  category: string;
}

const Home: React.FC = () => {
  const navigate = useNavigate();
  const [sessions, setSessions] = useState<LearningSession[]>([]);
  const [stats, setStats] = useState<UserStats | null>(null);
  const [achievements, setAchievements] = useState<Achievement[]>([]);
  const [insights, setInsights] = useState<LearnerInsight[]>([]);

  // loading for dashboard data
  const [dashboardLoading, setDashboardLoading] = useState(true);

  // 4 Intake inputs for new learning session
  const [task, setTask] = useState('');
  const [goal, setGoal] = useState('');
  const [learnerState, setLearnerState] = useState('');
  const [interests, setInterests] = useState('');

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      setDashboardLoading(true);
      try {
        const [sessRes, statsRes, achRes, insRes] = await Promise.all([
          api.get('/sessions'),
          api.get('/user/stats'),
          api.get('/user/achievements'),
          api.get('/user/insights'),
        ]);
        setSessions(sessRes.data);
        setStats(statsRes.data);
        setAchievements(achRes.data);
        setInsights(insRes.data);
      } catch (err) {
        console.error('Error fetching dashboard data:', err);
      } finally {
        setDashboardLoading(false);
      }
    };
    fetchData();
  }, []);

  const handleStartSession = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const res = await api.post('/sessions', {
        task,
        goal,
        learner_state: learnerState,
        interests,
      });
      navigate(`/roadmap/${res.data.id}`);
    } catch (err) {
      console.error('Failed to create session:', err);
      setError('Could not start new learning session. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const activeSession = sessions.find((s) => s.status === 'active') || sessions[0];

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Navbar />

      <main className="max-w-6xl w-full mx-auto p-6 space-y-8 my-4">
        {/* Greeting Banner */}
        <div className="bg-gradient-to-r from-green-600 to-emerald-700 rounded-3xl p-8 text-white shadow-xl flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
          <div>
            <span className="inline-block px-3 py-1 rounded-full bg-white/20 text-white font-extrabold text-xs uppercase tracking-wider mb-2 backdrop-blur-xs">
              Level {stats?.level || 1} • {stats?.title || 'Curious Explorer'}
            </span>
            <h1 className="text-4xl font-black">Welcome back, Learner! 👋</h1>
            <p className="text-green-100 font-medium text-lg mt-1">
              "Come confused. Leave with clarity." Ready to make concepts click today?
            </p>
          </div>

          {activeSession && (
            <button
              onClick={() => navigate(`/roadmap/${activeSession.id}`)}
              className="bg-white hover:bg-yellow-300 text-green-900 font-extrabold text-lg py-4 px-8 rounded-2xl border-b-4 border-yellow-500 active:border-b-0 active:translate-y-1 transition-all shadow-lg cursor-pointer whitespace-nowrap"
            >
              Continue Learning →
            </button>
          )}
        </div>

        {/* Core Layout Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="md:col-span-3 grid grid-cols-1 md:grid-cols-3 gap-4" aria-live="polite">
            {dashboardLoading ? (
              [0,1,2].map((i) => (
                <div key={i} className="p-5">
                  <div className="h-20 skeleton" style={{borderRadius:12}} aria-hidden="true" />
                </div>
              ))
            ) : (
              <>
                <div className="bg-white border-2 border-green-100 rounded-3xl p-5 shadow-sm">
                  <div className="text-xs uppercase tracking-widest font-extrabold text-green-700 mb-2">Momentum</div>
                  <div className="text-3xl font-black text-gray-900">{stats?.xp ?? 0}</div>
                  <div className="text-sm text-gray-500 mt-1">XP gained in your learning streak</div>
                </div>
                <div className="bg-white border-2 border-blue-100 rounded-3xl p-5 shadow-sm">
                  <div className="text-xs uppercase tracking-widest font-extrabold text-blue-700 mb-2">Clarity</div>
                  <div className="text-3xl font-black text-gray-900">{stats?.clarity ?? 0}%</div>
                  <div className="text-sm text-gray-500 mt-1">Current conceptual confidence</div>
                </div>
                <div className="bg-white border-2 border-yellow-100 rounded-3xl p-5 shadow-sm">
                  <div className="text-xs uppercase tracking-widest font-extrabold text-yellow-700 mb-2">Learning Flow</div>
                  <div className="text-3xl font-black text-gray-900">{sessions.length}</div>
                  <div className="text-sm text-gray-500 mt-1">Sessions built with your context</div>
                </div>
              </>
            )}
          </div>

          {/* Main 2 Column Section */}
          <div className="md:col-span-2 space-y-8">
            {/* New Learning Session Form (4 Inputs) */}
            <div className="bg-white p-8 rounded-3xl border-2 border-gray-200 shadow-sm">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-2xl bg-green-500 text-white font-black text-xl flex items-center justify-center">
                  🌱
                </div>
                <div>
                  <h2 className="text-2xl font-black text-gray-800">New Learning Session</h2>
                  <p className="text-xs font-bold text-gray-400">Tell CLARIO what you want to achieve today</p>
                </div>
              </div>

              {error && <div className="p-3 mb-4 bg-red-50 text-red-600 rounded-xl text-sm font-bold">{error}</div>}

              <form onSubmit={handleStartSession} className="space-y-4">
                <div>
                  <label className="block text-xs font-extrabold uppercase text-gray-500 mb-1">
                    1. TASK — What do you want to learn or accomplish?
                  </label>
                  <input
                    type="text"
                    required
                    value={task}
                    onChange={(e) => setTask(e.target.value)}
                    placeholder="e.g. Learn Machine Learning Fundamentals"
                    className="w-full p-3.5 border-2 border-gray-200 rounded-2xl font-medium focus:border-green-500 focus:outline-none"
                  />
                </div>

                <div>
                  <label className="block text-xs font-extrabold uppercase text-gray-500 mb-1">
                    2. GOAL — What should become clear by the end?
                  </label>
                  <input
                    type="text"
                    required
                    value={goal}
                    onChange={(e) => setGoal(e.target.value)}
                    placeholder="e.g. Understand how a model learns from data via gradient descent"
                    className="w-full p-3.5 border-2 border-gray-200 rounded-2xl font-medium focus:border-green-500 focus:outline-none"
                  />
                </div>

                <div>
                  <label className="block text-xs font-extrabold uppercase text-gray-500 mb-1">
                    3. LEARNER STATE — What do you already know? Where are you stuck?
                  </label>
                  <textarea
                    required
                    value={learnerState}
                    onChange={(e) => setLearnerState(e.target.value)}
                    placeholder="e.g. I know basic Python and algebra, but calculus concepts feel confusing."
                    className="w-full p-3.5 border-2 border-gray-200 rounded-2xl font-medium focus:border-green-500 focus:outline-none min-h-20"
                  />
                </div>

                <div>
                  <label className="block text-xs font-extrabold uppercase text-gray-500 mb-1">
                    4. INTERESTS — What interests or examples should we use?
                  </label>
                  <input
                    type="text"
                    value={interests}
                    onChange={(e) => setInterests(e.target.value)}
                    placeholder="e.g. Robotics, video games, sports"
                    className="w-full p-3.5 border-2 border-gray-200 rounded-2xl font-medium focus:border-green-500 focus:outline-none"
                  />
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full bg-green-500 hover:bg-green-600 disabled:opacity-50 text-white font-extrabold text-lg py-4 rounded-2xl border-b-4 border-green-700 active:border-b-0 active:translate-y-1 transition-all cursor-pointer shadow-md mt-2"
                >
                  {loading ? 'Building personalized AI roadmap...' : 'Generate Personalized Learning Map →'}
                </button>
              </form>
            </div>

            {/* Daily Mission Card */}
            <div className="bg-white p-6 rounded-3xl border-2 border-gray-200 shadow-sm flex items-center gap-6">
              <div className="w-16 h-16 rounded-2xl bg-yellow-100 text-yellow-700 flex items-center justify-center text-3xl font-black border-2 border-yellow-300">
                🎯
              </div>
              <div className="flex-1">
                <div className="text-xs font-bold text-yellow-700 uppercase tracking-wider">Daily Mission</div>
                <h3 className="font-extrabold text-gray-800 text-lg">Solve 1 Reasoning or Application Challenge</h3>
                <p className="text-xs text-gray-500">Earn +20 Clarity & unlock Consistency Builder achievement</p>
              </div>
              <span className="font-black text-green-600 bg-green-50 px-4 py-2 rounded-xl border border-green-200">
                +20 Clarity
              </span>
            </div>
          </div>

          {/* Sidebar Section */}
          <div className="space-y-8">
            {/* Learner Insights */}
            <div className="bg-white p-6 rounded-3xl border-2 border-gray-200 shadow-sm">
              <h3 className="font-extrabold text-gray-800 text-lg mb-4 flex items-center gap-2">
                <span>💡</span> Learning Insights
              </h3>
              <div className="space-y-3" aria-live="polite">
                {insights.length === 0 ? (
                  <div className="p-3.5 bg-blue-50 rounded-2xl border border-blue-200 text-xs font-medium text-blue-900 leading-relaxed">
                    No insights yet — try completing a learning activity to collect evidence of your learning.
                  </div>
                ) : (
                  insights.map((ins) => (
                    <div key={ins.id} className="p-3.5 bg-blue-50 rounded-2xl border border-blue-200 text-xs font-medium text-blue-900 leading-relaxed">
                      "{ins.insight_text}"
                    </div>
                  ))
                )}
              </div>
            </div>

            {/* Recent Achievements */}
            <div className="bg-white p-6 rounded-3xl border-2 border-gray-200 shadow-sm">
              <h3 className="font-extrabold text-gray-800 text-lg mb-4 flex items-center gap-2">
                <span>🏆</span> Achievements
              </h3>
              <div className="grid grid-cols-2 gap-3">
                {achievements.map((ach) => (
                  <div
                    key={ach.id}
                    className={`p-3 rounded-2xl border text-center transition-all ${
                      ach.unlocked
                        ? 'bg-yellow-50 border-yellow-300 text-yellow-900 shadow-xs'
                        : 'bg-gray-50 border-gray-200 text-gray-400 opacity-60'
                    }`}
                  >
                    <div className="text-2xl mb-1">{ach.icon}</div>
                    <div className="text-xs font-extrabold leading-tight">{ach.title}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Home;

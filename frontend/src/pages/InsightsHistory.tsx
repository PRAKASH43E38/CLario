import React, { useEffect, useState } from 'react';
import Navbar from '../components/Navbar';
import api from '../services/api';

interface LearnerInsight {
  id: number;
  insight_text: string;
  category: string;
  created_at: string;
}

interface Achievement {
  id: number;
  code: string;
  title: string;
  description: string;
  icon: string;
  xp_reward: number;
  clarity_reward: number;
  unlocked: boolean;
  unlocked_at?: string;
}

const InsightsHistory: React.FC = () => {
  const [insights, setInsights] = useState<LearnerInsight[]>([]);
  const [achievements, setAchievements] = useState<Achievement[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [insRes, achRes] = await Promise.all([
          api.get('/user/insights'),
          api.get('/user/achievements'),
        ]);
        setInsights(insRes.data);
        setAchievements(achRes.data);
      } catch (err) {
        console.error('Failed to load insights:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col">
        <Navbar />
        <div className="flex-1 flex items-center justify-center">
          <div className="w-12 h-12 border-4 border-green-500 border-t-transparent rounded-full animate-spin" role="status" aria-live="polite">
            <span className="sr-only">Loading insights</span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Navbar />

      <main className="max-w-5xl w-full mx-auto p-6 space-y-8 my-4">
        <div className="bg-white p-8 rounded-3xl border-2 border-gray-200 shadow-sm">
          <h1 className="text-3xl font-black text-gray-900 mb-2">Learner Insights & Evidence</h1>
          <p className="text-gray-500 font-medium">
            Evidence-based observations continuously derived from your learning behavior and reasoning exercises.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Insights List */}
          <div className="bg-white p-6 rounded-3xl border-2 border-gray-200 shadow-sm space-y-4">
            <h2 className="text-xl font-extrabold text-gray-800 flex items-center gap-2">
              <span>💡</span> Personal Learning Observations
            </h2>
            <div className="space-y-3">
              {insights.map((ins) => (
                <div key={ins.id} className="p-4 bg-green-50 rounded-2xl border border-green-200 text-sm font-medium text-green-900 leading-relaxed">
                  "{ins.insight_text}"
                </div>
              ))}
            </div>
          </div>

          {/* Achievements Grid */}
          <div className="bg-white p-6 rounded-3xl border-2 border-gray-200 shadow-sm space-y-4">
            <h2 className="text-xl font-extrabold text-gray-800 flex items-center gap-2">
              <span>🏆</span> Unlocked Achievements
            </h2>
            <div className="space-y-3">
              {achievements.map((ach) => (
                <div
                  key={ach.id}
                  className={`p-4 rounded-2xl border flex items-center gap-4 ${
                    ach.unlocked
                      ? 'bg-yellow-50 border-yellow-300 text-yellow-900'
                      : 'bg-gray-50 border-gray-200 text-gray-400 opacity-60'
                  }`}
                >
                  <div className="text-4xl">{ach.icon}</div>
                  <div className="flex-1">
                    <h4 className="font-extrabold text-sm">{ach.title}</h4>
                    <p className="text-xs">{ach.description}</p>
                  </div>
                  {ach.unlocked && <span className="text-xs font-black text-green-600 bg-green-100 px-3 py-1 rounded-full">Unlocked</span>}
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default InsightsHistory;

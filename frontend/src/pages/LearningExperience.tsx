import React, { useCallback, useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import AhaMomentModal from '../components/AhaMomentModal';
import Navbar from '../components/Navbar';
import api from '../services/api';

interface Activity {
  id: number;
  node_id: number;
  activity_type: string;
  prompt: string;
  expected_response?: string;
}

interface AttemptResult {
  id: number;
  result: 'correct' | 'needs_support' | 'partial';
  feedback: string;
  score: number;
  clarity_awarded: number;
  xp_awarded: number;
  misconception_detected?: string;
  new_node_inserted?: boolean;
}

const LearningExperience: React.FC = () => {
  const { roadmapId, nodeId } = useParams();
  const navigate = useNavigate();
  const goRoadmap = useCallback(() => {
    if (roadmapId) navigate(`/roadmap/${roadmapId}`, { replace: true });
    else navigate('/home', { replace: true });
  }, [navigate, roadmapId]);

  const [activity, setActivity] = useState<Activity | null>(null);
  const [responseInput, setResponseInput] = useState('');
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [attemptResult, setAttemptResult] = useState<AttemptResult | null>(null);

  // Aha Moment Celebration Modal state
  const [showAhaModal, setShowAhaModal] = useState(false);

  useEffect(() => {
    if (!roadmapId || !nodeId) {
      navigate('/home', { replace: true });
      return;
    }

    let active = true;

    const fetchActivity = async () => {
      try {
        const res = await api.post(`/roadmaps/${roadmapId}/nodes/${nodeId}/activity`);
        if (!active) return;
        setActivity(res.data);
      } catch (err: any) {
        if (!active) return;
        const status = err?.response?.status;
        if (status === 404 || status === 422) {
          goRoadmap();
          return;
        }
        console.error('Failed to load activity:', err);
      } finally {
        if (active) setLoading(false);
      }
    };

    fetchActivity();
    return () => {
      active = false;
    };
  }, [navigate, nodeId, roadmapId]);

  const handleSubmitAttempt = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!activity || !responseInput.trim() || submitting || attemptResult) return;

    setSubmitting(true);
    try {
      const res = await api.post(`/activities/${activity.id}/attempts`, {
        response: responseInput.trim(),
      });
      const data: AttemptResult = res.data;
      setAttemptResult(data);

      if (data.result === 'correct') {
        setShowAhaModal(true);
      }
    } catch (err: any) {
      const status = err?.response?.status;
      if (status === 404 || status === 422) {
        goRoadmap();
        return;
      }
      console.error('Failed to submit attempt:', err);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col">
        <Navbar />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center p-8 bg-white rounded-3xl border-2 border-gray-200 shadow-xl max-w-md">
            <div className="w-16 h-16 border-4 border-green-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
            <h2 className="text-2xl font-black text-gray-800">Preparing Your Interactive Lesson...</h2>
            <p className="text-gray-500 text-sm mt-2 font-medium">Mira is personalizing explanation & examples.</p>
          </div>
        </div>
      </div>
    );
  }

  if (!activity) {
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col">
        <Navbar />
        <div className="flex-1 flex items-center justify-center p-6">
          <div className="text-center p-8 bg-white rounded-3xl border-2 border-gray-200 shadow-xl max-w-md">
            <h2 className="text-2xl font-black text-red-600 mb-2">Lesson Not Found</h2>
            <button
              onClick={goRoadmap}
              className="bg-green-500 text-white font-extrabold px-6 py-3 rounded-2xl border-b-4 border-green-700 mt-4"
            >
              Back to Roadmap
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Navbar />

      <main className="max-w-4xl w-full mx-auto p-6 space-y-8 flex-1">
        {/* Navigation Breadcrumb */}
        <button
          onClick={goRoadmap}
          className="font-bold text-green-700 hover:text-green-900 transition-colors flex items-center gap-2 cursor-pointer"
        >
          ← Back to Learning Map
        </button>

        {/* Lesson Card */}
        <div className="bg-white rounded-3xl border-2 border-gray-200 shadow-xl p-8 space-y-6">
          {/* Header Badge */}
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-2xl bg-green-100 text-green-700 font-black text-2xl flex items-center justify-center border-2 border-green-300">
              {activity.activity_type === 'reasoning'
                ? '🧠'
                : activity.activity_type === 'application'
                ? '⚡'
                : activity.activity_type === 'misconception_repair'
                ? '🛠️'
                : '📖'}
            </div>
            <div>
              <span className="text-xs font-extrabold text-green-700 uppercase tracking-widest">
                Interactive {activity.activity_type}
              </span>
              <h1 className="text-2xl font-black text-gray-900">Concept Deep Dive</h1>
            </div>
          </div>

          {/* Activity Prompt Content */}
          <div className="bg-green-50 p-6 rounded-2xl border-2 border-green-200 leading-relaxed text-gray-800 font-medium space-y-4 whitespace-pre-wrap">
            {activity.prompt}
          </div>

          {/* Response Form */}
                  <form onSubmit={handleSubmitAttempt} className="space-y-4 pt-4 border-t border-gray-100" aria-labelledby="lesson-form-label">
            <label id="lesson-form-label" className="block text-sm font-extrabold text-gray-800">
              Your Thought Process & Reasoning Answer:
            </label>
 
            <textarea
              required
              aria-label="Your reasoning answer"
              value={responseInput}
              onChange={(e) => setResponseInput(e.target.value)}
              placeholder="Write your explanation or reasoning in your own words..."
              className="w-full min-h-36 p-4 border-2 border-gray-200 rounded-2xl font-medium focus:border-green-500 focus:outline-none"
            />
 
            <div className="flex justify-end gap-4">
              <button
                type="submit"
                disabled={submitting || !responseInput.trim()}
                aria-busy={submitting}
                className="bg-green-500 hover:bg-green-600 disabled:opacity-40 text-white font-extrabold text-lg py-4 px-8 rounded-2xl border-b-4 border-green-700 active:border-b-0 active:translate-y-1 transition-all cursor-pointer shadow-md"
              >
                {submitting ? 'Elara evaluating answer...' : 'Submit & Check Understanding →'}
              </button>
            </div>
          </form>

          {/* Wrong Answer & Misconception Support Banner */}
          {attemptResult && attemptResult.result !== 'correct' && (
            <div className="bg-amber-50 p-6 rounded-2xl border-2 border-amber-300 space-y-3 animate-fade-in">
              <div className="flex items-center gap-2 text-amber-900 font-extrabold text-lg">
                <span>🛠️</span>
                <span>Your idea is close, but one key part is missing</span>
              </div>
              <p className="text-amber-800 text-sm font-medium leading-relaxed">{attemptResult.feedback}</p>

              {attemptResult.new_node_inserted && (
                <div className="bg-white p-3.5 rounded-xl border border-amber-200 text-xs font-bold text-amber-900 flex items-center justify-between">
                  <span>+1 Misconception Repair node dynamically added to your learning path!</span>
                  <button
                    onClick={goRoadmap}
                    className="text-amber-700 underline font-extrabold"
                  >
                    View Map →
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      </main>

      {/* Aha Moment Celebration Modal */}
      <AhaMomentModal
        isOpen={showAhaModal}
        concept="Core Principles"
        clarityAwarded={attemptResult?.clarity_awarded || 20}
        xpAwarded={attemptResult?.xp_awarded || 30}
        onClose={() => {
          setShowAhaModal(false);
          goRoadmap();
        }}
      />
    </div>
  );
};

export default LearningExperience;

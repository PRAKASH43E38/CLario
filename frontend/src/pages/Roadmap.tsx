import React, { useCallback, useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import AssessmentView from '../components/AssessmentView';
import Navbar from '../components/Navbar';
import api from '../services/api';

interface RoadmapNode {
  id: number;
  position: number;
  concept: string;
  objective: string;
  activity_type: string;
  difficulty: string;
  estimated_minutes: number;
  status: 'locked' | 'unlocked' | 'current' | 'completed';
  is_current: boolean;
}

interface RoadmapData {
  id: number;
  session_id: number;
  title: string;
  objective: string;
  status: string;
  nodes: RoadmapNode[];
}

const Roadmap: React.FC = () => {
  const { sessionId } = useParams();
  const navigate = useNavigate();
  const goHome = useCallback(() => navigate('/home', { replace: true }), [navigate]);
  const [roadmap, setRoadmap] = useState<RoadmapData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedNode, setSelectedNode] = useState<RoadmapNode | null>(null);
  const [showAssessment, setShowAssessment] = useState(false);

  useEffect(() => {
    if (!sessionId || Number.isNaN(Number(sessionId))) {
      goHome();
      return;
    }

    let active = true;

    const fetchRoadmap = async () => {
      try {
        const response = await api.post(`/sessions/${sessionId}/roadmap`);
        if (!active) return;
        setRoadmap(response.data);
      } catch (err: any) {
        if (!active) return;
        const status = err?.response?.status;
        if (status === 404) {
          goHome();
          return;
        }
        setError('Could not load your personalized learning roadmap.');
      } finally {
        if (active) setLoading(false);
      }
    };

    fetchRoadmap();

    return () => {
      active = false;
    };
  }, [goHome, sessionId]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col">
        <Navbar />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center p-8 bg-white rounded-3xl border-2 border-gray-200 shadow-xl max-w-md">
            <div className="w-16 h-16 border-4 border-green-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
            <h2 className="text-2xl font-black text-gray-800">Designing Your Personal Learning Map...</h2>
            <p className="text-gray-500 text-sm mt-2 font-medium">
              Main Orchestrator is synthesizing your intake inputs and research context.
            </p>
          </div>
        </div>
      </div>
    );
  }

  if (error || !roadmap) {
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col">
        <Navbar />
        <div className="flex-1 flex items-center justify-center p-6">
          <div className="text-center p-8 bg-white rounded-3xl border-2 border-gray-200 shadow-xl max-w-md">
            <h2 className="text-2xl font-black text-red-600 mb-2">Failed to load roadmap</h2>
            <p className="text-gray-500 text-sm mb-6">{error || 'An unexpected error occurred.'}</p>
            <button
              onClick={goHome}
              className="bg-green-500 text-white font-extrabold px-6 py-3 rounded-2xl border-b-4 border-green-700"
            >
              Back to Home
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Navbar />

      <main className="max-w-4xl w-full mx-auto p-6 flex-1 flex flex-col items-center">
        {/* Roadmap Title Banner */}
        <div className="bg-white p-6 rounded-3xl border-2 border-gray-200 shadow-sm text-center w-full mb-8">
          <span className="inline-block px-3 py-1 rounded-full bg-green-100 text-green-800 font-extrabold text-xs uppercase tracking-wider mb-2">
            Personalized Path
          </span>
          <h1 className="text-3xl font-black text-gray-900">{roadmap.title}</h1>
          <p className="text-gray-500 font-medium text-sm mt-1">{roadmap.objective}</p>
        </div>

        {/* Zayn 5-Question Assessment Trigger Bar */}
        <div className="w-full bg-gradient-to-r from-yellow-400 to-amber-500 rounded-3xl p-6 text-white shadow-lg flex items-center justify-between mb-12 border-b-4 border-amber-600">
          <div className="flex items-center gap-4">
            <span className="text-4xl">🎓</span>
            <div>
              <h3 className="font-black text-xl">Zayn's 5-Question Assessment</h3>
              <p className="text-amber-100 text-xs font-medium">Test your clarity & earn +50 XP upon completing your map</p>
            </div>
          </div>
          <button
            onClick={() => setShowAssessment(true)}
            className="bg-white hover:bg-amber-50 text-amber-900 font-extrabold px-6 py-3 rounded-2xl shadow-md transition-all cursor-pointer border-b-4 border-amber-200 active:border-b-0 active:translate-y-1"
          >
            Take Assessment →
          </button>
        </div>

        {/* Duolingo-Inspired Curved Learning Path */}
        <div className="relative w-full max-w-xl py-6 flex flex-col items-center">
          {/* Path Nodes */}
          {roadmap.nodes.map((node, index) => {
            // Calculate curved offset (-100px, 0px, 100px wave)
            const offsets = [0, 90, 120, 60, -60, -120, -90, 0];
            const offsetX = offsets[index % offsets.length];

            const isCompleted = node.status === 'completed';
            const isCurrent = node.status === 'current' || node.is_current;
            const isUnlocked = node.status === 'unlocked' || isCurrent || isCompleted;

            let icon = '📖';
            if (node.activity_type === 'reasoning') icon = '🧠';
            else if (node.activity_type === 'application') icon = '⚡';
            else if (node.activity_type === 'misconception_repair') icon = '🛠️';
            else if (node.activity_type === 'assessment') icon = '🏆';

            return (
              <div
                key={node.id}
                className="relative my-6 flex flex-col items-center transition-all duration-300"
                style={{ transform: `translateX(${offsetX}px)` }}
              >
                {/* Connector line to next node */}
                {index < roadmap.nodes.length - 1 && (
                  <div className="absolute top-16 left-1/2 -translate-x-1/2 w-2 h-16 bg-green-200 -z-10 rounded-full" />
                )}

                {/* Node Button */}
                <button
                  onClick={() => setSelectedNode(node)}
                  aria-label={`Open node ${node.position}: ${node.concept}`}
                  aria-disabled={!isUnlocked}
                  disabled={!isUnlocked}
                  className={`w-20 h-20 rounded-full flex items-center justify-center text-3xl font-black shadow-xl transition-all border-b-8 ${!isUnlocked ? 'cursor-not-allowed' : 'cursor-pointer'} active:scale-95 ${
                    isCompleted
                      ? 'bg-green-500 border-green-700 text-white hover:bg-green-600'
                      : isCurrent
                      ? 'bg-yellow-400 border-yellow-600 text-white animate-bounce shadow-yellow-200 ring-8 ring-yellow-100'
                      : isUnlocked
                      ? 'bg-white border-gray-300 text-gray-700 hover:border-green-400'
                      : 'bg-gray-200 border-gray-300 text-gray-400 opacity-70'
                  }`}
                >
                  {isCompleted ? '✓' : icon}
                </button>

                {/* Concept Label Pill */}
                <div className="mt-3 bg-white px-4 py-1.5 rounded-2xl border-2 border-gray-200 shadow-xs text-center max-w-[180px]">
                  <span className="block text-xs font-extrabold text-gray-800 truncate">{node.concept}</span>
                  <span className="block text-[10px] font-bold text-gray-400 uppercase">{node.activity_type}</span>
                </div>
              </div>
            );
          })}
        </div>
      </main>

      {/* Interactive Node Details Modal */}
      {selectedNode && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-xs p-4">
          <div className="bg-white rounded-3xl p-8 max-w-md w-full shadow-2xl border-2 border-gray-200 text-center">
            <div className="w-16 h-16 rounded-2xl bg-green-100 text-green-700 font-black text-3xl flex items-center justify-center mx-auto mb-4 border-2 border-green-300">
              {selectedNode.activity_type === 'reasoning'
                ? '🧠'
                : selectedNode.activity_type === 'application'
                ? '⚡'
                : selectedNode.activity_type === 'misconception_repair'
                ? '🛠️'
                : '📖'}
            </div>

            <span className="inline-block px-3 py-1 rounded-full bg-green-100 text-green-800 font-extrabold text-xs uppercase tracking-wider mb-2">
              Node {selectedNode.position} • {selectedNode.activity_type}
            </span>

            <h3 className="text-2xl font-black text-gray-900 mb-2">{selectedNode.concept}</h3>
            <p className="text-gray-600 font-medium text-sm mb-6 leading-relaxed">{selectedNode.objective}</p>

            <div className="flex gap-4">
              <button
                onClick={() => setSelectedNode(null)}
                className="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-700 font-bold py-3.5 rounded-2xl"
              >
                Close
              </button>
              <button
                onClick={() => {
                  const nodeToOpen = selectedNode;
                  setSelectedNode(null);
                  navigate(`/learning/${roadmap.id}/${nodeToOpen.id}`);
                }}
                className="flex-1 bg-green-500 hover:bg-green-600 text-white font-extrabold py-3.5 rounded-2xl border-b-4 border-green-700 active:border-b-0 active:translate-y-1 transition-all cursor-pointer shadow-md"
              >
                Start Lesson →
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Zayn Assessment Modal */}
      {showAssessment && (
        <AssessmentView
          roadmapId={roadmap.id}
          onClose={() => setShowAssessment(false)}
        />
      )}
    </div>
  );
};

export default Roadmap;

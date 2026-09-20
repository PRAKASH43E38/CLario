import React from 'react';
import { useNavigate } from 'react-router-dom';

const Intro: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-radial from-green-50 to-white flex flex-col justify-between p-6">
      {/* Top Navbar */}
      <header className="max-w-6xl w-full mx-auto flex items-center justify-between py-4">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-2xl bg-green-500 text-white font-black text-3xl flex items-center justify-center shadow-lg border-b-4 border-green-700">
            C
          </div>
          <div>
            <span className="font-extrabold text-3xl tracking-wider text-green-900">CLARIO</span>
            <span className="block text-[11px] font-bold text-green-600 tracking-widest uppercase">Adaptive AI Tutor</span>
          </div>
        </div>

        <button
          onClick={() => navigate('/signin')}
          className="bg-white hover:bg-gray-50 text-green-700 font-extrabold px-6 py-2.5 rounded-2xl border-2 border-green-200 shadow-sm transition-all cursor-pointer"
        >
          Sign In
        </button>
      </header>

      {/* Main Hero */}
      <main className="max-w-5xl w-full mx-auto my-12 grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
        <div className="space-y-6 text-left">
          <div className="inline-block px-4 py-1.5 rounded-full bg-green-100 text-green-800 font-extrabold text-xs uppercase tracking-widest border border-green-200">
            Conceptual Clarity Platform
          </div>

          <h1 className="text-5xl md:text-6xl font-black text-gray-900 leading-tight">
            Come confused. <br />
            <span className="text-green-500">Leave with clarity.</span>
          </h1>

          <p className="text-xl text-gray-600 font-medium leading-relaxed">
            Stop struggling with static videos and passive notes. CLARIO dynamically adapts to your personal mind model so every tough concept actually <span className="font-extrabold text-green-700 underline decoration-green-400">clicks</span>.
          </p>

          <div className="pt-4">
            <button
              onClick={() => navigate('/signin')}
              className="bg-green-500 hover:bg-green-600 text-white text-xl font-extrabold py-5 px-10 rounded-2xl border-b-8 border-green-700 active:border-b-0 active:translate-y-2 transition-all cursor-pointer shadow-xl"
            >
              Get Started Free →
            </button>
          </div>
        </div>

        {/* Duolingo Visual Path Feature Preview */}
        <div className="bg-white p-8 rounded-3xl border-4 border-green-200 shadow-2xl relative transform rotate-1 hover:rotate-0 transition-transform">
          <div className="flex justify-between items-center mb-6">
            <span className="font-extrabold text-gray-800 text-lg">Machine Learning Fundamentals</span>
            <span className="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-xs font-bold">🔥 3 Day Streak</span>
          </div>

          <div className="space-y-4">
            <div className="p-4 rounded-2xl bg-green-50 border-2 border-green-300 flex items-center gap-4">
              <div className="w-12 h-12 rounded-full bg-green-500 text-white font-bold flex items-center justify-center text-xl shadow-md">✓</div>
              <div>
                <h4 className="font-bold text-green-900">1. Conceptual Exploration</h4>
                <p className="text-xs text-green-700">Mira: Worked examples & intuitive mental models</p>
              </div>
            </div>

            <div className="p-4 rounded-2xl bg-yellow-50 border-2 border-yellow-300 flex items-center gap-4 animate-pulse">
              <div className="w-12 h-12 rounded-full bg-yellow-400 text-white font-bold flex items-center justify-center text-xl shadow-md">2</div>
              <div>
                <h4 className="font-bold text-yellow-900">2. Critical Reasoning Task</h4>
                <p className="text-xs text-yellow-700">Ayan: Predict weight updates in gradient descent</p>
              </div>
            </div>

            <div className="p-4 rounded-2xl bg-gray-100 border-2 border-gray-200 opacity-60 flex items-center gap-4">
              <div className="w-12 h-12 rounded-full bg-gray-300 text-gray-600 font-bold flex items-center justify-center text-xl">3</div>
              <div>
                <h4 className="font-bold text-gray-700">3. Real-World Application</h4>
                <p className="text-xs text-gray-500">Kira: Write learning rate optimization snippet</p>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer Features */}
      <footer className="max-w-6xl w-full mx-auto border-t border-green-100 pt-8 pb-4 grid grid-cols-1 md:grid-cols-3 gap-8 text-left">
        <div>
          <h3 className="font-extrabold text-green-900 text-lg mb-1">🧠 Dynamic Learning Path</h3>
          <p className="text-gray-500 text-sm">Automated prerequisite skipping & instant misconception repair insertion.</p>
        </div>
        <div>
          <h3 className="font-extrabold text-green-900 text-lg mb-1">🤝 6 Specialized AI Agents</h3>
          <p className="text-gray-500 text-sm">Nova, Mira, Ayan, Kira, Zayn & Elara coordinate seamlessly behind the scenes.</p>
        </div>
        <div>
          <h3 className="font-extrabold text-green-900 text-lg mb-1">🏆 Evidence-Based Gamification</h3>
          <p className="text-gray-500 text-sm">Earn XP, Clarity %, and unlock achievements when concepts actually click.</p>
        </div>
      </footer>
    </div>
  );
};

export default Intro;

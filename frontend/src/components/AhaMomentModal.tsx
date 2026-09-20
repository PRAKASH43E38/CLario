import React from 'react';

interface AhaMomentModalProps {
  isOpen: boolean;
  concept: string;
  clarityAwarded: number;
  xpAwarded: number;
  onClose: () => void;
}

const AhaMomentModal: React.FC<AhaMomentModalProps> = ({
  isOpen,
  concept,
  clarityAwarded,
  xpAwarded,
  onClose,
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-xs p-4 animate-fade-in">
      <div className="bg-white rounded-3xl p-8 max-w-md w-full border-4 border-green-500 shadow-2xl text-center transform scale-100 transition-all">
        <div className="w-24 h-24 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4 animate-bounce border-4 border-green-400">
          <span className="text-5xl">💡</span>
        </div>

        <span className="inline-block px-4 py-1 rounded-full bg-green-100 text-green-800 font-extrabold text-xs uppercase tracking-widest mb-2">
          Conceptual Breakthrough
        </span>

        <h2 className="text-4xl font-black text-gray-900 mb-2">IT CLICKS!</h2>
        <p className="text-green-700 font-medium text-lg mb-6 leading-snug">
          You just achieved conceptual clarity on <strong className="text-green-900 font-extrabold">{concept}</strong>!
        </p>

        <div className="flex justify-center gap-4 mb-8">
          <div className="bg-blue-50 border-2 border-blue-200 rounded-2xl p-4 flex-1">
            <div className="text-2xl font-black text-blue-600">+{clarityAwarded}</div>
            <div className="text-xs font-bold text-blue-800 uppercase">Clarity</div>
          </div>
          <div className="bg-yellow-50 border-2 border-yellow-200 rounded-2xl p-4 flex-1">
            <div className="text-2xl font-black text-yellow-600">+{xpAwarded}</div>
            <div className="text-xs font-bold text-yellow-800 uppercase">XP</div>
          </div>
        </div>

        <button
          onClick={onClose}
          className="w-full bg-green-500 hover:bg-green-600 text-white font-extrabold text-lg py-4 rounded-2xl border-b-4 border-green-700 active:border-b-0 active:translate-y-1 transition-all cursor-pointer shadow-lg"
        >
          Continue Learning →
        </button>
      </div>
    </div>
  );
};

export default AhaMomentModal;

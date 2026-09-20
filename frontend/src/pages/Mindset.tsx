import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';

interface MindsetQuestion {
  number: number;
  question: string;
  options: { key: string; text: string }[];
}

const QUESTIONS: MindsetQuestion[] = [
  {
    number: 1,
    question: 'When you get a new topic, what do you usually do first?',
    options: [
      { key: 'A', text: 'Watch a video or visual explanation' },
      { key: 'B', text: 'Read notes or a textbook' },
      { key: 'C', text: 'Ask a friend or teacher' },
      { key: 'D', text: 'Start solving problems' },
    ],
  },
  {
    number: 2,
    question: 'When preparing for an exam, what feels easiest for you?',
    options: [
      { key: 'A', text: 'Drawing diagrams or using visuals' },
      { key: 'B', text: 'Listening to explanations or voice notes' },
      { key: 'C', text: 'Writing or rewriting notes' },
      { key: 'D', text: 'Solving lots of practice problems' },
    ],
  },
  {
    number: 3,
    question: 'When you lose focus in class, what helps you most?',
    options: [
      { key: 'A', text: 'More visuals or diagrams' },
      { key: 'B', text: 'A clear verbal explanation' },
      { key: 'C', text: 'Written notes or handouts' },
      { key: 'D', text: 'A small activity or task' },
    ],
  },
  {
    number: 4,
    question: 'When you feel stressed about an exam or assignment, what do you usually do first?',
    options: [
      { key: 'A', text: 'Overthink and freeze' },
      { key: 'B', text: 'Start studying at the last minute' },
      { key: 'C', text: 'Talk to a friend or mentor' },
      { key: 'D', text: 'Make a plan and work step by step' },
    ],
  },
  {
    number: 5,
    question: 'Which teaching style do you enjoy most?',
    options: [
      { key: 'A', text: 'Story or example first, then the concept' },
      { key: 'B', text: 'Definition or formula first, then examples' },
      { key: 'C', text: 'Group discussion or activities' },
      { key: 'D', text: 'Self-study, then clear doubts when needed' },
    ],
  },
];

const Mindset: React.FC = () => {
  const navigate = useNavigate();
  const { refreshUser } = useAuth();
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const currentQ = QUESTIONS[currentIndex];
  const selectedKey = answers[currentQ.number] || '';

  const handleSelect = (key: string) => {
    setAnswers({ ...answers, [currentQ.number]: key });
  };

  const handleNext = () => {
    if (currentIndex < QUESTIONS.length - 1) {
      setCurrentIndex(currentIndex + 1);
    } else {
      handleSubmit();
    }
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError('');
    try {
      const payload = {
        answers: Object.entries(answers).map(([qNum, ans]) => ({
          question_number: Number(qNum),
          answer: ans,
        })),
      };
      await api.put('/onboarding/mindset', payload);
      await refreshUser();
      navigate('/home');
    } catch (err) {
      console.error('Failed to save mindset responses:', err);
      setError('Could not complete mindset questions. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-6">
      <div className="bg-white p-10 rounded-3xl border-2 border-gray-200 shadow-xl max-w-xl w-full">
        {/* Header Progress */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-green-500 text-white font-black text-xl flex items-center justify-center">
              2
            </div>
            <div>
              <h1 className="text-xl font-black text-gray-900">Mindset Intake</h1>
              <p className="text-xs font-bold text-gray-400 uppercase">
                Question {currentIndex + 1} of 5
              </p>
            </div>
          </div>
          <div className="flex gap-1.5">
            {QUESTIONS.map((q, idx) => (
              <div
                key={q.number}
                className={`w-6 h-2 rounded-full ${
                  idx === currentIndex
                    ? 'bg-green-500'
                    : idx < currentIndex
                    ? 'bg-green-300'
                    : 'bg-gray-200'
                }`}
              />
            ))}
          </div>
        </div>

        {error && <div className="p-3 mb-6 bg-red-50 text-red-600 rounded-xl text-sm font-bold">{error}</div>}

        {/* Question Text */}
        <h2 className="text-2xl font-bold text-gray-800 mb-6 leading-snug">{currentQ.question}</h2>

        {/* Options */}
        <div className="space-y-3 mb-8">
          {currentQ.options.map((opt) => {
            const isSelected = selectedKey === opt.key;
            return (
              <button
                key={opt.key}
                onClick={() => handleSelect(opt.key)}
                className={`w-full text-left p-4 rounded-2xl border-2 font-medium transition-all flex items-center gap-4 cursor-pointer ${
                  isSelected
                    ? 'bg-green-500 text-white border-green-700 shadow-md font-bold'
                    : 'bg-white border-gray-200 text-gray-800 hover:border-green-300 hover:bg-green-50'
                }`}
              >
                <span
                  className={`w-8 h-8 rounded-xl font-black flex items-center justify-center text-sm ${
                    isSelected ? 'bg-white text-green-700' : 'bg-gray-100 text-gray-600'
                  }`}
                >
                  {opt.key}
                </span>
                <span className="flex-1">{opt.text}</span>
              </button>
            );
          })}
        </div>

        <div className="flex justify-between items-center">
          {currentIndex > 0 ? (
            <button
              onClick={() => setCurrentIndex(currentIndex - 1)}
              className="font-bold text-gray-500 hover:text-gray-800 px-4 py-2"
            >
              ← Previous
            </button>
          ) : (
            <div />
          )}

          <button
            onClick={handleNext}
            disabled={!selectedKey || loading}
            className="bg-green-500 hover:bg-green-600 disabled:opacity-40 text-white font-extrabold px-8 py-3.5 rounded-2xl border-b-4 border-green-700 active:border-b-0 active:translate-y-1 transition-all cursor-pointer shadow-md"
          >
            {loading ? 'Saving...' : currentIndex === QUESTIONS.length - 1 ? 'Finish & Unlock App →' : 'Next Question →'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Mindset;

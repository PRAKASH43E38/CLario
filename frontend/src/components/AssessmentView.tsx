import React, { useEffect, useState } from 'react';
import api from '../services/api';

interface Question {
  id: number;
  position: number;
  question_text: string;
  question_type: string;
  options: string[];
  time_limit: number;
}

interface Assessment {
  id: number;
  roadmap_id: number;
  title: string;
  difficulty: string;
  time_limit_per_question: number;
  questions: Question[];
}

interface AssessmentViewProps {
  roadmapId: number;
  onClose: () => void;
}

const AssessmentView: React.FC<AssessmentViewProps> = ({ roadmapId, onClose }) => {
  const [assessment, setAssessment] = useState<Assessment | null>(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [selectedOption, setSelectedOption] = useState('');
  const [timeLeft, setTimeLeft] = useState(60);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<any>(null);

  useEffect(() => {
    const fetchAssessment = async () => {
      try {
        const res = await api.post(`/roadmaps/${roadmapId}/assessment`);
        setAssessment(res.data);
        if (res.data?.questions?.length > 0) {
          setTimeLeft(res.data.questions[0].time_limit || 60);
        }
      } catch (err) {
        console.error('Failed to load assessment:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchAssessment();
  }, [roadmapId]);

  // Countdown timer for individual questions
  useEffect(() => {
    if (!assessment || result) return;
    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          handleNextQuestion();
          return assessment.questions[currentIndex + 1]?.time_limit || 60;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [assessment, currentIndex, result]);

  const handleNextQuestion = () => {
    if (!assessment) return;
    const currentQ = assessment.questions[currentIndex];
    const newAnswers = { ...answers, [currentQ.id]: selectedOption };
    setAnswers(newAnswers);
    setSelectedOption('');

    if (currentIndex < assessment.questions.length - 1) {
      const nextQ = assessment.questions[currentIndex + 1];
      setCurrentIndex(currentIndex + 1);
      setTimeLeft(nextQ.time_limit || 60);
    } else {
      submitAssessment(newAnswers);
    }
  };

  const submitAssessment = async (finalAnswers: Record<number, string>) => {
    if (!assessment) return;
    setSubmitting(true);
    try {
      const payload = {
        answers: Object.entries(finalAnswers).map(([qId, ans]) => ({
          question_id: Number(qId),
          user_answer: ans,
        })),
      };
      const res = await api.post(`/assessments/${assessment.id}/submit`, payload);
      setResult(res.data);
    } catch (err) {
      console.error('Failed to submit assessment:', err);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
        <div className="bg-white rounded-3xl p-8 max-w-lg w-full text-center">
          <div className="w-16 h-16 border-4 border-green-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <h3 className="text-2xl font-bold text-gray-800">Zayn is preparing your 5-question assessment...</h3>
          <p className="text-gray-500 text-sm mt-2">Testing conceptual clarity and reasoning</p>
        </div>
      </div>
    );
  }

  if (!assessment) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
        <div className="bg-white rounded-3xl p-8 max-w-md w-full text-center">
          <h3 className="text-2xl font-bold text-red-600">Could not load assessment</h3>
          <button onClick={onClose} className="mt-4 bg-gray-200 px-6 py-2 rounded-xl font-bold">
            Close
          </button>
        </div>
      </div>
    );
  }

  if (result) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
        <div className="bg-white rounded-3xl p-8 max-w-md w-full text-center border-4 border-green-400">
          <div className="text-5xl mb-2">🎓</div>
          <h2 className="text-3xl font-black text-gray-800 mb-2">Assessment Results</h2>
          <div className="text-5xl font-black text-green-600 my-4">{result.score}%</div>
          <p className="text-gray-600 font-medium mb-6">{result.feedback}</p>

          <div className="flex justify-center gap-4 mb-6">
            <div className="bg-blue-50 border border-blue-200 p-3 rounded-xl flex-1">
              <div className="text-xl font-bold text-blue-600">+{result.clarity_awarded}</div>
              <div className="text-xs font-bold text-blue-800">Clarity</div>
            </div>
            <div className="bg-yellow-50 border border-yellow-200 p-3 rounded-xl flex-1">
              <div className="text-xl font-bold text-yellow-600">+{result.xp_awarded}</div>
              <div className="text-xs font-bold text-yellow-800">XP</div>
            </div>
          </div>

          <button
            onClick={onClose}
            className="w-full bg-green-500 hover:bg-green-600 text-white font-bold py-3 rounded-2xl border-b-4 border-green-700 active:border-b-0 active:translate-y-1 transition-all"
          >
            Return to Roadmap
          </button>
        </div>
      </div>
    );
  }

  const currentQ = assessment.questions[currentIndex];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-xs p-4">
      <div className="bg-white rounded-3xl p-8 max-w-2xl w-full shadow-2xl border-2 border-gray-200">
        <div className="flex justify-between items-center mb-6">
          <div>
            <span className="text-xs font-extrabold text-green-600 uppercase tracking-widest">
              Question {currentIndex + 1} of 5
            </span>
            <h2 className="text-2xl font-bold text-gray-800">{assessment.title}</h2>
          </div>

          <div
            className={`flex items-center gap-2 px-4 py-2 rounded-2xl border-2 font-black text-lg ${
              timeLeft <= 10 ? 'bg-red-50 text-red-600 border-red-300 animate-pulse' : 'bg-gray-100 text-gray-700 border-gray-300'
            }`}
          >
            ⏱️ {timeLeft}s
          </div>
        </div>

        {/* Question Text */}
        <div className="bg-green-50 p-6 rounded-2xl border-2 border-green-200 mb-6">
          <p className="text-lg font-medium text-green-900 leading-relaxed">{currentQ.question_text}</p>
        </div>

        {/* MCQ Choices */}
        {currentQ.options && currentQ.options.length > 0 ? (
          <div className="space-y-3 mb-8">
            {currentQ.options.map((opt, idx) => (
              <button
                key={idx}
                onClick={() => setSelectedOption(opt)}
                className={`w-full text-left p-4 rounded-2xl border-2 font-medium transition-all flex items-center justify-between cursor-pointer ${
                  selectedOption === opt
                    ? 'bg-green-500 text-white border-green-700 shadow-md font-bold'
                    : 'bg-white border-gray-200 text-gray-800 hover:border-green-300 hover:bg-green-50'
                }`}
              >
                <span>{opt}</span>
                {selectedOption === opt && <span className="text-xl">✓</span>}
              </button>
            ))}
          </div>
        ) : (
          <textarea
            value={selectedOption}
            onChange={(e) => setSelectedOption(e.target.value)}
            placeholder="Type your reasoning answer here..."
            className="w-full min-h-32 p-4 border-2 border-gray-200 rounded-2xl mb-8 font-medium focus:border-green-500 focus:outline-none"
          />
        )}

        <div className="flex justify-between items-center">
          <button
            onClick={onClose}
            className="text-gray-400 font-bold hover:text-gray-600 transition-colors"
          >
            Quit
          </button>
          <button
            onClick={handleNextQuestion}
            disabled={submitting}
            className="bg-green-500 hover:bg-green-600 text-white font-extrabold px-8 py-3 rounded-2xl border-b-4 border-green-700 active:border-b-0 active:translate-y-1 transition-all cursor-pointer"
          >
            {submitting ? 'Submitting...' : currentIndex === assessment.questions.length - 1 ? 'Finish Assessment' : 'Next Question →'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default AssessmentView;

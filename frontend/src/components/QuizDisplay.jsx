import React, { useState } from 'react';
import { Eye, EyeOff, CheckCircle, BookOpen } from 'lucide-react';

export default function QuizDisplay({ quiz }) {
  const [showAnswers, setShowAnswers] = useState(false);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [showAnswerModal, setShowAnswerModal] = useState(false);

  if (!quiz) return null;

  // Debug log to see question count and study summary
  console.log('Quiz received:', quiz);
  console.log('Number of questions:', quiz.questions ? quiz.questions.length : 0);
  console.log('Has study_summary:', quiz.study_summary ? 'YES' : 'NO');
  console.log('Study summary content:', quiz.study_summary);

  const handleOptionSelect = (questionIndex, option) => {
    setSelectedAnswers(prev => ({
      ...prev,
      [questionIndex]: option
    }));
  };

  const getScore = () => {
    if (!quiz.questions) return 0;
    let correct = 0;
    quiz.questions.forEach((q, i) => {
      if (selectedAnswers[i] === q.answer) correct++;
    });
    return { correct, total: quiz.questions.length };
  };

  const AnswerModal = () => {
    if (!showAnswerModal) return null;
    const { correct, total } = getScore();
    
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
        <div className="max-w-2xl w-full mx-4 card max-h-[80vh] overflow-auto">
          <div className="flex justify-between items-center mb-4">
            <h3 className="font-semibold text-lg">Quiz Answers</h3>
            <div className="flex items-center gap-4">
              <span className="text-sm bg-blue-100 text-blue-800 px-3 py-1 rounded-full">
                Score: {correct}/{total} ({Math.round((correct/total)*100)}%)
              </span>
              <button onClick={() => setShowAnswerModal(false)} className="text-gray-500 hover:text-gray-800">✕</button>
            </div>
          </div>
          <div className="space-y-3">
            {quiz.questions && quiz.questions.map((q, i) => {
              const userAnswer = selectedAnswers[i];
              const isCorrect = userAnswer === q.answer;
              return (
                <div key={i} className={`p-4 rounded-lg border-2 ${isCorrect ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'}`}>
                  <div className="flex items-start gap-2">
                    {isCorrect ? <CheckCircle className="text-green-600 mt-0.5" size={16} /> : <span className="text-red-600 mt-0.5">✗</span>}
                    <div>
                      <p className="font-medium text-sm">Q{i+1}. {q.question}</p>
                      <p className="text-sm text-gray-600 mt-1">
                        <span className="font-medium">Correct:</span> {q.answer}
                      </p>
                      {userAnswer && !isCorrect && (
                        <p className="text-sm text-red-600 mt-1">
                          <span className="font-medium">You selected:</span> {userAnswer}
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-6">
      <div className="card">
        <div className="flex justify-between items-start">
          <div>
            <h2 className="font-semibold text-xl">{quiz.title}</h2>
            <p className="text-gray-600 mt-2">{quiz.summary}</p>
          </div>
          <button
            onClick={() => setShowAnswerModal(true)}
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-blue-500 text-white hover:bg-blue-600 transition-colors"
          >
            <Eye size={16} />
            Show Answers
          </button>
        </div>
      </div>

      <div className="space-y-4">
        {quiz.questions && quiz.questions.map((q, i) => (
          <div key={i} className="card fade-in">
            <div className="flex justify-between items-start">
              <h4 className="font-semibold">Q{i+1}. {q.question}</h4>
            </div>
            <ul className="mt-4 space-y-2">
              {q.options && q.options.map((opt, idx) => {
                const isSelected = selectedAnswers[i] === opt;
                return (
                  <li key={idx}>
                    <button
                      onClick={() => handleOptionSelect(i, opt)}
                      className={`w-full text-left p-3 rounded-lg border transition-all ${
                        isSelected 
                          ? 'bg-blue-100 border-blue-300 text-blue-800' 
                          : 'bg-gray-50 border-gray-200 hover:bg-gray-100'
                      }`}
                    >
                      <span className="font-medium mr-2">{String.fromCharCode(65 + idx)}.</span>
                      {opt}
                    </button>
                  </li>
                );
              })}
            </ul>
          </div>
        ))}
      </div>

      {quiz.study_summary && (
        <div className="card bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200">
          <div className="flex items-center gap-2 mb-3">
            <BookOpen className="text-blue-600" size={20} />
            <h3 className="font-semibold text-lg text-blue-800">Study Summary</h3>
          </div>
          <div className="prose prose-sm max-w-none">
            <div className="text-gray-700 whitespace-pre-line leading-relaxed">
              {quiz.study_summary}
            </div>
          </div>
        </div>
      )}

      <AnswerModal />
    </div>
  );
}
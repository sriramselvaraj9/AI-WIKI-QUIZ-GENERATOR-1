import React, { useState } from 'react';
import { Loader2, Zap, BookOpen } from 'lucide-react';
import QuizDisplay from '../components/QuizDisplay';
import { generateQuiz } from '../services/api';

export default function GenerateTab() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [quiz, setQuiz] = useState(null);
  const [error, setError] = useState(null);
  const [extraQuestions, setExtraQuestions] = useState(false);

  const handleGenerate = async () => {
    if (!url.trim()) {
      setError('Please enter a Wikipedia URL');
      return;
    }
    
    if (!url.includes('wikipedia.org')) {
      setError('Please enter a valid Wikipedia URL');
      return;
    }

    setLoading(true);
    setError(null);
    setQuiz(null);
    
    try {
      const res = await generateQuiz(url, extraQuestions);
      console.log('API Response:', res);
      console.log('Quiz data:', res.quiz);
      console.log('Questions count:', res.quiz?.questions?.length);
      setQuiz(res.quiz);
    } catch (e) {
      if (e.response?.status === 400) {
        setError(e.response.data.detail || 'Failed to access Wikipedia. Please check the URL and your internet connection.');
      } else if (e.response?.status === 500) {
        setError('Quiz generation failed. Please try again in a moment.');
      } else {
        setError('Network error. Please check your connection and try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleGenerate();
    }
  };

  return (
    <div className="space-y-6">
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <BookOpen className="text-blue-600" size={20} />
            <h3 className="font-semibold text-lg">Generate Quiz</h3>
            <span className={`text-xs px-2 py-1 rounded-full ${extraQuestions ? 'bg-purple-100 text-purple-800' : 'bg-yellow-100 text-yellow-800'}`}>
              {extraQuestions ? '15 Questions' : '10 Questions'}
            </span>
          </div>
          <button
            onClick={() => setExtraQuestions(!extraQuestions)}
            className={`px-3 py-1 rounded-lg text-sm font-medium transition-colors ${
              extraQuestions 
                ? 'bg-purple-500 text-white hover:bg-purple-600' 
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            {extraQuestions ? 'Standard (10)' : 'Add More (+5)'}
          </button>
        </div>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Wikipedia Article URL
            </label>
            <input 
              value={url} 
              onChange={e => setUrl(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="https://en.wikipedia.org/wiki/..." 
              className="w-full p-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-transparent"
              disabled={loading}
            />
          </div>
          <button 
            onClick={handleGenerate} 
            disabled={loading || !url.trim()}
            className="w-full sm:w-auto px-6 py-3 rounded-lg bg-sky-500 text-white flex items-center justify-center gap-2 hover:bg-sky-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? (
              <>
                <Loader2 className="animate-spin" size={16} />
                Generating Quiz...
              </>
            ) : (
              'Generate Quiz'
            )}
          </button>
        </div>
        <div className="text-sm text-gray-600 bg-blue-50 p-3 rounded-lg mt-3">
          <p className="font-medium mb-1">✨ Quiz Features:</p>
          <ul className="space-y-1 text-xs">
            <li>• Standard: 10 questions | Extended: 15 questions</li>
            <li>• Toggle "Add More (+5)" for comprehensive testing</li>
            <li>• Interactive answers with instant scoring</li>
            <li>• Works with any Wikipedia article URL</li>
          </ul>
        </div>
        
        {error && (
          <div className="mt-4 p-4 rounded-lg bg-red-50 border border-red-200">
            <p className="text-red-700 text-sm">{error}</p>
          </div>
        )}
      </div>

      <div>
        {loading && (
          <div className="card">
            <div className="animate-pulse space-y-4">
              <div className="h-4 bg-gray-200 rounded w-1/3" />
              <div className="space-y-2">
                <div className="h-3 bg-gray-200 rounded w-full" />
                <div className="h-3 bg-gray-200 rounded w-full" />
                <div className="h-3 bg-gray-200 rounded w-3/4" />
              </div>
            </div>
          </div>
        )}

        {quiz && (
          <div className="fade-in">
            <QuizDisplay quiz={quiz} />
          </div>
        )}
      </div>
    </div>
  );
}
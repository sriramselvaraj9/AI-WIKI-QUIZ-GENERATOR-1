import React, { useState } from 'react';
import GenerateTab from './tabs/GenerateTab';
import HistoryTab from './tabs/HistoryTab';
import './index.css';
import { BookOpen, Clock } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('generate');

  return (
    <div className="min-h-screen bg-pastel-sky p-4 sm:p-6">
      <div className="max-w-6xl mx-auto">
        <header className="mb-8">
          <div className="text-center mb-6">
            <h1 className="font-bold text-3xl text-gray-800 mb-2">
              🧠 AI Wiki Quiz Generator
            </h1>
            <p className="text-gray-600">
              Transform any Wikipedia article into an interactive quiz using AI
            </p>
          </div>
          
          <nav className="flex justify-center">
            <div className="flex bg-white rounded-lg shadow-md p-1">
              <button 
                onClick={() => setActiveTab('generate')} 
                className={`px-6 py-3 rounded-md flex items-center gap-2 transition-all ${
                  activeTab === 'generate'
                    ? 'bg-sky-500 text-white shadow-lg' 
                    : 'text-gray-600 hover:text-gray-800 hover:bg-gray-50'
                }`}
              >
                <BookOpen size={20} />
                Generate Quiz
              </button>
              <button 
                onClick={() => setActiveTab('history')} 
                className={`px-6 py-3 rounded-md flex items-center gap-2 transition-all ${
                  activeTab === 'history'
                    ? 'bg-sky-500 text-white shadow-lg' 
                    : 'text-gray-600 hover:text-gray-800 hover:bg-gray-50'
                }`}
              >
                <Clock size={20} />
                History
              </button>
            </div>
          </nav>
        </header>

        <main>
          {activeTab === 'generate' ? <GenerateTab /> : <HistoryTab />}
        </main>
        
        <footer className="mt-12 text-center text-gray-500 text-sm">
          <p>Powered by FastAPI, React, and Gemini AI</p>
        </footer>
      </div>
    </div>
  );
}
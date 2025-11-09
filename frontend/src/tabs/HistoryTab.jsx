import React, { useEffect, useState } from 'react';
import HistoryTable from '../components/HistoryTable';
import Modal from '../components/Modal';
import QuizDisplay from '../components/QuizDisplay';
import { getHistory, getQuizById } from '../services/api';

export default function HistoryTab() {
  const [quizzes, setQuizzes] = useState([]);
  const [selected, setSelected] = useState(null);
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);

  const fetchHistory = async () => {
    try {
      const res = await getHistory();
      setQuizzes(res.quizzes || []);
    } catch (error) {
      console.error('Failed to fetch history:', error);
    }
  };

  useEffect(() => {
    fetchHistory();
    // Auto-refresh every 10 seconds to reflect new quizzes
    const intervalId = setInterval(fetchHistory, 10000);
    return () => clearInterval(intervalId);
  }, []);

  const handleView = async (id) => {
    setLoading(true);
    try {
      const res = await getQuizById(id);
      setSelected(res.quiz);
      setOpen(true);
    } catch (error) {
      console.error('Failed to fetch quiz:', error);
      alert('Failed to load quiz details');
    } finally {
      setLoading(false);
    }
  };

  const handleCloseModal = () => {
    setOpen(false);
    setSelected(null);
  };

  return (
    <div className="space-y-6">
      <HistoryTable quizzes={quizzes} onView={handleView} />
      
      <Modal open={open} onClose={handleCloseModal} title={selected?.title || 'Quiz Details'}>
        {loading ? (
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-sky-500"></div>
          </div>
        ) : selected ? (
          <QuizDisplay quiz={selected} />
        ) : (
          <div className="text-center py-4 text-gray-500">Loading quiz...</div>
        )}
      </Modal>
    </div>
  );
}
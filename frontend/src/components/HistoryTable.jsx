import React from 'react';

export default function HistoryTable({ quizzes, onView }) {
  return (
    <div className="card">
      <h3 className="font-semibold mb-4">Quiz History</h3>
      <div className="overflow-auto">
        <table className="min-w-full text-left">
          <thead>
            <tr className="text-gray-600">
              <th className="pb-2">ID</th>
              <th className="pb-2">Title</th>
              <th className="pb-2">URL</th>
              <th className="pb-2">Date</th>
              <th className="pb-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {quizzes && quizzes.map(q => (
              <tr key={q.id} className="border-t">
                <td className="py-3">{q.id}</td>
                <td className="py-3 font-semibold">{q.title}</td>
                <td className="py-3 text-sm text-gray-600 truncate max-w-[40ch]">{q.url}</td>
                <td className="py-3 text-sm text-gray-500">
                  {q.date_generated ? new Date(q.date_generated).toLocaleDateString() : 'N/A'}
                </td>
                <td className="py-3">
                  <button 
                    onClick={() => onView(q.id)} 
                    className="px-3 py-1 rounded-md bg-sky-100 text-sky-700 hover:bg-sky-200 transition-colors"
                  >
                    View Quiz
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {(!quizzes || quizzes.length === 0) && (
          <div className="text-center py-8 text-gray-500">
            No quizzes generated yet. Create your first quiz!
          </div>
        )}
      </div>
    </div>
  );
}
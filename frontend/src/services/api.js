import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

export async function generateQuiz(url, extraQuestions = false) {
  const resp = await axios.post(`${API_BASE}/generate_quiz`, { 
    url, 
    extra_questions: extraQuestions 
  });
  return resp.data;
}

export async function getHistory() {
  const resp = await axios.get(`${API_BASE}/history`);
  return resp.data;
}

export async function getQuizById(id) {
  const resp = await axios.get(`${API_BASE}/quiz/${id}`);
  return resp.data;
}
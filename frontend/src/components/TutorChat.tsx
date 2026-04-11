import React, { useState } from 'react';
import api from '../api/client';

type Source = { chunk_id: string; page_number: number; section: string; content: string };

export default function TutorChat() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [sources, setSources] = useState<Source[]>([]);
  const [loading, setLoading] = useState(false);

  const handleQuestionChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setQuestion(e.target.value);
  };

  const ask = async () => {
    if (!question.trim()) return;
    setLoading(true);
    try {
      const res = await api.post('/chat', { question });
      setAnswer(res.data.answer || 'No answer');
      setSources(res.data.sources || []);
    } catch (error: unknown) {
      const message = (error as { response?: { data?: { detail?: string } } })?.response?.data?.detail;
      setAnswer(`Error: ${message || 'Chat failed'}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="rounded-xl bg-white p-4 shadow-md dark:bg-slate-800">
      <h2 className="mb-3 text-lg font-semibold">AI Tutor Chat</h2>
      <div className="mb-3 flex gap-2">
        <input
          value={question}
          onChange={handleQuestionChange}
          placeholder="Ask a question about the document..."
          className="flex-1 rounded border p-2"
        />
        <button onClick={ask} className="rounded bg-purple-600 px-4 py-2 text-white hover:bg-purple-700">
          {loading ? '...' : 'Ask'}
        </button>
      </div>

      <p className="whitespace-pre-wrap text-sm">{answer}</p>
      {!!sources.length && (
        <div className="mt-3">
          <p className="mb-2 text-sm font-medium">Sources</p>
          <ul className="space-y-2 text-xs text-slate-600 dark:text-slate-300">
            {sources.map((s, i) => (
              <li key={`${s.chunk_id}-${i}`} className="rounded border p-2">
                Page {s.page_number} - {s.section}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

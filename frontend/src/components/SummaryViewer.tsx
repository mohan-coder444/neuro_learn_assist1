import ReactMarkdown from 'react-markdown';
import { cleanTextForSpeech } from '../utils/textUtils';

type Props = { summary: string };

export default function SummaryViewer({ summary }: Readonly<Props>) {
  const speakSummary = () => {
    if (!("speechSynthesis" in globalThis) || !summary.trim()) return;
    const cleanText = cleanTextForSpeech(summary);
    const utterance = new SpeechSynthesisUtterance(cleanText.slice(0, 2200));
    utterance.rate = 1;
    globalThis.speechSynthesis.speak(utterance);
  };

  return (
    <section id="summary" className="rounded-2xl border border-slate-200 bg-white/90 p-5 shadow-sm dark:border-slate-700 dark:bg-slate-900/60">
      <div className="mb-3 flex items-center justify-between">
        <h2 className="text-lg font-semibold">AI Summary</h2>
        <button
          onClick={speakSummary}
          className="rounded-lg border border-blue-200 bg-blue-50 px-3 py-1.5 text-xs font-medium text-blue-700 transition hover:bg-blue-100 dark:border-blue-500/50 dark:bg-blue-500/10 dark:text-blue-300"
        >
          Listen Explanation
        </button>
      </div>
      <div className="prose prose-slate max-w-none text-[15px] leading-7 dark:prose-invert">
        {summary ? (
          <ReactMarkdown>{summary}</ReactMarkdown>
        ) : (
          <p className="text-slate-500">No summary yet.</p>
        )}
      </div>
    </section>
  );
}

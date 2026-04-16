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

  const [isGenerating, setIsGenerating] = React.useState(false);

  const downloadMP4 = async () => {
    setIsGenerating(true);
    try {
      // Use a hidden anchor to trigger download instead of window.open
      const response = await api.get('/download-mp4', { responseType: 'blob' });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'explanation.mp4');
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      console.error('Download failed:', err);
      alert('Video generation failed. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <section id="summary" className="rounded-2xl border border-slate-200 bg-white/90 p-5 shadow-sm dark:border-slate-700 dark:bg-slate-900/60">
      <div className="mb-3 flex items-center justify-between">
        <h2 className="text-lg font-semibold">AI Summary</h2>
        <div className="flex gap-2">
          <button
            onClick={speakSummary}
            className="rounded-lg border border-blue-200 bg-blue-50 px-3 py-1.5 text-xs font-medium text-blue-700 transition hover:bg-blue-100 dark:border-blue-500/50 dark:bg-blue-500/10 dark:text-blue-300"
          >
            Listen Explanation
          </button>
          <button
            onClick={downloadMP4}
            disabled={isGenerating}
            className="flex items-center gap-1.5 rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-xs font-medium text-slate-700 transition hover:bg-slate-50 disabled:opacity-50 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300 dark:hover:bg-slate-700"
          >
            {isGenerating ? (
              <>
                <div className="h-3 w-3 animate-spin rounded-full border-2 border-slate-400 border-t-transparent" />
                Generating...
              </>
            ) : (
              <>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                Download MP4
              </>
            )}
          </button>
        </div>
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

import React, { useMemo, useState } from 'react';

type QuizItem = {
  question: string;
  options: string[];
  correct_answer: string;
  explanation: string;
};

type Props = { quiz: QuizItem[] };

export default function Quiz({ quiz }: Readonly<Props>) {
  const [index, setIndex] = useState(0);
  const [selected, setSelected] = useState<Record<number, string>>({});

  const current = quiz[index];

  const progress = useMemo(() => {
    if (!quiz.length) return 0;
    return ((index + 1) / quiz.length) * 100;
  }, [index, quiz.length]);

  if (!quiz.length) {
    return (
      <section id="quiz" className="rounded-2xl border border-slate-200 bg-white/90 p-5 shadow-sm dark:border-slate-700 dark:bg-slate-900/60">
        <h2 className="text-lg font-semibold">Quiz</h2>
        <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">No quiz yet. Upload a document first.</p>
      </section>
    );
  }

  const picked = selected[index];

  const optionClass = (opt: string) => {
    if (!picked) return 'border-slate-200 hover:bg-slate-50 dark:border-slate-700 dark:hover:bg-slate-800';
    if (opt === current.correct_answer) return 'border-emerald-500 bg-emerald-50 text-emerald-800 dark:bg-emerald-500/10 dark:text-emerald-200';
    if (opt === picked) return 'border-rose-500 bg-rose-50 text-rose-800 dark:bg-rose-500/10 dark:text-rose-200';
    return 'border-slate-200 opacity-70 dark:border-slate-700';
  };

  return (
    <section id="quiz" className="rounded-2xl border border-slate-200 bg-white/90 p-5 shadow-sm dark:border-slate-700 dark:bg-slate-900/60">
      <div className="mb-3 flex items-center justify-between">
        <h2 className="text-lg font-semibold">Adaptive Quiz</h2>
        <p className="text-xs text-slate-500 dark:text-slate-400">Question {index + 1} / {quiz.length}</p>
      </div>

      <div className="mb-4 h-2 w-full overflow-hidden rounded-full bg-slate-200 dark:bg-slate-700">
        <div className="h-full rounded-full bg-blue-600 transition-all" style={{ width: `${progress}%` }} />
      </div>

      <div className="rounded-xl border border-slate-200 p-4 dark:border-slate-700">
        <p className="text-base font-medium leading-7">{current.question}</p>

        <div className="mt-4 grid gap-2">
          {current.options.map((opt, i) => (
            <button
              key={`${opt}-${i}`}
              onClick={() => setSelected((prev) => ({ ...prev, [index]: opt }))}
              className={`rounded-xl border px-3 py-2 text-left text-sm transition ${optionClass(opt)}`}
            >
              {opt}
            </button>
          ))}
        </div>

        {picked && (
          <div className="mt-3 rounded-lg bg-slate-50 p-3 text-sm dark:bg-slate-800/80">
            <p className="font-medium">{picked === current.correct_answer ? 'Correct ✅' : 'Incorrect ❌'}</p>
            <p className="mt-1 text-slate-600 dark:text-slate-300">{current.explanation}</p>
          </div>
        )}
      </div>

      <div className="mt-4 flex items-center gap-2">
        <button
          onClick={() => setIndex((v) => Math.max(0, v - 1))}
          disabled={index === 0}
          className="rounded-xl border border-slate-300 px-4 py-2 text-sm transition hover:bg-slate-100 disabled:opacity-50 dark:border-slate-600 dark:hover:bg-slate-800"
        >
          Previous
        </button>
        <button
          onClick={() => setIndex((v) => Math.min(quiz.length - 1, v + 1))}
          disabled={index === quiz.length - 1}
          className="rounded-xl bg-blue-600 px-4 py-2 text-sm text-white transition hover:bg-blue-700 disabled:opacity-50"
        >
          Next
        </button>
      </div>
    </section>
  );
}

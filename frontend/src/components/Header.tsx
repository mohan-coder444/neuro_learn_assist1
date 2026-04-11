import React from 'react';
import { Accessibility, BadgeCheck, Mic, MoonStar, Sun } from 'lucide-react';

type Props = {
  darkMode: boolean;
  onToggleDark: () => void;
  onMicClick: () => void;
  onOpenAccessibility: () => void;
};

export default function Header({ darkMode, onToggleDark, onMicClick, onOpenAccessibility }: Readonly<Props>) {
  return (
    <header className="sticky top-0 z-30 border-b border-slate-200/70 bg-white/70 px-5 py-4 shadow-sm backdrop-blur-xl dark:border-slate-700 dark:bg-slate-900/70">
      <div className="flex items-center justify-between gap-3">
        <div>
          <h1 className="text-xl font-semibold tracking-tight">NeuroLearn Assist</h1>
          <p className="text-xs text-slate-500 dark:text-slate-400">Inclusive AI Tutor for accessible learning</p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={onMicClick}
            className="rounded-xl border border-slate-200 bg-white p-2 text-slate-700 transition hover:-translate-y-0.5 hover:bg-slate-100 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200"
            aria-label="Open voice tutor"
          >
            <Mic size={18} />
          </button>

          <button
            onClick={onToggleDark}
            className="rounded-xl border border-slate-200 bg-white p-2 text-slate-700 transition hover:-translate-y-0.5 hover:bg-slate-100 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200"
            aria-label="Toggle dark mode"
          >
            {darkMode ? <Sun size={18} /> : <MoonStar size={18} />}
          </button>

          <button
            onClick={onOpenAccessibility}
            className="rounded-xl border border-slate-200 bg-white p-2 text-slate-700 transition hover:-translate-y-0.5 hover:bg-slate-100 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200"
            aria-label="Open accessibility settings"
          >
            <Accessibility size={18} />
          </button>

          <div className="ml-1 flex items-center gap-1 rounded-full border border-blue-200 bg-blue-50 px-3 py-1 text-xs font-medium text-blue-700 dark:border-blue-500/50 dark:bg-blue-500/10 dark:text-blue-300">
            <BadgeCheck size={14} />
            Demo
          </div>
        </div>
      </div>
    </header>
  );
}

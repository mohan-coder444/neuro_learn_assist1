import React from 'react';
import {
  BookOpenText,
  BrainCircuit,
  ChevronLeft,
  ChevronRight,
  FileUp,
  FileQuestion,
  Layers3,
  Mic2,
  Settings2,
} from 'lucide-react';

type NavItem = {
  id: string;
  label: string;
  icon: React.ReactNode;
};

type Props = {
  collapsed: boolean;
  activeSection: string;
  onToggle: () => void;
  onNavigate: (id: string) => void;
};

const NAV_ITEMS: NavItem[] = [
  { id: 'upload', label: 'Upload Document', icon: <FileUp size={18} /> },
  { id: 'summary', label: 'AI Summary', icon: <BookOpenText size={18} /> },
  { id: 'concepts', label: 'Key Concepts', icon: <BrainCircuit size={18} /> },
  { id: 'flashcards', label: 'Flashcards', icon: <Layers3 size={18} /> },
  { id: 'quiz', label: 'Quiz', icon: <FileQuestion size={18} /> },
  { id: 'voice', label: 'Voice Tutor', icon: <Mic2 size={18} /> },
  { id: 'settings', label: 'Accessibility Settings', icon: <Settings2 size={18} /> },
];

export default function Sidebar({ collapsed, activeSection, onToggle, onNavigate }: Readonly<Props>) {
  return (
    <aside
      className={`sticky top-0 h-screen border-r border-slate-200/60 bg-white/80 backdrop-blur-xl transition-all duration-300 dark:border-slate-700 dark:bg-slate-900/70 ${
        collapsed ? 'w-20' : 'w-72'
      }`}
    >
      <div className="flex h-full flex-col">
        <div className="flex items-center justify-between border-b border-slate-200/70 px-4 py-4 dark:border-slate-700">
          <div className="flex items-center gap-3">
            <div className="grid h-9 w-9 place-content-center rounded-xl bg-blue-600 text-white shadow-lg shadow-blue-500/30">N</div>
            {!collapsed && <p className="text-sm font-semibold tracking-wide">NeuroLearn Assist</p>}
          </div>
          <button
            onClick={onToggle}
            className="rounded-lg border border-slate-200 p-1 text-slate-600 transition hover:bg-slate-100 dark:border-slate-600 dark:text-slate-300 dark:hover:bg-slate-800"
            aria-label="Toggle sidebar"
          >
            {collapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
          </button>
        </div>

        <nav className="flex-1 space-y-1 p-3">
          {NAV_ITEMS.map((item) => {
            const active = activeSection === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onNavigate(item.id)}
                className={`group flex w-full items-center gap-3 rounded-xl px-3 py-2 text-sm transition ${
                  active
                    ? 'bg-blue-600 text-white shadow-md shadow-blue-500/30'
                    : 'text-slate-700 hover:bg-slate-100 dark:text-slate-200 dark:hover:bg-slate-800'
                }`}
              >
                <span className={`${active ? 'text-white' : 'text-slate-500 dark:text-slate-300'}`}>{item.icon}</span>
                {!collapsed && <span className="text-left">{item.label}</span>}
              </button>
            );
          })}
        </nav>
      </div>
    </aside>
  );
}

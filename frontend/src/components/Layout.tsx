import React from 'react';
import { Link } from 'react-router-dom';

import Header from './Header';
import Sidebar from './Sidebar';

type Props = {
  darkMode: boolean;
  sidebarCollapsed: boolean;
  activeSection: string;
  onToggleDark: () => void;
  onToggleSidebar: () => void;
  onNavigate: (id: string) => void;
  children: React.ReactNode;
};

export default function Layout({
  darkMode,
  sidebarCollapsed,
  activeSection,
  onToggleDark,
  onToggleSidebar,
  onNavigate,
  children,
}: Readonly<Props>) {
  return (
    <div className="dark flex min-h-screen bg-[#050816] text-slate-100">
      {/* Back to Landing strip */}
      <div className="fixed top-0 left-0 right-0 z-40 flex items-center justify-between
                      px-5 py-2 bg-[rgba(5,8,22,0.9)] backdrop-blur-xl
                      border-b border-white/[0.06] text-xs">
        <Link to="/"
          className="flex items-center gap-1.5 text-slate-400 hover:text-slate-100 transition-colors group">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
            <polyline points="15 18 9 12 15 6" />
          </svg>
          Back to Landing
        </Link>
        <span className="text-violet-400 font-semibold tracking-wide">NeuroLearn Assist Dashboard</span>
        <div className="flex items-center gap-1.5">
          <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" aria-hidden="true" />
          <span className="text-slate-500">AI Active</span>
        </div>
      </div>

      <Sidebar
        collapsed={sidebarCollapsed}
        activeSection={activeSection}
        onToggle={onToggleSidebar}
        onNavigate={onNavigate}
      />

      <div className="flex min-w-0 flex-1 flex-col pt-9">
        <Header
          darkMode={darkMode}
          onToggleDark={onToggleDark}
          onMicClick={() => onNavigate('voice')}
          onOpenAccessibility={() => onNavigate('settings')}
        />

        <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">
          <div className="mx-auto max-w-7xl space-y-6">{children}</div>
        </main>
      </div>
    </div>
  );
}

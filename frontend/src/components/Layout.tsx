import React from 'react';

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
    <div className="flex min-h-screen bg-slate-100 text-slate-900 dark:bg-slate-950 dark:text-slate-100">
      <Sidebar
        collapsed={sidebarCollapsed}
        activeSection={activeSection}
        onToggle={onToggleSidebar}
        onNavigate={onNavigate}
      />

      <div className="flex min-w-0 flex-1 flex-col">
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

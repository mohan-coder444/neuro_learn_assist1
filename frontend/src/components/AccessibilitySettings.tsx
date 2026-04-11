import React, { useEffect, useState } from 'react';
import type { AxiosResponse } from 'axios';
import api from '../api/client';

type Settings = {
  mode: 'visual' | 'audio' | 'braille' | 'combined';
  voice_speed: number;
  auto_read_aloud: boolean;
  braille_enabled: boolean;
  high_contrast: boolean;
};

const defaults: Settings = {
  mode: 'visual',
  voice_speed: 1,
  auto_read_aloud: false,
  braille_enabled: false,
  high_contrast: false,
};

export default function AccessibilitySettings() {
  const [settings, setSettings] = useState<Settings>(defaults);
  const [largeText, setLargeText] = useState(false);
  const [screenReaderMode, setScreenReaderMode] = useState(false);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    api
      .get('/accessibility')
      .then((r: AxiosResponse<Settings>) => setSettings(r.data))
      .catch(() => undefined);
  }, []);

  const save = async () => {
    await api.post('/accessibility', settings);
    setSaved(true);
    setTimeout(() => setSaved(false), 1800);
  };

  useEffect(() => {
    const root = document.documentElement;
    if (largeText) {
      root.classList.add('text-[17px]');
    } else {
      root.classList.remove('text-[17px]');
    }
  }, [largeText]);

  return (
    <section id="settings" className={`rounded-2xl border p-5 shadow-sm ${settings.high_contrast ? 'border-white bg-black text-white' : 'border-slate-200 bg-white/90 dark:border-slate-700 dark:bg-slate-900/60'}`}>
      <h2 className="mb-1 text-lg font-semibold">Accessibility Settings</h2>
      <p className="mb-4 text-sm text-slate-500 dark:text-slate-400">Inclusive controls for voice, contrast, braille, and reading comfort.</p>

      <div className="grid gap-4 md:grid-cols-2">
        <label className="text-sm font-medium">
          <span>Mode</span>
          <select
            value={settings.mode}
            onChange={(e: React.ChangeEvent<HTMLSelectElement>) =>
              setSettings({ ...settings, mode: e.target.value as Settings['mode'] })
            }
            className="mt-1 w-full rounded-xl border border-slate-300 bg-white p-2.5 text-black dark:border-slate-600 dark:bg-slate-800 dark:text-white"
          >
            <option value="visual">Visual Mode</option>
            <option value="audio">Audio Mode</option>
            <option value="braille">Braille Mode</option>
            <option value="combined">Combined Mode</option>
          </select>
        </label>

        <label className="text-sm font-medium">
          <span>Voice speed: {settings.voice_speed.toFixed(2)}</span>
          <input
            type="range"
            min={0.7}
            max={1.2}
            step={0.05}
            value={settings.voice_speed}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              setSettings({ ...settings, voice_speed: Number(e.target.value) })
            }
            className="mt-2 w-full accent-blue-600"
          />
        </label>

        <label className="flex items-center justify-between rounded-xl border border-slate-200 p-3 text-sm dark:border-slate-700">
          <span>Auto read aloud</span>
          <input
            type="checkbox"
            checked={settings.auto_read_aloud}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              setSettings({ ...settings, auto_read_aloud: e.target.checked })
            }
            className="h-4 w-4"
          />
        </label>

        <label className="flex items-center justify-between rounded-xl border border-slate-200 p-3 text-sm dark:border-slate-700">
          <span>Braille output</span>
          <input
            type="checkbox"
            checked={settings.braille_enabled}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              setSettings({ ...settings, braille_enabled: e.target.checked })
            }
            className="h-4 w-4"
          />
        </label>

        <label className="flex items-center justify-between rounded-xl border border-slate-200 p-3 text-sm dark:border-slate-700">
          <span>High contrast mode</span>
          <input
            type="checkbox"
            checked={settings.high_contrast}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              setSettings({ ...settings, high_contrast: e.target.checked })
            }
            className="h-4 w-4"
          />
        </label>

        <label className="flex items-center justify-between rounded-xl border border-slate-200 p-3 text-sm dark:border-slate-700">
          <span>Large text</span>
          <input type="checkbox" checked={largeText} onChange={(e) => setLargeText(e.target.checked)} className="h-4 w-4" />
        </label>

        <label className="flex items-center justify-between rounded-xl border border-slate-200 p-3 text-sm dark:border-slate-700">
          <span>Screen reader mode</span>
          <input type="checkbox" checked={screenReaderMode} onChange={(e) => setScreenReaderMode(e.target.checked)} className="h-4 w-4" />
        </label>
      </div>

      <button onClick={save} className="mt-4 rounded-xl bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-md shadow-blue-500/30 transition hover:bg-blue-700">
        Save accessibility settings
      </button>
      {saved && <p className="mt-2 text-xs text-emerald-600 dark:text-emerald-400">Settings saved.</p>}
      {screenReaderMode && <p className="mt-2 text-xs text-slate-500 dark:text-slate-400">Screen reader optimization enabled.</p>}
    </section>
  );
}

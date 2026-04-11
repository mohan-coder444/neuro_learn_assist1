import React, { useEffect, useMemo } from 'react';
import api from '../api/client';

type Concept = { concept: string; explanation: string };
type Props = { concepts: Concept[]; voiceExplanation?: string; fallbackSpeechText?: string };

export default function ConceptsViewer({ concepts, voiceExplanation, fallbackSpeechText }: Readonly<Props>) {
  const voiceUrl = useMemo(() => {
    if (!voiceExplanation) return '';
    if (voiceExplanation.startsWith('http')) return voiceExplanation;
    return `${api.defaults.baseURL}${voiceExplanation}`;
  }, [voiceExplanation]);

  useEffect(() => {
    if (voiceUrl) {
      localStorage.setItem('neurolearn_voice_explanation', voiceUrl);
    }
  }, [voiceUrl]);

  useEffect(() => {
    if (voiceUrl || !fallbackSpeechText?.trim()) return;
    if (!("speechSynthesis" in globalThis)) return;

    const key = `neurolearn_last_spoken_explanation_${fallbackSpeechText.slice(0, 48)}`;
    if (localStorage.getItem(key)) return;

    const utterance = new SpeechSynthesisUtterance(fallbackSpeechText.slice(0, 1800));
    utterance.rate = 1;
    globalThis.speechSynthesis.speak(utterance);
    localStorage.setItem(key, '1');
  }, [voiceUrl, fallbackSpeechText]);

  const explainConcept = (concept: Concept) => {
    if (!("speechSynthesis" in globalThis)) return;
    const utterance = new SpeechSynthesisUtterance(`${concept.concept}. ${concept.explanation}`);
    utterance.rate = 1;
    globalThis.speechSynthesis.speak(utterance);
  };

  return (
    <section id="concepts" className="rounded-2xl border border-slate-200 bg-white/90 p-5 shadow-sm dark:border-slate-700 dark:bg-slate-900/60">
      <div className="mb-4 flex items-center justify-between gap-3">
        <h2 className="text-lg font-semibold">Key Concepts</h2>
        <p className="text-xs text-slate-500 dark:text-slate-400">Smart concept cards with AI voice explain</p>
      </div>

      {voiceUrl && (
        <audio autoPlay controls className="mb-4 w-full rounded-xl" src={voiceUrl}>
          <track kind="captions" />
        </audio>
      )}

      <ul className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
        {concepts.map((c) => (
          <li
            key={c.concept}
            className="group rounded-2xl border border-slate-200 bg-slate-50 p-4 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md dark:border-slate-700 dark:bg-slate-800/70"
          >
            <p className="text-base font-semibold tracking-tight">{c.concept}</p>
            <p className="mt-2 text-sm leading-6 text-slate-600 dark:text-slate-300">{c.explanation}</p>
            <button
              onClick={() => explainConcept(c)}
              className="mt-3 rounded-lg border border-blue-200 bg-blue-50 px-3 py-1.5 text-xs font-medium text-blue-700 transition hover:bg-blue-100 dark:border-blue-500/40 dark:bg-blue-500/10 dark:text-blue-300"
            >
              Explain with AI
            </button>
          </li>
        ))}
      </ul>
    </section>
  );
}

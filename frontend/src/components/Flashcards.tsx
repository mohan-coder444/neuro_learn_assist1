import React, { useState } from 'react';

type Card = { question: string; answer: string };
type Props = { cards: Card[] };

export default function Flashcards({ cards }: Readonly<Props>) {
  const [index, setIndex] = useState(0);
  const [flipped, setFlipped] = useState(false);

  if (!cards.length) {
    return (
      <section id="flashcards" className="rounded-2xl border border-slate-200 bg-white/90 p-5 shadow-sm dark:border-slate-700 dark:bg-slate-900/60">
        <h2 className="text-lg font-semibold">Flashcards</h2>
        <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">No flashcards yet. Upload a document first.</p>
      </section>
    );
  }

  const card = cards[index];

  const goPrev = () => {
    setFlipped(false);
    setIndex((prev) => (prev === 0 ? cards.length - 1 : prev - 1));
  };

  const goNext = () => {
    setFlipped(false);
    setIndex((prev) => (prev === cards.length - 1 ? 0 : prev + 1));
  };

  return (
    <section id="flashcards" className="rounded-2xl border border-slate-200 bg-white/90 p-5 shadow-sm dark:border-slate-700 dark:bg-slate-900/60">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-lg font-semibold">Flashcards</h2>
        <p className="text-xs text-slate-500 dark:text-slate-400">Card {index + 1} / {cards.length}</p>
      </div>

      <button
        onClick={() => setFlipped((v) => !v)}
        className="relative h-56 w-full rounded-2xl border border-slate-200 bg-gradient-to-br from-white to-slate-50 p-6 text-left shadow-md transition duration-500 [transform-style:preserve-3d] hover:-translate-y-0.5 dark:border-slate-700 dark:from-slate-800 dark:to-slate-900"
        style={{ transform: flipped ? 'rotateY(180deg)' : 'rotateY(0deg)' }}
      >
        <div className="absolute inset-0 rounded-2xl p-6 [backface-visibility:hidden]">
          <p className="mb-3 text-xs uppercase tracking-wide text-blue-600 dark:text-blue-300">Question</p>
          <p className="text-base leading-7">{card.question}</p>
        </div>
        <div className="absolute inset-0 rounded-2xl p-6 [backface-visibility:hidden]" style={{ transform: 'rotateY(180deg)' }}>
          <p className="mb-3 text-xs uppercase tracking-wide text-emerald-600 dark:text-emerald-300">Answer</p>
          <p className="text-base leading-7">{card.answer}</p>
        </div>
      </button>

      <div className="mt-4 flex items-center gap-2">
        <button onClick={goPrev} className="rounded-xl border border-slate-300 px-4 py-2 text-sm transition hover:bg-slate-100 dark:border-slate-600 dark:hover:bg-slate-800">Previous</button>
        <button onClick={goNext} className="rounded-xl bg-blue-600 px-4 py-2 text-sm text-white transition hover:bg-blue-700">Next card</button>
      </div>
    </section>
  );
}

'use client';
import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';

const testimonials = [
  { name: 'Arjun S.', title: 'Student, Visual Impairment', initials: 'AS', color: '#3b82f6',
    quote: 'NeuroLearn Assist transformed how I study. The voice tutor feels like a real teacher available 24/7. Absolute game changer.' },
  { name: 'Priya M.', title: 'Special Education Teacher', initials: 'PM', color: '#8b5cf6',
    quote: 'I recommend this to all my students. The braille integration is seamless and adaptive quizzes keep every learner engaged.' },
  { name: 'Carlos R.', title: 'University Student', initials: 'CR', color: '#06b6d4',
    quote: 'The PDF analysis understood complex research papers and created perfect flashcards automatically. Truly incredible technology.' },
  { name: 'Fatima K.', title: 'Deaf-Blind Learner', initials: 'FK', color: '#ec4899',
    quote: 'For the first time, I can learn independently. The braille and voice combination is a complete breakthrough for me.' },
  { name: 'David L.', title: 'Parent of Blind Child', initials: 'DL', color: '#22c55e',
    quote: 'My daughter can now study alongside her peers. This platform gave her confidence and independence she deserved.' },
  { name: 'Riya T.', title: 'Accessibility Researcher', initials: 'RT', color: '#f97316',
    quote: 'Real WCAG compliance with actual usability — rare to find. Technically impressive and genuinely helpful for all users.' },
];

function TestimonialCard({ t }: { t: typeof testimonials[0] }) {
  return (
    <div className="glass-strong rounded-2xl p-7 min-w-[320px] max-w-[340px] flex-shrink-0 cursor-default
                    hover:border-violet-500/40 transition-all duration-300 hover:shadow-[0_0_30px_rgba(139,92,246,0.12)]">
      <div className="flex gap-1 mb-4" aria-label="5 star rating">
        {Array.from({ length: 5 }).map((_, i) => (
          <svg key={i} width="15" height="15" viewBox="0 0 24 24" fill="#fbbf24" aria-hidden="true">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
          </svg>
        ))}
      </div>
      <p className="text-slate-400 text-sm leading-relaxed italic mb-5">"{t.quote}"</p>
      <div className="flex items-center gap-3">
        <div
          className="w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0"
          style={{ background: `${t.color}22`, color: t.color }}
          aria-hidden="true"
        >
          {t.initials}
        </div>
        <div>
          <div className="text-sm font-semibold text-slate-200">{t.name}</div>
          <div className="text-xs text-slate-500">{t.title}</div>
        </div>
      </div>
    </div>
  );
}

export default function Testimonials() {
  const titleRef = useRef(null);
  const titleInView = useInView(titleRef, { once: true, margin: '-60px' });
  const doubled = [...testimonials, ...testimonials];

  return (
    <section id="testimonials" className="py-28 overflow-hidden" aria-labelledby="test-heading">
      <div className="max-w-6xl mx-auto px-6">
        <motion.div
          ref={titleRef}
          initial={{ opacity: 0, y: 32 }}
          animate={titleInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.7 }}
          className="text-center mb-14"
        >
          <div className="section-tag">Testimonials</div>
          <h2 className="text-4xl sm:text-5xl font-black text-slate-100 mt-2" id="test-heading">
            Loved by{' '}
            <span className="gradient-heading">Learners Worldwide</span>
          </h2>
        </motion.div>
      </div>

      <div
        className="relative [mask-image:linear-gradient(90deg,transparent,black_10%,black_90%,transparent)]"
        role="region"
        aria-label="Testimonials carousel"
      >
        <div className="flex gap-5 w-max [&:hover>*]:![animation-play-state:paused]">
        <motion.div
          className="flex gap-5 w-max"
          animate={{ x: ['0%', '-50%'] }}
          transition={{ duration: 40, ease: 'linear', repeat: Infinity }}
        >
          {doubled.map((t, i) => (
            <TestimonialCard key={`${t.name}-${i}`} t={t} />
          ))}
        </motion.div>
        </div>
      </div>
    </section>
  );
}

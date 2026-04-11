'use client';
import { useRef } from 'react';
import { motion, useInView, useScroll, useTransform } from 'framer-motion';

const steps = [
  {
    num: '01',
    icon: (
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <polyline points="14 2 14 8 20 8" />
        <line x1="16" y1="13" x2="8" y2="13" /><line x1="16" y1="17" x2="8" y2="17" />
      </svg>
    ),
    title: 'Upload Document',
    desc: 'Upload any PDF or document. Our AI extracts, reads, and fully comprehends the content with smart OCR fallback.',
  },
  {
    num: '02',
    icon: (
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
        <circle cx="12" cy="12" r="10" /><path d="M12 8v4l3 3" />
      </svg>
    ),
    title: 'AI Analyzes',
    desc: 'Multi-agent AI instantly generates summaries, concept maps, flashcards, and personalized quiz questions.',
  },
  {
    num: '03',
    icon: (
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
        <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" />
        <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
        <line x1="12" y1="19" x2="12" y2="23" /><line x1="8" y1="23" x2="16" y2="23" />
      </svg>
    ),
    title: 'Learn Your Way',
    desc: 'Use voice conversation, braille output, flashcards, or adaptive quizzes — whatever works best for you.',
  },
  {
    num: '04',
    icon: (
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
        <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
      </svg>
    ),
    title: 'Track Progress',
    desc: 'Adaptive AI monitors your performance and continuously fine-tunes difficulty to keep you challenged and growing.',
  },
];

// Single step card — hooks safe (not in a map)
function StepCard({ step, index }: { step: typeof steps[0]; index: number }) {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: '-60px' });
  return (
    <motion.div
      ref={ref}
      className="flex flex-col items-center text-center group"
      initial={{ opacity: 0, y: 48 }}
      animate={inView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.65, delay: index * 0.15, ease: 'easeOut' }}
    >
      <motion.div
        className="relative w-[88px] h-[88px] rounded-full mb-6 flex items-center justify-center
                   bg-gradient-to-br from-blue-600 to-violet-700 text-white z-10
                   shadow-[0_0_30px_rgba(139,92,246,0.4)] cursor-default"
        whileHover={{ scale: 1.12, boxShadow: '0 0 55px rgba(139,92,246,0.7)' }}
        transition={{ type: 'spring', stiffness: 260, damping: 20 }}
      >
        <div className="flex flex-col items-center">
          <span className="text-white/60 text-[0.6rem] font-black uppercase tracking-widest leading-none">{step.num}</span>
          <div className="mt-0.5 text-white">{step.icon}</div>
        </div>
      </motion.div>
      <h3 className="text-base font-bold text-slate-100 mb-2">{step.title}</h3>
      <p className="text-slate-400 text-sm leading-relaxed">{step.desc}</p>
    </motion.div>
  );
}

export default function HowItWorks() {
  const ref = useRef<HTMLElement>(null);
  const { scrollYProgress } = useScroll({ target: ref, offset: ['start end', 'end start'] });
  const lineWidth = useTransform(scrollYProgress, [0.1, 0.8], ['0%', '100%']);
  const titleRef = useRef(null);
  const titleInView = useInView(titleRef, { once: true, margin: '-60px' });

  return (
    <section
      ref={ref}
      id="how"
      className="relative py-28 px-6 overflow-hidden bg-[radial-gradient(ellipse_60%_50%_at_50%_50%,rgba(139,92,246,0.08)_0%,transparent_70%)]"
      aria-labelledby="how-heading"
    >
      <div className="max-w-6xl mx-auto">
        <motion.div
          ref={titleRef}
          initial={{ opacity: 0, y: 32 }}
          animate={titleInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.7 }}
          className="text-center mb-20"
        >
          <div className="section-tag">Process</div>
          <h2 className="text-4xl sm:text-5xl font-black text-slate-100 mt-2 mb-4" id="how-heading">
            Simple.{' '}
            <span className="gradient-heading">Powerful.</span>
            {' '}Accessible.
          </h2>
          <p className="text-slate-400 text-lg max-w-xl mx-auto">
            Get started in seconds — no technical knowledge required.
          </p>
        </motion.div>

        {/* Animated timeline connector (desktop only) */}
        <div className="hidden lg:block relative mb-12">
          <div className="absolute top-[44px] left-[12%] right-[12%] h-[2px] bg-white/5 rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-gradient-to-r from-blue-500 via-violet-500 to-pink-500 rounded-full"
              style={{ width: lineWidth }}
            />
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-10 relative">
          {steps.map((step, i) => (
            <StepCard key={step.num} step={step} index={i} />
          ))}
        </div>
      </div>
    </section>
  );
}

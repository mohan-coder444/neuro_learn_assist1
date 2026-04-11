'use client';
import { motion } from 'framer-motion';
import { useInView } from 'framer-motion';
import { useRef } from 'react';

const features = [
  {
    icon: (
      <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
        <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" />
        <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
        <line x1="12" y1="19" x2="12" y2="23" /><line x1="8" y1="23" x2="16" y2="23" />
      </svg>
    ),
    color: 'from-blue-500/20 to-blue-600/10 text-blue-400',
    glow: 'group-hover:shadow-[0_0_30px_rgba(59,130,246,0.25)]',
    badge: 'Voice First',
    title: 'Voice AI Tutor',
    desc: 'Natural AI-powered voice conversations. Ask questions, get explanations, and learn hands-free through intelligent dialogue.',
  },
  {
    icon: (
      <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <polyline points="14 2 14 8 20 8" /><line x1="16" y1="13" x2="8" y2="13" /><line x1="16" y1="17" x2="8" y2="17" />
      </svg>
    ),
    color: 'from-violet-500/20 to-violet-600/10 text-violet-400',
    glow: 'group-hover:shadow-[0_0_30px_rgba(139,92,246,0.25)]',
    badge: 'AI Powered',
    title: 'PDF Intelligence',
    desc: 'Upload any PDF and instantly get AI-generated summaries, concept maps, flashcards, and personalized quiz questions.',
  },
  {
    icon: (
      <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
        <rect x="2" y="3" width="20" height="14" rx="2" /><line x1="8" y1="21" x2="16" y2="21" /><line x1="12" y1="17" x2="12" y2="21" />
      </svg>
    ),
    color: 'from-cyan-500/20 to-cyan-600/10 text-cyan-400',
    glow: 'group-hover:shadow-[0_0_30px_rgba(6,182,212,0.25)]',
    badge: 'Hardware',
    title: 'Braille Output',
    desc: 'Seamless braille conversion with Arduino integration for tactile displays — full blind-accessible learning experience.',
  },
  {
    icon: (
      <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
        <path d="M9 3H5a2 2 0 0 0-2 2v4m6-6h10a2 2 0 0 1 2 2v4M9 3v18m0 0h10a2 2 0 0 0 2-2V9M9 21H5a2 2 0 0 1-2-2V9m0 0h18" />
      </svg>
    ),
    color: 'from-pink-500/20 to-pink-600/10 text-pink-400',
    glow: 'group-hover:shadow-[0_0_30px_rgba(236,72,153,0.25)]',
    badge: 'Adaptive AI',
    title: 'Adaptive Quizzes',
    desc: 'Dynamic difficulty that adjusts in real-time based on your performance. Always learning at exactly the right pace.',
  },
  {
    icon: (
      <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" /><circle cx="9" cy="7" r="4" />
        <path d="M23 21v-2a4 4 0 0 0-3-3.87" /><path d="M16 3.13a4 4 0 0 1 0 7.75" />
      </svg>
    ),
    color: 'from-green-500/20 to-green-600/10 text-green-400',
    glow: 'group-hover:shadow-[0_0_30px_rgba(34,197,94,0.25)]',
    badge: 'Multi-Agent',
    title: 'Multi-Agent Tutor',
    desc: 'A coordinated team of AI agents — knowledge, evaluation, command, and voice — working together seamlessly for you.',
  },
  {
    icon: (
      <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
        <rect x="3" y="11" width="18" height="11" rx="2" ry="2" /><path d="M7 11V7a5 5 0 0 1 10 0v4" />
      </svg>
    ),
    color: 'from-orange-500/20 to-orange-600/10 text-orange-400',
    glow: 'group-hover:shadow-[0_0_30px_rgba(249,115,22,0.25)]',
    badge: 'Privacy First',
    title: 'Private & Secure',
    desc: 'All documents processed end-to-end with encryption. Your learning data stays completely private, always.',
  },
];

function FeatureCard({ feature, index }: { feature: typeof features[0]; index: number }) {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: '-80px' });

  return (
    <motion.article
      ref={ref}
      initial={{ opacity: 0, y: 48 }}
      animate={inView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.65, delay: index * 0.1, ease: [0.22, 1, 0.36, 1] }}
      className="group glass-strong rounded-2xl p-8 card-hover cursor-pointer relative overflow-hidden"
      whileHover={{ scale: 1.01 }}
    >
      {/* Shine effect on hover */}
      <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none bg-[linear-gradient(135deg,rgba(59,130,246,0.04),rgba(139,92,246,0.04))]"
        aria-hidden="true"
      />

      <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${feature.color} ${feature.glow} flex items-center justify-center mb-5 transition-shadow duration-300`}>
        {feature.icon}
      </div>

      <h3 className="text-lg font-bold text-slate-100 mb-2">{feature.title}</h3>
      <p className="text-slate-400 text-sm leading-relaxed">{feature.desc}</p>

      <div className="mt-5 inline-block text-[0.65rem] font-bold uppercase tracking-widest text-blue-400 bg-blue-500/10 border border-blue-500/20 rounded-full px-3 py-1">
        {feature.badge}
      </div>
    </motion.article>
  );
}

export default function Features() {
  const titleRef = useRef(null);
  const titleInView = useInView(titleRef, { once: true, margin: '-60px' });

  return (
    <section
      id="features"
      className="relative py-28 px-6 bg-[linear-gradient(180deg,transparent,rgba(8,13,34,0.8)_50%,transparent)]"
      aria-labelledby="features-heading"
    >
      <div className="max-w-6xl mx-auto">
        <motion.div
          ref={titleRef}
          initial={{ opacity: 0, y: 32 }}
          animate={titleInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.7 }}
          className="text-center mb-16"
        >
          <div className="section-tag">Capabilities</div>
          <h2 className="text-4xl sm:text-5xl font-black text-slate-100 mt-2 mb-4" id="features-heading">
            Everything You Need to{' '}
            <span className="gradient-heading">Learn Freely</span>
          </h2>
          <p className="text-slate-400 text-lg max-w-xl mx-auto">
            A full accessibility-first AI platform built for every type of learner.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((f, i) => (
            <FeatureCard key={f.title} feature={f} index={i} />
          ))}
        </div>
      </div>
    </section>
  );
}

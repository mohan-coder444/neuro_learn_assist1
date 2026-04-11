'use client';
import { useRef } from 'react';
import { Link } from 'react-router-dom';
import type { Variants } from 'framer-motion';
import {
  motion, useScroll, useTransform, useSpring,
  useMotionValue,
} from 'framer-motion';

const stats = [
  { value: '10K+', label: 'Learners Empowered' },
  { value: '98%',  label: 'AI Accuracy' },
  { value: '15+',  label: 'Languages Supported' },
  { value: '24/7', label: 'AI Availability' },
];

function OrbVisual() {
  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);
  const rotateX = useSpring(useTransform(mouseY, [-150, 150], [12, -12]), { stiffness: 120, damping: 18 });
  const rotateY = useSpring(useTransform(mouseX, [-150, 150], [-12, 12]), { stiffness: 120, damping: 18 });

  return (
    <motion.div
      className="relative mx-auto w-64 h-64 sm:w-80 sm:h-80 cursor-pointer"
      style={{ rotateX, rotateY, transformPerspective: 1000 }}
      onMouseMove={e => {
        const rect = e.currentTarget.getBoundingClientRect();
        mouseX.set(e.clientX - rect.left - rect.width / 2);
        mouseY.set(e.clientY - rect.top - rect.height / 2);
      }}
      onMouseLeave={() => { mouseX.set(0); mouseY.set(0); }}
    >
      {/* Outer rings */}
      <div className="absolute inset-[-34px] rounded-full border border-dashed border-blue-500/20 animate-spin-slow" aria-hidden="true" />
      <div className="absolute inset-[-68px] rounded-full border border-dashed border-violet-500/15 animate-spin-reverse" aria-hidden="true" />

      {/* Core sphere */}
      <motion.div
        className="absolute inset-0 rounded-full flex items-center justify-center"
        style={{
          background: 'radial-gradient(circle at 40% 35%, rgba(59,130,246,0.35) 0%, rgba(139,92,246,0.2) 50%, transparent 80%)',
          border: '1px solid rgba(139,92,246,0.3)',
        }}
        animate={{
          boxShadow: [
            '0 0 60px rgba(59,130,246,0.25)',
            '0 0 110px rgba(139,92,246,0.55)',
            '0 0 60px rgba(59,130,246,0.25)',
          ],
        }}
        transition={{ duration: 4, repeat: Infinity, ease: 'easeInOut' }}
      >
        {/* Brain icon */}
        <motion.div animate={{ y: [0, -14, 0] }} transition={{ duration: 3, repeat: Infinity, ease: 'easeInOut' }}>
          <svg width="96" height="96" viewBox="0 0 24 24" fill="none" strokeWidth="1.2" aria-label="AI brain illustration">
            <defs>
              <linearGradient id="brain-grad" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stopColor="#3b82f6" />
                <stop offset="100%" stopColor="#8b5cf6" />
              </linearGradient>
            </defs>
            <path stroke="url(#brain-grad)" d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
            <polyline stroke="url(#brain-grad)" points="3.27 6.96 12 12.01 20.73 6.96" />
            <line stroke="url(#brain-grad)" x1="12" y1="22.08" x2="12" y2="12" />
          </svg>
        </motion.div>

        {/* Orbit dots */}
        {[0, 90, 180, 270].map((deg, i) => (
          <motion.div
            key={i}
            className="absolute w-2 h-2 rounded-full bg-blue-400"
            style={{
              top: '50%', left: '50%',
              x: Math.cos((deg * Math.PI) / 180) * 90,
              y: Math.sin((deg * Math.PI) / 180) * 90,
              marginTop: -4, marginLeft: -4,
              boxShadow: '0 0 8px #3b82f6',
            }}
            animate={{ opacity: [0.4, 1, 0.4], scale: [0.8, 1.2, 0.8] }}
            transition={{ duration: 2, delay: i * 0.5, repeat: Infinity }}
          />
        ))}
      </motion.div>
    </motion.div>
  );
}

export default function Hero() {
  const ref = useRef<HTMLElement>(null);
  const { scrollYProgress } = useScroll({ target: ref, offset: ['start start', 'end start'] });
  const y = useTransform(scrollYProgress, [0, 1], ['0%', '30%']);
  const opacity = useTransform(scrollYProgress, [0, 0.7], [1, 0]);

  const containerVariants: Variants = {
    hidden: {},
    show: { transition: { staggerChildren: 0.12 } },
  };
  const itemVariants: Variants = {
    hidden: { opacity: 0, y: 32 },
    show: { opacity: 1, y: 0, transition: { duration: 0.7, ease: 'easeOut' } },
  };

  return (
    <section
      ref={ref}
      id="hero"
      className="relative min-h-screen flex items-center justify-center px-6 pt-32 pb-20 text-center overflow-hidden"
      aria-labelledby="hero-heading"
    >
      {/* Parallax bg glow */}
      <motion.div style={{ y }} className="absolute inset-0 z-0 pointer-events-none" aria-hidden="true">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_80%_60%_at_50%_0%,rgba(59,130,246,0.14)_0%,transparent_70%)]" />
      </motion.div>

      <motion.div
        style={{ opacity }}
        className="relative z-10 max-w-5xl mx-auto"
        variants={containerVariants}
        initial="hidden"
        animate="show"
      >
        {/* Live badge */}
        <motion.div variants={itemVariants} className="flex justify-center mb-7">
          <div className="flex items-center gap-2 bg-blue-500/10 border border-blue-500/25 rounded-full px-5 py-1.5 text-xs font-bold text-blue-400 uppercase tracking-widest">
            <span className="w-2 h-2 bg-blue-400 rounded-full animate-pulse" aria-hidden="true" />
            AI-Powered Accessibility Platform
          </div>
        </motion.div>

        {/* Headline */}
        <motion.h1
          id="hero-heading"
          variants={itemVariants}
          className="text-5xl sm:text-6xl lg:text-[5.5rem] font-black leading-[1.02] tracking-tight text-balance"
        >
          Learn Beyond{' '}
          <span className="gradient-heading">Limits.</span>
          <br />
          <span className="text-slate-100">Powered by AI.</span>
        </motion.h1>

        {/* Subheading */}
        <motion.p
          variants={itemVariants}
          className="mt-6 text-lg sm:text-xl text-slate-400 max-w-2xl mx-auto leading-relaxed text-balance"
        >
          NeuroLearn Assist breaks barriers for visually impaired and deaf-blind learners — with adaptive AI tutoring,
          voice interaction, braille output, and real-time document intelligence.
        </motion.p>

        {/* CTA Buttons */}
        <motion.div variants={itemVariants} className="flex flex-wrap items-center justify-center gap-3 mt-10">
          <motion.a
            href="#demo"
            className="btn-primary animate-pulse-glow text-base"
            whileHover={{ scale: 1.04 }}
            whileTap={{ scale: 0.97 }}
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <polygon points="5 3 19 12 5 21 5 3" />
            </svg>
            See It in Action
          </motion.a>
          <Link to="/dashboard">
            <motion.div
              className="inline-flex items-center gap-2 px-8 py-4 rounded-xl text-base font-bold text-white
                         bg-gradient-to-r from-violet-600 to-pink-600 cursor-pointer"
              whileHover={{ scale: 1.04, boxShadow: '0 0 30px rgba(139,92,246,0.5)' }}
              whileTap={{ scale: 0.97 }}
            >
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
                <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4" />
                <polyline points="10 17 15 12 10 7" />
                <line x1="15" y1="12" x2="3" y2="12" />
              </svg>
              Launch App
            </motion.div>
          </Link>
          <motion.a
            href="#features"
            className="btn-ghost text-base"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.97 }}
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
              <circle cx="12" cy="12" r="10" /><line x1="12" y1="8" x2="12" y2="12" /><line x1="12" y1="16" x2="12.01" y2="16" />
            </svg>
            Explore Features
          </motion.a>
        </motion.div>

        {/* Orb Illustration */}
        <motion.div variants={itemVariants} className="mt-16">
          <OrbVisual />
        </motion.div>

        {/* Stats */}
        <motion.div
          variants={containerVariants}
          className="mt-14 flex flex-wrap justify-center gap-4"
          role="list"
          aria-label="Key statistics"
        >
          {stats.map((s, i) => (
            <motion.div
              key={s.label}
              variants={itemVariants}
              custom={i}
              role="listitem"
              className="glass-strong rounded-2xl px-6 py-4 text-center min-w-[130px]"
              whileHover={{ scale: 1.04, borderColor: 'rgba(139,92,246,0.4)' }}
            >
              <div className="text-2xl font-black gradient-heading">{s.value}</div>
              <div className="text-xs text-slate-400 mt-1">{s.label}</div>
            </motion.div>
          ))}
        </motion.div>
      </motion.div>
    </section>
  );
}

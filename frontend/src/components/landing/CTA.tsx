'use client';
import { useRef } from 'react';
import { Link } from 'react-router-dom';
import { motion, useInView, useScroll, useTransform } from 'framer-motion';

const chips = [
  { icon: <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg>, label: 'Voice Accessible' },
  { icon: <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/></svg>, label: 'Braille Ready' },
  { icon: <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>, label: 'WCAG 2.1 AA' },
  { icon: <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>, label: '15+ Languages' },
];

export default function CTA() {
  const ref = useRef<HTMLElement>(null);
  const boxRef = useRef(null);
  const { scrollYProgress } = useScroll({ target: ref, offset: ['start end', 'end start'] });
  const y = useTransform(scrollYProgress, [0, 1], ['-5%', '5%']);
  const inView = useInView(boxRef, { once: true, margin: '-60px' });

  return (
    <section
      ref={ref}
      id="cta"
      className="relative py-28 px-6 overflow-hidden"
      style={{ background: 'radial-gradient(ellipse 80% 65% at 50% 50%, rgba(139,92,246,0.1) 0%, transparent 70%)' }}
      aria-labelledby="cta-heading"
    >
      {/* Parallax glow behind box */}
      <motion.div
        style={{ y }}
        className="absolute inset-0 pointer-events-none z-0"
        aria-hidden="true"
      >
        <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2
                        w-[600px] h-[600px] rounded-full blur-[140px] opacity-15
                        bg-gradient-to-br from-blue-600 to-violet-700" />
      </motion.div>

      <div className="max-w-4xl mx-auto relative z-10">
        <motion.div
          ref={boxRef}
          initial={{ opacity: 0, y: 56, scale: 0.97 }}
          animate={inView ? { opacity: 1, y: 0, scale: 1 } : {}}
          transition={{ duration: 0.85, ease: [0.22, 1, 0.36, 1] }}
          className="relative glass-strong rounded-3xl p-14 text-center overflow-hidden
                     border-violet-500/30 shadow-[0_0_100px_rgba(139,92,246,0.14)]"
        >
          {/* Conic gradient rotation */}
          <div
            className="absolute inset-0 pointer-events-none rounded-3xl overflow-hidden"
            aria-hidden="true"
          >
            <motion.div
              className="absolute inset-[-50%] opacity-40"
              style={{
                background: 'conic-gradient(from 0deg, transparent 0%, rgba(139,92,246,0.06) 25%, transparent 50%)',
              }}
              animate={{ rotate: 360 }}
              transition={{ duration: 24, repeat: Infinity, ease: 'linear' }}
            />
          </div>

          {/* Content */}
          <div className="relative z-10">
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={inView ? { opacity: 1, scale: 1 } : {}}
              transition={{ delay: 0.2 }}
            >
              <div className="section-tag mb-5">Get Started Today</div>
            </motion.div>

            <motion.h2
              id="cta-heading"
              className="text-4xl sm:text-5xl font-black text-slate-100 mb-5"
              initial={{ opacity: 0, y: 24 }}
              animate={inView ? { opacity: 1, y: 0 } : {}}
              transition={{ delay: 0.25, duration: 0.7 }}
            >
              Ready to Learn{' '}
              <span className="gradient-heading">Without Limits?</span>
            </motion.h2>

            <motion.p
              className="text-slate-400 text-lg max-w-md mx-auto mb-10"
              initial={{ opacity: 0, y: 20 }}
              animate={inView ? { opacity: 1, y: 0 } : {}}
              transition={{ delay: 0.32, duration: 0.7 }}
            >
              Join thousands of learners who have transformed their education with NeuroLearn Assist.
            </motion.p>

            <motion.div
              className="flex flex-wrap items-center justify-center gap-4 mb-10"
              initial={{ opacity: 0, y: 20 }}
              animate={inView ? { opacity: 1, y: 0 } : {}}
              transition={{ delay: 0.4, duration: 0.7 }}
            >
              <Link to="/dashboard">
                <motion.div
                  className="btn-primary text-base animate-pulse-glow"
                  whileHover={{ scale: 1.06 }}
                  whileTap={{ scale: 0.96 }}
                >
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                    <polygon points="5 3 19 12 5 21 5 3" />
                  </svg>
                  Start for Free Today
                </motion.div>
              </Link>
              <motion.a
                href="#demo"
                className="btn-ghost text-base"
                whileHover={{ scale: 1.04 }}
                whileTap={{ scale: 0.96 }}
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" /><circle cx="12" cy="12" r="3" />
                </svg>
                Watch Demo
              </motion.a>
            </motion.div>

            {/* Accessibility chips */}
            <motion.div
              className="flex flex-wrap justify-center gap-3"
              initial={{ opacity: 0 }}
              animate={inView ? { opacity: 1 } : {}}
              transition={{ delay: 0.55 }}
              role="list"
              aria-label="Accessibility certifications"
            >
              {chips.map((c, i) => (
                <motion.div
                  key={c.label}
                  role="listitem"
                  className="flex items-center gap-2 glass rounded-full px-4 py-2 text-xs font-medium text-slate-400"
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={inView ? { opacity: 1, scale: 1 } : {}}
                  transition={{ delay: 0.6 + i * 0.08 }}
                  whileHover={{ scale: 1.05, borderColor: 'rgba(139,92,246,0.4)' }}
                >
                  {c.icon}
                  {c.label}
                </motion.div>
              ))}
            </motion.div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}

'use client';
import { useRef, useState } from 'react';
import { motion, useInView, AnimatePresence } from 'framer-motion';

const messages = [
  { role: 'ai', text: 'Hello! I\'ve analyzed your document. Chapter 3 covers Neural Plasticity — what would you like to explore?' },
  { role: 'user', text: 'Explain the 3 main concepts simply' },
  { role: 'ai', text: 'Here are the 3 core concepts:\n\n1. Hebbian Learning — "neurons that fire together, wire together"\n2. Long-term Potentiation — strengthening synaptic connections through repetition\n3. Neurogenesis — creation of new neurons in adult brains' },
  { role: 'user', text: 'Quiz me on LTP' },
  { role: 'ai', text: '🎯 Medium Quiz:\n\nLTP primarily occurs in which brain structure?\n\nA) Cerebellum  B) Hippocampus ✓  C) Amygdala  D) Brainstem' },
];

const stats = [
  { label: 'Comprehension', value: 98, color: 'from-blue-500 to-violet-500' },
  { label: 'Concepts Extracted', value: 80, display: '24', color: 'from-violet-500 to-pink-500' },
  { label: 'Quiz Score', value: 87, color: 'from-cyan-500 to-blue-500' },
  { label: 'Voice Sessions', value: 60, display: '12', color: 'from-green-500 to-cyan-500' },
];

function ProgressBar({ value, color, inView }: { value: number; color: string; inView: boolean }) {
  return (
    <div className="h-1.5 bg-white/10 rounded-full mt-2 overflow-hidden">
      <motion.div
        className={`h-full rounded-full bg-gradient-to-r ${color}`}
        initial={{ width: 0 }}
        animate={inView ? { width: `${value}%` } : { width: 0 }}
        transition={{ duration: 1.4, delay: 0.3, ease: [0.22, 1, 0.36, 1] }}
      />
    </div>
  );
}

export default function Demo() {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: '-80px' });
  const titleRef = useRef(null);
  const titleInView = useInView(titleRef, { once: true, margin: '-60px' });
  const [activeMsg, setActiveMsg] = useState<number | null>(null);

  return (
    <section
      id="demo"
      className="py-28 px-6"
      aria-labelledby="demo-heading"
    >
      <div className="max-w-6xl mx-auto">
        <motion.div
          ref={titleRef}
          initial={{ opacity: 0, y: 32 }}
          animate={titleInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.7 }}
          className="text-center mb-14"
        >
          <div className="section-tag">Live Demo</div>
          <h2 className="text-4xl sm:text-5xl font-black text-slate-100 mt-2 mb-4" id="demo-heading">
            See the{' '}
            <span className="gradient-heading">AI in Action</span>
          </h2>
          <p className="text-slate-400 text-lg max-w-xl mx-auto">
            Experience real-time AI tutoring and accessibility features.
          </p>
        </motion.div>

        <motion.div
          ref={ref}
          initial={{ opacity: 0, y: 48 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
          className="glass-strong rounded-3xl overflow-hidden"
        >
          {/* Window bar */}
          <div className="flex items-center gap-2 px-5 py-3.5 border-b border-white/[0.06] bg-white/[0.02]" aria-hidden="true">
            <div className="w-3 h-3 rounded-full bg-[#ff5f57]" />
            <div className="w-3 h-3 rounded-full bg-[#ffbd2e]" />
            <div className="w-3 h-3 rounded-full bg-[#28c940]" />
            <span className="ml-3 text-xs text-slate-500 font-medium">NeuroLearn Assist — AI Tutor Session</span>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-0">
            {/* Chat Panel */}
            <div className="p-7 border-r border-white/[0.05]">
              <div className="flex items-center gap-2 mb-5">
                <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
                <span className="text-xs font-medium text-slate-400">AI Tutor Active</span>
              </div>
              <div className="space-y-3" role="log" aria-label="AI conversation">
                {messages.map((msg, i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, y: 16, scale: 0.97 }}
                    animate={inView ? { opacity: 1, y: 0, scale: 1 } : {}}
                    transition={{ delay: 0.3 + i * 0.18, duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
                    className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <motion.div
                      className={`max-w-[85%] px-4 py-3 rounded-2xl text-sm leading-relaxed cursor-pointer select-none
                        ${msg.role === 'ai'
                          ? 'bg-blue-500/10 border border-blue-500/20 text-slate-200 rounded-tl-sm'
                          : 'bg-gradient-to-br from-blue-600 to-violet-700 text-white rounded-tr-sm'
                        }`}
                      whileHover={{ scale: 1.02 }}
                      onClick={() => setActiveMsg(activeMsg === i ? null : i)}
                      style={{ whiteSpace: 'pre-line' }}
                      role="article"
                    >
                      {msg.text}
                      <AnimatePresence>
                        {msg.role === 'ai' && activeMsg === i && (
                          <motion.div
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: 'auto' }}
                            exit={{ opacity: 0, height: 0 }}
                            className="mt-2 pt-2 border-t border-blue-500/20 text-xs text-slate-400"
                          >
                            Click to hear via voice tutor ›
                          </motion.div>
                        )}
                      </AnimatePresence>
                    </motion.div>
                  </motion.div>
                ))}
              </div>
            </div>

            {/* Stats Panel */}
            <div className="p-7 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-1 gap-5 content-start" role="list" aria-label="Session statistics">
              {stats.map((s, i) => (
                <motion.div
                  key={s.label}
                  role="listitem"
                  className="bg-white/[0.03] border border-white/[0.06] rounded-2xl p-5"
                  initial={{ opacity: 0, x: 30 }}
                  animate={inView ? { opacity: 1, x: 0 } : {}}
                  transition={{ delay: 0.4 + i * 0.12, duration: 0.6 }}
                  whileHover={{ backgroundColor: 'rgba(255,255,255,0.05)' }}
                >
                  <div className="text-[0.7rem] font-semibold text-slate-500 uppercase tracking-widest mb-1">{s.label}</div>
                  <div className="text-3xl font-black gradient-heading leading-none">
                    {s.display ?? `${s.value}%`}
                  </div>
                  <ProgressBar value={s.value} color={s.color} inView={inView} />
                </motion.div>
              ))}
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}

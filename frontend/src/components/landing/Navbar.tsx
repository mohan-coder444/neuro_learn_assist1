'use client';
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion, useScroll, useTransform, AnimatePresence } from 'framer-motion';

const navLinks = [
  { label: 'Features', href: '#features' },
  { label: 'How It Works', href: '#how' },
  { label: 'Demo', href: '#demo' },
  { label: 'Pricing', href: '#pricing' },
];

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const { scrollY } = useScroll();
  const bgOpacity = useTransform(scrollY, [0, 80], [0.6, 0.97]);

  useEffect(() => {
    const unsub = scrollY.on('change', v => setScrolled(v > 50));
    return unsub;
  }, [scrollY]);

  const scrollTo = (href: string) => {
    setMobileOpen(false);
    const el = document.querySelector(href);
    el?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  return (
    <motion.header
      aria-label="Main navigation"
      className="fixed top-3 left-1/2 z-50 w-[calc(100%-40px)] max-w-[1200px] -translate-x-1/2"
      initial={{ y: -80, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
    >
      <motion.nav
        className="rounded-2xl px-6 py-3.5 flex items-center justify-between
                   border border-white/[0.07] backdrop-blur-2xl"
        style={{
          backgroundColor: scrolled
            ? 'rgba(5,8,22,0.97)'
            : 'rgba(5,8,22,0.60)',
          borderColor: scrolled ? 'rgba(255,255,255,0.1)' : 'rgba(255,255,255,0.06)',
        }}
      >
        {/* Logo */}
        <Link to="/" className="flex items-center gap-2.5 group" aria-label="NeuroLearn Assist home">
          <motion.div
            className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-violet-600 flex items-center justify-center"
            whileHover={{ scale: 1.1, rotate: 5 }}
            transition={{ type: 'spring', stiffness: 300, damping: 18 }}
            style={{ boxShadow: '0 0 20px rgba(59,130,246,0.4)' }}
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" aria-hidden="true">
              <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
            </svg>
          </motion.div>
          <span className="font-black text-base bg-gradient-to-r from-blue-400 to-violet-400 bg-clip-text text-transparent">
            NeuroLearn Assist
          </span>
        </Link>

        {/* Desktop Nav Links */}
        <ul className="hidden md:flex items-center gap-7" role="list">
          {navLinks.map(link => (
            <li key={link.href}>
              <button
                onClick={() => scrollTo(link.href)}
                className="text-slate-400 hover:text-slate-100 text-sm font-medium transition-colors duration-200 cursor-pointer rounded px-1"
              >
                {link.label}
              </button>
            </li>
          ))}
        </ul>

        {/* Right side CTAs */}
        <div className="flex items-center gap-2.5">
          {/* Launch App */}
          <Link to="/dashboard">
            <motion.div
              className="hidden sm:flex items-center gap-1.5 px-4 py-2 rounded-xl text-sm font-semibold
                         text-slate-300 border border-white/[0.08] hover:border-violet-500/40
                         hover:text-white hover:bg-white/5 transition-all duration-200 cursor-pointer"
              whileHover={{ scale: 1.03 }}
              whileTap={{ scale: 0.97 }}
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
                <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4" />
                <polyline points="10 17 15 12 10 7" />
                <line x1="15" y1="12" x2="3" y2="12" />
              </svg>
              Launch App
            </motion.div>
          </Link>

          {/* Get Started */}
          <motion.button
            onClick={() => scrollTo('#cta')}
            className="hidden sm:flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-bold text-white
                       bg-gradient-to-r from-blue-500 to-violet-600 cursor-pointer animate-pulse-glow"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.97 }}
          >
            Get Started Free
          </motion.button>

          {/* Mobile menu toggle */}
          <button
            className="md:hidden p-2 text-slate-300 hover:text-white transition-colors rounded-lg hover:bg-white/5"
            onClick={() => setMobileOpen(v => !v)}
            aria-label="Toggle navigation menu"
            aria-expanded={mobileOpen}
          >
            <AnimatePresence mode="wait">
              {mobileOpen ? (
                <motion.svg key="x" width="21" height="21" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"
                  initial={{ rotate: -90, opacity: 0 }} animate={{ rotate: 0, opacity: 1 }} exit={{ rotate: 90, opacity: 0 }}>
                  <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
                </motion.svg>
              ) : (
                <motion.svg key="menu" width="21" height="21" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"
                  initial={{ rotate: 90, opacity: 0 }} animate={{ rotate: 0, opacity: 1 }} exit={{ rotate: -90, opacity: 0 }}>
                  <line x1="3" y1="6" x2="21" y2="6" /><line x1="3" y1="12" x2="21" y2="12" /><line x1="3" y1="18" x2="21" y2="18" />
                </motion.svg>
              )}
            </AnimatePresence>
          </button>
        </div>
      </motion.nav>

      {/* Mobile Drawer */}
      <AnimatePresence>
        {mobileOpen && (
          <motion.div
            className="md:hidden mt-2 rounded-2xl overflow-hidden border border-white/[0.07] backdrop-blur-2xl bg-[rgba(5,8,22,0.97)]"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3, ease: [0.22, 1, 0.36, 1] }}
          >
            <ul className="flex flex-col p-4 gap-1">
              {navLinks.map((link, i) => (
                <motion.li key={link.href}
                  initial={{ opacity: 0, x: -16 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.06 }}
                >
                  <button
                    onClick={() => scrollTo(link.href)}
                    className="w-full text-left px-4 py-3 rounded-xl text-slate-300 hover:text-white hover:bg-white/5 transition-all cursor-pointer text-sm font-medium"
                  >
                    {link.label}
                  </button>
                </motion.li>
              ))}
              <motion.li initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.25 }}
                className="flex flex-col gap-2 pt-2">
                <Link to="/dashboard" onClick={() => setMobileOpen(false)}
                  className="w-full text-center px-4 py-2.5 rounded-xl text-sm font-semibold text-slate-300 border border-white/10 hover:border-violet-500/40 hover:bg-white/5 transition-all">
                  Launch App
                </Link>
                <button onClick={() => scrollTo('#cta')}
                  className="w-full text-center px-4 py-3 rounded-xl text-sm font-bold text-white bg-gradient-to-r from-blue-500 to-violet-600 animate-pulse-glow">
                  Get Started Free
                </button>
              </motion.li>
            </ul>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.header>
  );
}

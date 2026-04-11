'use client';
import { useRef, useState } from 'react';
import { motion, useInView, AnimatePresence } from 'framer-motion';

const plans = [
  {
    name: 'Free',
    monthlyPrice: '$0',
    annualPrice: '$0',
    period: 'Forever free · No card needed',
    features: ['3 PDF uploads/month', 'Basic Voice AI', 'Flashcards & Quizzes', 'Community support'],
    cta: 'Get Started Free',
    variant: 'ghost',
    popular: false,
  },
  {
    name: 'Pro',
    monthlyPrice: '$19',
    annualPrice: '$13',
    period: 'per month',
    annualNote: 'per month, billed annually',
    features: [
      'Unlimited PDF uploads',
      'Advanced Voice AI Tutor',
      'Adaptive Quizzes',
      'Braille Output Support',
      'Multi-Agent Sessions',
      'Priority 24/7 support',
    ],
    cta: 'Start Pro Trial',
    variant: 'primary',
    popular: true,
  },
  {
    name: 'Enterprise',
    monthlyPrice: 'Custom',
    annualPrice: 'Custom',
    period: 'Contact us',
    features: [
      'Everything in Pro',
      'Custom AI model training',
      'Hardware integration help',
      'SSO & Admin Dashboard',
      'Dedicated CSM + SLA',
    ],
    cta: 'Contact Sales',
    variant: 'ghost',
    popular: false,
  },
];

function CheckIcon() {
  return (
    <span className="w-5 h-5 rounded-full bg-blue-500/15 flex items-center justify-center flex-shrink-0" aria-hidden="true">
      <svg width="10" height="10" viewBox="0 0 12 12" fill="none" stroke="#3b82f6" strokeWidth="2">
        <polyline points="2 6 5 9 10 3" />
      </svg>
    </span>
  );
}

export default function Pricing() {
  const [annual, setAnnual] = useState(false);
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: '-60px' });
  const titleRef = useRef(null);
  const titleInView = useInView(titleRef, { once: true, margin: '-60px' });

  return (
    <section
      id="pricing"
      className="py-28 px-6"
      style={{ background: 'radial-gradient(ellipse 70% 50% at 50% 50%, rgba(59,130,246,0.06) 0%, transparent 70%)' }}
      aria-labelledby="pricing-heading"
    >
      <div className="max-w-6xl mx-auto">
        <motion.div
          ref={titleRef}
          initial={{ opacity: 0, y: 32 }}
          animate={titleInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.7 }}
          className="text-center mb-10"
        >
          <div className="section-tag">Pricing</div>
          <h2 className="text-4xl sm:text-5xl font-black text-slate-100 mt-2 mb-4" id="pricing-heading">
            Simple,{' '}
            <span className="gradient-heading">Transparent</span> Pricing
          </h2>
          <p className="text-slate-400 text-lg max-w-xl mx-auto">
            Start free. Upgrade anytime. No surprises.
          </p>
        </motion.div>

        {/* Toggle */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={titleInView ? { opacity: 1 } : {}}
          transition={{ delay: 0.3 }}
          className="flex items-center justify-center gap-4 mb-12"
          role="group"
          aria-label="Billing period"
        >
          <span className={`text-sm font-medium transition-colors ${!annual ? 'text-slate-100' : 'text-slate-500'}`}>Monthly</span>
          <motion.button
            role="switch"
            aria-checked={annual}
            onClick={() => setAnnual(v => !v)}
            className={`relative w-14 h-7 rounded-full border transition-colors duration-300 cursor-pointer focus-visible:outline-2 focus-visible:outline-blue-500
              ${annual ? 'bg-gradient-to-r from-blue-500 to-violet-600 border-violet-500/50' : 'bg-white/10 border-white/15'}`}
          >
            <motion.div
              className="absolute top-0.5 left-0.5 w-6 h-6 bg-white rounded-full shadow-lg"
              animate={{ x: annual ? 28 : 0 }}
              transition={{ type: 'spring', stiffness: 300, damping: 22 }}
            />
          </motion.button>
          <span className={`text-sm font-medium flex items-center gap-2 transition-colors ${annual ? 'text-slate-100' : 'text-slate-500'}`}>
            Annual
            <span className="text-[0.65rem] font-bold uppercase bg-green-500/15 text-green-400 border border-green-500/25 rounded-full px-2 py-0.5">
              Save 30%
            </span>
          </span>
        </motion.div>

        {/* Cards */}
        <div ref={ref} className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {plans.map((plan, i) => (
            <motion.div
              key={plan.name}
              initial={{ opacity: 0, y: 48 }}
              animate={inView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.65, delay: i * 0.1, ease: [0.22, 1, 0.36, 1] }}
              className={`relative rounded-3xl p-9 flex flex-col transition-all duration-300 hover:-translate-y-1.5 cursor-default
                ${plan.popular
                  ? 'border border-violet-500/50 shadow-[0_0_50px_rgba(139,92,246,0.18)] bg-gradient-to-b from-[rgba(14,20,45,0.92)] to-[rgba(20,14,48,0.92)]'
                  : 'glass-strong hover:border-white/15 hover:shadow-[0_20px_60px_rgba(0,0,0,0.4)]'
                }`}
            >
              {plan.popular && (
                <div className="absolute -top-3 right-6 bg-gradient-to-r from-blue-500 to-violet-600 text-white text-[0.65rem] font-black uppercase tracking-widest px-3 py-1 rounded-full">
                  Most Popular
                </div>
              )}

              <div className="text-xs font-bold uppercase tracking-widest text-slate-500 mb-3">{plan.name}</div>

              <AnimatePresence mode="wait">
                <motion.div
                  key={annual ? 'annual' : 'monthly'}
                  initial={{ opacity: 0, y: -12 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 12 }}
                  transition={{ duration: 0.25 }}
                >
                  <div className="text-5xl font-black gradient-heading leading-none mb-1">
                    {annual ? plan.annualPrice : plan.monthlyPrice}
                  </div>
                  <div className="text-sm text-slate-500 mb-7">
                    {annual && plan.annualNote ? plan.annualNote : plan.period}
                  </div>
                </motion.div>
              </AnimatePresence>

              <ul className="space-y-3 mb-8 flex-1" aria-label={`${plan.name} plan features`}>
                {plan.features.map(f => (
                  <li key={f} className="flex items-center gap-3 text-sm text-slate-400">
                    <CheckIcon />
                    {f}
                  </li>
                ))}
              </ul>

              <motion.button
                className={plan.variant === 'primary' ? 'btn-primary justify-center w-full' : 'btn-ghost justify-center w-full'}
                whileHover={{ scale: 1.03 }}
                whileTap={{ scale: 0.97 }}
              >
                {plan.cta}
              </motion.button>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}

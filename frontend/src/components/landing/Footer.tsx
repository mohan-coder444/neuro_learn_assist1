import { motion } from 'framer-motion';

const links = ['Product', 'Features', 'Pricing', 'Accessibility', 'Privacy', 'Terms'];

export default function Footer() {
  return (
    <footer className="bg-[#080d22] border-t border-white/[0.06] py-14 px-6 text-center">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.7 }}
      >
        <div className="text-xl font-black gradient-heading mb-3">NeuroLearn Assist</div>
        <p className="text-slate-500 text-sm mb-6">AI-powered learning for every ability, everywhere.</p>

        <nav className="flex flex-wrap justify-center gap-x-7 gap-y-2 mb-8" aria-label="Footer navigation">
          {links.map((l, i) => (
            <motion.a
              key={l}
              href="#"
              className="text-slate-500 hover:text-slate-200 text-sm transition-colors duration-200"
              initial={{ opacity: 0, y: 10 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.06 }}
            >
              {l}
            </motion.a>
          ))}
        </nav>

        <div className="pt-6 border-t border-white/[0.05] text-slate-600 text-xs">
          © 2025 NeuroLearn Assist. Built with care for accessibility.
        </div>
      </motion.div>
    </footer>
  );
}

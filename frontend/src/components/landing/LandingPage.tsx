import ParticleField from '../ParticleField';
import Navbar from './Navbar';
import Hero from './Hero';
import Features from './Features';
import HowItWorks from './HowItWorks';
import Demo from './Demo';
import Testimonials from './Testimonials';
import Pricing from './Pricing';
import CTA from './CTA';
import Footer from './Footer';
import ScrollToTop from './ScrollToTop';

export default function LandingPage() {
  return (
    <div className="dark relative">
      {/* Global ambient orbs */}
      <div
        className="fixed top-[-200px] left-[-200px] w-[600px] h-[600px] rounded-full opacity-10 pointer-events-none z-0 animate-pulse-slow"
        style={{ background: 'radial-gradient(circle, #3b82f6, transparent)', filter: 'blur(130px)' }}
        aria-hidden="true"
      />
      <div
        className="fixed bottom-[-100px] right-[-100px] w-[500px] h-[500px] rounded-full opacity-10 pointer-events-none z-0 animate-pulse-slow"
        style={{ background: 'radial-gradient(circle, #8b5cf6, transparent)', filter: 'blur(130px)', animationDelay: '4s' }}
        aria-hidden="true"
      />

      <ParticleField />

      <div className="relative z-10">
        <Navbar />
        <main>
          <Hero />
          <Features />
          <HowItWorks />
          <Demo />
          <Testimonials />
          <Pricing />
          <CTA />
        </main>
        <Footer />
        <ScrollToTop />
      </div>
    </div>
  );
}

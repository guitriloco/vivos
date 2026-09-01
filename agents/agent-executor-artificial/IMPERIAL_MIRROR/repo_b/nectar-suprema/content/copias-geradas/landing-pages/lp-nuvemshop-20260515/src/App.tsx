import React from 'react';
import { Hero } from './components/Hero';
import { Problem } from './components/Problem';
import { Solution } from './components/Solution';
import { SocialProof } from './components/SocialProof';
import { Pricing } from './components/Pricing';
import { FAQ } from './components/FAQ';
import { Footer } from './components/Footer';

function App() {
  return (
    <div className="min-h-screen bg-white font-sans text-gray-900">
      {/* Top Banner / Countdown */}
      <div className="bg-red-600 text-white py-2 px-4 text-center text-sm font-bold animate-pulse">
        🔴 OFERTA TERMINA EM: 14:23:11 - Acesso promocional disponível por tempo limitado. Depois, preço cheio de R$ 297.
      </div>

      <Hero />
      <Problem />
      <Solution />
      <SocialProof />
      <Pricing />
      <FAQ />
      <Footer />
    </div>
  );
}

export default App;

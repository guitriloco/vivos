import React from 'react';
import { ShieldCheck, CheckCircle } from 'lucide-react';

export const Pricing = () => {
  const checkoutUrl = "#"; // Placeholder for Kiwify/Hotmart link

  return (
    <section className="py-20 px-4 bg-blue-900 text-white">
      <div className="max-w-4xl mx-auto text-center">
        <h2 className="text-4xl md:text-5xl font-black mb-6 uppercase italic">OFERTA IRRECUSÁVEL</h2>
        <div className="bg-white text-gray-900 p-8 md:p-12 rounded-3xl shadow-2xl relative overflow-hidden">
          <div className="absolute top-0 right-0 bg-red-600 text-white py-2 px-10 transform rotate-45 translate-x-10 translate-y-2 font-bold text-sm">
            67% OFF
          </div>
          <p className="text-xl text-gray-500 line-through mb-2">De: R$ 297,00</p>
          <p className="text-2xl font-bold text-gray-700">Por apenas:</p>
          <div className="text-6xl md:text-8xl font-black text-blue-600 my-4">
            R$ 97,00
          </div>
          <p className="text-xl font-medium mb-10 text-gray-600 italic">ou 12x de R$ 9,70 no cartão</p>
          
          <a 
            href={checkoutUrl}
            className="block w-full bg-green-600 hover:bg-green-700 text-white text-2xl md:text-3xl font-black py-6 px-8 rounded-2xl shadow-xl transform transition hover:scale-105 mb-6 text-center"
          >
            QUERO MEU ACESSO AGORA!
          </a>
          
          <div className="flex flex-col md:flex-row items-center justify-center gap-6 text-sm font-bold text-gray-500">
            <span className="flex items-center gap-2"><ShieldCheck className="text-green-600" /> COMPRA 100% SEGURA</span>
            <span className="flex items-center gap-2"><CheckCircle className="text-green-600" /> ACESSO IMEDIATO</span>
            <span className="flex items-center gap-2"><CheckCircle className="text-green-600" /> 7 DIAS DE GARANTIA</span>
          </div>
        </div>
        
        <div className="mt-16 text-left">
          <h3 className="text-2xl font-bold mb-8 text-center">🎁 BÔNUS EXCLUSIVOS (Para as primeiras 100 vagas)</h3>
          <div className="grid md:grid-cols-2 gap-4">
            {[
              "+200 fornecedores extras (atualizado Janeiro 2025)",
              "Checklist de produtos winners",
              "Acesso ao grupo VIP do WhatsApp",
              "Atualizações vitalícias inclusas"
            ].map((bonus, i) => (
              <div key={i} className="flex items-center gap-3 bg-blue-800 p-4 rounded-xl">
                <CheckCircle className="text-green-400 shrink-0" />
                <span className="font-medium text-lg">{bonus}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

import React from 'react';
import { MessageCircle } from 'lucide-react';

export const FAQ = () => (
  <section className="py-20 px-4 bg-white">
    <div className="max-w-3xl mx-auto">
      <h2 className="text-3xl md:text-4xl font-bold text-center mb-12 italic underline decoration-blue-600">Perguntas Frequentes</h2>
      <div className="space-y-8 text-left">
        {[
          { q: "Funciona mesmo pra quem nunca vendeu nada online?", a: "Sim! O método foi desenhado para iniciantes. Você recebe tudo pronto: lista de fornecedores, copy, método. Só aplicar." },
          { q: "Preciso ter estoque ou investir em produtos?", a: "Não! Esse é o princípio do dropshipping. Você vende e o fornecedor envia. Zero estoque." },
          { q: "Como recebo o material?", a: "Imediatamente após a compra via Kiwify ou Hotmart. Você recebe login e senha." },
          { q: "Posso vender de qualquer lugar do Brasil?", a: "Sim! Os fornecedores dessa lista entregam em todo o Brasil." },
          { q: "E se eu não me adaptar?", a: "Você tem 7 dias de garantia. Experimenta sem risco nenhum." }
        ].map((faq, i) => (
          <div key={i}>
            <h4 className="text-xl font-bold text-gray-900 mb-2 flex items-center gap-2">
               <MessageCircle className="text-blue-600" size={20} /> {faq.q}
            </h4>
            <p className="text-gray-600 text-lg leading-relaxed">{faq.a}</p>
          </div>
        ))}
      </div>
    </div>
  </section>
);

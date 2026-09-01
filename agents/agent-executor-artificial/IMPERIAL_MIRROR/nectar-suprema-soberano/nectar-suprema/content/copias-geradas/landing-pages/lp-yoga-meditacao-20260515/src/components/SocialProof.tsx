import React from 'react';
import { Star } from 'lucide-react';

export const SocialProof = () => (
  <section className="py-20 px-4 bg-white">
    <div className="max-w-5xl mx-auto">
      <h2 className="text-3xl md:text-4xl font-bold text-center mb-16">O que nossos alunos estão dizendo</h2>
      <div className="grid md:grid-cols-3 gap-8">
        {[
          { text: "Vendi R$ 2.300 na primeira semana. O material se pagou no primeiro dia.", author: "Mariana C., Rio de Janeiro" },
          { text: "Finally um material que funciona no Brasil. Fornecedores reais.", author: "Pedro H., Belo Horizonte" },
          { text: "Economizei 3 meses de tentativas e erros. Recomendo demais.", author: "Juliana M., Curitiba" }
        ].map((item, i) => (
          <div key={i} className="bg-gray-50 p-8 rounded-2xl border border-gray-100 relative">
            <div className="flex text-yellow-400 mb-4">
              {[...Array(5)].map((_, j) => <Star key={j} size={20} fill="currentColor" />)}
            </div>
            <p className="text-lg text-gray-700 mb-6 italic">"{item.text}"</p>
            <p className="font-bold text-gray-900">— {item.author}</p>
          </div>
        ))}
      </div>
    </div>
  </section>
);

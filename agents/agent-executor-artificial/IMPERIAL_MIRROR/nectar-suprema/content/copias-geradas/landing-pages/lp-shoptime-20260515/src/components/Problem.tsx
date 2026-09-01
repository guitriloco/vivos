import React from 'react';
import { AlertCircle } from 'lucide-react';

export const Problem = () => (
  <section className="py-20 px-4 bg-white">
    <div className="max-w-4xl mx-auto">
      <h2 className="text-3xl md:text-4xl font-bold text-center mb-12">Você se identifica?</h2>
      <div className="grid md:grid-cols-2 gap-6">
        {[
          "Comprei uma lista de fornecedores na internet mas nenhum respondia",
          "Fiz anúncios no Instagram e Facebook mas ninguém comprava",
          "Tentei vender mas meus leads não convertiam",
          "Desconfiei de tudo porque parecia bom demais"
        ].map((item, i) => (
          <div key={i} className="flex items-start gap-4 p-6 bg-red-50 rounded-xl border border-red-100">
            <AlertCircle className="text-red-500 shrink-0" size={24} />
            <p className="text-lg text-gray-700 font-medium italic">"{item}"</p>
          </div>
        ))}
      </div>
      <p className="text-center mt-12 text-xl font-bold text-gray-800">
        Se você marcou mesmo que 1 dessas opções, esse material é pra você.
      </p>
    </div>
  </section>
);

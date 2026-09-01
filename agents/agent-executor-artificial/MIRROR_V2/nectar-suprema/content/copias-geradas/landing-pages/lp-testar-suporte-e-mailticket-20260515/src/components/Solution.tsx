import React from 'react';
import { CheckCircle } from 'lucide-react';

export const Solution = () => (
  <section className="py-20 px-4 bg-gray-50">
    <div className="max-w-4xl mx-auto">
      <div className="bg-white p-8 md:p-12 rounded-3xl shadow-xl border border-gray-100">
        <h2 className="text-3xl md:text-4xl font-bold text-center mb-8 text-gray-900">
          E se existisse uma forma simples de começar?
        </h2>
        <p className="text-xl text-center mb-10 text-gray-600">Imagine receber tudo pronto:</p>
        <ul className="space-y-6">
          {[
            "Uma lista com +500 fornecedores que já respondem",
            "Uma seleção de produtos que mais vendem em 2025",
            "Scripts de vendas testados que você só copia e cola",
            "Método passo a passo, do zero absoluto ao primeiro REAL$ em vendas"
          ].map((item, i) => (
            <li key={i} className="flex items-center gap-4 text-lg md:text-xl font-medium text-gray-700">
              <CheckCircle className="text-green-500" />
              {item}
            </li>
          ))}
        </ul>
        <p className="text-center mt-12 text-2xl font-black text-blue-600 uppercase tracking-tight">
          Isso não é promessa. É resultado de quem já aplicou.
        </p>
      </div>
    </div>
  </section>
);

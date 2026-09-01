import React from 'react';

export const Footer = () => (
  <footer className="bg-gray-100 py-12 px-4 border-t border-gray-200">
    <div className="max-w-5xl mx-auto text-center text-gray-500 text-sm">
      <p className="mb-4 font-bold">Lista Quente © 2025 - Todos os direitos reservados</p>
      <p className="max-w-2xl mx-auto italic">
        Resultados podem variar. O método funciona, mas exige ação. Não prometemos enriquecimento instantâneo.
      </p>
      <div className="mt-8 flex justify-center gap-6 underline font-medium">
        <a href="#">Termos de Uso</a>
        <a href="#">Privacidade</a>
        <a href="#">Contato</a>
      </div>
    </div>
  </footer>
);

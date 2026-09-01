import json
import os
import sys

def generate_static_html(niche_name, output_path):
    niches_file = os.path.join(os.path.dirname(__file__), 'niches.json')
    with open(niches_file, 'r') as f:
        niches = json.load(f)
    
    if niche_name not in niches:
        print(f"Niche {niche_name} not found.")
        return False
    
    data = niches[niche_name]
    
    html_content = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data['title']}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .gradient-bg {{
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        }}
    </style>
</head>
<body class="bg-gray-50 text-gray-900 font-sans">
    <header class="gradient-bg text-white py-20 px-4 text-center">
        <div class="max-w-4xl mx-auto">
            <h1 class="text-4xl md:text-6xl font-bold mb-6">{data['headline']}</h1>
            <p class="text-xl md:text-2xl opacity-90 mb-10">{data['subheadline']}</p>
            <a href="#pricing" class="bg-yellow-400 hover:bg-yellow-500 text-blue-900 font-bold py-4 px-8 rounded-full text-xl transition-all transform hover:scale-105 inline-block shadow-lg">
                QUERO ACESSO IMEDIATO
            </a>
        </div>
    </header>

    <main class="max-w-6xl mx-auto py-20 px-4">
        <section id="benefits" class="grid md:grid-cols-2 gap-12 items-center mb-20">
            <div>
                <h2 class="text-3xl font-bold mb-6">Por que este nicho?</h2>
                <p class="text-lg text-gray-600 mb-6">
                    O mercado de {niche_name.replace('-', ' ')} está explodindo em 2025. Com nossa lista de fornecedores, você pula meses de testes e vai direto para o que funciona.
                </p>
                <ul class="space-y-4">
                    {"".join([f"<li class='flex items-center text-lg'><span class='text-green-500 mr-2'>✓</span> {bonus}</li>" for bonus in data['bonuses']])}
                </ul>
            </div>
            <div class="bg-blue-100 rounded-2xl p-8 aspect-video flex items-center justify-center border-2 border-blue-200">
                <span class="text-blue-500 font-bold text-xl uppercase tracking-widest">Vídeo de Vendas (VSL)</span>
            </div>
        </section>

        <section id="pricing" class="text-center bg-white rounded-3xl p-12 shadow-2xl border border-gray-100 max-w-2xl mx-auto">
            <h2 class="text-3xl font-bold mb-4">Oferta Especial de Lançamento</h2>
            <p class="text-gray-500 line-through text-xl">De R$ 297,00</p>
            <div class="text-6xl font-bold text-blue-600 my-6">R$ {data['pricing']}</div>
            <p class="text-gray-600 mb-8">Ou em até 12x no cartão de crédito</p>
            <a href="#" class="block bg-green-500 hover:bg-green-600 text-white font-bold py-5 px-10 rounded-2xl text-2xl transition-all shadow-xl">
                COMPRAR AGORA
            </a>
            <p class="mt-6 text-sm text-gray-400 flex items-center justify-center">
                <span class="mr-2">🔒</span> Pagamento 100% Seguro • Acesso Imediato
            </p>
        </section>
    </main>

    <footer class="bg-gray-900 text-white py-12 px-4 text-center">
        <p class="opacity-50">&copy; 2025 Nectar Suprema. Todos os direitos reservados.</p>
    </footer>
</body>
</html>
"""
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(html_content)
    
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 html-gen.py <niche> <output_path>")
    else:
        generate_static_html(sys.argv[1], sys.argv[2])

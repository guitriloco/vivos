import os
import re
import json
import shutil
import sys

def parse_md_lp(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract data using regex
    title_match = re.search(r'# Landing Page - (.*)', content)
    headline_match = re.search(r'\*\*Headline:\*\*\s+# (.*)', content)
    if not headline_match:
        headline_match = re.search(r'# (.*)', content.split('## HERO SECTION')[1] if '## HERO SECTION' in content else "")
        
    subheadline_match = re.search(r'\*\*Subtítulo:\*\*\s+(.*)', content)
    pricing_match = re.search(r'\*\*HOJE: R\$ (.*)\*\*', content)
    
    bonuses = re.findall(r'✅ (.*)', content)
    
    niche_id = os.path.basename(filepath).replace('landing-', '').replace('.md', '')
    
    return {
        "id": niche_id,
        "title": title_match.group(1).strip() if title_match else "Nectar LP",
        "headline": headline_match.group(1).strip() if headline_match else "Oferta Exclusiva",
        "subheadline": subheadline_match.group(1).strip() if subheadline_match else "Confira os detalhes abaixo",
        "pricing": pricing_match.group(1).strip() if pricing_match else "97,00",
        "bonuses": bonuses[:4] if bonuses else ["Acesso Vitalício", "Suporte VIP"]
    }

def generate_html(data):
    html_template = f"""
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
                    Este mercado está explodindo em 2025. Com nossa estratégia, você pula meses de testes e vai direto para o que funciona.
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
            <h2 class="text-3xl font-bold mb-4">Oferta Especial</h2>
            <p class="text-gray-500 line-through text-xl">De R$ 297,00</p>
            <div class="text-6xl font-bold text-blue-600 my-6">R$ {data['pricing']}</div>
            <p class="text-gray-600 mb-8">Ou em até 12x no cartão de crédito</p>
            <a href="#" class="block bg-green-500 hover:bg-green-600 text-white font-bold py-5 px-10 rounded-2xl text-2xl transition-all shadow-xl">
                COMPRAR AGORA
            </a>
        </section>
    </main>

    <footer class="bg-gray-900 text-white py-12 px-4 text-center">
        <p class="opacity-50">&copy; 2025 Nectar Suprema. Todos os direitos reservados.</p>
    </footer>
</body>
</html>
"""
    return html_template

def main():
    # Use shared path if available, otherwise fallback to home
    shared_path = "/home/team/shared/nectar-suprema"
    if os.path.exists(shared_path):
        repo_root = shared_path
    else:
        home = os.environ['HOME']
        repo_root = os.path.join(home, "nectar-suprema")
        
    content_dir = os.path.join(repo_root, "content/copias-geradas/landing-pages")
    docs_dir = os.path.join(repo_root, "docs/lps")
    dashboard_path = os.path.join(repo_root, "docs/index.html")
    
    if not os.path.exists(content_dir):
        print(f"Content dir {content_dir} not found.")
        return

    os.makedirs(docs_dir, exist_ok=True)
    
    with open(dashboard_path, 'r') as f:
        dashboard_content = f.read()

    for filename in os.listdir(content_dir):
        if filename.endswith(".md"):
            filepath = os.path.join(content_dir, filename)
            print(f"Processing {filename}...")
            
            data = parse_md_lp(filepath)
            html = generate_html(data)
            
            niche_path = os.path.join(docs_dir, data['id'])
            os.makedirs(niche_path, exist_ok=True)
            
            with open(os.path.join(niche_path, "index.html"), 'w') as f:
                f.write(html)
            
            # Update dashboard if not present
            link_path = f"lps/{data['id']}/index.html"
            if link_path not in dashboard_content:
                print(f"Adding {data['id']} to dashboard...")
                link_html = f'\n                    <a href="{link_path}" class="lp-item">🚀 LP: {data["title"]}</a>'
                dashboard_content = re.sub(r'(<div id="lp-list"[^>]*>)', r'\1' + link_html, dashboard_content)

    with open(dashboard_path, 'w') as f:
        f.write(dashboard_content)
    
    print("Sync complete.")

if __name__ == "__main__":
    main()

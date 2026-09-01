import os
from pathlib import Path

def analisar_arquivos_apenas_listar(pasta_origem):
    """
    Analisa arquivos em uma pasta e os organiza em categorias sem mover ou deletar.
    Apenas lista como ficariam organizados.
    """
    pasta_origem = Path(pasta_origem)

    if not pasta_origem.exists():
        print(f"A pasta {pasta_origem} não existe.")
        return

    # Dicionário para categorizar os arquivos
    categorias = {
        'APIs_Google': [],
        'Utilidades': [],
        'Web_Scraping': [],
        'Configuracoes_JSON': [],
        'Scripts_Auto': [],
        'Manipulacao_Dados': [],
        'Interface_Web': [],
        'Processamento_Texto': [],
        'Outros': []
    }

    # Tipos de arquivos que vamos processar
    extensoes_para_analisar = ['.py', '.json', '.js', '.jsx', '.ts', '.tsx', '.html', '.css', '.xml']

    print("Analisando arquivos e categorizando...")

    for arquivo in pasta_origem.rglob('*'):
        if arquivo.is_file() and arquivo.suffix.lower() in extensoes_para_analisar:
            nome_arquivo = arquivo.name.lower()

            # Categorizar arquivos com base no nome
            if any(api in nome_arquivo for api in ['api', 'google', 'v1', 'v1alpha1', 'v1beta', 'v2']):
                categorias['APIs_Google'].append(arquivo.name)
            elif any(util in nome_arquivo for util in ['util', 'utility', 'utils', '_utils', 'common', 'helper']):
                categorias['Utilidades'].append(arquivo.name)
            elif any(web in nome_arquivo for web in ['web', 'scrap', 'http', 'request', 'twitch', 'browser', 'firefox']):
                categorias['Web_Scraping'].append(arquivo.name)
            elif any(config in nome_arquivo for config in ['config', 'setting', 'conf']):
                categorias['Configuracoes_JSON'].append(arquivo.name)
            elif any(auto in nome_arquivo for auto in ['auto', 'script', 'install', 'setup']):
                categorias['Scripts_Auto'].append(arquivo.name)
            elif any(data in nome_arquivo for data in ['data', 'csv', 'excel', 'pandas', 'dataframe']):
                categorias['Manipulacao_Dados'].append(arquivo.name)
            elif any(web_ui in nome_arquivo for web_ui in ['html', 'css', 'ui', 'interface', 'dom']):
                categorias['Interface_Web'].append(arquivo.name)
            elif any(text in nome_arquivo for text in ['text', 'string', 'parse', 'coerce', 'union']):
                categorias['Processamento_Texto'].append(arquivo.name)
            else:
                categorias['Outros'].append(arquivo.name)

    # Imprimir resultados
    print("\n" + "="*60)
    print("ORGANIZAÇÃO SUGERIDA DOS ARQUIVOS")
    print("="*60)

    for categoria, arquivos in categorias.items():
        if arquivos:  # Mostrar apenas categorias com arquivos
            print(f"\n📁 {categoria} ({len(arquivos)} arquivos):")
            for arquivo in arquivos[:10]:  # Mostrar no máximo 10 arquivos por categoria
                print(f"  └─ {arquivo}")
            if len(arquivos) > 10:
                print(f"  ... e mais {len(arquivos) - 10} arquivos")

    # Estatísticas
    total_arquivos = sum(len(lista) for lista in categorias.values())
    print(f"\n📊 Total: {total_arquivos} arquivos identificados")

    # Mostrar categorias vazias apenas se solicitado
    categorias_vazias = [cat for cat, arqs in categorias.items() if not arqs]
    if categorias_vazias:
        print(f"\nCategorias vazias: {', '.join(categorias_vazias)}")

def main():
    desktop = Path.home() / "Desktop"
    pasta_scripts = desktop / "Script_Files"

    if pasta_scripts.exists():
        print(f"Iniciando análise dos arquivos em: {pasta_scripts}")
        print("(Apenas listando e categorizando - NENHUM arquivo será movido ou deletado)")
        print("-" * 70)

        analisar_arquivos_apenas_listar(pasta_scripts)

        print("\n" + "="*60)
        print("Análise concluída! Nenhum arquivo foi alterado.")
    else:
        print(f"A pasta {pasta_scripts} não existe.")
        print("Certifique-se de que o script organizar_arquivos.py foi executado primeiro.")

if __name__ == "__main__":
    main()
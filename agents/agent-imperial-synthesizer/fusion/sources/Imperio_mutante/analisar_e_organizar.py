import os
import shutil
from pathlib import Path
import ast
import json

def analisar_arquivo_python(caminho_arquivo):
    """
    Analisa um arquivo Python e retorna informações sobre seu conteúdo.
    """
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            content = f.read()

        tree = ast.parse(content)

        info = {
            'funcoes': [],
            'classes': [],
            'imports': [],
            'descricao': 'arquivo_python',
            'tipo': 'python'
        }

        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                info['funcoes'].append(node.name)
            elif isinstance(node, ast.ClassDef):
                info['classes'].append(node.name)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    info['imports'].append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module
                for alias in node.names:
                    info['imports'].append(f"{module}.{alias.name}")

        # Tentar inferir o propósito do arquivo com base nas funções/classes
        if info['funcoes']:
            if any('web' in func.lower() or 'http' in func.lower() or 'request' in func.lower() for func in info['funcoes']):
                info['descricao'] = 'web_scraping_api'
            elif any('data' in func.lower() or 'csv' in func.lower() or 'excel' in func.lower() for func in info['funcoes']):
                info['descricao'] = 'manipulacao_dados'
            elif any('image' in func.lower() or 'img' in func.lower() or 'pil' in func.lower() for func in info['funcoes']):
                info['descricao'] = 'processamento_imagens'
            elif any('audio' in func.lower() or 'sound' in func.lower() for func in info['funcoes']):
                info['descricao'] = 'processamento_audio'
            elif any('video' in func.lower() or 'movie' in func.lower() for func in info['funcoes']):
                info['descricao'] = 'processamento_video'
            elif any('math' in func.lower() or 'calc' in func.lower() or 'calculate' in func.lower() for func in info['funcoes']):
                info['descricao'] = 'matematica_calculos'
            elif any('text' in func.lower() or 'string' in func.lower() or 'regex' in func.lower() for func in info['funcoes']):
                info['descricao'] = 'processamento_texto'
            else:
                info['descricao'] = 'outras_funcoes'

        return info

    except Exception as e:
        print(f"Erro ao analisar {caminho_arquivo}: {str(e)}")
        return {'descricao': 'arquivo_python', 'tipo': 'python'}

def analisar_arquivo_json(caminho_arquivo):
    """
    Analisa um arquivo JSON e retorna informações sobre seu conteúdo.
    """
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            data = json.load(f)

        info = {
            'estrutura': list(data.keys()) if isinstance(data, dict) else 'lista',
            'descricao': 'arquivo_json',
            'tipo': 'json'
        }

        # Inferir tipo de dados com base na estrutura
        if isinstance(data, dict):
            keys = set(data.keys())
            if 'name' in keys and 'email' in keys:
                info['descricao'] = 'dados_usuario'
            elif 'title' in keys and 'author' in keys:
                info['descricao'] = 'conteudo_publicacao'
            elif 'config' in keys or 'settings' in keys:
                info['descricao'] = 'configuracao'
            elif 'data' in keys or 'items' in keys:
                info['descricao'] = 'dados_estruturados'
            elif any(k.endswith('_id') or k.endswith('Id') for k in keys):
                info['descricao'] = 'dados_relacionais'
            else:
                info['descricao'] = 'outro_json'
        else:
            info['descricao'] = 'dados_lista'

        return info

    except Exception as e:
        print(f"Erro ao analisar {caminho_arquivo}: {str(e)}")
        return {'descricao': 'arquivo_json', 'tipo': 'json'}

def analisar_arquivo_js(caminho_arquivo):
    """
    Analisa um arquivo JavaScript e retorna informações sobre seu conteúdo.
    """
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            content = f.read()

        info = {
            'funcoes': [],
            'variaveis': [],
            'imports': [],
            'descricao': 'arquivo_javascript',
            'tipo': 'javascript'
        }

        # Análise básica de conteúdo JS
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('function ') or '=>' in line and '(' in line:
                # Tenta extrair nome de função
                if line.startswith('function '):
                    parts = line.split('(')[0].split()
                    if len(parts) > 1:
                        info['funcoes'].append(parts[1])
            elif 'import' in line and 'from' in line:
                info['imports'].append(line)
            elif 'require(' in line:
                info['imports'].append(line)

        # Inferir propósito com base em conteúdo
        if 'fetch' in content or 'axios' in content or 'XMLHttpRequest' in content:
            info['descricao'] = 'requisicoes_web'
        elif 'document.' in content or 'window.' in content or 'DOM' in content:
            info['descricao'] = 'manipulacao_dom'
        elif 'localStorage' in content or 'sessionStorage' in content:
            info['descricao'] = 'armazenamento_local'
        elif 'canvas' in content or 'Canvas' in content:
            info['descricao'] = 'graficos_canvas'
        elif 'audio' in content or 'AudioContext' in content:
            info['descricao'] = 'processamento_audio'
        elif 'video' in content or 'Video' in content:
            info['descricao'] = 'manipulacao_video'
        else:
            info['descricao'] = 'outras_funcoes'

        return info

    except Exception as e:
        print(f"Erro ao analisar {caminho_arquivo}: {str(e)}")
        return {'descricao': 'arquivo_javascript', 'tipo': 'javascript'}

def organizar_por_tipo_inteligente(pasta_origem):
    """
    Analisa arquivos em uma pasta e os organiza em subpastas com base em seu conteúdo.
    """
    pasta_origem = Path(pasta_origem)

    if not pasta_origem.exists():
        print(f"A pasta {pasta_origem} não existe.")
        return

    # Pasta de destino para a organização inteligente
    pasta_destino = pasta_origem / "Organizados_Por_Tipo"
    pasta_destino.mkdir(exist_ok=True)

    # Tipos de arquivos que vamos processar
    extensoes_para_analisar = ['.py', '.json', '.js', '.jsx', '.ts', '.tsx']

    for arquivo in pasta_origem.rglob('*'):
        if arquivo.is_file() and arquivo.suffix.lower() in extensoes_para_analisar:
            print(f"Analisando: {arquivo.name}")

            # Analisar o conteúdo do arquivo
            if arquivo.suffix.lower() == '.py':
                info = analisar_arquivo_python(arquivo)
            elif arquivo.suffix.lower() == '.json':
                info = analisar_arquivo_json(arquivo)
            elif arquivo.suffix.lower() in ['.js', '.jsx', '.ts', '.tsx']:
                info = analisar_arquivo_js(arquivo)
            else:
                continue

            # Criar subpasta com base na descrição
            subpasta = pasta_destino / info['descricao']
            subpasta.mkdir(exist_ok=True)

            # Copiar arquivo para a subpasta apropriada
            destino = subpasta / arquivo.name
            contador = 1
            while destino.exists():
                nome_base = destino.stem
                extensao = destino.suffix
                novo_nome = f"{nome_base}_{contador}{extensao}"
                destino = subpasta / novo_nome
                contador += 1

            shutil.copy2(arquivo, destino)
            print(f"  -> Movido para: {info['descricao']}")

def main():
    desktop = Path.home() / "Desktop"
    pasta_scripts = desktop / "Script_Files"

    if pasta_scripts.exists():
        print(f"Iniciando análise e organização dos arquivos em: {pasta_scripts}")
        organizar_por_tipo_inteligente(pasta_scripts)
        print("\nProcesso concluído! Os arquivos foram organizados por tipo em subpastas.")
    else:
        print(f"A pasta {pasta_scripts} não existe.")
        print("Certifique-se de que o script organizar_arquivos.py foi executado primeiro.")

if __name__ == "__main__":
    main()
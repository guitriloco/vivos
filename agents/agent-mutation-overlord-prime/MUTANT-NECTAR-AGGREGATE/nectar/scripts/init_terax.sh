#!/bin/bash
# Nectar_Dev: Terax-AI Initialization Script

echo "[*] Inicializando o ambiente Nectar_Dev..."

# Criar arquivo .env se não existir
if [ ! -f .env ]; then
    echo "[*] Criando template .env..."
    echo "TERAX_API_KEY=your_key_here" > .env
    echo "MODEL_WEIGHTS=claude:0.6,gemini:0.4" >> .env
fi

# Adicionar scripts ao PATH (opcional, apenas para a sessão atual)
export PATH=$PATH:$(pwd)/scripts

echo "[*] Terax-AI pronto para operação."
echo "[*] Use 'python3 scripts/terax.py --help' para ver os comandos."

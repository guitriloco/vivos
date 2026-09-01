#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Demonstração da Fusão Claude-Gemini na Área de Trabalho
Local: Desktop/FUSAO_EXTREMA/demo_fusao_desktop.py
"""

import sys
# Adiciona o caminho correto para os módulos
sys.path.insert(0, r"C:\Users\Usuário\Desktop\FUSAO_EXTREMA")

# Imports diretos
from arsenal.intelligence_fusion import create_fusion_engine

def main():
    print("🚀 INICIANDO DEMONSTRAÇÃO DA FUSÃO CLAUDE-GEMINI (ÁREA DE TRABALHO) 🚀\n")

    # Cria os componentes
    try:
        fusion_engine = create_fusion_engine()
        print("✅ Motor de fusão criado com sucesso!")

        # Testa funcionalidade básica
        claude_resp = "Python é uma linguagem de programação poderosa e versátil, ideal para desenvolvimento rápido e legibilidade de código."
        gemini_resp = "Além disso, Python oferece uma comunidade ativa e vasta biblioteca de módulos que facilitam desde tarefas científicas até desenvolvimento web."

        print(f"\n📝 Resposta Claude: {claude_resp[:60]}...")
        print(f"📝 Resposta Gemini: {gemini_resp[:60]}...")

        synergy_score = fusion_engine.calculate_synergy_score(claude_resp, gemini_resp)
        print(f"\n🔗 Score de sinergia calculado: {synergy_score:.2f}")

        # Testa fusão
        fusion_result = fusion_engine.fuse_responses(claude_resp, gemini_resp, "technical")
        print(f"\n✅ Resposta fundida criada com sucesso!")
        print(f"   Score final: {fusion_result['synergy_score']:.2f}")
        print(f"   Comprimento da resposta fundida: {len(fusion_result['fused_response'])} caracteres")

        print(f"\n🔄 Resposta fundida resultante:")
        print(fusion_result['fused_response'])

        # Testa diferentes tipos de tarefas
        print(f"\n🎯 Testando diferentes tipos de tarefas:")

        tasks = [
            ("creative", "Como criar uma história envolvente sobre IA?", "Criatividade"),
            ("analytical", "Quais são os prós e contras dessa abordagem?", "Análise"),
            ("problem_solving", "Como resolver este problema de lógica?", "Resolução")
        ]

        for task_type, prompt, desc in tasks:
            optimized = fusion_engine.get_optimized_prompt(prompt, task_type)
            print(f"   {desc}: {optimized[:50]}...")

        print("\n✨ Demonstração concluída com sucesso!")
        print("\n📊 RESUMO:")
        print(f"  - Motor de fusão: ✓ Ativo")
        print(f"  - Cálculo de sinergia: ✓ Funcional")
        print(f"  - Otimização de prompts: ✓ Disponível")
        print(f"  - Score de sinergia final: {synergy_score:.2f}/1.00")
        print(f"\n📁 Pasta do projeto: C:\\Users\\Usuário\\Desktop\\FUSAO_EXTREMA")

    except Exception as e:
        print(f"❌ Erro durante a execução: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
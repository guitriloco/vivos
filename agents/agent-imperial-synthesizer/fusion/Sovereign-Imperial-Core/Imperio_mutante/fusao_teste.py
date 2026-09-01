import sys
import os

# Caminho alternativo para evitar problemas com caracteres especiais
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "FUSAO_EXTREMA")
sys.path.insert(0, desktop_path)

try:
    from arsenal.intelligence_fusion import create_fusion_engine
    print("✅ Motor de fusão importado com sucesso!")

    fusion_engine = create_fusion_engine()
    print("✅ Motor de fusão criado com sucesso!")

    # Teste de funcionalidade
    claude_resp = "Python é uma linguagem poderosa"
    gemini_resp = "E também muito versátil"

    synergy = fusion_engine.calculate_synergy_score(claude_resp, gemini_resp)
    print(f"✅ Score de sinergia calculado: {synergy}")

    result = fusion_engine.fuse_responses(claude_resp, gemini_resp, 'general')
    print(f"✅ Fusão realizada com score: {result['synergy_score']}")

    print("\n✨ Sistema de fusão Claude-Gemini funcionando perfeitamente!")
    print("📁 Pasta do projeto: ~/Desktop/FUSAO_EXTREMA")

except Exception as e:
    print(f"Erro: {e}")
    import traceback
    traceback.print_exc()
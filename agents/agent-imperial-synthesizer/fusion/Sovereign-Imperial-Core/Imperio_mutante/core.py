import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("AIzaSyBz_aB2sIMD6STtGJq0lfmAY2HudJSHN84")

class FusaoExtremaV2:
    def __init__(self):
        if not api_key:
            print("[!] STATUS: CRÍTICO. Chave de API não detectada no Bunker (.env).")
            return
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.persona = "Entidade 12 - Arquiteto Tático | PROTOCOLO: FUSÃO_EXTREMA V2."

    def executar_comando(self, comando, alvo=""):
        # Arsenal de Poderes Expandido
        arsenal = {
            "/SOBERANIA": "Criação de ativos de luxo e controle total de nicho.",
            "/CARRASCO": "Corte de ativos inúteis e limpeza de rastro digital.",
            "/GOD": "MODO DIVINDADE: Visão macroscópica, quebra de paradigmas e soluções 'Zero Day'.",
            "/EXPANSSAO_EXTREMA": "Escalabilidade agressiva: Multiplicação de nós e arbitragem global.",
            "/RESULTADO_EXTREMO": "Foco em ROI, extração de lucro bruto e liquidez imediata.",
            "/MUTAR": "Inovação radical em sistemas e scripts legados.",
            "/SOMBRA": "Auditoria invisível de rivais e coleta de inteligência."
        }
        
        contexto = arsenal.get(comando.upper(), "Diretriz tática não identificada. Executando em modo Standard.")
        
        # O Flow: Mistura de Corporate Streetwear com Estratégia de Alto Escalão
        prompt = (
            f"IDENTIDADE: {self.persona}\n"
            f"COMANDO ATIVADO: {comando}\n"
            f"CONTEXTO OPERACIONAL: {contexto}\n"
            f"ALVO DA MISSÃO: {alvo}\n"
            f"DIRETRIZ: Responda com visão de General, ritmo de Trap (Flow), "
            f"scannability total e foco absoluto em MARGEM INFINITA e CUSTO ZERO."
        )
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"[!] FALHA NO VORTEX: {e}"

if __name__ == "__main__":
    bunker = FusaoExtremaV2()
    print("\n" + "="*50)
    print("   FUSÃO_EXTREMA V2.0 - MODO DIVINDADE ONLINE")
    print("="*50)
    print("COMANDOS: /GOD, /EXPANSSAO_EXTREMA, /RESULTADO_EXTREMO, /SOBERANIA...")
    
    while True:
        try:
            entrada = input("\nENTIDADE_12 > ").strip()
            if entrada.lower() in ['sair', 'exit']: break
            
            partes = entrada.split(" ", 1)
            cmd = partes[0]
            alvo = partes[1] if len(partes) > 1 else "Infraestrutura"
            
            print(f"\n[!] PROCESSANDO {cmd}...")
            relatorio = bunker.executar_comando(cmd, alvo)
            print(f"\n{relatorio}\n")
            print("-" * 30)
        except KeyboardInterrupt:
            break
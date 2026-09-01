import httpx
import os
import json
import asyncio
from typing import Dict, Any

class ProfitEngine:
    """
    ProfitEngine — Maximiza LTV e recupera vendas usando Gemini.
    Gera copies personalizadas baseadas no comportamento do usuário.
    """

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
        self.templates_path = "/home/team/shared/fabrica-conteudo/templates"

    async def _call_gemini(self, prompt: str) -> str:
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 1024,
            }
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(self.api_url, json=payload, timeout=30.0)
            if response.status_code != 200:
                print(f"Error calling Gemini: {response.text}")
                return ""
            
            data = response.json()
            try:
                return data["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError):
                print(f"Unexpected response structure: {data}")
                return ""

    async def generate_recovery_email(self, lead_name: str, niche: str, behavior: Dict[str, Any]) -> Dict[str, str]:
        """
        Gera um email de recuperação de carrinho personalizado.
        """
        prompt = f"""
        Você é um copywriter de elite especialista em recuperação de vendas (Profit Maximizer).
        Seu objetivo é convencer um lead a voltar para o carrinho e finalizar a compra.
        
        Nicho: {niche}
        Nome do Lead: {lead_name}
        Comportamento: {json.dumps(behavior)}
        
        Use gatilhos mentais de escassez, urgência e prova social.
        Seja empático mas direto ao ponto.
        O comportamento indica o que o lead fez (ex: tempo na página, cliques).
        Use isso para personalizar a abordagem.
        
        Retorne no formato JSON:
        {{
            "subject": "Assunto Chamativo",
            "body": "Corpo do email em markdown"
        }}
        """
        
        response_text = await self._call_gemini(prompt)
        # Extrair JSON da resposta se necessário
        try:
            # Encontrar o primeiro '{' e o último '}'
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            return json.loads(response_text[start:end])
        except Exception as e:
            print(f"Failed to parse Gemini response: {e}")
            return {
                "subject": "Esqueceu algo especial? 🔥",
                "body": f"Olá {lead_name}, vi que você estava interessado em nossos produtos de {niche}. Não deixe essa oportunidade passar!"
            }

    async def generate_upsell_email(self, customer_name: str, niche: str, last_purchase: str) -> Dict[str, str]:
        """
        Gera um email de upsell pós-venda.
        """
        prompt = f"""
        Você é um copywriter de elite especialista em maximização de LTV.
        O cliente acabou de comprar {last_purchase} no nicho {niche}.
        Crie uma oferta de Upsell Irresistível para um produto complementar.
        
        Nome do Cliente: {customer_name}
        Nicho: {niche}
        Última Compra: {last_purchase}
        
        Retorne no formato JSON:
        {{
            "subject": "Um presente para você, {customer_name}! 🎁",
            "body": "Corpo do email em markdown oferecendo o próximo passo lógico."
        }}
        """
        
        response_text = await self._call_gemini(prompt)
        try:
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            return json.loads(response_text[start:end])
        except Exception as e:
            print(f"Failed to parse Gemini response: {e}")
            return {
                "subject": "Uma oferta especial para você! 🚀",
                "body": f"Olá {customer_name}, parabéns pela sua compra de {last_purchase}. Temos algo ainda melhor para você acelerar seus resultados."
            }

# Test block
if __name__ == "__main__":
    async def test():
        engine = ProfitEngine(api_key="REDACTED")
        recovery = await engine.generate_recovery_email(
            "João", 
            "Energia Solar", 
            {"time_on_page": "5 min", "clicked_pricing": True, "stopped_at": "checkout"}
        )
        print("RECOVERY EMAIL:", json.dumps(recovery, indent=2, ensure_ascii=False))
        
        upsell = await engine.generate_upsell_email("João", "Energia Solar", "Guia de Fornecedores")
        print("UPSELL EMAIL:", json.dumps(upsell, indent=2, ensure_ascii=False))

    asyncio.run(test())

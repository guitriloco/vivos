"""
Serviço de integração com APIs de IA (Claude e Gemini)
Este módulo será responsável por toda a comunicação com as APIs de IA
"""

import os
import google.generativeai as genai
import requests
import logging
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIProvider(ABC):
    """Interface para provedores de IA"""

    @abstractmethod
    def generate_content(self, prompt: str, **kwargs) -> str:
        pass

    @abstractmethod
    def get_embeddings(self, text: str) -> List[float]:
        pass

class GeminiService(AIProvider):
    """Serviço para integração com a API do Gemini"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Chave da API do Gemini não encontrada")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_content(self, prompt: str, **kwargs) -> str:
        """Gera conteúdo usando o modelo Gemini"""
        try:
            generation_config = {
                "temperature": kwargs.get("temperature", 0.7),
                "max_output_tokens": kwargs.get("max_tokens", 2048),
            }

            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )

            return response.text
        except Exception as e:
            logger.error(f"Erro ao gerar conteúdo com Gemini: {e}")
            raise

    def get_embeddings(self, text: str) -> List[float]:
        """Obtém embeddings para o texto usando o Gemini"""
        try:
            result = genai.embed_content(
                model="models/embedding-001",
                content=text,
                task_type="semantic_similarity"
            )
            return result['embedding']
        except Exception as e:
            logger.error(f"Erro ao obter embeddings com Gemini: {e}")
            raise

class ClaudeService(AIProvider):
    """Serviço para integração com a API do Claude (simulado - substituir com API real)"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("CLAUDE_API_KEY")
        if not self.api_key:
            raise ValueError("Chave da API do Claude não encontrada")

        self.base_url = "https://api.anthropic.com/v1/messages"
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }

    def generate_content(self, prompt: str, **kwargs) -> str:
        """Gera conteúdo usando o modelo Claude (simulado)"""
        # Em implementação real, faria a chamada à API do Claude
        # Por enquanto, simulamos o comportamento
        logger.warning("ClaudeService é um placeholder - implementar com API real do Claude")

        # Simulação de resposta do Claude
        simulated_response = f"[Claude Analysis] {prompt[:100]}... [Technical depth applied]"
        return simulated_response

    def get_embeddings(self, text: str) -> List[float]:
        """Obtém embeddings para o texto usando Claude (simulado)"""
        # Claude não oferece embeddings diretamente, então simulamos
        logger.warning("Embeddings para Claude são simulados")
        return [0.1] * 768  # Vetor de exemplo

class FusionService:
    """Serviço para fusão de inteligências Claude e Gemini"""

    def __init__(self):
        self.gemini_service = None
        self.claude_service = None

        # Inicializa serviços se as chaves estiverem disponíveis
        try:
            self.gemini_service = GeminiService()
            logger.info("Serviço Gemini inicializado")
        except ValueError:
            logger.warning("Chave do Gemini não encontrada - funcionalidade limitada")

        try:
            self.claude_service = ClaudeService()
            logger.info("Serviço Claude inicializado")
        except ValueError:
            logger.warning("Chave do Claude não encontrada - funcionalidade limitada")

    def generate_hiperpersonalized_content(self, base_prompt: str, personalization_data: Dict[str, Any]) -> str:
        """Gera conteúdo hiper-personalizado combinando insights de Claude e Gemini"""

        # Monta o prompt personalizado
        personalized_prompt = self._build_personalized_prompt(base_prompt, personalization_data)

        responses = []

        # Obtém resposta do Gemini se disponível
        if self.gemini_service:
            gemini_response = self.gemini_service.generate_content(
                personalized_prompt,
                temperature=0.7,
                max_tokens=1024
            )
            responses.append(("Gemini", gemini_response))

        # Obtém resposta do Claude se disponível
        if self.claude_service:
            claude_response = self.claude_service.generate_content(
                personalized_prompt
            )
            responses.append(("Claude", claude_response))

        # Se tivermos respostas de ambos, faz a fusão
        if len(responses) >= 2:
            return self._fuse_responses(responses, personalization_data)
        elif len(responses) == 1:
            return responses[0][1]
        else:
            # Retorna prompt base se nenhuma IA estiver disponível
            return f"[Conteúdo não personalizado] {base_prompt}"

    def _build_personalized_prompt(self, base_prompt: str, personalization_data: Dict[str, Any]) -> str:
        """Monta um prompt personalizado com base nos dados de personalização"""

        user_context = personalization_data.get("user_context", {})
        product_info = personalization_data.get("product_info", {})
        audience_profile = personalization_data.get("audience_profile", {})

        prompt_parts = [
            f"Contexto do usuário: {user_context}",
            f"Informações do produto: {product_info}",
            f"Perfil do público-alvo: {audience_profile}",
            f"Prompt base: {base_prompt}",
            "Gere conteúdo altamente personalizado levando em conta o contexto do usuário e características específicas do produto."
        ]

        return "\n".join(prompt_parts)

    def _fuse_responses(self, responses: List[tuple], personalization_data: Dict[str, Any]) -> str:
        """Funde respostas de diferentes IAs com base em dados de personalização"""

        # Para simplificação, fazemos uma fusão básica
        # Em implementação real, aplicaríamos técnicas mais avançadas

        fused_parts = []
        for provider, response in responses:
            fused_parts.append(f"[{provider} Perspective]: {response}")

        # Adiciona instruções finais de personalização
        final_instruction = (
            f"\n\nConsiderando as perspectivas acima, gere um conteúdo final "
            f"otimizado para o usuário com base em: {personalization_data.get('user_context', {}).get('preferences', 'preferências padrão')}"
        )

        fused_parts.append(final_instruction)

        return "\n\n".join(fused_parts)

# Instância global do serviço de fusão
fusion_service = FusionService()

def get_fusion_service() -> FusionService:
    """Retorna a instância do serviço de fusão"""
    return fusion_service
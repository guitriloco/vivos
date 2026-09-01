import os
import google.generativeai as genai
from typing import Optional, Dict, Any

class GeminiAPIIntegration:
    """
    Classe para integrar com a API do Gemini e ampliar as capacidades do Claude Code
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa a integração com a API do Gemini

        Args:
            api_key: Chave da API do Gemini. Se não fornecida, tentará ler da variável de ambiente GEMINI_API_KEY
        """
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = os.getenv('GEMINI_API_KEY')

        if not self.api_key:
            raise ValueError("Chave da API do Gemini não encontrada. Defina a variável de ambiente GEMINI_API_KEY ou forneça a chave como parâmetro.")

        genai.configure(api_key=self.api_key)

        # Configuração padrão do modelo
        self.model_name = "gemini-pro"  # ou "gemini-pro-vision" para multimodal
        self.model = genai.GenerativeModel(self.model_name)

    def generate_content(self, prompt: str, temperature: float = 0.7, max_output_tokens: int = 8192) -> str:
        """
        Gera conteúdo usando o modelo Gemini

        Args:
            prompt: Texto de entrada para gerar resposta
            temperature: Controle de criatividade (0.0 a 1.0)
            max_output_tokens: Máximo de tokens na saída

        Returns:
            Resposta gerada pelo modelo
        """
        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens
        )

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            return response.text
        except Exception as e:
            return f"Erro ao gerar conteúdo: {str(e)}"

    def chat_session(self, initial_history: Optional[list] = None) -> genai.ChatSession:
        """
        Cria uma sessão de chat com histórico opcional

        Args:
            initial_history: Histórico inicial opcional para o chat

        Returns:
            Sessão de chat configurada
        """
        return self.model.start_chat(history=initial_history or [])

    def embed_content(self, text: str) -> list:
        """
        Gera embeddings para o texto fornecido

        Args:
            text: Texto para gerar embeddings

        Returns:
            Vetor de embeddings
        """
        try:
            result = genai.embed_content(
                model="models/embedding-001",
                content=text,
                task_type="semantic_similarity"
            )
            return result['embedding']
        except Exception as e:
            return f"Erro ao gerar embedding: {str(e)}"


def setup_claude_gemini_bridge():
    """
    Função para configurar a ponte entre Claude Code e Gemini API
    """
    print("Configurando integração Claude-Gemini...")

    try:
        # Verifica se a chave da API está definida
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("AVISO: A variável de ambiente GEMINI_API_KEY não está definida.")
            print("Por favor, defina-a antes de usar esta integração:")
            print("  export GEMINI_API_KEY='sua_chave_aqui'")
            return None

        # Cria a instância da integração
        gemini_integration = GeminiAPIIntegration()
        print("Integração Claude-Gemini configurada com sucesso!")

        return gemini_integration

    except Exception as e:
        print(f"Erro ao configurar integração: {str(e)}")
        return None


def enhanced_generate_content(gemini_integration: GeminiAPIIntegration, prompt: str) -> str:
    """
    Função que combina as capacidades do Claude com o Gemini para respostas aprimoradas
    """
    if not gemini_integration:
        return "Integração com Gemini não está configurada corretamente."

    # Envia o prompt para o Gemini e retorna a resposta
    return gemini_integration.generate_content(prompt)


if __name__ == "__main__":
    # Exemplo de uso
    integration = setup_claude_gemini_bridge()

    if integration:
        # Exemplo de uso
        prompt = "Explique como funciona a inteligência artificial generativa"
        response = integration.generate_content(prompt)
        print(f"Resposta do Gemini: {response}")
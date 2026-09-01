from flask import request, jsonify
from typing import Dict, Any
import logging
from datetime import datetime
import hashlib
import json

# Importa os modelos
from api.models.content import ContentGenerator, PersonalizationProfile, PersonalizationData
from api.models.user import User

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentController:
    def __init__(self):
        self.content_gen = ContentGenerator()
        self.profile_manager = PersonalizationProfile()
        self.user_manager = User()

    def generate_personalized_content(self) -> Dict[Any, Any]:
        """Gera conteúdo hiper-personalizado baseado em dados do usuário"""
        try:
            # Obtém dados da requisição
            data = request.get_json()
            if not data:
                return {"error": "Dados inválidos"}, 400

            user_id = data.get('user_id')
            product_info = data.get('product_info', {})
            content_type = data.get('content_type', 'descricao')
            personalization_params = data.get('personalization_params', {})

            if not user_id:
                return {"error": "ID do usuário é obrigatório"}, 400

            # Verifica se já existe conteúdo gerado recentemente para evitar regeneração
            cached_content = self.content_gen.get_personalized_content(
                user_id, product_info.get('id', ''), content_type
            )

            if cached_content and not personalization_params.get('force_regenerate', False):
                logger.info(f"Conteúdo em cache encontrado para usuário {user_id}")
                return {
                    "content": cached_content,
                    "cached": True,
                    "timestamp": datetime.now().isoformat()
                }

            # Recupera informações do usuário para personalização
            user_info = self._get_user_info(user_id)
            if not user_info:
                return {"error": "Usuário não encontrado"}, 404

            # Prepara dados de personalização
            personalization_data = self._prepare_personalization_data(
                user_info, product_info, personalization_params
            )

            # Gera conteúdo personalizado (simulado por enquanto)
            generated_content = self._simulate_ai_generation(
                personalization_data, content_type
            )

            # Salva no histórico
            content_id = self.content_gen.save_generated_content(
                user_id,
                product_info.get('id', ''),
                content_type,
                generated_content,
                personalization_data.__dict__ if hasattr(personalization_data, '__dict__') else personalization_data
            )

            logger.info(f"Conteúdo gerado com sucesso para usuário {user_id}, ID: {content_id}")

            return {
                "content_id": content_id,
                "content": generated_content,
                "cached": False,
                "timestamp": datetime.now().isoformat(),
                "personalization_factors": {
                    "user_context": personalization_data.user_context,
                    "product_info": personalization_data.product_info,
                    "content_type": content_type
                }
            }

        except Exception as e:
            logger.error(f"Erro ao gerar conteúdo: {str(e)}")
            return {"error": "Erro interno ao gerar conteúdo"}, 500

    def get_content_history(self) -> Dict[Any, Any]:
        """Recupera histórico de conteúdo gerado para um usuário"""
        try:
            user_id = request.args.get('user_id')
            limit = int(request.args.get('limit', 10))

            if not user_id:
                return {"error": "ID do usuário é obrigatório"}, 400

            history = self.content_gen.get_content_history(int(user_id), limit)

            return {
                "history": history,
                "count": len(history),
                "user_id": user_id
            }

        except Exception as e:
            logger.error(f"Erro ao recuperar histórico: {str(e)}")
            return {"error": "Erro interno ao recuperar histórico"}, 500

    def _get_user_info(self, user_id: int) -> Dict:
        """Recupera informações do usuário para personalização"""
        # Este método seria implementado para buscar informações reais do usuário
        # Por enquanto, retorna dados simulados
        conn = self.user_manager.db_path
        # Na implementação real, buscaria informações detalhadas do usuário
        return {
            "id": user_id,
            "preferences": {},
            "behavioral_data": {},
            "demographics": {}
        }

    def _prepare_personalization_data(self, user_info: Dict, product_info: Dict, params: Dict) -> PersonalizationData:
        """Prepara dados de personalização para geração de conteúdo"""
        return PersonalizationData(
            user_context={
                "preferences": user_info.get("preferences", {}),
                "behavioral_data": user_info.get("behavioral_data", {}),
                "demographics": user_info.get("demographics", {}),
                "purchase_history": params.get("purchase_history", [])
            },
            product_info={
                "name": product_info.get("name", ""),
                "category": product_info.get("category", ""),
                "features": product_info.get("features", []),
                "price": product_info.get("price", 0),
                "brand": product_info.get("brand", "")
            },
            audience_profile=params.get("audience_profile", {}),
            behavioral_data=params.get("behavioral_data", {}),
            contextual_factors=params.get("contextual_factors", {})
        )

    def _simulate_ai_generation(self, personalization_data: PersonalizationData, content_type: str) -> str:
        """Simula a geração de conteúdo por IA - substituir com API real"""
        # Esta função seria substituída pela integração real com Claude/Gemini

        # Simulação de conteúdo personalizado
        user_context = personalization_data.user_context
        product_info = personalization_data.product_info

        if content_type == "descricao":
            return f"""
            Descobrimos algo incrível que parece ter sido criado especialmente para você, {user_context.get('demographics', {}).get('name', 'usuário')}!

            O {product_info.get('name', 'produto')} é perfeito para quem, como você, valoriza {', '.join(product_info.get('features', ['qualidade', 'inovação']))}.

            Com base no seu histórico e preferências, acreditamos que este produto vai transformar sua experiência de {product_info.get('category', 'categoria')} em algo excepcional.

            Oferecemos {product_info.get('name', 'produto')} com entrega imediata e garantia estendida, porque sabemos que você merece o melhor.
            """
        elif content_type == "titulo":
            return f"{product_info.get('name', 'Produto')} - Ideal para {user_context.get('demographics', {}).get('interests', ['você'])}"
        elif content_type == "chamada":
            return f"Descubra por que {user_context.get('demographics', {}).get('name', 'usuário')} está apaixonado(a) por {product_info.get('name', 'produto')}!"
        else:
            return f"Conteúdo personalizado de tipo '{content_type}' para {product_info.get('name', 'produto')} baseado em seu perfil único."

content_controller = ContentController()
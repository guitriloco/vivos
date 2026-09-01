from flask import Blueprint
from api.controllers.content_controller import content_controller

content_bp = Blueprint('content', __name__)

# Rotas para geração de conteúdo
@content_bp.route('/generate', methods=['POST'])
def generate_content():
    return content_controller.generate_personalized_content()

@content_bp.route('/history', methods=['GET'])
def get_content_history():
    return content_controller.get_content_history()

@content_bp.route('/validate', methods=['POST'])
def validate_personalization():
    """Valida os parâmetros de personalização"""
    from flask import request
    data = request.get_json()

    required_fields = ['user_id', 'product_info']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return {"error": f"Campos obrigatórios ausentes: {missing_fields}"}, 400

    return {"valid": True, "message": "Parâmetros válidos para personalização"}

# Rota para simular integração com IA (substituir com API real)
@content_bp.route('/simulate-ai-integration', methods=['POST'])
def simulate_ai_integration():
    """Rota temporária para simular a integração com IA"""
    from flask import request
    import time

    data = request.get_json()

    # Simula o tempo de processamento da IA
    time.sleep(0.5)

    # Retorna uma resposta simulada
    return {
        "success": True,
        "message": "Integração com IA simulada com sucesso",
        "estimated_processing_time": "0.5 segundos",
        "next_steps": [
            "Substituir esta rota com a integração real com Claude/Gemini",
            "Implementar autenticação para APIs de IA",
            "Adicionar tratamento de erros e limites de taxa"
        ]
    }
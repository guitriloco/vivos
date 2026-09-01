from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Importa os blueprints
from api.routes.content_routes import content_bp
from api.routes.user_routes import user_bp
from api.routes.analytics_routes import analytics_bp

def create_app():
    app = Flask(__name__)
    CORS(app)  # Habilita CORS para todas as rotas

    # Configurações
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['DATABASE_URL'] = os.getenv('DATABASE_URL', 'sqlite:///hiperp.db')

    # Registra blueprints
    app.register_blueprint(content_bp, url_prefix='/api/v1/content')
    app.register_blueprint(user_bp, url_prefix='/api/v1/user')
    app.register_blueprint(analytics_bp, url_prefix='/api/v1/analytics')

    # Rota raiz
    @app.route('/')
    def home():
        return jsonify({
            "message": "Bem-vindo ao Hiperpersonalizador - API de Conteúdo Hiper-Personalizado",
            "version": "1.0.0",
            "endpoints": {
                "content_generation": "/api/v1/content/generate",
                "user_management": "/api/v1/user/",
                "analytics": "/api/v1/analytics/"
            }
        })

    # Rota de health check
    @app.route('/health')
    def health():
        return jsonify({"status": "healthy", "service": "hiperp-api"})

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
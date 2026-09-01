import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///hiperp.db'
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    CLAUDE_API_KEY = os.environ.get('CLAUDE_API_KEY')
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'

    # Configurações de IA
    DEFAULT_MODEL = os.environ.get('DEFAULT_MODEL') or 'gemini-pro'
    TEMPERATURE = float(os.environ.get('TEMPERATURE', 0.7))
    MAX_TOKENS = int(os.environ.get('MAX_TOKENS', 2048))

    # Configurações de cache
    CACHE_TTL_SECONDS = int(os.environ.get('CACHE_TTL_SECONDS', 3600))

    # Configurações de segurança
    RATE_LIMIT_REQUESTS = int(os.environ.get('RATE_LIMIT_REQUESTS', 100))
    RATE_LIMIT_WINDOW = int(os.environ.get('RATE_LIMIT_WINDOW', 3600))  # 1 hora

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
"""
Funções utilitárias para o projeto Hiperpersonalizador
"""

import hashlib
import json
from datetime import datetime
from typing import Dict, Any, Union
import re

def generate_cache_key(data: Dict[str, Any]) -> str:
    """Gera uma chave de cache baseada nos dados de entrada"""
    serialized_data = json.dumps(data, sort_keys=True)
    return hashlib.md5(serialized_data.encode()).hexdigest()

def sanitize_input(text: str) -> str:
    """Sanitiza entrada de texto removendo possíveis injeções"""
    if not isinstance(text, str):
        return ""

    # Remove caracteres potencialmente perigosos
    sanitized = re.sub(r'[<>"\']', '', text)
    return sanitized.strip()

def validate_email(email: str) -> bool:
    """Valida formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def format_currency(value: float, currency: str = "BRL") -> str:
    """Formata valor monetário"""
    if currency == "BRL":
        return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    else:
        return f"${value:,.2f}"

def calculate_similarity(text1: str, text2: str) -> float:
    """Calcula similaridade entre dois textos (simulação básica)"""
    set1 = set(text1.lower().split())
    set2 = set(text2.lower().split())

    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))

    return intersection / union if union != 0 else 0.0

def extract_keywords(text: str, max_keywords: int = 10) -> list:
    """Extrai palavras-chave de um texto"""
    # Remove pontuação e converte para minúsculas
    clean_text = re.sub(r'[^\w\s]', ' ', text.lower())
    words = clean_text.split()

    # Remove palavras comuns (stopwords)
    common_words = {
        'a', 'o', 'e', 'de', 'do', 'da', 'em', 'um', 'para', 'é', 'com', 'não', 'na', 'por',
        'os', 'as', 'se', 'um', 'uma', 'no', 'nas', 'ao', 'aos', 'são', 'como', 'mas',
        'ao', 'aos', 'ser', 'será', 'está', 'estão', 'você', 'sua', 'seu', 'nos', 'me', 'te'
    }

    keywords = [word for word in words if word not in common_words and len(word) > 2]
    # Retorna as palavras mais frequentes
    word_freq = {}
    for word in keywords:
        word_freq[word] = word_freq.get(word, 0) + 1

    sorted_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, freq in sorted_keywords[:max_keywords]]

def get_sentiment_score(text: str) -> float:
    """Calcula pontuação de sentimento (simulação básica)"""
    positive_words = {
        'bom', 'ótimo', 'excelente', 'incrível', 'maravilhoso', 'fantástico', 'perfeito',
        'melhor', 'amazing', 'great', 'good', 'love', 'adore', 'excelente', 'super',
        'top', 'premium', 'luxo', 'exclusivo', 'especial', 'único', 'diferenciado'
    }

    negative_words = {
        'ruim', 'péssimo', 'horrível', 'terrível', 'medonho', 'pavoroso', 'terrível',
        'nunca', 'odeio', 'detesto', 'errar', 'falhar', 'problema', 'erro', 'difícil'
    }

    words = set(text.lower().split())
    positive_count = len(words.intersection(positive_words))
    negative_count = len(words.intersection(negative_words))

    total_opinion_words = positive_count + negative_count

    if total_opinion_words == 0:
        return 0.0

    return (positive_count - negative_count) / total_opinion_words

def format_personalization_data(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Formata dados de personalização para padronização"""
    formatted = {
        "user_profile": {
            "age_group": user_data.get("age_group", "unknown"),
            "location": user_data.get("location", "unknown"),
            "interests": user_data.get("interests", []),
            "preferences": user_data.get("preferences", {}),
            "purchase_history": user_data.get("purchase_history", [])
        },
        "contextual_data": {
            "time_of_day": user_data.get("time_of_day", "unknown"),
            "device_type": user_data.get("device_type", "unknown"),
            "previous_interactions": user_data.get("previous_interactions", 0)
        },
        "product_relevance": {
            "category_match": user_data.get("category_match", 0.0),
            "feature_relevance": user_data.get("feature_relevance", 0.0),
            "price_sensitivity": user_data.get("price_sensitivity", 0.0)
        }
    }

    return formatted

def create_audit_log(action: str, user_id: int, details: Dict[str, Any]) -> Dict[str, Any]:
    """Cria log de auditoria para rastreamento"""
    return {
        "timestamp": datetime.now().isoformat(),
        "user_id": user_id,
        "action": action,
        "details": details,
        "ip_address": details.get("ip_address", "unknown")
    }

def mask_sensitive_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Mascara dados sensíveis para logging"""
    masked_data = data.copy()

    sensitive_fields = ['email', 'phone', 'cpf', 'credit_card', 'password', 'api_key']

    for field in sensitive_fields:
        if field in masked_data:
            original_value = str(masked_data[field])
            if len(original_value) > 4:
                masked_data[field] = original_value[:2] + '*' * (len(original_value) - 4) + original_value[-2:]
            else:
                masked_data[field] = '***'

    return masked_data
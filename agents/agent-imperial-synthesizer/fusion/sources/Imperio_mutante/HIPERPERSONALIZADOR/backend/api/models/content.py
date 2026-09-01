from datetime import datetime
from typing import Dict, List, Optional, Any
import sqlite3
import json
from dataclasses import dataclass

@dataclass
class PersonalizationData:
    """Dados de personalização para geração de conteúdo"""
    user_context: Dict[str, Any]
    product_info: Dict[str, Any]
    audience_profile: Dict[str, Any]
    behavioral_data: Dict[str, Any]
    contextual_factors: Dict[str, Any]

class ContentGenerator:
    def __init__(self, db_path: str = "hiperp.db"):
        self.db_path = db_path

    def save_generated_content(self, user_id: int, product_id: str, content_type: str,
                             generated_content: str, personalization_data: Dict) -> int:
        """Salva o conteúdo gerado no histórico"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO content_history
            (user_id, product_id, content_type, generated_content, personalization_data)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, product_id, content_type, generated_content,
              json.dumps(personalization_data)))

        content_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return content_id

    def get_content_history(self, user_id: int, limit: int = 50) -> List[Dict]:
        """Recupera o histórico de conteúdo gerado para um usuário"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM content_history
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (user_id, limit))

        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]

        history = []
        for row in rows:
            record = dict(zip(columns, row))
            # Converte JSON de volta para objeto
            if record['personalization_data']:
                record['personalization_data'] = json.loads(record['personalization_data'])
            history.append(record)

        conn.close()
        return history

    def get_personalized_content(self, user_id: int, product_id: str, content_type: str) -> Optional[str]:
        """Busca conteúdo personalizado previamente gerado para evitar regeneração"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT generated_content FROM content_history
            WHERE user_id = ? AND product_id = ? AND content_type = ?
            ORDER BY created_at DESC
            LIMIT 1
        """, (user_id, product_id, content_type))

        result = cursor.fetchone()
        conn.close()

        return result[0] if result else None

class PersonalizationProfile:
    def __init__(self, db_path: str = "hiperp.db"):
        self.db_path = db_path

    def create_profile(self, user_id: int, profile_name: str, profile_data: Dict, is_default: bool = False):
        """Cria um perfil de personalização"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Se for padrão, remove o padrão dos outros perfis do usuário
        if is_default:
            cursor.execute("""
                UPDATE personalization_profiles
                SET is_default = FALSE
                WHERE user_id = ? AND is_default = TRUE
            """, (user_id,))

        cursor.execute("""
            INSERT INTO personalization_profiles
            (user_id, profile_name, profile_data, is_default)
            VALUES (?, ?, ?, ?)
        """, (user_id, profile_name, json.dumps(profile_data), is_default))

        profile_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return profile_id

    def get_user_profiles(self, user_id: int) -> List[Dict]:
        """Recupera todos os perfis de personalização de um usuário"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM personalization_profiles
            WHERE user_id = ?
            ORDER BY is_default DESC, created_at DESC
        """, (user_id,))

        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]

        profiles = []
        for row in rows:
            record = dict(zip(columns, row))
            # Converte JSON de volta para objeto
            if record['profile_data']:
                record['profile_data'] = json.loads(record['profile_data'])
            profiles.append(record)

        conn.close()
        return profiles

    def get_default_profile(self, user_id: int) -> Optional[Dict]:
        """Recupera o perfil padrão de um usuário"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM personalization_profiles
            WHERE user_id = ? AND is_default = TRUE
            LIMIT 1
        """, (user_id,))

        row = cursor.fetchone()
        conn.close()

        if row:
            columns = [description[0] for description in cursor.description]
            profile = dict(zip(columns, row))
            if profile['profile_data']:
                profile['profile_data'] = json.loads(profile['profile_data'])
            return profile

        return None
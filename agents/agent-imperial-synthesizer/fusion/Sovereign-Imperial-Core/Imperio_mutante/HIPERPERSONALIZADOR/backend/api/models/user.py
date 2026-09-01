from datetime import datetime
from typing import Dict, List, Optional
import sqlite3
import hashlib
import json

class User:
    def __init__(self, db_path: str = "hiperp.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Inicializa o banco de dados com as tabelas necessárias"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Tabela de usuários
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                company TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                preferences TEXT DEFAULT '{}',
                api_key_hash TEXT
            )
        """)

        # Tabela de histórico de conteúdo gerado
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS content_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                product_id TEXT,
                content_type TEXT,
                generated_content TEXT,
                personalization_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)

        # Tabela de perfis de personalização
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS personalization_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                profile_name TEXT,
                profile_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_default BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)

        conn.commit()
        conn.close()

    def create_user(self, email: str, name: str, company: str = None) -> Dict:
        """Cria um novo usuário"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO users (email, name, company)
                VALUES (?, ?, ?)
            """, (email, name, company))

            user_id = cursor.lastrowid
            conn.commit()

            return {
                "id": user_id,
                "email": email,
                "name": name,
                "company": company,
                "created_at": datetime.now().isoformat()
            }
        except sqlite3.IntegrityError:
            return {"error": "Email já cadastrado"}
        finally:
            conn.close()

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Busca usuário por email"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()

        if row:
            columns = [description[0] for description in cursor.description]
            user = dict(zip(columns, row))
            return user

        conn.close()
        return None

    def update_preferences(self, user_id: int, preferences: Dict) -> bool:
        """Atualiza as preferências do usuário"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users SET preferences = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (json.dumps(preferences), user_id))

        conn.commit()
        conn.close()
        return cursor.rowcount > 0
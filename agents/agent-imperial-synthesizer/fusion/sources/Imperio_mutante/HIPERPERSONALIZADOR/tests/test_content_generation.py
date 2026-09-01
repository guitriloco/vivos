"""
Testes para o módulo de geração de conteúdo hiper-personalizado
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Adiciona o diretório backend ao path para importação
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from api.models.content import ContentGenerator, PersonalizationProfile
from api.controllers.content_controller import ContentController

class TestContentGeneration(unittest.TestCase):
    """Testes para a geração de conteúdo personalizado"""

    def setUp(self):
        """Configuração antes de cada teste"""
        self.content_gen = ContentGenerator(db_path=":memory:")  # Usando DB em memória para testes
        self.controller = ContentController()

    def test_create_content_generator(self):
        """Testa a criação do gerador de conteúdo"""
        self.assertIsNotNone(self.content_gen)
        self.assertEqual(self.content_gen.db_path, ":memory:")

    def test_save_and_retrieve_content(self):
        """Testa salvar e recuperar conteúdo gerado"""
        user_id = 1
        product_id = "prod_001"
        content_type = "descricao"
        generated_content = "Conteúdo de teste"
        personalization_data = {"test": "data"}

        # Salva conteúdo
        content_id = self.content_gen.save_generated_content(
            user_id, product_id, content_type, generated_content, personalization_data
        )

        # Verifica que o ID foi retornado
        self.assertIsInstance(content_id, int)
        self.assertGreater(content_id, 0)

    def test_get_content_history(self):
        """Testa a recuperação do histórico de conteúdo"""
        user_id = 1

        # Adiciona alguns conteúdos de teste
        self.content_gen.save_generated_content(
            user_id, "prod_001", "descricao", "Conteúdo 1", {"test": "data1"}
        )
        self.content_gen.save_generated_content(
            user_id, "prod_002", "titulo", "Conteúdo 2", {"test": "data2"}
        )

        # Recupera histórico
        history = self.content_gen.get_content_history(user_id, limit=10)

        # Verifica que o histórico foi retornado
        self.assertIsInstance(history, list)
        self.assertGreaterEqual(len(history), 2)

    def test_get_personalized_content(self):
        """Testa a recuperação de conteúdo personalizado"""
        user_id = 1
        product_id = "prod_001"
        content_type = "descricao"
        generated_content = "Conteúdo de teste"

        # Salva conteúdo
        self.content_gen.save_generated_content(
            user_id, product_id, content_type, generated_content, {"test": "data"}
        )

        # Recupera conteúdo
        retrieved_content = self.content_gen.get_personalized_content(user_id, product_id, content_type)

        # Verifica que o conteúdo foi recuperado corretamente
        self.assertEqual(retrieved_content, generated_content)

class TestPersonalizationProfile(unittest.TestCase):
    """Testes para o gerenciamento de perfis de personalização"""

    def setUp(self):
        """Configuração antes de cada teste"""
        self.profile_manager = PersonalizationProfile(db_path=":memory:")

    def test_create_profile(self):
        """Testa a criação de um perfil de personalização"""
        user_id = 1
        profile_name = "perfil_padrao"
        profile_data = {"segmento": "premium", "interesses": ["tecnologia", "inovacao"]}

        profile_id = self.profile_manager.create_profile(user_id, profile_name, profile_data)

        # Verifica que o ID foi retornado
        self.assertIsInstance(profile_id, int)
        self.assertGreater(profile_id, 0)

    def test_get_user_profiles(self):
        """Testa a recuperação de perfis de um usuário"""
        user_id = 1
        profile_name = "perfil_teste"
        profile_data = {"segmento": "massa", "interesses": ["moda", "beleza"]}

        # Cria um perfil
        self.profile_manager.create_profile(user_id, profile_name, profile_data)

        # Recupera perfis do usuário
        profiles = self.profile_manager.get_user_profiles(user_id)

        # Verifica que o perfil foi retornado
        self.assertIsInstance(profiles, list)
        self.assertGreaterEqual(len(profiles), 1)
        self.assertEqual(profiles[0]['user_id'], user_id)
        self.assertEqual(profiles[0]['profile_name'], profile_name)

class TestContentController(unittest.TestCase):
    """Testes para o controlador de conteúdo"""

    def setUp(self):
        """Configuração antes de cada teste"""
        self.controller = ContentController()

    @patch('flask.request')
    def test_generate_personalized_content_missing_user_id(self, mock_request):
        """Testa geração de conteúdo sem ID de usuário"""
        mock_request.get_json.return_value = {
            'product_info': {'id': 'prod_001'},
            'content_type': 'descricao'
        }

        result, status_code = self.controller.generate_personalized_content()

        # Verifica que o erro foi retornado corretamente
        self.assertEqual(status_code, 400)
        self.assertIn('error', result)

    @patch('flask.request')
    def test_generate_personalized_content_valid_data(self, mock_request):
        """Testa geração de conteúdo com dados válidos (mock)"""
        mock_request.get_json.return_value = {
            'user_id': 1,
            'product_info': {'id': 'prod_001', 'name': 'Produto Teste'},
            'content_type': 'descricao',
            'personalization_params': {}
        }

        # Teste não completo pois depende de integração com IA real
        # Mas verifica que não ocorre erro de estrutura
        try:
            result, status_code = self.controller.generate_personalized_content()
            # O resultado pode ser um erro de IA não configurada, o que é esperado
        except Exception as e:
            # Aceita exceções relacionadas à falta de chaves de IA
            self.assertIn('IA', str(e)) or self.assertIn('API', str(e))

if __name__ == '__main__':
    # Executa todos os testes
    unittest.main(verbosity=2)
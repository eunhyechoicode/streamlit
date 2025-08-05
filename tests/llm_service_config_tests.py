import unittest
from unittest.mock import patch, MagicMock
from llm_service_config import LLMConfig, LLMService, get_llm_model, get_llm, get_judge_llm


class TestLLMConfig(unittest.TestCase):
    def test_from_config_with_valid_data(self):
        test_config = {
            'llm': {
                'model': 'gpt-4',
                'temperature': 0.7
            }
        }

        config = LLMConfig.from_config(test_config)

        self.assertEqual(config.model, 'gpt-4')
        self.assertEqual(config.temperature, 0.7)

    def test_from_config_with_empty_data(self):
        with self.assertRaises(KeyError):
            LLMConfig.from_config({})

    def test_from_config_with_missing_fields(self):
        test_config = {
            'llm': {
                'model': 'gpt-4'
                # missing temperature
            }
        }

        with self.assertRaises(KeyError):
            LLMConfig.from_config(test_config)


class TestLLMService(unittest.TestCase):
    def setUp(self):
        LLMService._instance = None
        # Mock ChatOpenAI
        self.mock_chat_openai = MagicMock()
        self.mock_chat_openai.model_name = 'gpt-4'
        self.mock_chat_openai.temperature = 0.7
        self.patcher = patch('llm_service_config.ChatOpenAI', return_value=self.mock_chat_openai)
        self.mock_chat_openai_class = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_create_chat_model_with_temperature(self):
        config = LLMConfig(model='gpt-4', temperature=0.7)
        service = LLMService(config)

        chat_model = service.create_chat_model(use_temperature=True)

        self.mock_chat_openai_class.assert_called_once_with(model='gpt-4', temperature=0.7)
        self.assertEqual(chat_model.model_name, 'gpt-4')
        self.assertEqual(chat_model.temperature, 0.7)

    def test_create_chat_model_without_temperature(self):
        config = LLMConfig(model='gpt-4', temperature=0.7)
        service = LLMService(config)

        chat_model = service.create_chat_model()

        self.mock_chat_openai_class.assert_called_once_with(model='gpt-4')
        self.assertEqual(chat_model.model_name, 'gpt-4')


class TestPublicInterface(unittest.TestCase):
    def setUp(self):
        # Reset the singleton instance and clear lru_cache before each test
        LLMService._instance = None
        get_llm_model.cache_clear()

        # Mock ChatOpenAI
        self.mock_chat_openai = MagicMock()
        self.mock_chat_openai.model_name = 'gpt-4'
        self.mock_chat_openai.temperature = 0.7
        self.patcher = patch('llm_service_config.ChatOpenAI', return_value=self.mock_chat_openai)
        self.mock_chat_openai_class = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    @patch('llm_service_config.load_config')
    def test_get_llm_model_caching(self, mock_load_config):
        mock_load_config.return_value = {
            'llm': {
                'model': 'gpt-4',
                'temperature': 0.7
            }
        }

        # First call
        model1 = get_llm_model()
        # Second call
        model2 = get_llm_model()

        self.assertEqual(model1, 'gpt-4')
        self.assertEqual(model2, 'gpt-4')
        # Config should be loaded only once
        mock_load_config.assert_called_once()

    def test_integration_all_public_functions(self):
        with patch('llm_service_config.load_config') as mock_load_config:
            mock_load_config.return_value = {
                'llm': {
                    'model': 'gpt-4',
                    'temperature': 0.7
                }
            }

            # Test all public functions work together
            model = get_llm_model()
            llm = get_llm()
            judge_llm = get_judge_llm()

            self.assertEqual(model, 'gpt-4')
            self.assertEqual(llm.model_name, 'gpt-4')
            self.assertEqual(judge_llm.model_name, 'gpt-4')
            self.assertEqual(judge_llm.temperature, 0.7)
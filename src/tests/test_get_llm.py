
import unittest
from unittest.mock import patch, Mock
from langchain_openai import ChatOpenAI
from src.services.llm.get_llm import get_llm, LLM


class TestGetLLM(unittest.TestCase):

    def setUp(self):
        # Reset the singleton instance and clear lru_cache before each test
        LLM._instance = None
        LLM.get_instance.cache_clear()
        # Create a patch for ChatOpenAI
        self.chat_openai_patch = patch('src.services.llm.get_llm.ChatOpenAI')
        self.mock_chat_openai = self.chat_openai_patch.start()
        # Configure the mock to return a Mock instance that behaves like ChatOpenAI
        self.mock_chat_openai.return_value = Mock(spec=ChatOpenAI)

    def tearDown(self):
        self.chat_openai_patch.stop()

    def test_get_llm_returns_chat_openai_instance(self):
        """Test that get_llm returns a ChatOpenAI instance"""
        llm_instance = get_llm()
        self.assertTrue(isinstance(llm_instance, Mock))
        self.assertEqual(self.mock_chat_openai.call_count, 1)

    def test_get_llm_singleton_behavior(self):
        """Test that multiple calls to get_llm return the same instance"""
        first_instance = get_llm()
        second_instance = get_llm()
        self.assertIs(first_instance, second_instance)
        # Verify ChatOpenAI was instantiated only once
        self.assertEqual(self.mock_chat_openai.call_count, 1)

    def test_direct_initialization_raises_error(self):
        """Test that directly initializing LLM raises RuntimeError"""
        # First create an instance through the proper channel
        LLM.get_instance()
        # Now trying to create another instance directly should raise the error
        with self.assertRaises(RuntimeError) as context:
            LLM()
        self.assertEqual(str(context.exception), "Use get_instance() instead")

    @patch('src.services.llm.get_llm.get_llm_model')
    def test_llm_uses_configured_model(self, mock_get_model):
        """Test that LLM uses the model name from configuration"""
        expected_model = "gpt-4"
        mock_get_model.return_value = expected_model
        get_llm()
        # Verify ChatOpenAI was called with the correct model_name
        self.mock_chat_openai.assert_called_once_with(model_name=expected_model)

    def test_get_instance_returns_same_llm(self):
        """Test that LLM.get_instance() returns the same ChatOpenAI instance"""
        direct_instance = LLM.get_instance()
        get_llm_instance = get_llm()
        self.assertIs(direct_instance, get_llm_instance)
        # Verify ChatOpenAI was instantiated only once
        self.assertEqual(self.mock_chat_openai.call_count, 1)
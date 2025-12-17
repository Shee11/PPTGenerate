"""Tests for LLM client singleton and retry logic."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.utils.llm_client import get_llm_client, call_llm


class TestLLMClientSingleton:
    """Test singleton pattern for LLM client."""
    
    def test_get_llm_client_returns_singleton(self):
        """Verify get_llm_client() returns the same instance on multiple calls."""
        client1 = get_llm_client()
        client2 = get_llm_client()
        assert client1 is client2
    
    @patch.dict('os.environ', {
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com',
        'AZURE_OPENAI_API_KEY': 'test-key',
        'AZURE_OPENAI_API_VERSION': '2024-02-15-preview',
    })
    def test_client_configuration_from_env(self):
        """Verify client loads configuration from environment variables."""
        with patch('src.utils.llm_client.AzureOpenAI') as mock_azure:
            get_llm_client()
            mock_azure.assert_called_once()
            call_args = mock_azure.call_args
            assert call_args.kwargs['azure_endpoint'] == 'https://test.openai.azure.com'
            assert call_args.kwargs['api_key'] == 'test-key'
            assert call_args.kwargs['api_version'] == '2024-02-15-preview'


class TestCallLLM:
    """Test LLM call function with retry logic."""
    
    @patch('src.utils.llm_client.get_llm_client')
    def test_call_llm_success(self, mock_get_client):
        """Verify successful LLM API call returns expected response."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content='{"result": "success"}'))]
        mock_client.chat.completions.create.return_value = mock_response
        mock_get_client.return_value = mock_client
        
        result = call_llm(
            system_prompt="You are a test assistant",
            user_prompt="Test prompt",
            deployment="gpt-4-turbo",
            temperature=0.7,
            max_tokens=1000
        )
        
        assert result == '{"result": "success"}'
        mock_client.chat.completions.create.assert_called_once()
    
    @patch('src.utils.llm_client.get_llm_client')
    @patch('src.utils.llm_client.time.sleep', return_value=None)  # Skip actual sleep
    def test_call_llm_retry_on_failure(self, mock_sleep, mock_get_client):
        """Verify retry logic with exponential backoff on API failures."""
        mock_client = Mock()
        # Fail twice, then succeed
        mock_client.chat.completions.create.side_effect = [
            Exception("API Error"),
            Exception("API Error"),
            Mock(choices=[Mock(message=Mock(content='{"result": "success"}'))])
        ]
        mock_get_client.return_value = mock_client
        
        result = call_llm(
            system_prompt="Test",
            user_prompt="Test",
            deployment="gpt-4-turbo"
        )
        
        assert result == '{"result": "success"}'
        assert mock_client.chat.completions.create.call_count == 3
        assert mock_sleep.call_count == 2  # Two retries
    
    @patch('src.utils.llm_client.get_llm_client')
    @patch('src.utils.llm_client.time.sleep', return_value=None)
    def test_call_llm_max_retries_exceeded(self, mock_sleep, mock_get_client):
        """Verify exception raised when max retries exceeded."""
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_get_client.return_value = mock_client
        
        with pytest.raises(Exception, match="API Error"):
            call_llm(
                system_prompt="Test",
                user_prompt="Test",
                deployment="gpt-4-turbo",
                max_retries=2
            )
        
        assert mock_client.chat.completions.create.call_count == 3  # Initial + 2 retries
    
    @patch('src.utils.llm_client.get_llm_client')
    def test_call_llm_with_json_response_format(self, mock_get_client):
        """Verify response_format parameter is passed correctly for JSON mode."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content='{"json": "data"}'))]
        mock_client.chat.completions.create.return_value = mock_response
        mock_get_client.return_value = mock_client
        
        result = call_llm(
            system_prompt="Return JSON",
            user_prompt="Test",
            deployment="gpt-4-turbo",
            response_format="json"
        )
        
        call_args = mock_client.chat.completions.create.call_args
        assert call_args.kwargs.get('response_format') == {"type": "json_object"}

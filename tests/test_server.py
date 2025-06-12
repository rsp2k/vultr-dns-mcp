"""Tests for MCP server functionality."""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import os
from vultr_dns_mcp.server import create_mcp_server, VultrDNSServer


@pytest.mark.unit
class TestMCPServer:
    """Test MCP server creation and basic functionality."""
    
    def test_create_mcp_server_with_api_key(self):
        """Test creating MCP server with API key."""
        server = create_mcp_server("test-api-key")
        assert server is not None
        assert server.name == "vultr-dns-mcp"
    
    def test_create_mcp_server_without_api_key(self):
        """Test creating MCP server without API key raises error."""
        with pytest.raises(ValueError, match="VULTR_API_KEY must be provided"):
            create_mcp_server()
    
    @patch.dict('os.environ', {'VULTR_API_KEY': 'env-api-key'})
    def test_create_mcp_server_from_env(self):
        """Test creating MCP server with API key from environment."""
        server = create_mcp_server()
        assert server is not None
        assert server.name == "vultr-dns-mcp"
    
    def test_server_has_expected_tools(self):
        """Test that server has expected tool handlers."""
        server = create_mcp_server("test-api-key")
        
        # Check that server has proper handlers
        assert hasattr(server, '_tool_handlers') or hasattr(server, 'tool_handlers')
        assert hasattr(server, '_resource_handlers') or hasattr(server, 'resource_handlers')
    
    def test_server_info(self):
        """Test server information and metadata."""
        server = create_mcp_server("test-api-key")
        
        assert server.name == "vultr-dns-mcp"
        assert hasattr(server, 'version') or hasattr(server, '_version')


@pytest.mark.unit
class TestVultrDNSServer:
    """Test VultrDNSServer class functionality."""
    
    @pytest.fixture
    def mock_api_key(self):
        """Provide a mock API key for testing."""
        return "test-api-key-12345"
    
    def test_vultr_dns_server_creation(self, mock_api_key):
        """Test VultrDNSServer instantiation."""
        server = VultrDNSServer(mock_api_key)
        assert server.api_key == mock_api_key
        assert server.base_url == "https://api.vultr.com/v2"
    
    def test_vultr_dns_server_headers(self, mock_api_key):
        """Test that server sets correct headers."""
        server = VultrDNSServer(mock_api_key)
        expected_headers = {
            "Authorization": f"Bearer {mock_api_key}",
            "Content-Type": "application/json"
        }
        assert server.headers == expected_headers
    
    @pytest.mark.asyncio
    async def test_make_request_success(self, mock_api_key):
        """Test successful API request."""
        server = VultrDNSServer(mock_api_key)
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.status_code = 200
            mock_response.json = AsyncMock(return_value={"test": "data"})
            
            # Properly mock the async context manager
            mock_client.return_value.__aenter__ = AsyncMock(return_value=mock_client.return_value)
            mock_client.return_value.__aexit__ = AsyncMock(return_value=None)
            mock_client.return_value.request = AsyncMock(return_value=mock_response)
            
            result = await server._make_request("GET", "/test")
            assert result == {"test": "data"}
    
    @pytest.mark.asyncio
    async def test_make_request_error(self, mock_api_key):
        """Test API request with error response."""
        server = VultrDNSServer(mock_api_key)
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.status_code = 400
            mock_response.text = "Bad Request"
            
            mock_client.return_value.__aenter__ = AsyncMock(return_value=mock_client.return_value)
            mock_client.return_value.__aexit__ = AsyncMock(return_value=None)
            mock_client.return_value.request = AsyncMock(return_value=mock_response)
            
            with pytest.raises(Exception) as exc_info:
                await server._make_request("GET", "/test")
            
            assert "Bad Request" in str(exc_info.value)


@pytest.mark.integration
class TestServerIntegration:
    """Integration tests for server functionality."""
    
    def test_server_with_mock_vultr_client(self):
        """Test server creation with mocked Vultr client."""
        with patch('vultr_dns_mcp.server.VultrDNSServer') as mock_vultr:
            mock_vultr.return_value = MagicMock()
            
            server = create_mcp_server("test-api-key")
            assert server is not None
    
    def test_server_environment_integration(self):
        """Test server respects environment configuration."""
        # Test without environment variable
        if 'VULTR_API_KEY' in os.environ:
            del os.environ['VULTR_API_KEY']
        
        with pytest.raises(ValueError):
            create_mcp_server()
        
        # Test with environment variable
        os.environ['VULTR_API_KEY'] = 'test-key'
        try:
            server = create_mcp_server()
            assert server is not None
        finally:
            del os.environ['VULTR_API_KEY']


@pytest.mark.unit
def test_server_constants():
    """Test server constants and configuration."""
    server = VultrDNSServer("test-key")
    
    # Test API base URL
    assert server.base_url.startswith("https://")
    assert "vultr.com" in server.base_url
    
    # Test that headers include authorization
    assert "Authorization" in server.headers
    assert "Bearer" in server.headers["Authorization"]

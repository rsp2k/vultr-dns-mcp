"""Tests for the core VultrDNSServer functionality."""

import pytest
import httpx
from unittest.mock import AsyncMock, patch
from vultr_dns_mcp.server import VultrDNSServer


@pytest.mark.unit
class TestVultrDNSServer:
    """Test the VultrDNSServer class."""
    
    def test_server_initialization(self, mock_api_key):
        """Test server initialization."""
        server = VultrDNSServer(mock_api_key)
        assert server.api_key == mock_api_key
        assert server.headers["Authorization"] == f"Bearer {mock_api_key}"
        assert server.headers["Content-Type"] == "application/json"
        assert server.API_BASE == "https://api.vultr.com/v2"
    
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
    async def test_make_request_created(self, mock_api_key):
        """Test API request with 201 Created status."""
        server = VultrDNSServer(mock_api_key)
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.status_code = 201
            mock_response.json = AsyncMock(return_value={"created": "resource"})
            
            mock_client.return_value.__aenter__ = AsyncMock(return_value=mock_client.return_value)
            mock_client.return_value.__aexit__ = AsyncMock(return_value=None)
            mock_client.return_value.request = AsyncMock(return_value=mock_response)
            
            result = await server._make_request("POST", "/test", {"data": "value"})
            assert result == {"created": "resource"}
    
    @pytest.mark.asyncio
    async def test_make_request_no_content(self, mock_api_key):
        """Test API request with 204 No Content status."""
        server = VultrDNSServer(mock_api_key)
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.status_code = 204
            
            mock_client.return_value.__aenter__ = AsyncMock(return_value=mock_client.return_value)
            mock_client.return_value.__aexit__ = AsyncMock(return_value=None)
            mock_client.return_value.request = AsyncMock(return_value=mock_response)
            
            result = await server._make_request("DELETE", "/test")
            assert result == {}
    
    @pytest.mark.asyncio
    async def test_make_request_error_400(self, mock_api_key):
        """Test API request with 400 Bad Request error."""
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
            
            assert "Vultr API error 400: Bad Request" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_make_request_error_401(self, mock_api_key):
        """Test API request with 401 Unauthorized error."""
        server = VultrDNSServer(mock_api_key)
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.status_code = 401
            mock_response.text = "Unauthorized"
            
            mock_client.return_value.__aenter__ = AsyncMock(return_value=mock_client.return_value)
            mock_client.return_value.__aexit__ = AsyncMock(return_value=None)
            mock_client.return_value.request = AsyncMock(return_value=mock_response)
            
            with pytest.raises(Exception) as exc_info:
                await server._make_request("GET", "/test")
            
            assert "Vultr API error 401: Unauthorized" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_make_request_error_500(self, mock_api_key):
        """Test API request with 500 Internal Server Error."""
        server = VultrDNSServer(mock_api_key)
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.status_code = 500
            mock_response.text = "Internal Server Error"
            
            mock_client.return_value.__aenter__ = AsyncMock(return_value=mock_client.return_value)
            mock_client.return_value.__aexit__ = AsyncMock(return_value=None)
            mock_client.return_value.request = AsyncMock(return_value=mock_response)
            
            with pytest.raises(Exception) as exc_info:
                await server._make_request("GET", "/test")
            
            assert "Vultr API error 500: Internal Server Error" in str(exc_info.value)


@pytest.mark.unit
class TestDomainMethods:
    """Test domain management methods."""
    
    @pytest.mark.asyncio
    async def test_list_domains(self, mock_api_key):
        """Test listing domains."""
        server = VultrDNSServer(mock_api_key)
        expected_domains = [{"domain": "example.com"}]
        
        with patch.object(server, '_make_request') as mock_request:
            mock_request.return_value = {"domains": expected_domains}
            
            result = await server.list_domains()
            assert result == expected_domains
            mock_request.assert_called_once_with("GET", "/domains")
    
    @pytest.mark.asyncio
    async def test_list_domains_empty(self, mock_api_key):
        """Test listing domains when none exist."""
        server = VultrDNSServer(mock_api_key)
        
        with patch.object(server, '_make_request') as mock_request:
            mock_request.return_value = {}  # No domains key
            
            result = await server.list_domains()
            assert result == []
    
    @pytest.mark.asyncio
    async def test_get_domain(self, mock_api_key, sample_domain_data):
        """Test getting a specific domain."""
        server = VultrDNSServer(mock_api_key)
        
        with patch.object(server, '_make_request') as mock_request:
            mock_request.return_value = sample_domain_data
            
            result = await server.get_domain("example.com")
            assert result == sample_domain_data
            mock_request.assert_called_once_with("GET", "/domains/example.com")
    
    @pytest.mark.asyncio
    async def test_create_domain(self, mock_api_key):
        """Test creating a domain."""
        server = VultrDNSServer(mock_api_key)
        expected_data = {"domain": "newdomain.com", "ip": "192.168.1.100"}
        
        with patch.object(server, '_make_request') as mock_request:
            mock_request.return_value = {"domain": "newdomain.com"}
            
            result = await server.create_domain("newdomain.com", "192.168.1.100")
            assert result == {"domain": "newdomain.com"}
            mock_request.assert_called_once_with("POST", "/domains", expected_data)
    
    @pytest.mark.asyncio
    async def test_delete_domain(self, mock_api_key):
        """Test deleting a domain."""
        server = VultrDNSServer(mock_api_key)
        
        with patch.object(server, '_make_request') as mock_request:
            mock_request.return_value = {}
            
            result = await server.delete_domain("example.com")
            assert result == {}
            mock_request.assert_called_once_with("DELETE", "/domains/example.com")


@pytest.mark.unit
class TestRecordMethods:
    """Test DNS record management methods."""
    
    @pytest.mark.asyncio
    async def test_list_records(self, mock_api_key):
        """Test listing DNS records."""
        server = VultrDNSServer(mock_api_key)
        expected_records = [{"id": "rec1", "type": "A"}]
        
        with patch.object(server, '_make_request') as mock_request:
            mock_request.return_value = {"records": expected_records}
            
            result = await server.list_records("example.com")
            assert result == expected_records
            mock_request.assert_called_once_with("GET", "/domains/example.com/records")
    
    @pytest.mark.asyncio
    async def test_list_records_empty(self, mock_api_key):
        """Test listing records when none exist."""
        server = VultrDNSServer(mock_api_key)
        
        with patch.object(server, '_make_request') as mock_request:
            mock_request.return_value = {}  # No records key
            
            result = await server.list_records("example.com")
            assert result == []
    
    @pytest.mark.asyncio
    async def test_get_record(self, mock_api_key, sample_record_data):
        """Test getting a specific DNS record."""
        server = VultrDNSServer(mock_api_key)
        
        with patch.object(server, '_make_request') as mock_request:
            mock_request.return_value = sample_record_data
            
            result = await server.get_record("example.com", "record-123")
            assert result == sample_record_data
            mock_request.assert_called_once_with("GET", "/domains/example.com/records/record-123")
    
    @pytest.mark.asyncio
    async def test_create_record_minimal(self, mock_api_key):
        """Test creating a DNS record with minimal parameters."""
        server = VultrDNSServer(mock_api_key)
        expected_payload = {
            "type": "A",
            "name": "www",
            "data": "192.168.1.100"
        }
        
        with patch.object(server, '_make_request') as mock_request:
            mock_request.return_value = {"id": "new-record"}
            
            result = await server.create_record("example.com", "A", "www", "192.168.1.100")
            assert result == {"id": "new-record"}
            mock_request.assert_called_once_with("POST", "/domains/example.com/records", expected_payload)
    
    @pytest.mark.asyncio
    async def test_create_record_with_ttl(self, mock_api_key):
        """Test creating a DNS record with TTL."""
        server = VultrDNSServer(mock_api_key)
        expected_payload = {
            "type": "A",
            "name": "www",
            "data": "192.168.1.100",
            "ttl": 600
        }
        
        with patch.object(server, '_make_request') as mock_request:
            mock_request.return_value = {"id": "new-record"}
            
            result = await server.create_record("example.com", "A", "www", "192.168.1.100", ttl=600)
            assert result == {"id": "new-record"}
            mock_request.assert_called_once_with("POST", "/domains/example.com/records", expected_payload)
    
    @pytest.mark.asyncio
    async def test_create_record_with_priority(self, mock_api_key):
        """Test creating a DNS record with priority."""
        server = VultrDNSServer(mock_api_key)
        expected_payload = {
            "type": "MX",
            "name": "@",
            "data": "mail.example.com",
            "priority": 10
        }
        
        with patch.object(server, '_make_request') as mock_request:
            mock_request.return_value = {"id": "new-record"}
            
            result = await server.create_record("example.com", "MX", "@", "mail.example.com", priority=10)
            assert result == {"id": "new-record"}
            mock_request.assert_called_once_with("POST", "/domains/example.com/records", expected_payload)
    
    @pytest.mark.asyncio
    async def test_create_record_full_parameters(self, mock_api_key):
        """Test creating a DNS record with all parameters."""
        server = VultrDNSServer(mock_api_key)
        expected_payload = {
            "type": "MX",
            "name": "@",
            "data": "mail.example.com",
            "ttl": 300,
            "priority": 10
        }
        
        with patch.object(server, '_make_request') as mock_request:
            mock_request.return_value = {"id": "new-record"}
            
            result = await server.create_record(
                "example.com", "MX", "@", "mail.example.com", ttl=300, priority=10
            )
            assert result == {"id": "new-record"}
            mock_request.assert_called_once_with("POST", "/domains/example.com/records", expected_payload)
    
    @pytest.mark.asyncio
    async def test_update_record(self, mock_api_key):
        """Test updating a DNS record."""
        server = VultrDNSServer(mock_api_key)
        expected_payload = {
            "type": "A",
            "name": "www",
            "data": "192.168.1.200",
            "ttl": 600
        }
        
        with patch.object(server, '_make_request') as mock_request:
            mock_request.return_value = {"id": "record-123"}
            
            result = await server.update_record(
                "example.com", "record-123", "A", "www", "192.168.1.200", ttl=600
            )
            assert result == {"id": "record-123"}
            mock_request.assert_called_once_with("PATCH", "/domains/example.com/records/record-123", expected_payload)
    
    @pytest.mark.asyncio
    async def test_delete_record(self, mock_api_key):
        """Test deleting a DNS record."""
        server = VultrDNSServer(mock_api_key)
        
        with patch.object(server, '_make_request') as mock_request:
            mock_request.return_value = {}
            
            result = await server.delete_record("example.com", "record-123")
            assert result == {}
            mock_request.assert_called_once_with("DELETE", "/domains/example.com/records/record-123")


@pytest.mark.integration
class TestServerIntegration:
    """Integration tests for the VultrDNSServer."""
    
    @pytest.mark.asyncio
    async def test_complete_domain_workflow(self, mock_api_key):
        """Test a complete domain management workflow."""
        server = VultrDNSServer(mock_api_key)
        
        with patch.object(server, '_make_request') as mock_request:
            # Configure mock responses for the workflow
            mock_request.side_effect = [
                {"domains": []},  # Initial empty list
                {"domain": "newdomain.com"},  # Create domain
                {"domains": [{"domain": "newdomain.com"}]},  # List with new domain
                {"domain": "newdomain.com", "records": []},  # Get domain
                {}  # Delete domain
            ]
            
            # 1. List domains (empty)
            domains = await server.list_domains()
            assert domains == []
            
            # 2. Create a domain
            create_result = await server.create_domain("newdomain.com", "192.168.1.100")
            assert create_result["domain"] == "newdomain.com"
            
            # 3. List domains (should have one)
            domains = await server.list_domains()
            assert len(domains) == 1
            
            # 4. Get domain details
            domain_info = await server.get_domain("newdomain.com")
            assert domain_info["domain"] == "newdomain.com"
            
            # 5. Delete domain
            delete_result = await server.delete_domain("newdomain.com")
            assert delete_result == {}
            
            # Verify all expected API calls were made
            assert mock_request.call_count == 5
    
    @pytest.mark.asyncio
    async def test_complete_record_workflow(self, mock_api_key):
        """Test a complete record management workflow."""
        server = VultrDNSServer(mock_api_key)
        
        with patch.object(server, '_make_request') as mock_request:
            # Configure mock responses
            mock_request.side_effect = [
                {"records": []},  # Initial empty list
                {"id": "new-record", "type": "A"},  # Create record
                {"records": [{"id": "new-record", "type": "A"}]},  # List with new record
                {"id": "new-record", "type": "A", "data": "192.168.1.200"},  # Update record
                {}  # Delete record
            ]
            
            # 1. List records (empty)
            records = await server.list_records("example.com")
            assert records == []
            
            # 2. Create a record
            create_result = await server.create_record("example.com", "A", "www", "192.168.1.100")
            assert create_result["id"] == "new-record"
            
            # 3. List records (should have one)
            records = await server.list_records("example.com")
            assert len(records) == 1
            
            # 4. Update the record
            update_result = await server.update_record(
                "example.com", "new-record", "A", "www", "192.168.1.200"
            )
            assert update_result["data"] == "192.168.1.200"
            
            # 5. Delete the record
            delete_result = await server.delete_record("example.com", "new-record")
            assert delete_result == {}
            
            # Verify all expected API calls were made
            assert mock_request.call_count == 5


@pytest.mark.slow
class TestErrorScenarios:
    """Test various error scenarios."""
    
    @pytest.mark.asyncio
    async def test_network_timeout(self, mock_api_key):
        """Test handling of network timeout."""
        server = VultrDNSServer(mock_api_key)
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.request.side_effect = httpx.TimeoutException("Timeout")
            
            with pytest.raises(httpx.TimeoutException):
                await server._make_request("GET", "/domains")
    
    @pytest.mark.asyncio
    async def test_connection_error(self, mock_api_key):
        """Test handling of connection error."""
        server = VultrDNSServer(mock_api_key)
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.request.side_effect = httpx.ConnectError("Connection failed")
            
            with pytest.raises(httpx.ConnectError):
                await server._make_request("GET", "/domains")
    
    @pytest.mark.asyncio
    async def test_rate_limit_error(self, mock_api_key):
        """Test handling of rate limit error."""
        server = VultrDNSServer(mock_api_key)
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.status_code = 429
            mock_response.text = "Rate limit exceeded"
            
            mock_client.return_value.__aenter__ = AsyncMock(return_value=mock_client.return_value)
            mock_client.return_value.__aexit__ = AsyncMock(return_value=None)
            mock_client.return_value.request = AsyncMock(return_value=mock_response)
            
            with pytest.raises(Exception) as exc_info:
                await server._make_request("GET", "/domains")
            
            assert "Rate limit exceeded" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main([__file__])

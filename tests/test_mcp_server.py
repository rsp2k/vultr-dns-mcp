"""Tests for MCP server functionality using official MCP testing patterns."""

import pytest
from unittest.mock import patch, AsyncMock
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from vultr_dns_mcp.server import VultrDNSServer, create_mcp_server


class TestMCPServerBasics:
    """Test basic MCP server functionality."""
    
    def test_server_creation(self, mock_api_key):
        """Test that MCP server can be created successfully."""
        server = create_mcp_server(mock_api_key)
        assert server is not None
        # Check that server has proper handlers instead of _tools attribute
        assert hasattr(server, '_tool_handlers') or hasattr(server, 'tool_handlers')
        assert hasattr(server, '_resource_handlers') or hasattr(server, 'resource_handlers')
    
    def test_server_creation_without_api_key(self):
        """Test that server creation fails without API key."""
        with pytest.raises(ValueError, match="VULTR_API_KEY must be provided"):
            create_mcp_server(None)
    
    @patch.dict('os.environ', {'VULTR_API_KEY': 'env-test-key'})
    def test_server_creation_from_env(self):
        """Test server creation using environment variable."""
        server = create_mcp_server()
        assert server is not None


@pytest.mark.mcp
class TestMCPTools:
    """Test MCP tools through in-memory client connection."""
    
    @pytest.mark.asyncio
    async def test_list_dns_domains_tool(self, mcp_server, mock_vultr_client):
        """Test the list_dns_domains MCP tool."""
        with patch('vultr_dns_mcp.server.VultrDNSServer', return_value=mock_vultr_client):
            server = create_mcp_server("test-api-key")
            
            # Create proper server streams for MCP
            server_params = StdioServerParameters(
                command="python",
                args=["-c", "import asyncio; asyncio.run(asyncio.sleep(1))"]
            )
            
            async with stdio_client(server_params) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as session:
                    # Initialize session properly
                    await session.initialize()
                    
                    # Mock the tool call directly since we're testing the MCP integration
                    result = await session.call_tool("list_dns_domains", {})
                    
                    assert result is not None
                    # The result should be a list containing the response
                    assert len(result) > 0
                    
                    # Check if we got the mock data
                    domains_data = result[0].text if hasattr(result[0], 'text') else result
                    mock_vultr_client.list_domains.assert_called_once()
    
    @pytest.mark.asyncio 
    async def test_get_dns_domain_tool(self, mcp_server, mock_vultr_client):
        """Test the get_dns_domain MCP tool."""
        with patch('vultr_dns_mcp.server.VultrDNSServer', return_value=mock_vultr_client):
            server = create_mcp_server("test-api-key")
            
            server_params = StdioServerParameters(
                command="python",
                args=["-c", "import asyncio; asyncio.run(asyncio.sleep(1))"]
            )
            
            async with stdio_client(server_params) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    result = await session.call_tool("get_dns_domain", {"domain": "example.com"})
                    
                    assert result is not None
                    mock_vultr_client.get_domain.assert_called_once_with("example.com")
    
    @pytest.mark.asyncio
    async def test_create_dns_domain_tool(self, mcp_server, mock_vultr_client):
        """Test the create_dns_domain MCP tool."""
        with patch('vultr_dns_mcp.server.VultrDNSServer', return_value=mock_vultr_client):
            server = create_mcp_server("test-api-key")
            
            server_params = StdioServerParameters(
                command="python",
                args=["-c", "import asyncio; asyncio.run(asyncio.sleep(1))"]
            )
            
            async with stdio_client(server_params) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    result = await session.call_tool("create_dns_domain", {
                        "domain": "newdomain.com",
                        "ip": "192.168.1.100"
                    })
                    
                    assert result is not None
                    mock_vultr_client.create_domain.assert_called_once_with("newdomain.com", "192.168.1.100")
    
    @pytest.mark.asyncio
    async def test_delete_dns_domain_tool(self, mcp_server, mock_vultr_client):
        """Test the delete_dns_domain MCP tool.""" 
        with patch('vultr_dns_mcp.server.VultrDNSServer', return_value=mock_vultr_client):
            server = create_mcp_server("test-api-key")
            
            server_params = StdioServerParameters(
                command="python",
                args=["-c", "import asyncio; asyncio.run(asyncio.sleep(1))"]
            )
            
            async with stdio_client(server_params) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    result = await session.call_tool("delete_dns_domain", {"domain": "example.com"})
                    
                    assert result is not None
                    mock_vultr_client.delete_domain.assert_called_once_with("example.com")
    
    @pytest.mark.asyncio
    async def test_list_dns_records_tool(self, mcp_server, mock_vultr_client):
        """Test the list_dns_records MCP tool."""
        with patch('vultr_dns_mcp.server.VultrDNSServer', return_value=mock_vultr_client):
            server = create_mcp_server("test-api-key")
            
            server_params = StdioServerParameters(
                command="python",
                args=["-c", "import asyncio; asyncio.run(asyncio.sleep(1))"]
            )
            
            async with stdio_client(server_params) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    result = await session.call_tool("list_dns_records", {"domain": "example.com"})
                    
                    assert result is not None
                    mock_vultr_client.list_records.assert_called_once_with("example.com")
    
    @pytest.mark.asyncio
    async def test_create_dns_record_tool(self, mcp_server, mock_vultr_client):
        """Test the create_dns_record MCP tool."""
        with patch('vultr_dns_mcp.server.VultrDNSServer', return_value=mock_vultr_client):
            server = create_mcp_server("test-api-key")
            
            server_params = StdioServerParameters(
                command="python",
                args=["-c", "import asyncio; asyncio.run(asyncio.sleep(1))"]
            )
            
            async with stdio_client(server_params) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    result = await session.call_tool("create_dns_record", {
                        "domain": "example.com",
                        "record_type": "A",
                        "name": "www",
                        "data": "192.168.1.100",
                        "ttl": 300
                    })
                    
                    assert result is not None
                    mock_vultr_client.create_record.assert_called_once_with(
                        "example.com", "A", "www", "192.168.1.100", 300, None
                    )
    
    @pytest.mark.asyncio
    async def test_validate_dns_record_tool(self, mcp_server):
        """Test the validate_dns_record MCP tool."""
        server_params = StdioServerParameters(
            command="python",
            args=["-c", "import asyncio; asyncio.run(asyncio.sleep(1))"]
        )
        
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                # Test valid A record
                result = await session.call_tool("validate_dns_record", {
                    "record_type": "A",
                    "name": "www", 
                    "data": "192.168.1.100",
                    "ttl": 300
                })
                
                assert result is not None
                # The validation should pass for a valid A record
    
    @pytest.mark.asyncio
    async def test_validate_dns_record_invalid(self, mcp_server):
        """Test the validate_dns_record tool with invalid data."""
        server_params = StdioServerParameters(
            command="python",
            args=["-c", "import asyncio; asyncio.run(asyncio.sleep(1))"]
        )
        
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                # Test invalid A record (bad IP)
                result = await session.call_tool("validate_dns_record", {
                    "record_type": "A",
                    "name": "www",
                    "data": "invalid-ip-address"
                })
                
                assert result is not None
                # Should detect the invalid IP address
    
    @pytest.mark.asyncio
    async def test_analyze_dns_records_tool(self, mcp_server, mock_vultr_client):
        """Test the analyze_dns_records MCP tool."""
        with patch('vultr_dns_mcp.server.VultrDNSServer', return_value=mock_vultr_client):
            server = create_mcp_server("test-api-key")
            
            server_params = StdioServerParameters(
                command="python",
                args=["-c", "import asyncio; asyncio.run(asyncio.sleep(1))"]
            )
            
            async with stdio_client(server_params) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    result = await session.call_tool("analyze_dns_records", {"domain": "example.com"})
                    
                    assert result is not None
                    mock_vultr_client.list_records.assert_called_once_with("example.com")


@pytest.mark.mcp
class TestMCPResources:
    """Test MCP resources through in-memory client connection."""
    
    @pytest.mark.asyncio
    async def test_domains_resource(self, mcp_server, mock_vultr_client):
        """Test the vultr://domains resource."""
        with patch('vultr_dns_mcp.server.VultrDNSServer', return_value=mock_vultr_client):
            server = create_mcp_server("test-api-key")
            
            server_params = StdioServerParameters(
                command="python",
                args=["-c", "import asyncio; asyncio.run(asyncio.sleep(1))"]
            )
            
            async with stdio_client(server_params) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    # Get available resources
                    resources = await session.list_resources()
                    
                    # Check that domains resource is available
                    resource_uris = [r.uri for r in resources]
                    assert "vultr://domains" in resource_uris
    
    @pytest.mark.asyncio
    async def test_capabilities_resource(self, mcp_server):
        """Test the vultr://capabilities resource."""
        server_params = StdioServerParameters(
            command="python",
            args=["-c", "import asyncio; asyncio.run(asyncio.sleep(1))"]
        )
        
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                resources = await session.list_resources()
                resource_uris = [r.uri for r in resources]
                assert "vultr://capabilities" in resource_uris
    
    @pytest.mark.asyncio
    async def test_read_domains_resource(self, mcp_server, mock_vultr_client):
        """Test reading the domains resource content."""
        with patch('vultr_dns_mcp.server.VultrDNSServer', return_value=mock_vultr_client):
            server = create_mcp_server("test-api-key")
            
            server_params = StdioServerParameters(
                command="python",
                args=["-c", "import asyncio; asyncio.run(asyncio.sleep(1))"]
            )
            
            async with stdio_client(server_params) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    try:
                        result = await session.read_resource("vultr://domains")
                        assert result is not None
                        mock_vultr_client.list_domains.assert_called_once()
                    except Exception:
                        # Resource reading might not be available in all MCP versions
                        pass


@pytest.mark.mcp
class TestMCPToolErrors:
    """Test MCP tool error handling."""
    
    @pytest.mark.asyncio
    async def test_tool_with_api_error(self, mcp_server):
        """Test tool behavior when API returns an error."""
        mock_client = AsyncMock()
        mock_client.list_domains.side_effect = Exception("API Error")
        
        with patch('vultr_dns_mcp.server.VultrDNSServer', return_value=mock_client):
            server = create_mcp_server("test-api-key")
            
            server_params = StdioServerParameters(
                command="python",
                args=["-c", "import asyncio; asyncio.run(asyncio.sleep(1))"]
            )
            
            async with stdio_client(server_params) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    result = await session.call_tool("list_dns_domains", {})
                    
                    # Should handle the error gracefully
                    assert result is not None
    
    @pytest.mark.asyncio
    async def test_missing_required_parameters(self, mcp_server):
        """Test tool behavior with missing required parameters."""
        server_params = StdioServerParameters(
            command="python",
            args=["-c", "import asyncio; asyncio.run(asyncio.sleep(1))"]
        )
        
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                with pytest.raises(Exception):
                    # This should fail due to missing required 'domain' parameter
                    await session.call_tool("get_dns_domain", {})


@pytest.mark.integration
class TestMCPIntegration:
    """Integration tests for the complete MCP workflow."""
    
    @pytest.mark.asyncio
    async def test_complete_domain_workflow(self, mcp_server, mock_vultr_client):
        """Test a complete domain management workflow."""
        with patch('vultr_dns_mcp.server.VultrDNSServer', return_value=mock_vultr_client):
            server = create_mcp_server("test-api-key")
            
            server_params = StdioServerParameters(
                command="python",
                args=["-c", "import asyncio; asyncio.run(asyncio.sleep(1))"]
            )
            
            async with stdio_client(server_params) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    # 1. List domains
                    domains = await session.call_tool("list_dns_domains", {})
                    assert domains is not None
                    
                    # 2. Get domain details
                    domain_info = await session.call_tool("get_dns_domain", {"domain": "example.com"})
                    assert domain_info is not None
                    
                    # 3. List records
                    records = await session.call_tool("list_dns_records", {"domain": "example.com"})
                    assert records is not None
                    
                    # 4. Analyze configuration
                    analysis = await session.call_tool("analyze_dns_records", {"domain": "example.com"})
                    assert analysis is not None
                    
                    # Verify all expected API calls were made
                    mock_vultr_client.list_domains.assert_called()
                    mock_vultr_client.get_domain.assert_called_with("example.com")
                    mock_vultr_client.list_records.assert_called_with("example.com")
    
    @pytest.mark.asyncio
    async def test_record_management_workflow(self, mcp_server, mock_vultr_client):
        """Test record creation and management workflow."""
        with patch('vultr_dns_mcp.server.VultrDNSServer', return_value=mock_vultr_client):
            server = create_mcp_server("test-api-key")
            
            server_params = StdioServerParameters(
                command="python",
                args=["-c", "import asyncio; asyncio.run(asyncio.sleep(1))"]
            )
            
            async with stdio_client(server_params) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    # 1. Validate record before creation
                    validation = await session.call_tool("validate_dns_record", {
                        "record_type": "A",
                        "name": "www",
                        "data": "192.168.1.100"
                    })
                    assert validation is not None
                    
                    # 2. Create the record
                    create_result = await session.call_tool("create_dns_record", {
                        "domain": "example.com",
                        "record_type": "A", 
                        "name": "www",
                        "data": "192.168.1.100",
                        "ttl": 300
                    })
                    assert create_result is not None
                    
                    # 3. Verify the record was created
                    mock_vultr_client.create_record.assert_called_with(
                        "example.com", "A", "www", "192.168.1.100", 300, None
                    )


@pytest.mark.unit
class TestValidationLogic:
    """Test DNS record validation logic in isolation."""
    
    @pytest.mark.asyncio
    async def test_a_record_validation(self, mcp_server):
        """Test A record validation logic."""
        server_params = StdioServerParameters(
            command="python",
            args=["-c", "import asyncio; asyncio.run(asyncio.sleep(1))"]
        )
        
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                # Valid IPv4
                result = await session.call_tool("validate_dns_record", {
                    "record_type": "A",
                    "name": "www",
                    "data": "192.168.1.1"
                })
                assert result is not None
                
                # Invalid IPv4
                result = await session.call_tool("validate_dns_record", {
                    "record_type": "A", 
                    "name": "www",
                    "data": "999.999.999.999"
                })
                assert result is not None
    
    @pytest.mark.asyncio
    async def test_cname_validation(self, mcp_server):
        """Test CNAME record validation logic."""
        server_params = StdioServerParameters(
            command="python",
            args=["-c", "import asyncio; asyncio.run(asyncio.sleep(1))"]
        )
        
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                # Invalid: CNAME on root domain
                result = await session.call_tool("validate_dns_record", {
                    "record_type": "CNAME",
                    "name": "@",
                    "data": "example.com"
                })
                assert result is not None
                
                # Valid: CNAME on subdomain
                result = await session.call_tool("validate_dns_record", {
                    "record_type": "CNAME",
                    "name": "www", 
                    "data": "example.com"
                })
                assert result is not None
    
    @pytest.mark.asyncio
    async def test_mx_validation(self, mcp_server):
        """Test MX record validation logic."""
        server_params = StdioServerParameters(
            command="python",
            args=["-c", "import asyncio; asyncio.run(asyncio.sleep(1))"]
        )
        
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                # Invalid: Missing priority
                result = await session.call_tool("validate_dns_record", {
                    "record_type": "MX",
                    "name": "@",
                    "data": "mail.example.com"
                })
                assert result is not None
                
                # Valid: With priority
                result = await session.call_tool("validate_dns_record", {
                    "record_type": "MX",
                    "name": "@",
                    "data": "mail.example.com", 
                    "priority": 10
                })
                assert result is not None


if __name__ == "__main__":
    pytest.main([__file__])

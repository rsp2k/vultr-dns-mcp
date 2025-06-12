"""Basic package validation tests."""

from pathlib import Path

import pytest


def test_package_can_be_imported():
    """Test that the main package can be imported."""
    import vultr_dns_mcp

    assert vultr_dns_mcp is not None


def test_package_has_version():
    """Test that package has a version attribute."""
    import vultr_dns_mcp

    assert hasattr(vultr_dns_mcp, "__version__")
    assert vultr_dns_mcp.__version__ is not None


def test_server_module_exists():
    """Test that server module can be imported."""
    from vultr_dns_mcp import server

    assert server is not None


def test_client_module_exists():
    """Test that client module can be imported."""
    from vultr_dns_mcp import client

    assert client is not None


def test_cli_module_exists():
    """Test that CLI module can be imported."""
    from vultr_dns_mcp import cli

    assert cli is not None


@pytest.mark.unit
def test_create_mcp_server():
    """Test creating MCP server with API key."""
    from vultr_dns_mcp.server import create_mcp_server

    server = create_mcp_server("test-api-key-for-testing")
    assert server is not None

    # Check that server has the correct attributes based on MCP library version
    # The server should have either handlers or decorated functions
    assert hasattr(server, "name")
    assert server.name == "vultr-dns-mcp"
    
    # Check for handler methods or attributes (flexible for different MCP versions)
    has_handlers = (
        hasattr(server, "_handlers") or 
        hasattr(server, "handlers") or
        hasattr(server, "_tool_handlers") or
        hasattr(server, "tool_handlers") or
        hasattr(server, "_tools") or
        hasattr(server, "tools") or
        hasattr(server, "_list_tools") or
        hasattr(server, "list_tools")
    )
    
    has_resources = (
        hasattr(server, "_resource_handlers") or
        hasattr(server, "resource_handlers") or
        hasattr(server, "_resources") or
        hasattr(server, "resources") or
        hasattr(server, "_list_resources") or
        hasattr(server, "list_resources")
    )
    
    # At least one of these should be true for a properly configured MCP server
    assert has_handlers or has_resources, "Server should have tool or resource handlers"


@pytest.mark.unit
def test_create_mcp_server_without_api_key():
    """Test that server creation fails without API key."""
    from vultr_dns_mcp.server import create_mcp_server

    with pytest.raises(ValueError, match="VULTR_API_KEY must be provided"):
        create_mcp_server()


def test_cli_entry_points():
    """Test that CLI entry points are properly configured."""
    from vultr_dns_mcp import cli

    # Test that main functions exist
    assert hasattr(cli, "main")
    assert callable(cli.main)

    # Test server command exists
    assert hasattr(cli, "server_command")
    assert callable(cli.server_command)


@pytest.mark.unit
def test_vultr_dns_server_creation():
    """Test VultrDNSServer can be created."""
    from vultr_dns_mcp.server import VultrDNSServer

    server = VultrDNSServer("test-api-key")
    assert server is not None
    assert server.api_key == "test-api-key"


def test_package_structure():
    """Test that package has expected structure."""
    import vultr_dns_mcp

    package_path = Path(vultr_dns_mcp.__file__).parent

    # Check that essential files exist
    assert (package_path / "__init__.py").exists()
    assert (package_path / "server.py").exists()
    assert (package_path / "client.py").exists()
    assert (package_path / "cli.py").exists()
    assert (package_path / "py.typed").exists()

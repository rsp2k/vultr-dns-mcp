"""Pytest configuration and shared fixtures."""

import pytest
import asyncio
import os
from unittest.mock import AsyncMock, MagicMock
from pathlib import Path


@pytest.fixture
def mock_api_key():
    """Provide a mock API key for testing."""
    return "test-api-key-12345"


@pytest.fixture
def mock_vultr_client():
    """Provide a mock VultrDNSServer client."""
    client = MagicMock()
    
    # Mock async methods to return AsyncMock
    client.list_domains = AsyncMock(return_value={
        "domains": [
            {"domain": "example.com", "status": "active"},
            {"domain": "test.com", "status": "active"}
        ]
    })
    
    client.get_domain = AsyncMock(return_value={
        "domain": {"domain": "example.com", "status": "active"}
    })
    
    client.create_domain = AsyncMock(return_value={
        "domain": {"domain": "newdomain.com", "status": "active"}
    })
    
    client.delete_domain = AsyncMock(return_value={})
    
    client.list_records = AsyncMock(return_value={
        "records": [
            {
                "id": "123",
                "type": "A",
                "name": "www",
                "data": "192.168.1.1",
                "ttl": 300
            }
        ]
    })
    
    client.create_record = AsyncMock(return_value={
        "record": {
            "id": "456",
            "type": "A", 
            "name": "www",
            "data": "192.168.1.100",
            "ttl": 300
        }
    })
    
    client.update_record = AsyncMock(return_value={
        "record": {
            "id": "123",
            "type": "A",
            "name": "www", 
            "data": "192.168.1.200",
            "ttl": 300
        }
    })
    
    client.delete_record = AsyncMock(return_value={})
    
    return client


@pytest.fixture
def mcp_server(mock_api_key):
    """Provide an MCP server instance for testing."""
    from vultr_dns_mcp.server import create_mcp_server
    return create_mcp_server(mock_api_key)


@pytest.fixture
def clean_environment():
    """Clean environment variables for testing."""
    original_api_key = os.environ.get('VULTR_API_KEY')
    
    # Clean up before test
    if 'VULTR_API_KEY' in os.environ:
        del os.environ['VULTR_API_KEY']
    
    yield
    
    # Restore after test
    if original_api_key:
        os.environ['VULTR_API_KEY'] = original_api_key
    elif 'VULTR_API_KEY' in os.environ:
        del os.environ['VULTR_API_KEY']


@pytest.fixture
def temp_config_dir(tmp_path):
    """Provide a temporary directory for configuration files."""
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    return config_dir


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_httpx_response():
    """Provide a mock httpx response for testing."""
    response = MagicMock()
    response.status_code = 200
    response.json = MagicMock(return_value={"success": True})
    response.text = "OK"
    return response


@pytest.fixture
def sample_dns_records():
    """Provide sample DNS records for testing."""
    return [
        {
            "id": "record-1",
            "type": "A",
            "name": "@",
            "data": "192.168.1.1",
            "ttl": 300,
            "priority": None
        },
        {
            "id": "record-2", 
            "type": "A",
            "name": "www",
            "data": "192.168.1.1",
            "ttl": 300,
            "priority": None
        },
        {
            "id": "record-3",
            "type": "MX",
            "name": "@",
            "data": "mail.example.com",
            "ttl": 3600,
            "priority": 10
        },
        {
            "id": "record-4",
            "type": "CNAME",
            "name": "blog",
            "data": "example.com",
            "ttl": 300,
            "priority": None
        }
    ]


@pytest.fixture
def sample_domains():
    """Provide sample domains for testing."""
    return [
        {
            "domain": "example.com",
            "date_created": "2023-01-01T00:00:00+00:00",
            "dns_sec": "disabled"
        },
        {
            "domain": "test.com",
            "date_created": "2023-01-02T00:00:00+00:00", 
            "dns_sec": "enabled"
        }
    ]


# Configure pytest markers
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: Unit tests for individual components"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests requiring external services"
    )
    config.addinivalue_line(
        "markers", "mcp: MCP protocol specific tests"
    )
    config.addinivalue_line(
        "markers", "slow: Tests that take a long time to run"
    )
    config.addinivalue_line(
        "markers", "network: Tests that require network access"
    )
    config.addinivalue_line(
        "markers", "api: Tests that interact with the Vultr API"
    )
    config.addinivalue_line(
        "markers", "cli: Tests for command-line interface"
    )


# Pytest collection hooks
def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers and skip conditions."""
    
    # Add slow marker to async tests by default
    for item in items:
        if asyncio.iscoroutinefunction(item.function):
            item.add_marker(pytest.mark.slow)
        
        # Add markers based on test name patterns
        if "test_cli" in item.name or "cli" in str(item.fspath):
            item.add_marker(pytest.mark.cli)
        
        if "integration" in item.name:
            item.add_marker(pytest.mark.integration)
        
        if "mcp" in item.name:
            item.add_marker(pytest.mark.mcp)
        
        if "api" in item.name or "vultr" in item.name:
            item.add_marker(pytest.mark.api)


# Async test configuration
@pytest.fixture(autouse=True)
def setup_asyncio():
    """Setup asyncio for tests."""
    # Configure asyncio for tests
    asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())

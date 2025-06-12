# Tests for vultr-dns-mcp

This directory contains comprehensive tests for the vultr-dns-mcp package.

## Test Structure

### Test Files

- `test_package_validation.py` - Basic package validation and import tests
- `test_server.py` - Server functionality and MCP integration tests  
- `conftest.py` - Shared fixtures and pytest configuration
- `__init__.py` - Package initialization

### Test Categories

Tests are organized using pytest markers:

- `@pytest.mark.unit` - Unit tests for individual components
- `@pytest.mark.integration` - Integration tests requiring external services
- `@pytest.mark.mcp` - MCP protocol specific tests
- `@pytest.mark.cli` - Command-line interface tests
- `@pytest.mark.api` - Tests that interact with the Vultr API
- `@pytest.mark.slow` - Tests that take a long time to run
- `@pytest.mark.network` - Tests requiring network access

## Running Tests

### Run All Tests
```bash
pytest tests/ -v
```

### Run with Coverage
```bash
pytest tests/ -v --cov=src/vultr_dns_mcp --cov-report=term-missing
```

### Run Specific Categories
```bash
# Unit tests only
pytest tests/ -v -m "unit"

# Integration tests only  
pytest tests/ -v -m "integration"

# CLI tests only
pytest tests/ -v -m "cli"

# MCP protocol tests only
pytest tests/ -v -m "mcp"
```

### Run Specific Files
```bash
# Package validation tests
pytest tests/test_package_validation.py -v

# Server tests
pytest tests/test_server.py -v

```

## Test Configuration

The tests are configured via `pyproject.toml` with:

- Coverage reporting (minimum 80% required)
- Async test support
- Proper test discovery
- Quality gates and exclusions

## Fixtures

Common fixtures are provided in `conftest.py`:

- `mock_api_key` - Mock API key for testing
- `mock_vultr_client` - Mock Vultr DNS client with API responses
- `mcp_server` - MCP server instance for testing
- `clean_environment` - Environment cleanup for isolated tests
- `sample_dns_records` - Sample DNS record data
- `sample_domains` - Sample domain data

## Test Coverage

The test suite covers:

✅ Package imports and structure  
✅ MCP server creation and configuration  
✅ VultrDNSServer client functionality  
✅ API request handling and error cases  
✅ CLI command execution and help  
✅ Environment variable handling  
✅ Error handling and validation  
✅ Async functionality with proper mocking  

## Adding New Tests

When adding new tests:

1. Use appropriate markers (`@pytest.mark.unit`, etc.)
2. Follow the existing naming conventions
3. Add proper docstrings
4. Use fixtures from `conftest.py` when possible
5. Mock external dependencies (httpx, MCP clients, etc.)

## CI Integration

These tests are automatically run in GitHub Actions with:

- Matrix testing across Python 3.10, 3.11, 3.12
- Coverage reporting with quality gates
- Test categorization and parallel execution
- Proper async test handling

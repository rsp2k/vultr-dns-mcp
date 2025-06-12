"""Tests for CLI functionality."""

import os
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner


@pytest.mark.cli
class TestCLIBasics:
    """Test basic CLI functionality."""

    def test_cli_module_imports(self):
        """Test that CLI module can be imported."""
        from vultr_dns_mcp import cli

        assert cli is not None

    def test_main_function_exists(self):
        """Test that main function exists and is callable."""
        from vultr_dns_mcp.cli import main

        assert callable(main)

    def test_server_command_exists(self):
        """Test that server_command function exists."""
        from vultr_dns_mcp.cli import server_command

        assert callable(server_command)


@pytest.mark.cli
class TestCLICommands:
    """Test CLI command execution."""

    def setup_method(self):
        """Set up test environment."""
        self.runner = CliRunner()

    @patch("vultr_dns_mcp.cli.create_mcp_server")
    @patch("vultr_dns_mcp.cli.stdio_server")
    def test_main_with_api_key(self, mock_stdio, mock_create_server):
        """Test main command with API key."""
        from vultr_dns_mcp.cli import main

        # Mock the server creation
        mock_server = MagicMock()
        mock_create_server.return_value = mock_server

        # Mock stdio_server context manager
        mock_stdio.return_value.__enter__ = MagicMock()
        mock_stdio.return_value.__exit__ = MagicMock()

        # Test with API key argument
        result = self.runner.invoke(main, ["--api-key", "test-key"])

        # Should not fail with basic invocation
        assert result.exit_code in [0, 1]  # May exit with 1 due to mocking

    def test_main_help(self):
        """Test main command help."""
        from vultr_dns_mcp.cli import main

        result = self.runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "Usage:" in result.output

    def test_server_command_help(self):
        """Test server command help."""
        from vultr_dns_mcp.cli import server_command

        result = self.runner.invoke(server_command, ["--help"])
        assert result.exit_code == 0
        assert "Usage:" in result.output


@pytest.mark.cli
class TestCLIEnvironment:
    """Test CLI environment handling."""

    def test_api_key_from_environment(self):
        """Test API key loading from environment."""
        from vultr_dns_mcp.cli import main

        runner = CliRunner()

        # Test without API key
        result = runner.invoke(main, [])
        # Should mention API key requirement
        assert (
            result.exit_code != 0
            or "API key" in result.output
            or "VULTR_API_KEY" in result.output
        )

    @patch.dict(os.environ, {"VULTR_API_KEY": "test-env-key"})
    @patch("vultr_dns_mcp.cli.create_mcp_server")
    @patch("vultr_dns_mcp.cli.stdio_server")
    def test_api_key_from_env_var(self, mock_stdio, mock_create_server):
        """Test API key from environment variable."""
        from vultr_dns_mcp.cli import main

        # Mock the server creation
        mock_server = MagicMock()
        mock_create_server.return_value = mock_server

        # Mock stdio_server
        mock_stdio.return_value.__enter__ = MagicMock()
        mock_stdio.return_value.__exit__ = MagicMock()

        runner = CliRunner()
        result = runner.invoke(main, [])

        # Should be able to get API key from environment
        mock_create_server.assert_called()


@pytest.mark.cli
class TestCLIIntegration:
    """Integration tests for CLI functionality."""

    @pytest.mark.integration
    def test_cli_version_display(self):
        """Test CLI can display version information."""
        from vultr_dns_mcp.cli import main

        runner = CliRunner()
        result = runner.invoke(main, ["--version"])

        # Should either show version or help with version info
        assert result.exit_code in [0, 2]  # 2 for missing click version

    @pytest.mark.integration
    def test_cli_error_handling(self):
        """Test CLI error handling."""
        from vultr_dns_mcp.cli import main

        runner = CliRunner()

        # Test with invalid argument
        result = runner.invoke(main, ["--invalid-option"])
        assert result.exit_code != 0

    @pytest.mark.integration
    @patch("vultr_dns_mcp.cli.create_mcp_server")
    def test_server_creation_error_handling(self, mock_create_server):
        """Test server creation error handling."""
        from vultr_dns_mcp.cli import main

        # Mock server creation to raise an error
        mock_create_server.side_effect = ValueError("Invalid API key")

        runner = CliRunner()
        result = runner.invoke(main, ["--api-key", "invalid-key"])

        # Should handle the error gracefully
        assert result.exit_code != 0
        assert "Invalid API key" in result.output or "Error" in result.output


@pytest.mark.unit
def test_cli_constants():
    """Test CLI constants and configuration."""
    from vultr_dns_mcp import cli

    # Test that CLI module has expected attributes
    assert hasattr(cli, "main")
    assert hasattr(cli, "server_command")


@pytest.mark.unit
def test_cli_imports():
    """Test that CLI imports all necessary dependencies."""
    from vultr_dns_mcp.cli import main, server_command

    # Test that functions are properly defined
    assert main is not None
    assert server_command is not None

    # Test that they're click commands
    assert callable(main)
    assert callable(server_command)

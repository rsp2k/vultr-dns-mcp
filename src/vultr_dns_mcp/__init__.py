"""
Vultr DNS MCP - A Model Context Protocol server for Vultr DNS management.

This package provides a comprehensive MCP server for managing DNS records
through the Vultr API. It includes tools for domain management, DNS record
operations, configuration analysis, and validation.

Example usage:
    from vultr_dns_mcp import VultrDNSServer, create_mcp_server

    # Create a server instance
    server = VultrDNSServer(api_key="your-api-key")

    # Create MCP server
    mcp_server = create_mcp_server(api_key="your-api-key")
    mcp_server.run()

Main classes:
    VultrDNSServer: Direct API client for Vultr DNS operations

Main functions:
    create_mcp_server: Factory function to create a configured MCP server
    run_server: Convenience function to run the MCP server
"""

from ._version import __version__, __version_info__
from .client import VultrDNSClient
from .server import VultrDNSServer, create_mcp_server, run_server


def main():
    """MCP Time Server - Time and timezone conversion functionality for MCP"""
    import asyncio

    asyncio.run(run_server())


if __name__ == "__main__":
    main()


__all__ = [
    "VultrDNSClient",
    "VultrDNSServer",
    "__version__",
    "__version_info__",
    "create_mcp_server",
    "main",
    "run_server",
]

# Package metadata
__author__ = "Ryan Malloy"
__email__ = "ryan@supported.systems"
__license__ = "MIT"
__description__ = (
    "A comprehensive Model Context Protocol server for Vultr DNS management"
)

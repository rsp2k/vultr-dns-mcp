# Vultr DNS MCP

[![PyPI version](https://badge.fury.io/py/vultr-dns-mcp.svg)](https://badge.fury.io/py/vultr-dns-mcp)
[![Python Support](https://img.shields.io/pypi/pyversions/vultr-dns-mcp.svg)](https://pypi.org/project/vultr-dns-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive **Model Context Protocol (MCP) server** for managing Vultr DNS records. This package provides both an MCP server for AI assistants and a Python client library for direct DNS management.

## 🚀 Features

- **Complete DNS Management** - Manage domains and all record types (A, AAAA, CNAME, MX, TXT, NS, SRV)
- **MCP Server** - Full Model Context Protocol server for AI assistant integration
- **Python Client** - Direct Python API for DNS operations
- **CLI Tool** - Command-line interface for DNS management
- **Smart Validation** - Built-in DNS record validation and best practices
- **Configuration Analysis** - Analyze DNS setup with recommendations
- **Natural Language Interface** - Understand complex DNS requests through MCP

## 📦 Installation

Install from PyPI:

```bash
pip install vultr-dns-mcp
```

Or install with development dependencies:

```bash
pip install vultr-dns-mcp[dev]
```

## 🔑 Setup

Get your Vultr API key from the [Vultr Control Panel](https://my.vultr.com/settings/#settingsapi).

Set your API key as an environment variable:

```bash
export VULTR_API_KEY="your_vultr_api_key_here"
```

## 🖥️ Usage

### MCP Server

Start the MCP server for AI assistant integration:

```bash
vultr-dns-mcp server
```

Or use the Python API:

```python
from vultr_dns_mcp import run_server

run_server("your-api-key")
```

### Python Client

Use the client library directly in your Python code:

```python
import asyncio
from vultr_dns_mcp import VultrDNSClient

async def main():
    client = VultrDNSClient("your-api-key")
    
    # List all domains
    domains = await client.domains()
    print(f"Found {len(domains)} domains")
    
    # Get domain info
    summary = await client.get_domain_summary("example.com")
    
    # Add DNS records
    await client.add_a_record("example.com", "www", "192.168.1.100")
    await client.add_mx_record("example.com", "@", "mail.example.com", priority=10)
    
    # Set up basic website
    await client.setup_basic_website("newdomain.com", "203.0.113.1")

asyncio.run(main())
```

### Command Line Interface

The package includes a comprehensive CLI:

```bash
# List domains
vultr-dns-mcp domains list

# Get domain information
vultr-dns-mcp domains info example.com

# Create a new domain
vultr-dns-mcp domains create example.com 192.168.1.100

# List DNS records
vultr-dns-mcp records list example.com

# Add DNS records
vultr-dns-mcp records add example.com A www 192.168.1.100
vultr-dns-mcp records add example.com MX @ mail.example.com --priority 10

# Set up a website
vultr-dns-mcp setup-website example.com 192.168.1.100

# Set up email
vultr-dns-mcp setup-email example.com mail.example.com
```

## 🤖 MCP Integration

### Claude Desktop

Add to your `~/.config/claude/mcp.json`:

```json
{
  "mcpServers": {
    "vultr-dns": {
      "command": "vultr-dns-mcp",
      "args": ["server"],
      "env": {
        "VULTR_API_KEY": "your_vultr_api_key_here"
      }
    }
  }
}
```

### Other MCP Clients

The server provides comprehensive MCP resources and tools that any MCP-compatible client can discover and use.

## 📝 Supported DNS Record Types

| Type | Description | Example |
|------|-------------|---------|
| **A** | IPv4 address | `192.168.1.100` |
| **AAAA** | IPv6 address | `2001:db8::1` |
| **CNAME** | Domain alias | `example.com` |
| **MX** | Mail server | `mail.example.com` (requires priority) |
| **TXT** | Text data | `v=spf1 include:_spf.google.com ~all` |
| **NS** | Name server | `ns1.example.com` |
| **SRV** | Service record | `0 5 443 example.com` (requires priority) |

## 🔧 API Reference

### VultrDNSClient

Main client class for DNS operations:

```python
client = VultrDNSClient(api_key)

# Domain operations
await client.domains()                    # List domains
await client.domain("example.com")       # Get domain info
await client.add_domain(domain, ip)      # Create domain
await client.remove_domain(domain)       # Delete domain

# Record operations
await client.records(domain)             # List records
await client.add_record(domain, type, name, value, ttl, priority)
await client.update_record(domain, record_id, type, name, value, ttl, priority)
await client.remove_record(domain, record_id)

# Convenience methods
await client.add_a_record(domain, name, ip, ttl)
await client.add_cname_record(domain, name, target, ttl)
await client.add_mx_record(domain, name, mail_server, priority, ttl)

# Utilities
await client.find_records_by_type(domain, record_type)
await client.get_domain_summary(domain)
await client.setup_basic_website(domain, ip)
await client.setup_email(domain, mail_server, priority)
```

### MCP Tools

When running as an MCP server, provides these tools:

- `list_dns_domains()` - List all domains
- `get_dns_domain(domain)` - Get domain details  
- `create_dns_domain(domain, ip)` - Create domain
- `delete_dns_domain(domain)` - Delete domain
- `list_dns_records(domain)` - List records
- `create_dns_record(...)` - Create record
- `update_dns_record(...)` - Update record
- `delete_dns_record(domain, record_id)` - Delete record
- `validate_dns_record(...)` - Validate record parameters
- `analyze_dns_records(domain)` - Analyze configuration

## 🛡️ Error Handling

All operations include comprehensive error handling:

```python
result = await client.add_a_record("example.com", "www", "192.168.1.100")

if "error" in result:
    print(f"Error: {result['error']}")
else:
    print(f"Success: Created record {result['id']}")
```

## 🧪 Development

Clone the repository and install development dependencies:

```bash
git clone https://github.com/vultr/vultr-dns-mcp.git
cd vultr-dns-mcp
pip install -e .[dev]
```

Run tests:

```bash
pytest
```

Format code:

```bash
black src tests
isort src tests
```

Type checking:

```bash
mypy src
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests to help improve this project.

## 📚 Links

- [PyPI Package](https://pypi.org/project/vultr-dns-mcp/)
- [GitHub Repository](https://github.com/vultr/vultr-dns-mcp)
- [Vultr API Documentation](https://www.vultr.com/api/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

## 🆘 Support

- Check the [documentation](https://vultr-dns-mcp.readthedocs.io/) for detailed guides
- Open an [issue](https://github.com/vultr/vultr-dns-mcp/issues) for bug reports
- Join discussions in the [community forum](https://github.com/vultr/vultr-dns-mcp/discussions)

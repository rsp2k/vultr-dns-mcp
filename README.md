# 🌐 Vultr DNS MCP

<div align="center">

[![PyPI version](https://badge.fury.io/py/vultr-dns-mcp.svg)](https://badge.fury.io/py/vultr-dns-mcp)
[![Python Support](https://img.shields.io/pypi/pyversions/vultr-dns-mcp.svg)](https://pypi.org/project/vultr-dns-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/rsp2k/vultr-dns-mcp/workflows/tests/badge.svg)](https://github.com/rsp2k/vultr-dns-mcp/actions)

**A comprehensive Model Context Protocol (MCP) server for managing Vultr DNS records with AI assistants and direct Python integration**

[Installation](#-installation) • [Quick Start](#-quick-start) • [Features](#-features) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🤖 **AI Assistant Integration**
- **MCP Server** - Full Model Context Protocol support
- **Claude Integration** - Direct integration with Claude AI
- **Natural Language** - Understand complex DNS requests
- **Smart Validation** - Built-in DNS record validation

</td>
<td width="50%">

### 🐍 **Python Developer Tools**
- **Client Library** - Direct Python API for DNS operations
- **CLI Tool** - Command-line interface for DNS management
- **Async Support** - Full async/await compatibility
- **Type Safety** - Complete type hints and validation

</td>
</tr>
<tr>
<td width="50%">

### 🌐 **Complete DNS Management**
- **All Record Types** - A, AAAA, CNAME, MX, TXT, NS, SRV
- **Domain Operations** - Create, update, delete domains
- **Bulk Operations** - Efficient batch processing
- **TTL Management** - Flexible time-to-live settings

</td>
<td width="50%">

### 📊 **Advanced Features**
- **Configuration Analysis** - Analyze DNS setup with recommendations
- **Best Practices** - Built-in DNS validation and suggestions
- **Error Handling** - Comprehensive error management
- **Monitoring** - Track DNS changes and performance

</td>
</tr>
</table>

---

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI
pip install vultr-dns-mcp

# Or install with development dependencies
pip install vultr-dns-mcp[dev]
```

### Get Your API Key

Get your Vultr API key from the [Vultr Control Panel](https://my.vultr.com/settings/#settingsapi).

```bash
export VULTR_API_KEY="your_vultr_api_key_here"
```

### Start the MCP Server

```bash
# Start the MCP server for AI assistant integration
vultr-dns-mcp server
```

### Python Usage

```python
import asyncio
from vultr_dns_mcp import VultrDNSClient

async def main():
    client = VultrDNSClient("your-api-key")
    
    # List all domains
    domains = await client.domains()
    print(f"Found {len(domains)} domains")
    
    # Add DNS records
    await client.add_a_record("example.com", "www", "192.168.1.100")
    await client.add_mx_record("example.com", "@", "mail.example.com", priority=10)
    
    # Set up basic website
    await client.setup_basic_website("newdomain.com", "203.0.113.1")

asyncio.run(main())
```

---

## 🛠️ CLI Usage

The package includes a comprehensive CLI for all DNS operations:

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

---

## 🤖 AI Assistant Integration

### Claude Integration

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

### Available MCP Tools

The server provides comprehensive MCP resources and tools that any MCP-compatible client can discover and use:

| Tool | Description | Example Usage |
|------|-------------|---------------|
| `list_dns_domains()` | List all domains | "Show me all my domains" |
| `get_dns_domain(domain)` | Get domain details | "Get info for example.com" |
| `create_dns_domain(domain, ip)` | Create domain | "Create domain newsite.com" |
| `delete_dns_domain(domain)` | Delete domain | "Remove old.example.com" |
| `list_dns_records(domain)` | List records | "Show DNS records for mysite.com" |
| `create_dns_record(...)` | Create record | "Add A record for www" |
| `update_dns_record(...)` | Update record | "Change the IP for www" |
| `delete_dns_record(domain, record_id)` | Delete record | "Remove the CNAME record" |
| `validate_dns_record(...)` | Validate record | "Check this MX record" |
| `analyze_dns_records(domain)` | Analyze configuration | "Analyze DNS setup for mysite.com" |

---

## 📋 Supported DNS Record Types

| Type | Description | Example |
|------|-------------|---------|
| **A** | IPv4 address | `192.168.1.100` |
| **AAAA** | IPv6 address | `2001:db8::1` |
| **CNAME** | Domain alias | `example.com` |
| **MX** | Mail server | `mail.example.com` (requires priority) |
| **TXT** | Text data | `v=spf1 include:_spf.google.com ~all` |
| **NS** | Name server | `ns1.example.com` |
| **SRV** | Service record | `0 5 443 example.com` (requires priority) |

---

## 🔧 API Reference

### Main Client Class

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

### Error Handling

All operations include comprehensive error handling:

```python
result = await client.add_a_record("example.com", "www", "192.168.1.100")
if "error" in result:
    print(f"Error: {result['error']}")
else:
    print(f"Success: Created record {result['id']}")
```

---

## 🧪 Development

### Setup

```bash
# Clone the repository
git clone https://github.com/rsp2k/vultr-dns-mcp.git
cd vultr-dns-mcp

# Install development dependencies
pip install -e .[dev]
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=vultr_dns_mcp

# Run specific test file
pytest tests/test_server.py -v
```

### Code Quality

```bash
# Format code
black src tests
isort src tests

# Type checking  
mypy src

# Linting
flake8 src tests
```

---

## 📖 Documentation

- **[API Documentation](https://vultr-dns-mcp.readthedocs.io/)** - Complete API reference
- **[MCP Protocol Guide](https://modelcontextprotocol.io/)** - Understanding MCP
- **[Vultr API Docs](https://www.vultr.com/api/)** - Vultr DNS API reference
- **[Examples](./examples/)** - Code examples and tutorials

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Quick Contribution Setup

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Make** your changes
4. **Test** your changes (`pytest`)
5. **Commit** your changes (`git commit -m 'Add amazing feature'`)
6. **Push** to the branch (`git push origin feature/amazing-feature`)
7. **Open** a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/rsp2k/vultr-dns-mcp/issues)
- **Discussions**: [GitHub Discussions](https://github.com/rsp2k/vultr-dns-mcp/discussions)  
- **Email**: [Support Email](mailto:support@example.com)

---

## 🙏 Acknowledgments

- [Vultr](https://vultr.com) for providing an excellent DNS API
- [Anthropic](https://anthropic.com) for the Model Context Protocol
- [FastMCP](https://github.com/jlowin/fastmcp) for MCP framework inspiration
- All our [contributors](https://github.com/rsp2k/vultr-dns-mcp/graphs/contributors)

---

<div align="center">

**[⬆ Back to Top](#-vultr-dns-mcp)**

Made with ❤️ by the Vultr DNS MCP Team

</div>

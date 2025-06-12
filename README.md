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

## 🤖 AI Assistant Integration

### Claude Integration

Add to your `~/.config/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "vultr-dns": {
      "command": "uvx",
      "args": ["vultr-dns-mcp"],
      "env": {
        "VULTR_API_KEY": "your_vultr_api_key_here"
      }
    }
  }
}
```
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
# format
black check --diff

# lint
ruff check src/

# Type checking TODO
# mypy src


```

---

## 📖 Documentation

- **[API Documentation](https://vultr-dns-mcp.readthedocs.io/)** - Complete API reference
- **[MCP Protocol Guide](https://modelcontextprotocol.io/)** - Understanding MCP
- **[Vultr API Docs](https://www.vultr.com/api/)** - Vultr DNS API reference


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

Made with ❤️ by rsp2k

</div>

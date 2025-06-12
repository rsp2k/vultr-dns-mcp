"""Version information for vultr-dns-mcp package."""

try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version

__version__ = version("vultr_dns_mcp")
__version_info__ = tuple(int(i) for i in __version__.split(".") if i.isdigit())

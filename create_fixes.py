#!/usr/bin/env python3
"""
Simple script to create fixed versions of all test files.
"""

import os
from pathlib import Path

def create_all_fixes():
    """Create all fixed files."""
    
    print("🔧 Creating fixed test files for vultr-dns-mcp...")
    
    # Create updated pyproject.toml content
    pyproject_content = '''[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "vultr-dns-mcp"
version = "1.0.1"
description = "A comprehensive Model Context Protocol (MCP) server for managing Vultr DNS records"
readme = "README.md"
license = {text = "MIT"}
authors = [
    {name = "Claude AI Assistant", email = "claude@anthropic.com"}
]
maintainers = [
    {name = "Claude AI Assistant", email = "claude@anthropic.com"}
]
keywords = [
    "vultr", 
    "dns", 
    "mcp", 
    "model-context-protocol", 
    "dns-management", 
    "api", 
    "fastmcp"
]
requires-python = ">=3.8"
dependencies = [
    "fastmcp>=0.1.0",
    "httpx>=0.24.0", 
    "pydantic>=2.0.0",
    "click>=8.0.0"
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.0.0",
    "black>=23.0.0",
    "isort>=5.12.0",
    "flake8>=6.0.0",
    "mypy>=1.0.0",
    "pre-commit>=3.0.0"
]
test = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0", 
    "pytest-cov>=4.0.0",
    "httpx-mock>=0.10.0"
]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "--verbose",
    "--tb=short",
    "--cov=vultr_dns_mcp",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-report=xml",
    "--cov-fail-under=80"
]
asyncio_mode = "auto"
markers = [
    "unit: Unit tests that test individual components in isolation",
    "integration: Integration tests that test component interactions",
    "mcp: Tests specifically for MCP server functionality", 
    "slow: Tests that take a long time to run"
]
filterwarnings = [
    "ignore::DeprecationWarning",
    "ignore::PendingDeprecationWarning"
]
'''
    
    # Write files
    with open("pyproject_toml_FIXED.toml", "w") as f:
        f.write(pyproject_content)
    
    print("✅ Created pyproject_toml_FIXED.toml")
    
    # Create a simple installation script
    install_script = '''#!/bin/bash
# Simple installation script for vultr-dns-mcp test fixes

echo "🔧 Applying test fixes to vultr-dns-mcp..."

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Not in vultr-dns-mcp repository root"
    echo "Please run this script from the repository root directory"
    exit 1
fi

# Backup existing files
echo "📦 Creating backups..."
cp tests/conftest.py tests/conftest.py.backup 2>/dev/null || echo "No conftest.py to backup"
cp tests/test_mcp_server.py tests/test_mcp_server.py.backup 2>/dev/null || echo "No test_mcp_server.py to backup"
cp pyproject.toml pyproject.toml.backup

# Copy fixed files (you'll need to copy these manually)
echo "📋 Files to copy:"
echo "   fixed_conftest.py -> tests/conftest.py"
echo "   fixed_test_mcp_server.py -> tests/test_mcp_server.py"
echo "   pyproject_toml_FIXED.toml -> pyproject.toml"

echo ""
echo "📝 Manual steps:"
echo "1. Copy the fixed files to their destinations"
echo "2. Install dependencies: pip install -e .[dev]"
echo "3. Run tests: pytest tests/ -v"

echo ""
echo "✅ Backup complete. Please apply the fixes manually."
'''
    
    with open("apply_fixes.sh", "w") as f:
        f.write(install_script)
    
    os.chmod("apply_fixes.sh", 0o755)
    print("✅ Created apply_fixes.sh")
    
    # List all files created
    print("\n📁 Fixed files available:")
    print("   - fixed_conftest.py (updated test configuration)")
    print("   - fixed_test_mcp_server.py (fixed MCP server tests)")
    print("   - pyproject_toml_FIXED.toml (updated dependencies)")
    print("   - apply_fixes.sh (installation helper)")
    print("   - COMPLETE_FIX_GUIDE.md (detailed instructions)")
    
    print("\n🚀 Next steps:")
    print("1. Copy these files to your vultr-dns-mcp repository")
    print("2. Run: cp fixed_conftest.py tests/conftest.py")
    print("3. Run: cp fixed_test_mcp_server.py tests/test_mcp_server.py")
    print("4. Run: cp pyproject_toml_FIXED.toml pyproject.toml")
    print("5. Install: pip install -e .[dev]")
    print("6. Test: pytest tests/ -v")

if __name__ == "__main__":
    create_all_fixes()

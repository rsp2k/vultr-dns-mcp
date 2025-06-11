#!/bin/bash

# Development installation script for vultr-dns-mcp
# This script installs the package in development mode for testing

set -e

echo "🔧 Installing vultr-dns-mcp in development mode..."

# Change to package directory
cd "$(dirname "$0")"

# Check if we're in a virtual environment
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚠️  Warning: Not in a virtual environment"
    echo "   Consider running: python -m venv .venv && source .venv/bin/activate"
    echo ""
fi

# Install in development mode
echo "📦 Installing package dependencies..."
pip install -e .

echo "🧪 Installing development dependencies..."
pip install -e .[dev]

echo "✅ Installation complete!"
echo ""
echo "🚀 You can now run:"
echo "   vultr-dns-mcp --help"
echo "   vultr-dns-mcp server"
echo ""
echo "🧪 Run tests with:"
echo "   python test_fix.py"
echo "   pytest"
echo ""
echo "📝 Set your API key:"
echo "   export VULTR_API_KEY='your-api-key-here'"

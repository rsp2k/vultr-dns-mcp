#!/bin/bash
# Vultr DNS MCP Test Fix Installer
# This script applies all necessary fixes to the test suite

set -e

echo "🔧 Vultr DNS MCP Test Suite Fixer"
echo "=================================="

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ] || [ ! -d "tests" ]; then
    echo "❌ Error: Please run this script from the vultr-dns-mcp repository root"
    echo "   Expected files: pyproject.toml, tests/ directory"
    exit 1
fi

echo "✅ Found vultr-dns-mcp repository structure"

# Create backups
echo "📦 Creating backups..."
backup_dir="test_backups_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$backup_dir"

if [ -f "tests/conftest.py" ]; then
    cp "tests/conftest.py" "$backup_dir/conftest.py.backup"
    echo "   Backed up conftest.py"
fi

if [ -f "tests/test_mcp_server.py" ]; then
    cp "tests/test_mcp_server.py" "$backup_dir/test_mcp_server.py.backup"
    echo "   Backed up test_mcp_server.py"
fi

cp "pyproject.toml" "$backup_dir/pyproject.toml.backup"
echo "   Backed up pyproject.toml"

# Check if fix files are available
fix_dir="/home/rpm/claude/vultr-dns-mcp-fix"
if [ ! -d "$fix_dir" ]; then
    echo "❌ Error: Fix files not found at $fix_dir"
    echo "   Please ensure the fix files are available"
    exit 1
fi

echo "✅ Found fix files"

# Apply fixes
echo ""
echo "🔧 Applying fixes..."

if [ -f "$fix_dir/fixed_conftest.py" ]; then
    cp "$fix_dir/fixed_conftest.py" "tests/conftest.py"
    echo "   ✅ Updated tests/conftest.py"
else
    echo "   ⚠️  Warning: fixed_conftest.py not found"
fi

if [ -f "$fix_dir/fixed_test_mcp_server.py" ]; then
    cp "$fix_dir/fixed_test_mcp_server.py" "tests/test_mcp_server.py"
    echo "   ✅ Updated tests/test_mcp_server.py"
else
    echo "   ⚠️  Warning: fixed_test_mcp_server.py not found"
fi

# Update pyproject.toml (add missing pytest config)
echo ""
echo "🔧 Updating pyproject.toml..."

# Check if pytest config exists
if ! grep -q "tool.pytest.ini_options" pyproject.toml; then
    echo ""
    echo "# Added by test fixer" >> pyproject.toml
    echo "[tool.pytest.ini_options]" >> pyproject.toml
    echo 'asyncio_mode = "auto"' >> pyproject.toml
    echo 'addopts = ["--strict-markers", "--verbose"]' >> pyproject.toml
    echo 'markers = [' >> pyproject.toml
    echo '    "unit: Unit tests",' >> pyproject.toml
    echo '    "integration: Integration tests",' >> pyproject.toml
    echo '    "mcp: MCP server tests",' >> pyproject.toml
    echo '    "slow: Slow tests"' >> pyproject.toml
    echo ']' >> pyproject.toml
    echo "   ✅ Added pytest configuration"
else
    echo "   ✅ pytest configuration already exists"
fi

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
if command -v pip &> /dev/null; then
    pip install -e .[dev] || {
        echo "   ⚠️  Dev install failed, trying basic dependencies..."
        pip install pytest pytest-asyncio pytest-cov fastmcp httpx pydantic click
    }
    echo "   ✅ Dependencies installed"
else
    echo "   ❌ Error: pip not found"
    exit 1
fi

# Run tests to verify
echo ""
echo "🧪 Testing the fixes..."
echo "=================================="

# Test basic import
if python -c "from vultr_dns_mcp.server import create_mcp_server; print('✅ Import test passed')" 2>/dev/null; then
    echo "✅ Basic imports working"
else
    echo "❌ Import test failed - please check installation"
fi

# Run a simple test
if pytest tests/test_package_validation.py -v -x; then
    echo "✅ Package validation tests passed"
else
    echo "⚠️  Package validation tests had issues"
fi

# Run MCP tests
echo ""
echo "🚀 Running MCP server tests..."
if pytest tests/test_mcp_server.py -v -x; then
    echo ""
    echo "🎉 SUCCESS! All MCP tests are now passing!"
else
    echo ""
    echo "⚠️  Some MCP tests still failing - check output above"
fi

echo ""
echo "=================================="
echo "✅ Fix application complete!"
echo ""
echo "📊 Summary:"
echo "   - Backup created in: $backup_dir/"
echo "   - Fixed files applied to tests/"
echo "   - Dependencies installed"
echo "   - Tests executed"
echo ""
echo "🚀 Next steps:"
echo "   1. Run: pytest tests/ -v (all tests)"
echo "   2. Run: pytest tests/ -m mcp -v (MCP tests only)"
echo "   3. Run: pytest tests/ --cov=vultr_dns_mcp (with coverage)"
echo ""
echo "💡 If issues persist:"
echo "   - Check the logs above for specific errors"
echo "   - Restore from backup: cp $backup_dir/* tests/"
echo "   - Review: cat FINAL_SOLUTION.md"

echo ""
echo "🎯 Test suite fix complete!"

# PyPI Publishing Setup Guide

This guide explains how to set up and use the automated PyPI publishing workflow for the `vultr-dns-mcp` package.

## 🔐 Setting Up Trusted Publishing (Recommended)

The workflow uses [PyPI's trusted publishing](https://docs.pypi.org/trusted-publishers/) feature, which eliminates the need for API tokens. This is the most secure method.

### For PyPI (Production)

1. **Go to your project on PyPI**: https://pypi.org/manage/project/vultr-dns-mcp/
2. **Navigate to "Publishing"** tab
3. **Add a new trusted publisher** with these settings:
   - **PyPI Project Name**: `vultr-dns-mcp`
   - **Owner**: `rsp2k`
   - **Repository name**: `vultr-dns-mcp`
   - **Workflow filename**: `publish.yml`
   - **Environment name**: `pypi`

### For TestPyPI (Testing)

1. **Go to TestPyPI**: https://test.pypi.org/manage/project/vultr-dns-mcp/
2. **Navigate to "Publishing"** tab
3. **Add a new trusted publisher** with these settings:
   - **PyPI Project Name**: `vultr-dns-mcp`
   - **Owner**: `rsp2k`
   - **Repository name**: `vultr-dns-mcp`
   - **Workflow filename**: `publish.yml`
   - **Environment name**: `testpypi`

### GitHub Environment Setup

1. **Go to your repository settings**: https://github.com/rsp2k/vultr-dns-mcp/settings/environments
2. **Create two environments**:
   - `pypi` (for production releases)
   - `testpypi` (for testing)
3. **Optional**: Add protection rules to require manual approval for production releases

## 🚀 How to Publish

### Automatic Publishing

1. **Update the version** in `pyproject.toml`:
   ```toml
   [project]
   name = "vultr-dns-mcp"
   version = "1.0.2"  # Increment this
   ```

2. **Commit your changes**:
   ```bash
   git add pyproject.toml
   git commit -m "Bump version to 1.0.2"
   git push
   ```

3. **Create and push a version tag**:
   ```bash
   git tag v1.0.2
   git push origin v1.0.2
   ```

4. **The workflow will automatically**:
   - Run basic validation
   - Build the package
   - Publish to PyPI
   - Create a GitHub release
   - Test the published package

### Manual Publishing

You can also trigger publishing manually:

1. **Go to Actions** → **Publish to PyPI**
2. **Click "Run workflow"**
3. **Choose options**:
   - ✅ **Publish to TestPyPI**: Test your release first
   - ✅ **Skip if version exists**: Avoid errors for existing versions

## 📋 Publishing Checklist

Before creating a release tag:

- [ ] Basic validation passes on the main branch
- [ ] Version number is updated in `pyproject.toml`
- [ ] `CHANGELOG.md` is updated with the new version
- [ ] Documentation is up to date
- [ ] No breaking changes without major version bump

## 🔢 Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR** version: incompatible API changes (`2.0.0`)
- **MINOR** version: new functionality, backwards compatible (`1.1.0`)
- **PATCH** version: bug fixes, backwards compatible (`1.0.1`)

### Pre-release Versions

The workflow automatically detects pre-releases:
- `1.0.0a1` (alpha)
- `1.0.0b1` (beta)
- `1.0.0rc1` (release candidate)
- `1.0.0.dev1` (development)

Pre-releases are marked as "pre-release" on GitHub.

## 📝 Changelog Format

The workflow automatically extracts changelog entries. Format your `CHANGELOG.md` like this:

```markdown
# Changelog

## [1.0.2] - 2025-01-15

### Added
- New feature X
- Support for Y

### Fixed
- Bug in Z functionality

### Changed
- Improved performance of A

## [1.0.1] - 2025-01-10

### Fixed
- Critical bug fix
```

## 🛠️ Troubleshooting

### Common Issues

**"Version already exists"**: 
- PyPI doesn't allow overwriting versions
- Increment the version number in `pyproject.toml`

**"Trusted publisher not configured"**:
- Ensure you've set up trusted publishing correctly
- Check the environment names match exactly

**"Validation failing"**:
- The workflow requires basic validation to pass
- Fix any failing checks before tagging

**"Tag doesn't match version"**:
- Ensure the git tag matches the version in `pyproject.toml`
- Tag: `v1.0.2` should match version: `1.0.2`

### Manual Testing

Test your package locally before publishing:

```bash
# Install in development mode
pip install -e .[dev]

# Run the validation that the CI uses
# Check package can be imported
python -c "import vultr_dns_mcp; print('✅ Package imports successfully')"

# Run basic linting
black --check --diff src/
isort --check-only --diff src/
flake8 src/
mypy src/

# Build and check the package
python -m build
python -m twine check dist/*
```

## 📊 Monitoring

After publishing, monitor:
- **PyPI downloads**: https://pypistats.org/packages/vultr-dns-mcp
- **GitHub releases**: https://github.com/rsp2k/vultr-dns-mcp/releases
- **Actions logs**: https://github.com/rsp2k/vultr-dns-mcp/actions

## 🎯 Next Steps

1. Set up trusted publishing on PyPI and TestPyPI
2. Create your first release by tagging `v1.0.1`
3. Monitor the workflow execution
4. Set up branch protection rules if desired
5. Consider adding dependabot for automated dependency updates

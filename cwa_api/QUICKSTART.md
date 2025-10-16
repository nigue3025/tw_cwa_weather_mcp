# Quick Start Guide

## Testing Locally

Before publishing, test your server locally:

```powershell
# Install in development mode
pip install -e .

# Test the server
python -m tw_cwa_weather_mcp.app_mcp
```

## File Checklist

Before publishing, ensure these files exist:

- ✅ `server.json` - MCP registry configuration
- ✅ `pyproject.toml` - Python package metadata
- ✅ `README.md` - Package documentation (with mcp-name)
- ✅ `LICENSE` - MIT License
- ✅ `MANIFEST.in` - Include data files
- ✅ `.gitignore` - Exclude unnecessary files
- ✅ `.github/workflows/publish-mcp.yml` - Automation
- ✅ `tw_cwa_weather_mcp/__init__.py` - Package marker
- ✅ `tw_cwa_weather_mcp/app_mcp.py` - Main server
- ✅ `tw_cwa_weather_mcp/aliased.txt` - Data file
- ✅ `tw_cwa_weather_mcp/counties.txt` - Data file

## Publishing Checklist

1. [ ] Created PyPI account and API token
2. [ ] Added `PYPI_API_TOKEN` to GitHub Secrets
3. [ ] Committed all changes to git
4. [ ] Created and pushed version tag (`git tag v1.0.0 && git push origin v1.0.0`)
5. [ ] Monitored GitHub Actions workflow
6. [ ] Verified package on PyPI
7. [ ] Verified server in MCP Registry

## Quick Commands

```powershell
# Build package
python -m build

# Check package contents
tar -tzf dist/tw-cwa-weather-mcp-1.0.0.tar.gz

# Validate server.json
python validate_server.py

# Create release
git add .
git commit -m "Prepare v1.0.0 release"
git push origin main
git tag v1.0.0
git push origin v1.0.0
```

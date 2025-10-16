# Publishing Your Taiwan CWA Weather MCP Server

## Overview

This guide will help you publish your MCP server to both PyPI and the official MCP Registry using automated GitHub Actions.

## ✅ What's Already Set Up

1. **Package Structure**: Your code is now organized as a proper Python package (`tw_cwa_weather_mcp/`)
2. **server.json**: Created and validated against MCP schema ✅
3. **pyproject.toml**: Package metadata and dependencies configured
4. **README.md**: Includes the required `mcp-name` identifier for PyPI validation
5. **GitHub Actions Workflow**: Automated publishing pipeline ready
6. **Validation Script**: `validate_server.py` to check server.json

## 📋 Prerequisites

Before publishing, you need to:

### 1. Create a PyPI Account and API Token

1. Go to https://pypi.org and create an account
2. Verify your email address
3. Go to Account Settings → API tokens
4. Create a new token with scope "Entire account"
5. Copy the token (it starts with `pypi-`)

### 2. Add PyPI Token to GitHub Secrets

1. Go to your GitHub repository: https://github.com/nigue3025/tw_cwa_weather_mcp
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `PYPI_API_TOKEN`
5. Value: Paste your PyPI token
6. Click **Add secret**

### 3. Verify GitHub Actions Permissions

1. Go to **Settings** → **Actions** → **General**
2. Under "Workflow permissions", ensure:
   - ☑️ "Read and write permissions" is selected
   - OR at minimum "Read repository contents and packages permissions" plus the workflow has `id-token: write`

## 🚀 Publishing Process

### Step 1: Test Build Locally (Optional but Recommended)

```powershell
# Navigate to your project
cd d:\Git\tw_cwa_weather_mcp\cwa_api

# Activate virtual environment (if not already active)
.venv\Scripts\Activate.ps1

# Install build tools
pip install build twine

# Build the package
python -m build

# This creates files in dist/:
# - tw_cwa_weather_mcp-1.0.0.tar.gz
# - tw_cwa_weather_mcp-1.0.0-whl
```

### Step 2: Commit and Push Your Changes

```powershell
# Add all new files
git add .

# Commit
git commit -m "Add MCP server publishing setup"

# Push to main branch
git push origin main
```

### Step 3: Create a Release Tag

This triggers the automated publishing workflow:

```powershell
# Create and push a version tag
git tag v1.0.0
git push origin v1.0.0
```

### Step 4: Monitor the Workflow

1. Go to your repository on GitHub
2. Click the **Actions** tab
3. You should see "Publish to MCP Registry" workflow running
4. The workflow will:
   - ✅ Build your Python package
   - ✅ Publish to PyPI
   - ✅ Wait for PyPI to index
   - ✅ Login to MCP Registry (via GitHub OIDC)
   - ✅ Publish to MCP Registry

## 🔍 Verification

### Verify PyPI Publication

After the workflow completes, check:
```
https://pypi.org/project/tw-cwa-weather-mcp/
```

### Verify MCP Registry Publication

Search for your server:
```bash
curl "https://registry.modelcontextprotocol.io/v0/servers?search=io.github.nigue3025/tw-cwa-weather-mcp"
```

Or browse: https://mcp.so

## 📝 Updating Your Server

To publish a new version:

1. Update the version in `pyproject.toml`:
   ```toml
   version = "1.0.1"
   ```

2. Update the version in `server.json`:
   ```json
   {
     "version": "1.0.1",
     "packages": [
       {
         "version": "1.0.1",
         ...
       }
     ]
   }
   ```

3. Commit, tag, and push:
   ```powershell
   git add pyproject.toml server.json
   git commit -m "Bump version to 1.0.1"
   git push origin main
   git tag v1.0.1
   git push origin v1.0.1
   ```

## 🐛 Troubleshooting

### "Package validation failed"
- Ensure your package was successfully published to PyPI first
- Wait at least 30 seconds for PyPI to index (the workflow has a wait step)
- Verify the `mcp-name: io.github.nigue3025/tw-cwa-weather-mcp` line exists in README.md

### "Authentication failed" (GitHub OIDC)
- Ensure `id-token: write` permission is in the workflow (it is)
- Check that your repository has Actions enabled

### "PYPI_API_TOKEN not found"
- Verify you added the secret with the exact name `PYPI_API_TOKEN`
- Check it's a repository secret, not an environment secret

### Build fails locally
- Make sure you're in the correct directory
- Ensure all required files are present (pyproject.toml, README.md, etc.)
- Check that the package structure is correct

## 📦 Package Structure

Your published package will have this structure:
```
tw-cwa-weather-mcp/
├── tw_cwa_weather_mcp/
│   ├── __init__.py
│   ├── app_mcp.py (main server code)
│   ├── aliased.txt (county aliases)
│   └── counties.txt (available locations)
├── README.md
├── LICENSE
├── pyproject.toml
├── server.json
└── MANIFEST.in
```

## 🎯 Next Steps

After publishing:
1. Users can install with: `pip install tw-cwa-weather-mcp`
2. Your server will be discoverable in MCP-compatible clients
3. Update documentation with usage examples
4. Consider adding tests and CI for code quality

## 📚 Additional Resources

- [MCP Publishing Guide](https://raw.githubusercontent.com/modelcontextprotocol/registry/refs/heads/main/docs/guides/publishing/publish-server.md)
- [GitHub Actions for MCP](https://raw.githubusercontent.com/modelcontextprotocol/registry/refs/heads/main/docs/guides/publishing/github-actions.md)
- [PyPI Documentation](https://packaging.python.org/)

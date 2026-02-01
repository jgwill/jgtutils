#!/bin/bash

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}════════════════════════════════════════${NC}"
echo -e "${BLUE}     JGTUtils Release Script${NC}"
echo -e "${BLUE}════════════════════════════════════════${NC}"

# Check if on main branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo -e "${RED}✗ Error: Must be on 'main' branch to release (currently on '$CURRENT_BRANCH')${NC}"
    exit 1
fi
echo -e "${GREEN}✓ On main branch${NC}"

# Check for uncommitted changes (ignore untracked files)
UNCOMMITTED=$(git status --porcelain | grep -v '^??' || echo "")
if [ -n "$UNCOMMITTED" ]; then
    echo -e "${RED}✗ Error: Uncommitted changes detected. Please commit or stash changes first.${NC}"
    echo "$UNCOMMITTED"
    exit 1
fi
echo -e "${GREEN}✓ No uncommitted changes${NC}"

# Ensure main is up to date
echo -e "${YELLOW}→ Fetching latest from origin...${NC}"
git fetch origin
if [ "$(git rev-parse HEAD)" != "$(git rev-parse origin/main)" ]; then
    echo -e "${RED}✗ Error: Local main branch is behind origin. Please pull latest changes.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Branch is up to date${NC}"

# Run tests
echo -e "${YELLOW}→ Running tests...${NC}"
if command -v pytest &> /dev/null; then
    pytest
    echo -e "${GREEN}✓ Tests passed${NC}"
else
    echo -e "${YELLOW}⚠ pytest not found, skipping tests${NC}"
fi

# Get current version before bump
CURRENT_VERSION=$(python3 -c 'from jgtutils import version; print(version)')
echo -e "${BLUE}Current version: ${CURRENT_VERSION}${NC}"

# Bump version
echo -e "${YELLOW}→ Bumping version...${NC}"
python bump_version.py
NEW_VERSION=$(python3 -c 'from jgtutils import version; print(version)')
echo -e "${GREEN}✓ Version bumped to ${NEW_VERSION}${NC}"

# Verify version files were updated
if ! grep -q "version = \"${NEW_VERSION}\"" pyproject.toml; then
    echo -e "${RED}✗ Error: pyproject.toml not updated correctly${NC}"
    exit 1
fi
if ! grep -q "\"version\": \"${NEW_VERSION}\"" package.json; then
    echo -e "${RED}✗ Error: package.json not updated correctly${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Version files verified${NC}"

# Commit version bump
echo -e "${YELLOW}→ Committing version bump...${NC}"
git add jgtutils/__init__.py pyproject.toml package.json
git commit -m "Bump version to ${NEW_VERSION}"
echo -e "${GREEN}✓ Version bump committed${NC}"

# Clean and build
echo -e "${YELLOW}→ Cleaning and building distribution...${NC}"
make clean
make dist
echo -e "${GREEN}✓ Distribution built${NC}"

# Verify dist files exist
if [ ! -f "dist/jgtutils-${NEW_VERSION}.tar.gz" ] && [ ! -f "dist/jgtutils-${NEW_VERSION}-py3-none-any.whl" ]; then
    echo -e "${YELLOW}⚠ Warning: Expected distribution files not found in standard names${NC}"
fi
ls -lh dist/
echo -e "${GREEN}✓ Distribution files created${NC}"

# Create git tag
echo -e "${YELLOW}→ Creating git tag...${NC}"
git tag -a "v${NEW_VERSION}" -m "Release version ${NEW_VERSION}"
echo -e "${GREEN}✓ Git tag created${NC}"

# Push to git
echo -e "${YELLOW}→ Pushing to git...${NC}"
git push origin main
git push origin --tags
echo -e "${GREEN}✓ Pushed to git${NC}"

# Upload to PyPI
echo -e "${YELLOW}→ Uploading to PyPI...${NC}"
if command -v twine &> /dev/null; then
    twine upload dist/jgtutils-${NEW_VERSION}*
    echo -e "${GREEN}✓ Uploaded to PyPI${NC}"
else
    echo -e "${RED}✗ Error: twine not found. Install with: pip install twine${NC}"
    echo -e "${YELLOW}To complete upload manually, run:${NC}"
    echo -e "  twine upload dist/jgtutils-${NEW_VERSION}*"
    exit 1
fi

echo -e "${BLUE}════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Release ${NEW_VERSION} completed successfully!${NC}"
echo -e "${BLUE}════════════════════════════════════════${NC}"

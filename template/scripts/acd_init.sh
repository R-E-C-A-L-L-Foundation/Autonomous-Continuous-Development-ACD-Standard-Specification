#!/bin/bash
# ACD Initialization Script
# This script sets up ACD tools and configuration for your repository

set -e

echo "=================================================="
echo "  ACD Repository Initialization"
echo "=================================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Error: Not in a git repository. Please initialize git first."
    exit 1
fi

echo "Step 1: Creating directory structure..."
mkdir -p .acd
mkdir -p docs/fix_summaries
mkdir -p acd_artifacts/traces
mkdir -p scripts

echo -e "${GREEN}✓${NC} Directory structure created"

echo ""
echo "Step 2: Checking for ACD tools..."

# Check if validate_acd.py exists
if [ ! -f "scripts/validate_acd.py" ]; then
    echo "Downloading validate_acd.py..."
    curl -sL https://raw.githubusercontent.com/R-E-C-A-L-L-Foundation/Autonomous-Continuous-Development-ACD-Standard-Specification/main/src/validate_acd.py -o scripts/validate_acd.py
    chmod +x scripts/validate_acd.py
    echo -e "${GREEN}✓${NC} validate_acd.py installed"
else
    echo -e "${GREEN}✓${NC} validate_acd.py already exists"
fi

# Check if acd_parser.py exists
if [ ! -f "scripts/acd_parser.py" ]; then
    echo "Downloading acd_parser.py..."
    curl -sL https://raw.githubusercontent.com/R-E-C-A-L-L-Foundation/Autonomous-Continuous-Development-ACD-Standard-Specification/main/src/acd_parser.py -o scripts/acd_parser.py
    chmod +x scripts/acd_parser.py
    echo -e "${GREEN}✓${NC} acd_parser.py installed"
else
    echo -e "${GREEN}✓${NC} acd_parser.py already exists"
fi

# Check if gdb_acd.py exists
if [ ! -f "scripts/gdb_acd.py" ]; then
    echo "Downloading gdb_acd.py..."
    curl -sL https://raw.githubusercontent.com/R-E-C-A-L-L-Foundation/Autonomous-Continuous-Development-ACD-Standard-Specification/main/scripts/gdb_acd.py -o scripts/gdb_acd.py
    echo -e "${GREEN}✓${NC} gdb_acd.py installed"
else
    echo -e "${GREEN}✓${NC} gdb_acd.py already exists"
fi

echo ""
echo "Step 3: Checking Python dependencies..."
python3 -c "import yaml" 2>/dev/null || {
    echo -e "${YELLOW}Warning:${NC} PyYAML not installed. Install with: pip install pyyaml"
}

echo ""
echo "Step 4: Adding .gitignore entries..."
if [ -f ".gitignore" ]; then
    if ! grep -q "acd_artifacts" .gitignore; then
        echo "" >> .gitignore
        echo "# ACD artifacts" >> .gitignore
        echo "acd_artifacts/*.json" >> .gitignore
        echo "acd_artifacts/*.md" >> .gitignore
        echo "acd_artifacts/traces/" >> .gitignore
        echo -e "${GREEN}✓${NC} Added ACD entries to .gitignore"
    else
        echo -e "${GREEN}✓${NC} .gitignore already contains ACD entries"
    fi
else
    echo -e "${YELLOW}Warning:${NC} No .gitignore file found"
fi

echo ""
echo "Step 5: Setting up Git hooks (optional)..."
if [ -d ".git/hooks" ]; then
    echo -e "${YELLOW}Note:${NC} You can add a pre-commit hook to validate ACD metadata"
    echo "      See docs/IMPLEMENTATION_GUIDE.md for details"
fi

echo ""
echo "=================================================="
echo -e "  ${GREEN}ACD Initialization Complete!${NC}"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Review and customize .acd/config.yml"
echo "2. Add SCIS metadata to your source files"
echo "3. Run: python3 scripts/validate_acd.py src/"
echo "4. See docs/IMPLEMENTATION_GUIDE.md for detailed usage"
echo ""
echo "For more information, visit:"
echo "https://github.com/R-E-C-A-L-L-Foundation/Autonomous-Continuous-Development-ACD-Standard-Specification"
echo ""

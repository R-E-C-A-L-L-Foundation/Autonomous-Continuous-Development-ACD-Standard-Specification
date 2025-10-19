#!/bin/bash
#
# ACD Specification Repository Bootstrap Script
# 
# This script sets up the development environment for the ACD Specification
# reference implementation, including build dependencies, Python environment,
# and initial validation.
#
# Reference: ACD Standard Specification v1.0

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ACD standard logging
log_phase() {
    echo -e "${BLUE}[ACD Bootstrap]${NC} [$(date -u +"%Y-%m-%d %H:%M:%S UTC")] [PHASE: $1]"
}

log_info() {
    echo -e "${GREEN}[ACD Bootstrap]${NC} [$(date -u +"%Y-%m-%d %H:%M:%S UTC")] [INFO] $1"
}

log_warn() {
    echo -e "${YELLOW}[ACD Bootstrap]${NC} [$(date -u +"%Y-%m-%d %H:%M:%S UTC")] [WARN] $1"
}

log_error() {
    echo -e "${RED}[ACD Bootstrap]${NC} [$(date -u +"%Y-%m-%d %H:%M:%S UTC")] [ERROR] $1"
}

# Detect the repository root
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

log_phase "INIT"
log_info "ACD Specification Repository Bootstrap v1.0"
log_info "Repository root: $REPO_ROOT"
echo ""

# Check Python version
log_phase "DEPENDENCY_CHECK"
log_info "Checking Python version..."

if ! command -v python3 &> /dev/null; then
    log_error "Python 3 is not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
log_info "Python version: $PYTHON_VERSION"

# Check if Python version is >= 3.11
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 11 ]); then
    log_warn "Python 3.11+ is recommended for ACD tools (found $PYTHON_VERSION)"
fi

# Check CMake version
log_info "Checking CMake version..."

if ! command -v cmake &> /dev/null; then
    log_warn "CMake is not installed (required for C++ examples)"
else
    CMAKE_VERSION=$(cmake --version | head -1 | cut -d' ' -f3)
    log_info "CMake version: $CMAKE_VERSION"
    
    # Check if CMake version is >= 3.20
    CMAKE_MAJOR=$(echo $CMAKE_VERSION | cut -d'.' -f1)
    CMAKE_MINOR=$(echo $CMAKE_VERSION | cut -d'.' -f2)
    
    if [ "$CMAKE_MAJOR" -lt 3 ] || ([ "$CMAKE_MAJOR" -eq 3 ] && [ "$CMAKE_MINOR" -lt 20 ]); then
        log_warn "CMake 3.20+ is recommended (found $CMAKE_VERSION)"
    fi
fi

# Check C++ compiler
log_info "Checking C++ compiler..."

if command -v g++ &> /dev/null; then
    GCC_VERSION=$(g++ --version | head -1 | cut -d' ' -f4)
    log_info "g++ version: $GCC_VERSION"
elif command -v clang++ &> /dev/null; then
    CLANG_VERSION=$(clang++ --version | head -1 | cut -d' ' -f3)
    log_info "clang++ version: $CLANG_VERSION"
else
    log_warn "No C++ compiler found (g++ or clang++ required for examples)"
fi

echo ""

# Create directory structure if not exists
log_phase "DIRECTORY_SETUP"
log_info "Creating directory structure..."

mkdir -p "$REPO_ROOT/spec"
mkdir -p "$REPO_ROOT/src"
mkdir -p "$REPO_ROOT/examples"
mkdir -p "$REPO_ROOT/scripts"
mkdir -p "$REPO_ROOT/tests"
mkdir -p "$REPO_ROOT/ci"
mkdir -p "$REPO_ROOT/acd_artifacts"
mkdir -p "$REPO_ROOT/artifacts"

log_info "Directory structure created"
echo ""

# Validate required files exist
log_phase "FILE_VALIDATION"
log_info "Validating required files..."

REQUIRED_FILES=(
    "spec/ACD_SCHEMA_v1.0.json"
    "src/validate_acd.py"
    "README.md"
)

ALL_PRESENT=true
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$REPO_ROOT/$file" ]; then
        log_info "✓ $file"
    else
        log_error "✗ $file (missing)"
        ALL_PRESENT=false
    fi
done

if [ "$ALL_PRESENT" = false ]; then
    log_error "Some required files are missing"
    exit 1
fi

echo ""

# Make scripts executable
log_phase "PERMISSIONS"
log_info "Setting executable permissions..."

chmod +x "$REPO_ROOT/src/validate_acd.py" 2>/dev/null || true
chmod +x "$REPO_ROOT/scripts/bootstrap.sh" 2>/dev/null || true

log_info "Permissions set"
echo ""

# Test ACD validator
log_phase "VALIDATOR_TEST"
log_info "Testing ACD validator..."

if python3 "$REPO_ROOT/src/validate_acd.py" --version; then
    log_info "ACD validator is working"
else
    log_error "ACD validator test failed"
    exit 1
fi

echo ""

# Run validation on examples if they exist
if [ -d "$REPO_ROOT/examples" ] && [ "$(ls -A $REPO_ROOT/examples/*.cpp 2>/dev/null)" ]; then
    log_phase "EXAMPLE_VALIDATION"
    log_info "Validating example files..."
    
    if python3 "$REPO_ROOT/src/validate_acd.py" "$REPO_ROOT/examples" --export "$REPO_ROOT/acd_artifacts/example_validation.json"; then
        log_info "Example validation completed successfully"
    else
        log_warn "Example validation found issues (see output above)"
    fi
    echo ""
fi

# Summary
log_phase "COMPLETE"
echo ""
echo "======================================================================"
echo "  ACD Specification Repository Bootstrap Complete"
echo "======================================================================"
echo ""
echo "Repository Structure:"
echo "  /spec/       → Schema definitions"
echo "  /src/        → Reference implementation (validator, tools)"
echo "  /examples/   → Sample instrumented code"
echo "  /scripts/    → Build & validation automation"
echo "  /tests/      → Unit and compliance tests"
echo "  /ci/         → GitHub Actions workflows"
echo "  /acd_artifacts/→ Validation reports and trace artifacts"
echo "  /artifacts/  → Build and test artifacts"
echo ""
echo "Available Tools:"
echo "  src/validate_acd.py  → ACD metadata validator"
echo ""
echo "Next Steps:"
echo "  1. Review the ACD Standard Specification in README.md"
echo "  2. Examine example instrumented code in examples/"
echo "  3. Run: python3 src/validate_acd.py examples/"
echo "  4. Integrate ACD metadata into your source code"
echo ""
echo "For more information, see README.md and CONTRIBUTING.md"
echo "======================================================================"
echo ""

exit 0

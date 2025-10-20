# ACD Template Usage Guide

This comprehensive guide explains how to use the ACD repository template to quickly adopt the Autonomous Continuous Development (ACD) Standard in your projects.

## Table of Contents

1. [Overview](#overview)
2. [What You Get](#what-you-get)
3. [Installation Methods](#installation-methods)
4. [Step-by-Step Setup](#step-by-step-setup)
5. [Customization](#customization)
6. [Usage Examples](#usage-examples)
7. [Troubleshooting](#troubleshooting)

## Overview

The ACD Template is a drop-in repository structure that enables you to quickly adopt the ACD Specification. It includes:
- Pre-configured directory structure
- Ready-to-use validation tools
- CI/CD integration
- Example code with proper SCIS metadata
- Comprehensive documentation

## What You Get

### Directory Structure

```
your-project/
├── .acd/
│   └── config.yml              # Project-specific ACD configuration
├── .github/
│   └── workflows/
│       └── acd_validation.yml  # Automated validation workflow
├── docs/
│   ├── IMPLEMENTATION_GUIDE.md # Detailed implementation guide
│   └── fix_summaries/         # Historical fix documentation
│       └── FIX_TEMPLATE.md    # Template for documenting fixes
├── examples/
│   ├── example_with_acd.c     # C example with SCIS metadata
│   └── example_with_acd.py    # Python example with SCIS metadata
├── scripts/
│   └── acd_init.sh            # Initialization script
├── src/                       # Your source code goes here
├── tests/                     # Your tests go here
└── README.md                  # Project README with ACD info
```

### Tools Included

1. **Configuration File** (`.acd/config.yml`)
   - Define your project's phases
   - Configure validation rules
   - Set export preferences

2. **Initialization Script** (`scripts/acd_init.sh`)
   - One-command setup
   - Downloads required tools
   - Configures Git integration

3. **GitHub Actions Workflow** (`.github/workflows/acd_validation.yml`)
   - Automatic validation on push/PR
   - Report generation
   - PR comments with results

4. **Example Code** (`examples/`)
   - C and Python examples
   - Proper SCIS metadata usage
   - Various complexity levels

5. **Documentation** (`docs/`)
   - Implementation guide
   - Fix summary template
   - Best practices

## Installation Methods

### Method 1: Copy Template to Existing Project

If you have an existing project:

```bash
# Clone the ACD Specification repository
git clone https://github.com/R-E-C-A-L-L-Foundation/Autonomous-Continuous-Development-ACD-Standard-Specification.git /tmp/acd_spec

# Copy template to your project
cd /path/to/your/project
cp -r /tmp/acd_spec/template/* .
cp -r /tmp/acd_spec/template/.acd .
cp -r /tmp/acd_spec/template/.github .

# Initialize ACD
chmod +x scripts/acd_init.sh
./scripts/acd_init.sh

# Clean up
rm -rf /tmp/acd_spec
```

### Method 2: Start New Project from Template

For a new project:

```bash
# Clone the ACD Specification repository
git clone https://github.com/R-E-C-A-L-L-Foundation/Autonomous-Continuous-Development-ACD-Standard-Specification.git /tmp/acd_spec

# Create your project from template
mkdir my-new-project
cd my-new-project
git init

# Copy template files
cp -r /tmp/acd_spec/template/* .
cp -r /tmp/acd_spec/template/.acd .
cp -r /tmp/acd_spec/template/.github .

# Initialize ACD
chmod +x scripts/acd_init.sh
./scripts/acd_init.sh

# Customize README
# Edit README.md to replace [Your Project Name] with your actual project name

# Clean up
rm -rf /tmp/acd_spec

# First commit
git add .
git commit -m "Initialize project with ACD template"
```

### Method 3: Manual Setup

If you prefer manual setup:

1. Create directory structure:
```bash
mkdir -p .acd docs/fix_summaries examples scripts src tests .github/workflows
```

2. Download configuration and tools:
```bash
# Download from the template directory in the ACD Specification repo
# Copy each file individually from:
# https://github.com/R-E-C-A-L-L-Foundation/Autonomous-Continuous-Development-ACD-Standard-Specification/tree/main/template
```

3. Run initialization:
```bash
chmod +x scripts/acd_init.sh
./scripts/acd_init.sh
```

## Step-by-Step Setup

### Step 1: Install the Template

Choose one of the installation methods above and set up the template in your project.

### Step 2: Customize Configuration

Edit `.acd/config.yml` to match your project:

```yaml
# Update project information
project:
  name: "Your Actual Project Name"
  repository: "your-org/your-repo"
  description: "Your project description"

# Define your phases
phases:
  - name: "AUTHENTICATION"
    description: "User authentication and authorization"
    complexity: "HIGH"
  
  - name: "DATA_PROCESSING"
    description: "Data transformation and validation"
    complexity: "MEDIUM"
  
  # Add more phases specific to your project
```

### Step 3: Update README

Edit `README.md` and replace placeholders:
- `[Your Project Name]` → Your actual project name
- `[Your License Here]` → Your license information
- Add project-specific information

### Step 4: Add Metadata to Existing Code

If you have existing code, add SCIS metadata:

**For C/C++ files:**
```cpp
/*
 * AI_PHASE: YOUR_PHASE
 * AI_STATUS: IMPLEMENTED
 * AI_COMPLEXITY: MEDIUM
 * AI_NOTE: Description of the function
 * AI_DEPENDENCIES: OTHER_PHASE
 * AI_COMMIT: $(git rev-parse --short HEAD)
 */
void your_function() {
    // existing code
}
```

**For Python files:**
```python
# AI_PHASE: YOUR_PHASE
# AI_STATUS: IMPLEMENTED
# AI_COMPLEXITY: MEDIUM
# AI_NOTE: Description of the function
# AI_DEPENDENCIES: OTHER_PHASE
# AI_COMMIT: $(git rev-parse --short HEAD)
def your_function():
    """Existing function."""
    pass
```

### Step 5: Validate Your Metadata

Run validation to check your metadata:

```bash
python3 scripts/validate_acd.py src/ --verbose
```

Fix any issues reported by the validator.

### Step 6: Set Up CI/CD

If using GitHub:
1. The workflow is already in `.github/workflows/acd_validation.yml`
2. Push to GitHub and it will automatically run
3. Check the Actions tab for results

For other CI/CD systems:
1. Adapt the workflow from `.github/workflows/acd_validation.yml`
2. Add to your CI/CD configuration

### Step 7: Test the Setup

```bash
# Validate metadata
python3 scripts/validate_acd.py src/

# Generate analysis report
python3 scripts/acd_parser.py src/ --analyze --markdown report.md

# View the report
cat report.md
```

## Customization

### Adding Custom Phases

Edit `.acd/config.yml`:

```yaml
phases:
  - name: "MY_CUSTOM_PHASE"
    description: "Description of what this phase does"
    complexity: "MEDIUM"
```

Then use in your code:

```cpp
/*
 * AI_PHASE: MY_CUSTOM_PHASE
 * AI_STATUS: IMPLEMENTED
 */
```

### Customizing Validation Rules

Edit `.acd/config.yml`:

```yaml
validation:
  # Make AI_COMMIT required
  required_tags:
    - "AI_PHASE"
    - "AI_STATUS"
    - "AI_COMMIT"
  
  # Add file patterns
  include_patterns:
    - "**/*.go"
    - "**/*.rs"
```

### Customizing CI/CD Workflow

Edit `.github/workflows/acd_validation.yml`:

```yaml
# Add additional validation steps
- name: Custom Validation
  run: |
    # Your custom validation commands
    
# Add notifications
- name: Notify on Failure
  if: failure()
  run: |
    # Your notification logic
```

### Adding Language Support

The template supports any language. Add your language's comment style to your code:

**JavaScript/TypeScript:**
```javascript
/*
 * AI_PHASE: API_HANDLER
 * AI_STATUS: IMPLEMENTED
 * AI_COMPLEXITY: MEDIUM
 */
function handleRequest() {
    // code
}
```

**Ruby:**
```ruby
# AI_PHASE: DATA_VALIDATION
# AI_STATUS: IMPLEMENTED
# AI_COMPLEXITY: LOW
def validate_data(data)
  # code
end
```

**Go:**
```go
/*
 * AI_PHASE: CONCURRENCY
 * AI_STATUS: IMPLEMENTED
 * AI_COMPLEXITY: HIGH
 */
func processAsync(data []byte) error {
    // code
}
```

## Usage Examples

### Example 1: New Feature Development

1. **Plan the feature** - Define phases in `.acd/config.yml`
2. **Start implementation** - Mark as `PARTIAL`:
   ```cpp
   /*
    * AI_PHASE: NEW_FEATURE
    * AI_STATUS: PARTIAL
    * AI_COMPLEXITY: HIGH
    */
   ```
3. **Complete implementation** - Update to `IMPLEMENTED`
4. **Commit and update**:
   ```bash
   git commit -m "Implement new feature"
   # Update AI_COMMIT with the commit hash
   ```

### Example 2: Bug Fix

1. **Identify the issue** - Use `info ACD` in GDB if available
2. **Fix the code** - Change status to `FIXED`
3. **Document the fix** - Create fix summary:
   ```bash
   cp docs/fix_summaries/FIX_TEMPLATE.md docs/fix_summaries/FIX_20231020_memory_leak.md
   # Edit with fix details
   ```
4. **Update metadata**:
   ```cpp
   /*
    * AI_STATUS: FIXED
    * AI_COMMIT: new_commit_hash
    * AI_COMMIT_HISTORY: old_commit_hash, ...
    */
   ```

### Example 3: Refactoring

1. **Before refactoring** - Run validation:
   ```bash
   python3 scripts/validate_acd.py src/ --export before_refactor.json
   ```
2. **Refactor code** - Keep metadata updated
3. **After refactoring** - Validate again:
   ```bash
   python3 scripts/validate_acd.py src/ --export after_refactor.json
   ```
4. **Compare** - Ensure no metadata was lost

### Example 4: Code Review

1. **Generate report** for the PR:
   ```bash
   python3 scripts/acd_parser.py src/ --analyze --markdown pr_report.md
   ```
2. **Check dependencies**:
   ```bash
   python3 scripts/acd_parser.py src/ --dot dependencies.dot
   dot -Tpng dependencies.dot -o dependencies.png
   ```
3. **Review** - Include in PR description

## Troubleshooting

### Common Issues

**Q: Scripts don't execute**
```bash
# Solution: Make them executable
chmod +x scripts/*.sh
chmod +x scripts/*.py
```

**Q: Python import errors**
```bash
# Solution: Install required packages
pip install pyyaml
```

**Q: Validation fails on example files**
```bash
# Solution: Update commit hashes in examples
# Replace 'initial' with actual commit hashes
```

**Q: GitHub Actions workflow fails**
```bash
# Solution: Check that scripts/ directory is committed
git add scripts/
git commit -m "Add ACD scripts"
git push
```

**Q: Can't download ACD tools**
```bash
# Solution: Download manually from GitHub
# https://github.com/R-E-C-A-L-L-Foundation/Autonomous-Continuous-Development-ACD-Standard-Specification/tree/main/src
# https://github.com/R-E-C-A-L-L-Foundation/Autonomous-Continuous-Development-ACD-Standard-Specification/tree/main/scripts
```

### Getting Help

- **Documentation**: Read `docs/IMPLEMENTATION_GUIDE.md`
- **Examples**: Check `examples/` directory
- **Specification**: https://github.com/R-E-C-A-L-L-Foundation/Autonomous-Continuous-Development-ACD-Standard-Specification
- **Issues**: https://github.com/R-E-C-A-L-L-Foundation/Autonomous-Continuous-Development-ACD-Standard-Specification/issues

## Next Steps

After setup:

1. ✅ Review and understand the examples
2. ✅ Add metadata to your existing code
3. ✅ Set up CI/CD validation
4. ✅ Create your first fix summary
5. ✅ Generate dependency graphs
6. ✅ Share your experience

## Benefits of Using This Template

- **Quick Setup**: Get ACD running in minutes
- **Best Practices**: Pre-configured with recommended settings
- **CI/CD Ready**: Automated validation included
- **Examples**: Learn from working code
- **Documentation**: Comprehensive guides included
- **Flexibility**: Easy to customize for your needs

## Template Maintenance

This template is maintained as part of the ACD Specification. To get updates:

```bash
# Check for template updates
cd /tmp
git clone https://github.com/R-E-C-A-L-L-Foundation/Autonomous-Continuous-Development-ACD-Standard-Specification.git
cd ACD_Specification/template

# Compare with your project
diff -r . /path/to/your/project

# Merge updates as needed
```

---

**Powered by the [ACD Standard v1.0](https://github.com/R-E-C-A-L-L-Foundation/Autonomous-Continuous-Development-ACD-Standard-Specification)**  
© 2025 Timothy Deters / R.E.C.A.L.L. Foundation

For questions, issues, or contributions, visit:  
https://github.com/R-E-C-A-L-L-Foundation/Autonomous-Continuous-Development-ACD-Standard-Specification

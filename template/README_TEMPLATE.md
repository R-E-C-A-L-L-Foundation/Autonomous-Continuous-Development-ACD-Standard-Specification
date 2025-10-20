# ACD Repository Template

This directory contains a complete drop-in template for adopting the Autonomous Continuous Development (ACD) Standard in your projects.

## Quick Start

### For Existing Projects

```bash
# Copy template to your project
cd /path/to/your/project
cp -r /path/to/ACD_Specification/template/* .
cp -r /path/to/ACD_Specification/template/.acd .
cp -r /path/to/ACD_Specification/template/.github .
cp /path/to/ACD_Specification/template/.gitignore .gitignore.acd

# Initialize ACD
chmod +x scripts/acd_init.sh
./scripts/acd_init.sh

# Customize for your project
# 1. Edit .acd/config.yml with your phases
# 2. Edit README.md with your project info
# 3. Add SCIS metadata to your code
```

### For New Projects

```bash
# Create new project from template
mkdir my-new-project
cd my-new-project
git init

cp -r /path/to/ACD_Specification/template/* .
cp -r /path/to/ACD_Specification/template/.acd .
cp -r /path/to/ACD_Specification/template/.github .
cp /path/to/ACD_Specification/template/.gitignore .

# Initialize
chmod +x scripts/acd_init.sh
./scripts/acd_init.sh

# Customize and commit
git add .
git commit -m "Initialize project with ACD template"
```

## What's Included

- **Configuration** (`.acd/config.yml`) - Project-specific ACD settings
- **GitHub Actions** (`.github/workflows/`) - Automated validation
- **Documentation** (`docs/`) - Implementation guide and fix summary templates
- **Examples** (`examples/`) - C and Python code examples
- **Scripts** (`scripts/`) - Initialization and setup tools
- **Structure** - Pre-configured directory layout

## Documentation

For detailed usage instructions, see:
- [TEMPLATE_USAGE.md](../TEMPLATE_USAGE.md) - Complete template guide
- [docs/IMPLEMENTATION_GUIDE.md](docs/IMPLEMENTATION_GUIDE.md) - Implementation details
- [ACD Specification](../README.md) - Full ACD standard

## Features

✅ Drop-in ready - Copy and start using  
✅ Language agnostic - Works with any programming language  
✅ CI/CD integrated - GitHub Actions included  
✅ Examples provided - C and Python templates  
✅ Fully documented - Comprehensive guides  
✅ Customizable - Easy to adapt to your needs

## Support

- **Specification**: https://github.com/R-E-C-A-L-L-Foundation/Autonomous-Continuous-Development-ACD-Standard-Specification
- **Issues**: https://github.com/R-E-C-A-L-L-Foundation/Autonomous-Continuous-Development-ACD-Standard-Specification/issues
- **Tools Guide**: https://github.com/R-E-C-A-L-L-Foundation/Autonomous-Continuous-Development-ACD-Standard-Specification/blob/main/docs/TOOLS_GUIDE.md

---

**Part of the ACD Standard v1.0**  
© 2025 Timothy Deters / R.E.C.A.L.L. Foundation

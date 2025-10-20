# ACD Template - File Index

Complete reference of all files in this template.

## 📁 Directory Structure

```
template/
├── .acd/                           # ACD configuration
├── .github/workflows/              # CI/CD automation
├── acd_artifacts/                  # Generated artifacts (not committed)
├── docs/                          # Documentation
├── examples/                      # Example code
├── scripts/                       # Tools and utilities
├── src/                           # Your source code
└── tests/                         # Your tests
```

## 📄 Files Reference

### Root Files

| File | Purpose | Required |
|------|---------|----------|
| `README.md` | Project README with ACD info | ✅ Yes |
| `README_TEMPLATE.md` | Template information | ℹ️ Info |
| `GETTING_STARTED.md` | Setup checklist | 📖 Guide |
| `INDEX.md` | This file - complete reference | 📖 Guide |
| `.gitignore` | Git ignore patterns | ✅ Yes |

### Configuration (`.acd/`)

| File | Purpose | Required |
|------|---------|----------|
| `config.yml` | Project-specific ACD settings | ✅ Yes |

**Key settings:**
- Project information
- Phase definitions
- Validation rules
- Export preferences

### GitHub Actions (`.github/workflows/`)

| File | Purpose | Required |
|------|---------|----------|
| `acd_validation.yml` | Automated validation workflow | ⚠️ If using GitHub |

**Features:**
- Validates on push/PR
- Generates reports
- Comments on PRs
- Uploads artifacts

### Documentation (`docs/`)

| File | Purpose | Required |
|------|---------|----------|
| `IMPLEMENTATION_GUIDE.md` | Detailed implementation guide | 📖 Important |
| `QUICK_REFERENCE.md` | Quick command reference | 📖 Handy |
| `fix_summaries/FIX_TEMPLATE.md` | Template for documenting fixes | 📝 Template |

### Examples (`examples/`)

| File | Purpose | Required |
|------|---------|----------|
| `example_with_acd.c` | C example with SCIS metadata | 📖 Example |
| `example_with_acd.py` | Python example with SCIS metadata | 📖 Example |

**Shows:**
- Proper SCIS tag usage
- Various complexity levels
- Different status values
- Dependency tracking

### Scripts (`scripts/`)

| File | Purpose | Required |
|------|---------|----------|
| `acd_init.sh` | Initialization script | ✅ Yes |
| `validate_acd.py` | Metadata validator | ✅ Downloaded |
| `acd_parser.py` | Metadata parser/analyzer | ✅ Downloaded |
| `gdb_acd.py` | GDB extension | 📦 Optional |
| `README.md` | Scripts directory info | ℹ️ Info |

**Note:** The Python scripts are downloaded by `acd_init.sh`.

### Source Code (`src/`)

| File | Purpose | Required |
|------|---------|----------|
| `README.md` | Directory guide | ℹ️ Info |
| *(Your source files)* | Your code with SCIS metadata | ✅ Yes |

### Tests (`tests/`)

| File | Purpose | Required |
|------|---------|----------|
| `README.md` | Directory guide | ℹ️ Info |
| *(Your test files)* | Your tests | ⚠️ Recommended |

### Artifacts (`acd_artifacts/`)

| Directory/File | Purpose | Committed |
|----------------|---------|-----------|
| `README.md` | Directory info | ✅ Yes |
| `metadata.json` | Exported metadata | ❌ No |
| `analysis.json` | Analysis results | ❌ No |
| `report.md` | Analysis report | ❌ No |
| `dependencies.dot` | Dependency graph | ❌ No |
| `traces/` | Debug traces | ❌ No |
| `traces/README.md` | Traces info | ✅ Yes |

**Note:** Generated files are in `.gitignore`.

## 🎯 Essential Files for Quick Start

### Must Have (Required)

1. `.acd/config.yml` - Configuration
2. `scripts/acd_init.sh` - Initialization
3. `README.md` - Project documentation
4. `.gitignore` - Ignore patterns

### Should Have (Important)

5. `docs/IMPLEMENTATION_GUIDE.md` - How to implement
6. `docs/QUICK_REFERENCE.md` - Quick commands
7. `.github/workflows/acd_validation.yml` - CI/CD
8. `GETTING_STARTED.md` - Setup checklist

### Nice to Have (Helpful)

9. `examples/` - Learn from examples
10. `docs/fix_summaries/FIX_TEMPLATE.md` - Document fixes
11. `INDEX.md` - This reference
12. `README_TEMPLATE.md` - Template info

## 📝 File Descriptions

### Configuration Files

**`.acd/config.yml`**
- Defines project-specific phases
- Sets validation requirements
- Configures export formats
- Controls Git integration

**`.gitignore`**
- Ignores build artifacts
- Ignores generated ACD reports
- Keeps repository clean

### Documentation Files

**`docs/IMPLEMENTATION_GUIDE.md`**
- Step-by-step setup instructions
- SCIS metadata guide
- Best practices
- Troubleshooting tips

**`docs/QUICK_REFERENCE.md`**
- Tag reference table
- Code examples for multiple languages
- Common command patterns
- Workflow cheatsheet

**`docs/fix_summaries/FIX_TEMPLATE.md`**
- Template for documenting fixes
- Includes all required sections
- Provides example content

### Example Files

**`examples/example_with_acd.c`**
- C code with proper SCIS metadata
- Shows various tag combinations
- Demonstrates different complexities
- Includes dependency tracking

**`examples/example_with_acd.py`**
- Python code with SCIS metadata
- Comment-style metadata format
- Multiple function examples
- Error handling patterns

### Script Files

**`scripts/acd_init.sh`**
- One-command setup
- Downloads required tools
- Creates directory structure
- Configures Git integration

**`scripts/validate_acd.py`** (downloaded)
- Validates SCIS metadata
- Checks required tags
- Generates reports
- Exports to JSON

**`scripts/acd_parser.py`** (downloaded)
- Parses metadata
- Analyzes implementation status
- Generates dependency graphs
- Exports to multiple formats

**`scripts/gdb_acd.py`** (downloaded)
- GDB extension for debugging
- `info ACD` command
- `ACD-suggest` command
- Shows context during debugging

### Workflow Files

**`.github/workflows/acd_validation.yml`**
- GitHub Actions workflow
- Validates on every push/PR
- Generates and uploads reports
- Comments on pull requests

## 🔄 File Lifecycle

### Static Files (Never Change)

- `examples/` - Reference examples
- `docs/fix_summaries/FIX_TEMPLATE.md` - Template
- `README_TEMPLATE.md` - Template info
- `INDEX.md` - This file

### Configuration Files (Edit Once)

- `.acd/config.yml` - Customize for your project
- `README.md` - Update with project info
- `.github/workflows/acd_validation.yml` - Adjust if needed

### Working Files (Frequent Updates)

- `src/` - Your source code
- `tests/` - Your tests
- `docs/fix_summaries/` - Add new fix summaries

### Generated Files (Automatic)

- `acd_artifacts/*.json` - Validation/analysis output
- `acd_artifacts/*.md` - Reports
- `acd_artifacts/traces/*.json` - Debug traces

## 📦 What to Commit

### Always Commit

- Configuration files
- Documentation
- Source code with metadata
- Tests
- Scripts
- README files in empty directories

### Never Commit

- Generated artifacts (`acd_artifacts/*.json`, `*.md`, `*.csv`)
- Build artifacts
- Dependencies
- Temporary files

## 🚀 Usage Patterns

### First Time Setup

1. Copy template to your project
2. Run `scripts/acd_init.sh`
3. Edit `.acd/config.yml`
4. Update `README.md`

### Daily Development

1. Write code with SCIS metadata
2. Validate: `python3 scripts/validate_acd.py src/`
3. Commit changes
4. CI/CD runs automatically

### Debugging

1. Run with GDB: `gdb -x scripts/gdb_acd.py ./program`
2. Use `info ACD` to see context
3. Use `ACD-suggest` for suggestions
4. Document fix in `docs/fix_summaries/`

### Code Review

1. Generate report: `python3 scripts/acd_parser.py src/ --markdown report.md`
2. Check dependencies: `python3 scripts/acd_parser.py src/ --dot deps.dot`
3. Review metadata completeness
4. Verify CI/CD passes

---

## 📚 Additional Resources

- **Full Specification**: [ACD_Specification/README.md](../README.md)
- **Template Usage Guide**: [TEMPLATE_USAGE.md](../TEMPLATE_USAGE.md)
- **Tools Guide**: [ACD_Specification/docs/TOOLS_GUIDE.md](../docs/TOOLS_GUIDE.md)
- **GitHub**: https://github.com/RECALLInstituteACD/Autonomous-Continuous-Development-ACD-Standard-Specification

---

**Last Updated**: October 2025  
**Template Version**: 1.0  
**ACD Version**: 1.0

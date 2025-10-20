# ACD Implementation Guide

This guide provides step-by-step instructions for implementing the ACD Specification in your project.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Adding SCIS Metadata](#adding-scis-metadata)
4. [Maintaining Commit History](#maintaining-commit-history)
5. [Validation and CI/CD](#validation-and-cicd)
6. [Creating Fix Summaries](#creating-fix-summaries)
7. [Best Practices](#best-practices)

## Prerequisites

- Git repository
- Python 3.7 or higher
- (Optional) GDB for enhanced debugging
- (Optional) PyYAML for configuration: `pip install pyyaml`

## Quick Start

### 1. Initialize ACD in Your Repository

```bash
# Run the initialization script
chmod +x scripts/acd_init.sh
./scripts/acd_init.sh
```

This will:
- Create the required directory structure
- Download ACD tools
- Set up `.gitignore` entries
- Create configuration files

### 2. Configure Your Project

Edit `.acd/config.yml` to define your project's phases:

```yaml
phases:
  - name: "INIT"
    description: "Initialization code"
    complexity: "MEDIUM"
  
  - name: "YOUR_CUSTOM_PHASE"
    description: "Description of your phase"
    complexity: "MEDIUM"
```

### 3. Add Metadata to Your Code

Add SCIS metadata comments to your functions:

**C/C++ Example:**
```cpp
/*
 * AI_PHASE: INIT
 * AI_STATUS: IMPLEMENTED
 * AI_COMPLEXITY: LOW
 * AI_NOTE: Initializes the application context
 * AI_DEPENDENCIES: 
 * AI_COMMIT: a1b2c3d
 */
void initialize() {
    // Your code
}
```

**Python Example:**
```python
# AI_PHASE: INIT
# AI_STATUS: IMPLEMENTED
# AI_COMPLEXITY: LOW
# AI_NOTE: Initializes the application context
# AI_DEPENDENCIES: 
# AI_COMMIT: a1b2c3d
def initialize():
    """Initialize the application."""
    pass
```

### 4. Validate Your Metadata

```bash
python3 scripts/validate_acd.py src/
```

## Adding SCIS Metadata

### Required Tags

Every function should have at minimum:

```
AI_PHASE: <phase_name>
AI_STATUS: <status_value>
```

### Recommended Tags

For production code, include:

```
AI_PHASE: <phase_name>
AI_STATUS: <status_value>
AI_COMPLEXITY: <complexity_value>
AI_NOTE: <description>
AI_DEPENDENCIES: <comma_separated_phases>
AI_COMMIT: <git_sha>
```

### Status Values

- `IMPLEMENTED` - Code is complete and tested
- `PARTIAL` - Code is incomplete or partially working
- `NOT_STARTED` - Stub or placeholder only
- `FIXED` - Code was broken and has been repaired
- `DEPRECATED` - Code is obsolete but not yet removed

### Complexity Values

- `LOW` - Simple, straightforward logic
- `MEDIUM` - Moderate complexity
- `HIGH` - Complex logic with multiple concerns
- `CRITICAL` - Mission-critical or error-prone

## Maintaining Commit History

### The Workflow

1. **Before Making Changes**: Note the current `AI_COMMIT` value
2. **Make Your Changes**: Edit the code as needed
3. **Commit Your Changes**: `git commit -m "Your message"`
4. **Update Metadata**: 
   - Set `AI_COMMIT` to the new commit hash
   - Prepend old commit to `AI_COMMIT_HISTORY`

### Example Evolution

```cpp
// Initial implementation (commit: abc123f)
/*
 * AI_PHASE: INIT
 * AI_STATUS: PARTIAL
 * AI_COMMIT: abc123f
 */

// After first fix (commit: def456a)
/*
 * AI_PHASE: INIT
 * AI_STATUS: IMPLEMENTED
 * AI_COMMIT: def456a
 * AI_COMMIT_HISTORY: abc123f
 */

// After optimization (commit: ghi789b)
/*
 * AI_PHASE: INIT
 * AI_STATUS: IMPLEMENTED
 * AI_COMMIT: ghi789b
 * AI_COMMIT_HISTORY: def456a, abc123f
 */
```

### Automated Commit History

You can create a Git hook to automate this process. Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# TODO: Add script to update AI_COMMIT fields automatically
```

## Validation and CI/CD

### Local Validation

Run validation before committing:

```bash
# Basic validation
python3 scripts/validate_acd.py src/

# Validation with export
python3 scripts/validate_acd.py src/ --export acd_artifacts/metadata.json

# Verbose output
python3 scripts/validate_acd.py src/ --verbose
```

### CI/CD Integration

The template includes a GitHub Actions workflow (`.github/workflows/acd_validation.yml`) that:
- Validates ACD metadata on every push and PR
- Generates reports
- Uploads artifacts
- Comments on PRs with validation results

### Custom CI/CD

For other CI/CD systems, add these steps:

```yaml
- name: Validate ACD
  run: python3 scripts/validate_acd.py src/

- name: Generate Report
  run: python3 scripts/acd_parser.py src/ --analyze --markdown report.md
```

## Creating Fix Summaries

Document significant fixes in `docs/fix_summaries/`:

### Fix Summary Template

Create a file like `docs/fix_summaries/FIX_YYYYMMDD_issue_name.md`:

```markdown
# Fix Summary: [Issue Name]

## Issue Description
What problem was encountered?

## Root Cause
- AI_PHASE: [AFFECTED_PHASE]
- Technical analysis of the underlying issue

## Solution
Implementation details of the fix

## Verification
How the fix was tested and validated

## Related ACD Phases
- PHASE_NAME (AI_STATUS: STATUS)

## Commit References
- Main fix: [commit_hash]
- Follow-up: [commit_hash]
```

## Best Practices

### 1. Start Simple

Begin with required tags only:
```cpp
/*
 * AI_PHASE: YOUR_PHASE
 * AI_STATUS: IMPLEMENTED
 */
```

Add more tags as needed.

### 2. Use Consistent Phase Names

Define your phases in `.acd/config.yml` and use them consistently across your codebase.

### 3. Keep Metadata Current

Update `AI_STATUS` as implementation progresses:
- Start with `PARTIAL` or `NOT_STARTED`
- Change to `IMPLEMENTED` when complete
- Use `FIXED` when repairing issues

### 4. Document Dependencies

List all phases your code depends on:
```
AI_DEPENDENCIES: INIT, ERROR_HANDLING, VALIDATION
```

This helps with:
- Debugging initialization order issues
- Understanding code relationships
- Generating dependency graphs

### 5. Leverage Tools

Use the provided tools:
- `validate_acd.py` for validation
- `acd_parser.py` for analysis and visualization
- `gdb_acd.py` for enhanced debugging

### 6. Create Fix Summaries

Document significant issues and their resolutions. This builds institutional memory for autonomous agents.

### 7. Validate Regularly

Run validation:
- Before committing
- In CI/CD pipelines
- After refactoring

### 8. Review Generated Reports

Check the reports generated by `acd_parser.py`:
```bash
python3 scripts/acd_parser.py src/ --analyze --markdown report.md
cat report.md
```

## Advanced Features

### Dependency Graphs

Generate visual dependency graphs:

```bash
python3 scripts/acd_parser.py src/ --dot dependencies.dot
dot -Tpng dependencies.dot -o dependencies.png
```

### GDB Integration

Use ACD-aware debugging:

```bash
gdb -x scripts/gdb_acd.py ./your_program

# Inside GDB:
(gdb) info ACD
(gdb) ACD-suggest
```

### Export Formats

Export metadata in various formats:

```bash
# JSON export
python3 scripts/acd_parser.py src/ --json metadata.json

# CSV export
python3 scripts/acd_parser.py src/ --csv metadata.csv

# Markdown report
python3 scripts/acd_parser.py src/ --markdown report.md
```

## Troubleshooting

### Validation Errors

**Problem**: "Missing required tag AI_PHASE"
**Solution**: Add the required tag to the function metadata

**Problem**: "Unknown phase name"
**Solution**: Define the phase in `.acd/config.yml`

### Tool Issues

**Problem**: "PyYAML not installed"
**Solution**: `pip install pyyaml`

**Problem**: "Permission denied" on scripts
**Solution**: `chmod +x scripts/*.sh scripts/*.py`

## Getting Help

- [ACD Specification](https://github.com/RECALLInstituteACD/Autonomous-Continuous-Development-ACD-Standard-Specification)
- [Tools Guide](https://github.com/RECALLInstituteACD/Autonomous-Continuous-Development-ACD-Standard-Specification/blob/main/docs/TOOLS_GUIDE.md)
- [Examples](examples/)

## Next Steps

1. Add SCIS metadata to all your functions
2. Set up CI/CD validation
3. Create your first fix summary
4. Generate dependency graphs
5. Share your experience with the ACD community

---

**Powered by the [ACD Standard v1.0](https://github.com/RECALLInstituteACD/Autonomous-Continuous-Development-ACD-Standard-Specification)**

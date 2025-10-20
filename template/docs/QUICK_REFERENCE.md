# ACD Quick Reference Guide

Quick reference for using ACD in your project.

## SCIS Metadata Tags

### Required Tags

```
AI_PHASE: <phase_name>
AI_STATUS: <status_value>
```

### Recommended Tags

```
AI_COMPLEXITY: <complexity_value>
AI_NOTE: <description>
AI_DEPENDENCIES: <comma_separated_phases>
AI_COMMIT: <git_sha>
```

### All Available Tags

| Tag | Description | Example |
|-----|-------------|---------|
| `AI_PHASE` | Functional phase/category | `INIT`, `ERROR_HANDLING` |
| `AI_STATUS` | Implementation status | `IMPLEMENTED`, `PARTIAL`, `NOT_STARTED`, `FIXED`, `DEPRECATED` |
| `AI_COMPLEXITY` | Risk/difficulty level | `LOW`, `MEDIUM`, `HIGH`, `CRITICAL` |
| `AI_NOTE` | Human-readable description | "Initializes the context" |
| `AI_DEPENDENCIES` | Required phases | `INIT, ERROR_HANDLING` |
| `AI_COMMIT` | Current git commit | `a1b2c3d` |
| `AI_COMMIT_HISTORY` | Previous commits | `def456a, ghi789b` |
| `AI_PATTERN` | Implementation pattern | `SINGLETON_V1` |
| `AI_STRATEGY` | High-level approach | "Use caching for performance" |
| `AI_VERSION` | Code version | `1.0` |
| `AI_CHANGE` | Recent change description | "Fixed memory leak" |
| `SOURCE_API_REF` | Source API reference | `malloc() - stdlib.h` |
| `TARGET_API_REF` | Target API reference | `backend_alloc() - backend.h` |

## Code Examples

### C/C++

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

### Python

```python
# AI_PHASE: VALIDATION
# AI_STATUS: IMPLEMENTED
# AI_COMPLEXITY: MEDIUM
# AI_NOTE: Validates input data
# AI_DEPENDENCIES: ERROR_HANDLING
# AI_COMMIT: a1b2c3d
def validate(data):
    """Validate input data."""
    pass
```

### JavaScript/TypeScript

```javascript
/*
 * AI_PHASE: API_HANDLER
 * AI_STATUS: IMPLEMENTED
 * AI_COMPLEXITY: HIGH
 * AI_NOTE: Handles user authentication
 * AI_DEPENDENCIES: VALIDATION, DATABASE
 * AI_COMMIT: a1b2c3d
 */
async function authenticate(credentials) {
    // Your code
}
```

## Common Commands

### Validation

```bash
# Validate all source files
python3 scripts/validate_acd.py src/

# Validate with verbose output
python3 scripts/validate_acd.py src/ --verbose

# Validate and export to JSON
python3 scripts/validate_acd.py src/ --export metadata.json

# Validate specific file
python3 scripts/validate_acd.py src/myfile.c
```

### Analysis

```bash
# Analyze implementation status
python3 scripts/acd_parser.py src/ --analyze

# Generate markdown report
python3 scripts/acd_parser.py src/ --markdown report.md

# Export to JSON
python3 scripts/acd_parser.py src/ --json metadata.json

# Generate dependency graph
python3 scripts/acd_parser.py src/ --dot deps.dot
dot -Tpng deps.dot -o deps.png
```

### Debugging

```bash
# Start GDB with ACD extension
gdb -x scripts/gdb_acd.py ./your_program

# Inside GDB:
(gdb) break main
(gdb) run
(gdb) info ACD              # Show ACD context
(gdb) ACD-suggest           # Get debugging suggestions
```

## Workflow Cheatsheet

### Adding New Code

1. Write function with SCIS metadata
2. Set `AI_STATUS: PARTIAL` initially
3. Complete implementation
4. Change `AI_STATUS: IMPLEMENTED`
5. Commit: `git commit -m "Add feature"`
6. Update `AI_COMMIT` with commit hash

### Fixing a Bug

1. Identify issue (use `info ACD` in GDB)
2. Fix the code
3. Change `AI_STATUS: FIXED`
4. Create fix summary in `docs/fix_summaries/`
5. Commit: `git commit -m "Fix bug"`
6. Update `AI_COMMIT`, prepend old to `AI_COMMIT_HISTORY`

### Refactoring

1. Validate before: `python3 scripts/validate_acd.py src/ --export before.json`
2. Refactor code
3. Keep metadata updated
4. Validate after: `python3 scripts/validate_acd.py src/ --export after.json`
5. Commit changes

### Code Review

1. Generate report: `python3 scripts/acd_parser.py src/ --markdown pr_report.md`
2. Check dependencies: `python3 scripts/acd_parser.py src/ --dot deps.dot`
3. Review metadata completeness
4. Check for new phases or missing dependencies

## Status Values

| Status | When to Use |
|--------|-------------|
| `IMPLEMENTED` | Code is complete and tested |
| `PARTIAL` | Code is incomplete, work in progress |
| `NOT_STARTED` | Stub or placeholder only |
| `FIXED` | Code was broken and has been repaired |
| `DEPRECATED` | Code is obsolete but not yet removed |

## Complexity Values

| Complexity | Description |
|------------|-------------|
| `LOW` | Simple, straightforward logic |
| `MEDIUM` | Moderate complexity, some state management |
| `HIGH` | Complex logic, multiple concerns |
| `CRITICAL` | Mission-critical, error-prone, or high-risk |

## Git Commit History Workflow

```bash
# Before making changes, note current AI_COMMIT
# Example: AI_COMMIT: abc123f

# Make your changes and commit
git commit -m "Your change"
# New commit: def456a

# Update metadata:
# AI_COMMIT: def456a
# AI_COMMIT_HISTORY: abc123f, [previous history]
```

## Common Patterns

### API Translation Pattern

```cpp
/*
 * AI_PHASE: API_TRANSLATION
 * AI_STATUS: IMPLEMENTED
 * AI_COMPLEXITY: MEDIUM
 * AI_PATTERN: API_WRAPPER_V1
 * SOURCE_API_REF: original_function() - source_api.h
 * TARGET_API_REF: target_function() - target_api.h
 */
int wrapper_function(params) {
    return target_function(params);
}
```

### Error Handling Pattern

```python
# AI_PHASE: ERROR_HANDLING
# AI_STATUS: IMPLEMENTED
# AI_COMPLEXITY: LOW
# AI_PATTERN: EXCEPTION_WRAPPER_V1
class ApplicationError(Exception):
    """Application-specific error."""
    pass
```

## CI/CD Integration

The template includes GitHub Actions workflow:
- `.github/workflows/acd_validation.yml`
- Runs on every push and PR
- Validates metadata
- Generates reports
- Comments on PRs

### Manual CI/CD Steps

```yaml
steps:
  - name: Validate ACD
    run: python3 scripts/validate_acd.py src/
  
  - name: Generate Report
    run: python3 scripts/acd_parser.py src/ --analyze
```

## Troubleshooting

### Validation Errors

**Missing required tag**
- Add the required tag to metadata block

**Unknown phase name**
- Add phase to `.acd/config.yml`

**Invalid commit hash**
- Use 7-40 character hex string
- Get from: `git rev-parse --short HEAD`

### Tool Errors

**PyYAML not installed**
```bash
pip install pyyaml
```

**Script not executable**
```bash
chmod +x scripts/*.sh
```

**Import errors**
```bash
# Ensure scripts are in correct location
ls -l scripts/validate_acd.py
```

## Configuration

Edit `.acd/config.yml` to customize:

```yaml
# Define project phases
phases:
  - name: "YOUR_PHASE"
    description: "Description"
    complexity: "MEDIUM"

# Set required tags
validation:
  required_tags:
    - "AI_PHASE"
    - "AI_STATUS"
```

## Resources

- **Specification**: [README.md](../README.md)
- **Implementation Guide**: [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)
- **Template Usage**: [TEMPLATE_USAGE.md](../../TEMPLATE_USAGE.md)
- **GitHub**: https://github.com/RECALLInstituteACD/Autonomous-Continuous-Development-ACD-Standard-Specification

---

**Quick Tip**: Start simple with just `AI_PHASE` and `AI_STATUS`, then add more tags as needed.

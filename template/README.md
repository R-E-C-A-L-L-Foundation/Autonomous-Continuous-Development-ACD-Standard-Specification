# [Your Project Name] - ACD Enabled

This project follows the [Autonomous Continuous Development (ACD) Standard v1.0](https://github.com/R-E-C-A-L-L-Foundation/Autonomous-Continuous-Development-ACD-Standard-Specification).

## Quick Start

This repository is configured to use the ACD Specification, enabling autonomous AI agents to understand, debug, and improve your codebase with complete historical context.

### What is ACD?

The Autonomous Continuous Development (ACD) standard transforms stateless AI agents into context-aware collaborators by providing:
- **Complete Historical Memory** - Full tracking of every decision ever made
- **Cognitive Segmentation** - Code organized into logical, functional units
- **Implementation Tracking** - Operational maturity explicitly declared
- **Risk Profiling** - Inherent cognitive difficulty quantified
- **Full Traceability** - Complete graph of development decisions

### Repository Structure

```
.
├── .acd/                    # ACD configuration
│   └── config.yml          # Project-specific ACD settings
├── docs/                   # Documentation
│   └── fix_summaries/      # Historical fix documentation
├── examples/               # Example code with ACD metadata
├── scripts/                # ACD tools and utilities
├── src/                    # Your source code (instrumented with SCIS)
└── tests/                  # Your tests
```

### Getting Started

1. **Install ACD Tools**
   ```bash
   ./scripts/acd_init.sh
   ```

2. **Add SCIS Metadata to Your Code**
   
   Add ACD metadata comments to your functions:
   ```cpp
   /*
    * AI_PHASE: YOUR_PHASE_NAME
    * AI_STATUS: IMPLEMENTED
    * AI_COMPLEXITY: MEDIUM
    * AI_NOTE: Description of what this code does
    * AI_DEPENDENCIES: INIT, ERROR_HANDLING
    * AI_COMMIT: abc123f
    */
   void yourFunction() {
       // Your code here
   }
   ```

3. **Validate Your Metadata**
   ```bash
   python3 scripts/validate_acd.py src/
   ```

4. **Enable CI/CD Validation**
   
   The included GitHub Actions workflow automatically validates ACD metadata on every commit.

## ACD Features in This Repository

- ✅ **SCIS Tags** - Source Code Intelligence Standard metadata in all code
- ✅ **GDB Extension** - Enhanced debugging with `info ACD` and `ACD-suggest`
- ✅ **Validation Tools** - Automated metadata validation
- ✅ **CI/CD Integration** - Continuous validation in GitHub Actions
- ✅ **Fix Summaries** - Historical documentation of all fixes
- ✅ **Dependency Tracking** - Automatic dependency graph generation

## Development Workflow

1. **Write Code** - Add SCIS metadata to your functions
2. **Commit Changes** - Update `AI_COMMIT` fields with git commit hash
3. **Update History** - Prepend old commit to `AI_COMMIT_HISTORY`
4. **Validate** - Run validation to ensure metadata completeness
5. **Document Fixes** - Create fix summaries for significant issues

## ACD Tools Available

- `scripts/validate_acd.py` - Validate SCIS metadata
- `scripts/acd_parser.py` - Parse and analyze ACD metadata
- `scripts/gdb_acd.py` - GDB extension for ACD-aware debugging
- `scripts/acd_init.sh` - Initialize ACD in your repository

## Documentation

- [ACD Specification](https://github.com/R-E-C-A-L-L-Foundation/Autonomous-Continuous-Development-ACD-Standard-Specification)
- [Implementation Guide](docs/IMPLEMENTATION_GUIDE.md)
- [Fix Summaries](docs/fix_summaries/)
- [Tools Guide](https://github.com/R-E-C-A-L-L-Foundation/Autonomous-Continuous-Development-ACD-Standard-Specification/blob/main/docs/TOOLS_GUIDE.md)

## Contributing

When contributing to this project:
1. Add SCIS metadata to all new functions
2. Keep metadata current as code evolves
3. Document significant fixes in `docs/fix_summaries/`
4. Run validation before committing

## License

[Your License Here]

---

**Powered by the [ACD Standard v1.0](https://github.com/R-E-C-A-L-L-Foundation/Autonomous-Continuous-Development-ACD-Standard-Specification)**  
© 2025 Timothy Deters / R.E.C.A.L.L. Foundation

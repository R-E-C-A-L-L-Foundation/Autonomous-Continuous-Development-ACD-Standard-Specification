# ACD Scripts Directory

This directory contains ACD tools and utilities.

## Tools

When you run `acd_init.sh`, the following tools will be downloaded:

- **validate_acd.py** - Validates SCIS metadata in source files
- **acd_parser.py** - Parses and analyzes ACD metadata, generates reports
- **gdb_acd.py** - GDB extension for ACD-aware debugging

## Usage

See [docs/IMPLEMENTATION_GUIDE.md](../docs/IMPLEMENTATION_GUIDE.md) for detailed usage instructions.

### Quick Reference

```bash
# Validate metadata
python3 scripts/validate_acd.py src/

# Generate analysis report
python3 scripts/acd_parser.py src/ --analyze --markdown report.md

# Use GDB extension
gdb -x scripts/gdb_acd.py ./your_program
```

## Adding Custom Scripts

You can add your own project-specific scripts to this directory.

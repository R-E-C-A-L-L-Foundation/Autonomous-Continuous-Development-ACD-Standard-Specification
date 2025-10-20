# ACD Tools and Examples Guide

**Copyright (C) 2025 Timothy Deters / The RECALL Institute for Autonomous Continuous Development**

This document is part of the ACD Specification, licensed under the GNU General Public License v3.0.  
For commercial licensing inquiries, contact The RECALL Institute for Autonomous Continuous Development.  
Patent Pending: U.S. Application No. 63/898,838

---

This document provides detailed information about the tools and examples in the ACD Specification repository.

## Table of Contents

1. [Core Tools](#core-tools)
2. [Examples](#examples)
3. [Usage Guide](#usage-guide)
4. [Integration](#integration)

---

## Core Tools

### 1. ACD Validator (`src/validate_acd.py`)

The validator parses and validates ACD metadata in source code files.

**Features:**
- Parses SCIS tags from C/C++ comments
- Validates required vs optional tags
- Verifies dependency chains
- Exports metadata to JSON
- Generates completeness reports

**Usage:**
```bash
# Validate a directory
python3 src/validate_acd.py /path/to/source

# Validate and export to JSON
python3 src/validate_acd.py /path/to/source --export acd_metadata.json

# Validate with repository context
python3 src/validate_acd.py /path/to/source --repository terminills/my_repo

# Verbose output
python3 src/validate_acd.py /path/to/source --verbose
```

### 2. ACD Parser (`src/acd_parser.py`)

Advanced parser for extracting, analyzing, and exporting ACD metadata.

**Features:**
- Parse metadata and organize by phase/file
- Export to JSON, CSV, Markdown, DOT formats
- Generate dependency graphs
- Analyze implementation status
- Find missing dependencies

**Usage:**
```bash
# Analyze implementation status
python3 src/acd_parser.py /path/to/source --analyze

# Export to multiple formats
python3 src/acd_parser.py /path/to/source --json output.json --csv output.csv --markdown report.md --dot dependencies.dot
```

### 3. GDB Extension (`scripts/gdb_acd.py`)

GDB extension providing ACD-aware debugging commands.

**Commands:**
- `info ACD` - Display ACD metadata for current location
- `ACD-suggest` - Get automated debugging suggestions

**Usage:**
```bash
# Load extension when starting GDB
gdb -x scripts/gdb_acd.py ./your_program

# Or load from within GDB
(gdb) source scripts/gdb_acd.py

# Use commands
(gdb) info ACD
(gdb) ACD-suggest
```

### 4. ACD Metadata Header (`src/ai_metadata.h`)

C/C++ header file providing constants and utilities for ACD metadata.

**Usage:**
```c++
#include "ai_metadata.h"

// Use constants
if (status == ACD_STATUS_IMPLEMENTED) {
    // Production ready
}

// Optional: Enable runtime API
#define ACD_ENABLE_RUNTIME_API
#include "ai_metadata.h"

bool ready = acd_is_production_ready(ACD_STATUS_IMPLEMENTED);
bool risky = acd_is_high_risk(ACD_COMPLEXITY_CRITICAL);
```

---

## Examples

### 1. Memory API Example (`examples/memory_api.cpp`)
Demonstrates memory management functions with various implementation states.

### 2. Stream API Example (`examples/stream_api.cpp`)
Demonstrates stream and event management operations.

### 3. Header Example (`examples/header_example.cpp`)
Demonstrates using the `ai_metadata.h` header file.

---

## Usage Guide

### Adding ACD Metadata to Your Code

```c++
/*
 * AI_PHASE: YOUR_PHASE_NAME
 * AI_STATUS: IMPLEMENTED
 * AI_COMPLEXITY: MEDIUM
 * AI_NOTE: Description of what this function does
 * AI_DEPENDENCIES: OTHER_PHASE1, OTHER_PHASE2
 * AI_COMMIT: abc1234
 * AI_COMMIT_HISTORY: def5678, ghi9012
 */
void your_function() {
    // Implementation
}
```

### Workflow Integration

**CI/CD Pipeline:**
```yaml
- name: Validate ACD Metadata
  run: |
    python3 src/validate_acd.py src/ --export acd_report.json
    python3 src/acd_parser.py src/ --analyze
```

**Development Workflow:**
1. Write code with ACD metadata
2. Validate with `validate_acd.py`
3. Debug with GDB + `gdb_acd.py`
4. Analyze with `acd_parser.py`
5. Commit with updated `AI_COMMIT`

---

## Best Practices

1. **Be Consistent:** Use standard phase names
2. **Stay Current:** Update `AI_COMMIT` and `AI_COMMIT_HISTORY`
3. **Be Thorough:** Include recommended tags
4. **Document Fixes:** Use `FIX_REASON` when fixing bugs
5. **Validate Early:** Run validation frequently
6. **Use Analysis:** Check for high-risk implementations
7. **Leverage GDB:** Use ACD-aware debugging

---

For complete reference, see [README.md](../README.md) and the ACD Standard Specification v1.0.

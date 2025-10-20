# Source Code Directory

Place your source code files here.

## Adding ACD Metadata

All source files should include SCIS (Source Code Intelligence Standard) metadata.

### Example (C/C++)

```cpp
/*
 * AI_PHASE: YOUR_PHASE
 * AI_STATUS: IMPLEMENTED
 * AI_COMPLEXITY: MEDIUM
 * AI_NOTE: Description of the function
 * AI_DEPENDENCIES: OTHER_PHASE
 * AI_COMMIT: abc123f
 */
void your_function() {
    // implementation
}
```

### Example (Python)

```python
# AI_PHASE: YOUR_PHASE
# AI_STATUS: IMPLEMENTED
# AI_COMPLEXITY: MEDIUM
# AI_NOTE: Description of the function
# AI_DEPENDENCIES: OTHER_PHASE
# AI_COMMIT: abc123f
def your_function():
    """Function docstring."""
    pass
```

## Validation

Validate your metadata:

```bash
python3 scripts/validate_acd.py src/
```

## More Information

See [docs/IMPLEMENTATION_GUIDE.md](../docs/IMPLEMENTATION_GUIDE.md) for detailed instructions.

# Tests Directory

Place your test files here.

## Testing with ACD

While test files don't typically require ACD metadata, you can optionally add it to complex test fixtures or utilities.

## Running Tests

Add your test commands to CI/CD workflow (`.github/workflows/acd_validation.yml`):

```yaml
- name: Run Tests
  run: |
    # Your test commands here
    # pytest tests/
    # npm test
    # go test ./...
```

## Test Organization

Consider organizing tests by phase:

```
tests/
├── test_init.py
├── test_error_handling.py
├── test_core_logic.py
└── fixtures/
```

This makes it easier to correlate tests with ACD phases in your source code.

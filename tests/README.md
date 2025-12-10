# Tests Directory

This directory contains test scripts for the Context Window Labs package.

## Test Files

### 1. `test_installation.py`
Simple installation verification script that tests all imports and public API.

**Run:**
```bash
python tests/test_installation.py
```

**Tests:**
- ✓ Main package import
- ✓ Helper functions import
- ✓ Lab runner imports
- ✓ Individual lab imports
- ✓ Public API exports

### 2. `test_quick_start.py`
Displays the quick start guide for using the package.

**Run:**
```bash
python tests/test_quick_start.py
```

**Shows:**
- Package version
- Import examples
- Lab 1 trial options
- Lab 2 dataset options
- Lab 3 & 4 usage
- Helper function examples

### 3. `test_package.py`
Comprehensive pytest test suite for the package (requires pytest).

**Run:**
```bash
# Install pytest first
pip install pytest

# Run tests
pytest tests/test_package.py -v

# Run with coverage
pip install pytest-cov
pytest tests/test_package.py --cov=context_window_labs --cov-report=html
```

**Test Classes:**
- `TestPackageImports` - Tests all import statements
- `TestPublicAPI` - Validates `__all__` exports
- `TestLab1` - Lab 1 specific tests (including trial validation)
- `TestLab2` - Lab 2 specific tests
- `TestLab3` - Lab 3 specific tests
- `TestLab4` - Lab 4 specific tests
- `TestAzureOpenAIHelper` - Helper module tests

## Running All Tests

### Simple Tests (No Dependencies)
```bash
python tests/test_installation.py
python tests/test_quick_start.py
```

### Pytest Suite (Requires pytest)
```bash
# Install pytest
pip install -e ".[dev]"

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_package.py -v

# Run specific test class
pytest tests/test_package.py::TestPackageImports -v

# Run specific test method
pytest tests/test_package.py::TestPackageImports::test_import_main_package -v

# Run with coverage report
pytest tests/ --cov=context_window_labs --cov-report=html
```

## Test Results

All tests should pass if the package is correctly installed:

```
✓ Test 1: Import main package
✓ Test 2: Import helper functions
✓ Test 3: Import lab runners
✓ Test 4: Import from individual labs
✓ Test 5: Check public API

ALL TESTS PASSED! ✓
```

## Adding New Tests

When adding new functionality:

1. Add simple verification to `test_installation.py`
2. Add pytest test cases to `test_package.py`
3. Update this README with test descriptions

## CI/CD Integration

These tests can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Install package
  run: pip install -e .

- name: Run simple tests
  run: |
    python tests/test_installation.py
    python tests/test_quick_start.py

- name: Run pytest suite
  run: pytest tests/ -v --cov=context_window_labs
```

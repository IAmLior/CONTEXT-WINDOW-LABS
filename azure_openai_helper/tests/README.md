# Azure OpenAI Helper Tests

This directory contains tests for the Azure OpenAI helper module.

## Test Files

### 1. `test_validation.py`
Tests configuration validation and environment setup.

**Tests:**
- Environment variable validation
- Configuration error handling
- Azure OpenAI client initialization
- API endpoint validation

**Run:**
```bash
python azure_openai_helper/tests/test_validation.py
```

### 2. `test_multi_model.py`
Tests multi-model support (primary and secondary models).

**Tests:**
- Primary model (GPT-4o) queries
- Secondary model (Phi-4-mini) queries
- Model switching functionality
- Error handling for unavailable models

**Run:**
```bash
python azure_openai_helper/tests/test_multi_model.py
```

## Running All Tests

### Using Python directly
```bash
# Run all tests
python azure_openai_helper/tests/test_validation.py
python azure_openai_helper/tests/test_multi_model.py
```

### Using pytest
```bash
# Install pytest if needed
pip install pytest

# Run all tests in this directory
pytest azure_openai_helper/tests/ -v

# Run specific test file
pytest azure_openai_helper/tests/test_validation.py -v
pytest azure_openai_helper/tests/test_multi_model.py -v
```

## Prerequisites

Before running tests, ensure you have:

1. **Environment Variables Set**
   Create a `.env` file in the project root:
   ```env
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_API_KEY=your-api-key-here
   AZURE_OPENAI_API_VERSION=2024-02-15-preview
   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
   AZURE_OPENAI_SECONDARY_DEPLOYMENT_NAME=Phi-4-mini-instruct
   ```

2. **Dependencies Installed**
   ```bash
   pip install openai python-dotenv
   ```

## Test Coverage

These tests verify:

- ✅ Environment configuration validation
- ✅ Azure OpenAI client creation
- ✅ Primary model (GPT-4o) functionality
- ✅ Secondary model (Phi-4-mini) functionality
- ✅ Model parameter validation
- ✅ Error handling and exceptions
- ✅ Configuration error messages

## Expected Output

Successful test run should show:
```
✓ Configuration validated successfully
✓ Primary model query successful
✓ Secondary model query successful
✓ All tests passed!
```

## Troubleshooting

### Common Issues

1. **Missing Environment Variables**
   - Error: `ConfigurationError: Missing required environment variable`
   - Solution: Check `.env` file has all required variables

2. **Invalid API Key**
   - Error: `Authentication failed`
   - Solution: Verify API key in Azure portal and update `.env`

3. **Model Not Found**
   - Error: `The API deployment for this resource does not exist`
   - Solution: Check deployment names match what's in Azure portal

4. **Import Errors**
   - Error: `ModuleNotFoundError: No module named 'azure_openai_helper'`
   - Solution: Run tests from project root or install package: `pip install -e .`

## Adding New Tests

When adding new functionality to the helper module:

1. Create a new test file: `test_<feature>.py`
2. Follow the existing test structure
3. Update this README with test description
4. Ensure tests can run independently

## Integration with Main Tests

These helper tests are separate from the main package tests in `/tests`:

- **Main Package Tests** (`/tests`): Test the overall package structure and lab runners
- **Helper Tests** (`azure_openai_helper/tests`): Test the Azure OpenAI helper functionality

Both test suites should pass for a complete validation.

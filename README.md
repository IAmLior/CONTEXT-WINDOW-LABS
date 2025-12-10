# Context Window Labs

A comprehensive Python package for testing Large Language Model (LLM) context window limitations and strategies through hands-on experiments. This project explores how modern LLMs handle different context sizes, retrieval strategies, and context management techniques.

## 🎯 Project Overview

Context Window Labs provides a systematic approach to understanding LLM behavior across four key dimensions:

1. **Position Bias**: Testing the "lost in the middle" phenomenon
2. **Context Size Impact**: Measuring performance degradation with prompt length
3. **Retrieval Strategies**: Comparing RAG vs Full Context approaches
4. **Context Management**: Evaluating strategies for growing context in multi-step tasks

The project is structured as an installable Python package with four independent labs, each focusing on a specific aspect of context window behavior.

## 📦 Installation

### Install in Editable Mode (Recommended for Development)

```bash
# Navigate to the project directory
cd context-window-labs

# Install in editable mode
pip install -e .

# Or with development dependencies (includes pytest, black, flake8, mypy)
pip install -e ".[dev]"
```

### Install from Git

```bash
pip install git+https://github.com/IAmLior/CONTEXT-WINDOW-LABS.git
```

### Verify Installation

```bash
python -c "import context_window_labs; print(context_window_labs.__version__)"
# Expected output: 0.1.0
```

## 🚀 Quick Start

### Running Labs

Each lab can be run with a single function call:

```python
from context_window_labs import run_lab1, run_lab2, run_lab3, run_lab4

# Run Lab 1 with default settings
run_lab1()

# Run Lab 1 with specific trial
run_lab1(trial="trial5")

# Run Lab 2 with specific dataset
run_lab2(dataset="cities")

# Run Labs 3 and 4
run_lab3()
run_lab4()
```

### Using the Azure OpenAI Helper

```python
from context_window_labs import llm_query, validate_configuration

# Validate your configuration
config = validate_configuration()

# Query the LLM directly
response = llm_query(
    "Explain quantum computing in simple terms",
    temperature=0.7,
    model="gpt-4o"
)
print(response)
```

## ⚙️ Configuration

Create a `.env` file in the project root with your Azure OpenAI credentials:

```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_SECONDARY_DEPLOYMENT_NAME=Phi-4-mini-instruct
```

## 📚 Package Structure

```
context-window-labs/
├── context_window_labs.py      # Main package module
├── pyproject.toml              # Package configuration
├── README.md                   # This file
├── run_all_tests.py           # Comprehensive test runner
├── azure_openai_helper/        # Azure OpenAI utilities
│   ├── llm_client.py
│   └── tests/                 # Helper module tests
├── lab1/                       # Lab 1: Needle in a Haystack
├── lab2/                       # Lab 2: Context Window Size Impact
├── lab3/                       # Lab 3: RAG vs Full Context
├── lab4/                       # Lab 4: Context Engineering Strategies
└── tests/                      # Package-level tests
```

## 🔬 Labs

### Lab 1: Needle in a Haystack

[Content to be added]

### Lab 2: Context Window Size Impact

[Content to be added]

### Lab 3: RAG vs Full Context

[Content to be added]

### Lab 4: Context Engineering Strategies

[Content to be added]

## 🛠️ Azure OpenAI Helper

[Content to be added]

## 🧪 Testing

### Test Organization

The project includes comprehensive test coverage across two levels:

**Main Package Tests** (`/tests`): These tests verify the overall package structure, imports, and lab runner functionality. They ensure that the package is correctly installed and all public APIs are accessible. The test suite includes installation verification, quick start guide validation, and comprehensive pytest tests for all package components. These tests can run without making actual API calls, making them fast and suitable for CI/CD pipelines.

**Azure OpenAI Helper Tests** (`azure_openai_helper/tests`): These tests validate the Azure OpenAI integration, including configuration validation, multi-model support, parameter validation, and actual API queries. They ensure that the helper module correctly interfaces with Azure OpenAI services and handles errors appropriately. These tests require valid Azure OpenAI credentials and make real API calls to verify end-to-end functionality.

### Running Tests

```bash
# Run all tests (main package + helper)
python run_all_tests.py

# Run main package tests only
python tests/test_installation.py
python tests/test_quick_start.py

# Run helper tests only
python azure_openai_helper/tests/test_validation.py
python azure_openai_helper/tests/test_multi_model.py

# Run with pytest (requires pytest installation)
pytest tests/ -v
pytest azure_openai_helper/tests/ -v

# Run with coverage
pytest tests/ --cov=context_window_labs --cov-report=html
```

## 📖 API Reference

### Main Package

#### Lab Runners
- `run_lab1(trial="trial1")` - Run Lab 1 with specified trial (trial1-trial5)
- `run_lab2(dataset="phi4mini", context_sizes=None)` - Run Lab 2 with dataset
- `run_lab3()` - Run Lab 3 experiment
- `run_lab4()` - Run Lab 4 experiment

#### Helper Functions
- `llm_query(prompt, temperature=0.7, model=None)` - Query Azure OpenAI
- `validate_configuration()` - Validate environment variables
- `get_client()` - Get configured Azure OpenAI client
- `ConfigurationError` - Configuration error exception class

#### Version
- `__version__` - Package version string (current: 0.1.0)

### Lab 1 Trials

| Trial   | Words/Doc | Distractors | Model        | Description                |
|---------|-----------|-------------|--------------|----------------------------|
| trial1  | 200       | No          | GPT-4o       | Baseline test              |
| trial2  | 1000      | Yes (3)     | GPT-4o       | Complex test               |
| trial3  | 3000      | Yes (8-12)  | GPT-4o       | Extreme test               |
| trial4  | 3000      | Yes (8-12)  | Phi-4-mini   | Model comparison           |
| trial5  | 3500      | Yes (10-15) | Phi-4-mini   | Final test at limit        |

### Lab 2 Datasets

| Dataset         | Words/Doc | Description           |
|-----------------|-----------|------------------------|
| phi4mini        | ~90       | Animal facts           |
| cities          | ~180      | World cities           |
| countries       | ~300      | Country information    |
| tech_companies  | ~400      | Tech company profiles  |

## 📊 Results

Each lab generates comprehensive outputs:

- **JSON files**: Raw experiment data
- **PNG visualizations**: Charts and plots
- **TXT reports**: Detailed analysis and findings

Results are organized in lab-specific directories:
- `lab1/results/`
- `lab2/results/`
- `lab3/results/`
- `lab4/results/`

## 🛠️ Development

### Requirements

- Python 3.8+
- Azure OpenAI account with API access
- Dependencies (auto-installed):
  - openai >= 1.0.0
  - python-dotenv >= 1.0.0
  - matplotlib >= 3.5.0
  - seaborn >= 0.12.0
  - pandas >= 1.5.0
  - numpy >= 1.24.0
  - scikit-learn >= 1.3.0
  - tiktoken >= 0.5.0
  - chromadb >= 0.4.0

### Development Tools

Install with development dependencies:

```bash
pip install -e ".[dev]"
```

This includes:
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting
- `black` - Code formatting
- `flake8` - Linting
- `mypy` - Type checking

### Code Quality

```bash
# Format code
black .

# Check linting
flake8

# Type checking
mypy context_window_labs.py
```

## 📝 License

MIT

## 👥 Author

Context Window Labs Team

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🔗 Links

- **Repository**: https://github.com/IAmLior/CONTEXT-WINDOW-LABS
- **Issues**: https://github.com/IAmLior/CONTEXT-WINDOW-LABS/issues

---

*Built with ❤️ for understanding LLM context windows*

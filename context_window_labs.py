"""
Context Window Labs: Testing LLM Context Window Limitations and Strategies

This package provides a comprehensive suite of experiments testing how Large Language Models
handle different context window sizes and strategies.

Labs:
- Lab 1: Needle in a Haystack - Tests the "lost in the middle" phenomenon
- Lab 2: Context Window Size Impact - Measures performance vs prompt size
- Lab 3: RAG vs Full Context - Compares retrieval strategies
- Lab 4: Context Engineering Strategies - Evaluates SELECT, COMPRESS, and WRITE strategies

Example Usage:
    >>> from context_window_labs import run_lab1, run_lab2, run_lab3, run_lab4
    >>> 
    >>> # Run individual labs
    >>> run_lab1()  # Default trial1
    >>> run_lab1(trial="trial5")  # Specific trial
    >>> run_lab2(dataset="cities")
    >>> run_lab3()
    >>> run_lab4()
    
    >>> # Or use the helper directly
    >>> from context_window_labs import llm_query
    >>> response = llm_query("What is the capital of France?")
"""

__version__ = "0.1.0"
__author__ = "Context Window Labs Team"
__license__ = "MIT"

# Core utilities - Azure OpenAI Helper
from azure_openai_helper import (
    llm_query,
    validate_configuration,
    get_client,
    ConfigurationError,
)

# Lab entry points - just the main runners
from lab1 import run_lab as run_lab1
from lab2 import run_lab as run_lab2
from lab3 import run_lab as run_lab3
from lab4 import run_lab as run_lab4

# Public API - simplified to just the essentials
__all__ = [
    # Version
    "__version__",
    # Core utilities
    "llm_query",
    "validate_configuration",
    "get_client",
    "ConfigurationError",
    # Lab runners
    "run_lab1",
    "run_lab2",
    "run_lab3",
    "run_lab4",
]

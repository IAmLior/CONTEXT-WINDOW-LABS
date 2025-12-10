"""
Azure OpenAI Helper Module

A robust helper module for interacting with Azure OpenAI's ChatCompletion API.
Loads configuration from environment variables and provides a clean interface
for querying the LLM.

Example:
    >>> from azure_openai_helper import llm_query, validate_configuration
    >>> config = validate_configuration()
    >>> response = llm_query("What is 2+2?", temperature=0.7)
    >>> print(response)
"""

__version__ = "0.1.0"

from .llm_client import (
    llm_query,
    validate_configuration,
    get_client,
    ConfigurationError,
)

__all__ = [
    "__version__",
    "llm_query",
    "validate_configuration",
    "get_client",
    "ConfigurationError",
]

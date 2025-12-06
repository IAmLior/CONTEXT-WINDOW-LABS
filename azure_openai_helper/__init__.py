"""
Azure OpenAI Helper Module

A robust helper module for interacting with Azure OpenAI's ChatCompletion API.
Loads configuration from environment variables and provides a clean interface
for querying the LLM.
"""

from .llm_client import llm_query, validate_configuration

__all__ = ['llm_query', 'validate_configuration']

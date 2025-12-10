"""
Pytest-compatible tests for context-window-labs package
Run with: pytest tests/test_package.py -v
"""

import pytest


class TestPackageImports:
    """Test that all package components can be imported"""
    
    def test_import_main_package(self):
        """Test importing the main package"""
        import context_window_labs
        assert hasattr(context_window_labs, '__version__')
        assert context_window_labs.__version__ == "0.1.0"
    
    def test_import_helper_functions(self):
        """Test importing helper functions"""
        from context_window_labs import (
            llm_query,
            validate_configuration,
            get_client,
            ConfigurationError
        )
        assert callable(llm_query)
        assert callable(validate_configuration)
        assert callable(get_client)
        assert issubclass(ConfigurationError, Exception)
    
    def test_import_lab_runners(self):
        """Test importing lab runner functions"""
        from context_window_labs import run_lab1, run_lab2, run_lab3, run_lab4
        assert callable(run_lab1)
        assert callable(run_lab2)
        assert callable(run_lab3)
        assert callable(run_lab4)
    
    def test_import_from_individual_labs(self):
        """Test importing from individual lab modules"""
        from lab1 import run_lab as lab1_run
        from lab2 import run_lab as lab2_run
        from lab3 import run_lab as lab3_run
        from lab4 import run_lab as lab4_run
        
        assert callable(lab1_run)
        assert callable(lab2_run)
        assert callable(lab3_run)
        assert callable(lab4_run)


class TestPublicAPI:
    """Test the public API exports"""
    
    def test_all_exports(self):
        """Test that __all__ is properly defined"""
        import context_window_labs
        assert hasattr(context_window_labs, '__all__')
        
        expected_exports = [
            '__version__',
            'llm_query',
            'validate_configuration',
            'get_client',
            'ConfigurationError',
            'run_lab1',
            'run_lab2',
            'run_lab3',
            'run_lab4',
        ]
        
        for export in expected_exports:
            assert export in context_window_labs.__all__, f"{export} not in __all__"
    
    def test_version_constant(self):
        """Test that version is accessible"""
        import context_window_labs
        assert isinstance(context_window_labs.__version__, str)
        assert len(context_window_labs.__version__) > 0


class TestLab1:
    """Test Lab 1 functionality"""
    
    def test_lab1_import(self):
        """Test that Lab 1 can be imported"""
        from lab1 import run_lab
        assert callable(run_lab)
    
    def test_lab1_trial_validation(self):
        """Test that Lab 1 validates trial parameter"""
        from lab1 import run_lab
        
        # This should raise ValueError for invalid trial
        with pytest.raises(ValueError, match="Invalid trial"):
            run_lab(trial="invalid_trial")


class TestLab2:
    """Test Lab 2 functionality"""
    
    def test_lab2_import(self):
        """Test that Lab 2 can be imported"""
        from lab2 import run_lab
        assert callable(run_lab)


class TestLab3:
    """Test Lab 3 functionality"""
    
    def test_lab3_import(self):
        """Test that Lab 3 can be imported"""
        from lab3 import run_lab
        assert callable(run_lab)


class TestLab4:
    """Test Lab 4 functionality"""
    
    def test_lab4_import(self):
        """Test that Lab 4 can be imported"""
        from lab4 import run_lab
        assert callable(run_lab)


class TestAzureOpenAIHelper:
    """Test Azure OpenAI helper module"""
    
    def test_helper_import(self):
        """Test that helper module can be imported"""
        import azure_openai_helper
        assert hasattr(azure_openai_helper, '__version__')
    
    def test_helper_exports(self):
        """Test that helper module exports expected functions"""
        from azure_openai_helper import (
            llm_query,
            validate_configuration,
            get_client,
            ConfigurationError
        )
        
        assert callable(llm_query)
        assert callable(validate_configuration)
        assert callable(get_client)
        assert issubclass(ConfigurationError, Exception)


if __name__ == "__main__":
    # Run tests if executed directly
    pytest.main([__file__, "-v"])

"""
Verify Lab 4 setup and dependencies.
"""
import sys
import os

def check_imports():
    """Verify all required packages are installed."""
    required = [
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('sklearn', 'scikit-learn'),
        ('matplotlib', 'matplotlib'),
        ('seaborn', 'seaborn'),
        ('tiktoken', 'tiktoken'),
    ]
    
    missing = []
    
    print("Checking dependencies...")
    print("-" * 60)
    
    for import_name, package_name in required:
        try:
            __import__(import_name)
            print(f"✓ {package_name}")
        except ImportError:
            print(f"✗ {package_name} - MISSING")
            missing.append(package_name)
    
    print("-" * 60)
    
    if missing:
        print(f"\n⚠ Missing packages: {', '.join(missing)}")
        print(f"\nInstall with: pip install {' '.join(missing)}")
        return False
    else:
        print("\n✓ All dependencies installed!")
        return True


def check_azure_openai():
    """Check if Azure OpenAI helper is accessible."""
    print("\nChecking Azure OpenAI helper...")
    print("-" * 60)
    
    try:
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from azure_openai_helper.llm_client import get_llm_client
        
        print("✓ Azure OpenAI helper found")
        
        # Try to get a client (don't actually call it)
        try:
            client = get_llm_client("gpt-4o-mini")
            print("✓ LLM client initialized")
        except Exception as e:
            print(f"⚠ LLM client initialization warning: {e}")
            print("  (This might be OK if credentials aren't set yet)")
        
        return True
        
    except ImportError as e:
        print(f"✗ Azure OpenAI helper not found: {e}")
        return False


def check_directories():
    """Verify lab directory structure."""
    print("\nChecking directory structure...")
    print("-" * 60)
    
    dirs = ['lab4', 'lab4/data', 'lab4/results']
    all_exist = True
    
    for dir_path in dirs:
        if os.path.exists(dir_path):
            print(f"✓ {dir_path}/")
        else:
            print(f"✗ {dir_path}/ - MISSING")
            all_exist = False
    
    return all_exist


def check_files():
    """Verify lab files exist."""
    print("\nChecking lab files...")
    print("-" * 60)
    
    files = [
        'lab4/__init__.py',
        'lab4/generate_scenario.py',
        'lab4/strategies.py',
        'lab4/experiment.py',
        'lab4/analyze_results.py',
        'lab4/run_lab.py',
        'lab4/README.md',
        'lab4/PROMPT_LOG.md'
    ]
    
    all_exist = True
    
    for file_path in files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} - MISSING")
            all_exist = False
    
    return all_exist


def main():
    """Run all verification checks."""
    print("=" * 60)
    print("LAB 4 SETUP VERIFICATION")
    print("=" * 60)
    
    results = []
    
    results.append(("Dependencies", check_imports()))
    results.append(("Azure OpenAI", check_azure_openai()))
    results.append(("Directories", check_directories()))
    results.append(("Files", check_files()))
    
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {name}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n✓ All checks passed! Lab 4 is ready to run.")
        print("\nRun the experiment with:")
        print("  python lab4/run_lab.py")
    else:
        print("\n⚠ Some checks failed. Please fix the issues above.")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

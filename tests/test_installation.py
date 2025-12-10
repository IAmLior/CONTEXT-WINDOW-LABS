"""
Test script to verify the context-window-labs package installation
"""

print("=" * 80)
print("TESTING CONTEXT WINDOW LABS PACKAGE")
print("=" * 80)

# Test 1: Import main package
print("\n[PASS] Test 1: Import main package")
import context_window_labs
print(f"  Package version: {context_window_labs.__version__}")

# Test 2: Import helper functions
print("\n[PASS] Test 2: Import helper functions")
from context_window_labs import llm_query, validate_configuration, get_client
print("  - llm_query")
print("  - validate_configuration")
print("  - get_client")

# Test 3: Import lab runners
print("\n[PASS] Test 3: Import lab runners")
from context_window_labs import run_lab1, run_lab2, run_lab3, run_lab4
print("  - run_lab1")
print("  - run_lab2")
print("  - run_lab3")
print("  - run_lab4")

# Test 4: Import from individual labs
print("\n[PASS] Test 4: Import from individual labs")
from lab1 import run_lab as lab1_run
from lab2 import run_lab as lab2_run
from lab3 import run_lab as lab3_run
from lab4 import run_lab as lab4_run
print("  - lab1.run_lab")
print("  - lab2.run_lab")
print("  - lab3.run_lab")
print("  - lab4.run_lab")

# Test 5: Check __all__ exports
print("\n[PASS] Test 5: Check public API")
print(f"  Public exports: {context_window_labs.__all__}")

print("\n" + "=" * 80)
print("ALL TESTS PASSED!")
print("=" * 80)

print("\nPackage is ready to use!")
print("\nExample usage:")
print("  >>> from context_window_labs import run_lab1")
print("  >>> run_lab1()  # Run trial1 (default)")
print("  >>> run_lab1(trial='trial5')  # Run specific trial")
print("  >>> ")
print("  >>> from context_window_labs import run_lab2")
print("  >>> run_lab2(dataset='cities')")
print("  >>> ")
print("  >>> from context_window_labs import run_lab3, run_lab4")
print("  >>> run_lab3()")
print("  >>> run_lab4()")

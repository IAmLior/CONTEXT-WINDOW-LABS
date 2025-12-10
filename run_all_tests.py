"""
Run all tests for Context Window Labs Package

This script runs both:
1. Main package tests (in /tests)
2. Azure OpenAI Helper tests (in azure_openai_helper/tests)
"""

import sys
import subprocess

print("=" * 80)
print("CONTEXT WINDOW LABS - COMPREHENSIVE TEST SUITE")
print("=" * 80)

test_results = []

# Test 1: Main Package Tests
print("\n" + "=" * 80)
print("RUNNING MAIN PACKAGE TESTS")
print("=" * 80)

print("\n[1/3] Running installation test...")
result = subprocess.run([sys.executable, "tests/test_installation.py"], capture_output=False)
test_results.append(("Main Package Installation Test", result.returncode == 0))

print("\n[2/3] Running quick start test...")
result = subprocess.run([sys.executable, "tests/test_quick_start.py"], capture_output=False)
test_results.append(("Quick Start Guide Test", result.returncode == 0))

# Test 2: Azure OpenAI Helper Tests
print("\n" + "=" * 80)
print("RUNNING AZURE OPENAI HELPER TESTS")
print("=" * 80)

print("\n[3/3] Running validation test...")
result = subprocess.run([sys.executable, "azure_openai_helper/tests/test_validation.py"], capture_output=False)
test_results.append(("Azure OpenAI Helper Validation Test", result.returncode == 0))

# Summary
print("\n" + "=" * 80)
print("TEST SUMMARY")
print("=" * 80)

passed = sum(1 for _, success in test_results if success)
failed = len(test_results) - passed

for test_name, success in test_results:
    status = "[PASS]" if success else "[FAIL]"
    print(f"{status} {test_name}")

print("\n" + "=" * 80)
if failed == 0:
    print(f"ALL {passed} TESTS PASSED!")
    print("=" * 80)
    sys.exit(0)
else:
    print(f"TESTS FAILED: {failed}/{len(test_results)}")
    print("=" * 80)
    sys.exit(1)

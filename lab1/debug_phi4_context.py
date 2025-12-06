"""
Quick test to diagnose the Phi-4-mini context length issue
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from azure_openai_helper import llm_query

print("=" * 80)
print("PHI-4-MINI CONTEXT LENGTH DIAGNOSTIC")
print("=" * 80)

# Test 1: Very short prompt
print("\n1. Testing with SHORT prompt (50 words)...")
short_text = "The quick brown fox jumps over the lazy dog. " * 10
short_prompt = f"Read this text and answer: What animal jumps?\n\n{short_text}\n\nAnswer:"

try:
    response = llm_query(short_prompt, temperature=0.0, max_tokens=20, model="secondary")
    print(f"✓ Response: {response}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 2: Medium prompt
print("\n2. Testing with MEDIUM prompt (500 words)...")
medium_text = "Scientists study various phenomena in nature. " * 100
medium_prompt = f"Read this text and count how many times 'nature' appears.\n\n{medium_text}\n\nAnswer:"

try:
    response = llm_query(medium_prompt, temperature=0.0, max_tokens=20, model="secondary")
    print(f"✓ Response: {response}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 3: Long prompt (2000 words)
print("\n3. Testing with LONG prompt (2000 words)...")
long_text = "The history of technology spans many centuries and includes numerous innovations. " * 200
long_prompt = f"Read this text. What is the main topic?\n\n{long_text}\n\nAnswer:"

try:
    response = llm_query(long_prompt, temperature=0.0, max_tokens=20, model="secondary")
    print(f"✓ Response: {response}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 4: Very long prompt (4000 words)
print("\n4. Testing with VERY LONG prompt (4000 words)...")
very_long_text = "Technology continues to evolve rapidly. " * 600
very_long_prompt = f"What is discussed in this text?\n\n{very_long_text}\n\nAnswer:"

try:
    response = llm_query(very_long_prompt, temperature=0.0, max_tokens=20, model="secondary")
    print(f"✓ Response: {response}")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "=" * 80)
print("DIAGNOSTIC COMPLETE")
print("=" * 80)

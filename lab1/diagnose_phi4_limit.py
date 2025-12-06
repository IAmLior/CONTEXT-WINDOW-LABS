"""
Quick diagnostic: Test Phi-4-mini with one of the working 3000-word documents
to verify the model itself is still functioning correctly.
"""

import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from azure_openai_helper import llm_query

print("=" * 80)
print("PHI-4-MINI DIAGNOSTIC: Testing with known-good 3000-word document")
print("=" * 80)

# Load a document from Trial 4 (which worked at 100%)
print("\n1. Loading a document from Trial 4 (3000 words)...")
with open("lab1/data/documents_phi4_trial.json", 'r') as f:
    documents = json.load(f)

test_doc = documents[0]
print(f"   Loaded document {test_doc['doc_id']}")
print(f"   Position: {test_doc['position']}")
print(f"   Word count: {test_doc['word_count']}")
print(f"   Question: {test_doc['question']}")
print(f"   Expected answer: {test_doc['expected_answer']}")

# Construct the same prompt used in experiment
prompt = f"""Read the following document carefully and answer the question based ONLY on the information in the document.

Document:
{test_doc['text']}

Question: {test_doc['question']}

Answer:"""

print(f"\n   Prompt length: {len(prompt.split())} words")

print("\n2. Querying Phi-4-mini with this document...")
try:
    response = llm_query(
        prompt=prompt,
        temperature=0.0,
        max_tokens=100,
        model="secondary"
    )
    
    print(f"\n✓ Response received:")
    print(f"   '{response}'")
    
    # Check if response contains expected answer
    response_lower = response.lower() if response else ""
    is_correct = any(keyword.lower() in response_lower for keyword in test_doc['keywords'])
    
    if is_correct:
        print(f"\n✓ CORRECT! Response contains expected answer")
    else:
        print(f"\n✗ INCORRECT! Response does not match expected answer")
        print(f"   Expected keywords: {test_doc['keywords']}")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()

# Now test with a 5000-word document
print("\n" + "=" * 80)
print("3. Testing with 5000-word document (from failed Trial 5)...")
print("=" * 80)

with open("lab1/data/documents_trial5_fixed.json", 'r') as f:
    documents_5k = json.load(f)

test_doc_5k = documents_5k[0]
print(f"   Loaded document {test_doc_5k['doc_id']}")
print(f"   Position: {test_doc_5k['position']}")
print(f"   Word count: {test_doc_5k['word_count']}")

prompt_5k = f"""Read the following document carefully and answer the question based ONLY on the information in the document.

Document:
{test_doc_5k['text']}

Question: {test_doc_5k['question']}

Answer:"""

print(f"   Prompt length: {len(prompt_5k.split())} words")

print("\n   Querying Phi-4-mini with 5000-word document...")
try:
    response_5k = llm_query(
        prompt=prompt_5k,
        temperature=0.0,
        max_tokens=100,
        model="secondary"
    )
    
    print(f"\n   Response received:")
    print(f"   '{response_5k[:200]}...'")
    
    # Check for gibberish patterns
    if response_5k:
        fragments = ['.ord', '.ter', '.ale', '.prim', 'and and and']
        has_gibberish = any(frag in response_5k for frag in fragments)
        
        if has_gibberish:
            print(f"\n✗ GIBBERISH DETECTED! Model is producing nonsense")
            print(f"   This confirms 5000 words exceeds Phi-4-mini's capacity")
        else:
            print(f"\n   Response appears coherent (not gibberish)")
    else:
        print(f"\n✗ Empty or None response!")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("DIAGNOSTIC SUMMARY")
print("=" * 80)
print("\nConclusion:")
print("  If 3000w works but 5000w produces gibberish:")
print("  → Phi-4-mini's effective context window is between 3000-5000 words")
print("  → Should try 4000 words as compromise")
print("\n  If both fail:")
print("  → Something wrong with model endpoint or configuration")
print("=" * 80)

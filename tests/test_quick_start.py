"""
Quick Start Guide for Context Window Labs Package
"""

print("=" * 80)
print("CONTEXT WINDOW LABS v0.1.0")
print("=" * 80)
print("\n[OK] Successfully installed as Python package!")
print("\n" + "=" * 80)
print("QUICK START GUIDE")
print("=" * 80)

print("\n1. Import Lab Runners:")
print("   from context_window_labs import run_lab1, run_lab2, run_lab3, run_lab4")

print("\n2. Run Lab 1 (Needle in a Haystack) - with trial support:")
print("   run_lab1()                    # Default: trial1 (200w, GPT-4o)")
print("   run_lab1(trial='trial2')      # Complex: 1000w, GPT-4o")
print("   run_lab1(trial='trial3')      # Extreme: 3000w, GPT-4o")
print("   run_lab1(trial='trial4')      # Model comparison: 3000w, Phi-4-mini")
print("   run_lab1(trial='trial5')      # Final test: 3500w, Phi-4-mini")

print("\n3. Run Lab 2 (Context Window Size Impact) - with dataset support:")
print("   run_lab2(dataset='phi4mini')        # Animals (90w/doc)")
print("   run_lab2(dataset='cities')          # Cities (180w/doc)")
print("   run_lab2(dataset='countries')       # Countries (300w/doc)")
print("   run_lab2(dataset='tech_companies')  # Tech companies (400w/doc)")

print("\n4. Run Lab 3 (RAG vs Full Context):")
print("   run_lab3()")

print("\n5. Run Lab 4 (Context Engineering Strategies):")
print("   run_lab4()")

print("\n6. Use Helper Functions:")
print("   from context_window_labs import llm_query")
print("   response = llm_query('What is 2+2?')")

print("\n" + "=" * 80)
print("For full documentation, see PACKAGE_README.md")
print("=" * 80)

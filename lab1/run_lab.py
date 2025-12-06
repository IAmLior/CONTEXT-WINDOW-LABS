"""
Master runner for Lab 1: Needle in a Haystack / Lost in the Middle

This script runs the complete experiment pipeline:
1. Generate synthetic documents
2. Run the experiment (query LLM)
3. Analyze results and create visualizations
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

print("=" * 80)
print("LAB 1: NEEDLE IN A HAYSTACK / LOST IN THE MIDDLE")
print("=" * 80)
print()
print("This experiment tests how LLM retrieval accuracy varies based on")
print("the position of critical facts within documents.")
print()
print("Pipeline:")
print("  1. Generate synthetic documents with embedded facts")
print("  2. Query LLM about facts at different positions")
print("  3. Analyze results and visualize 'lost in the middle' effect")
print()
print("=" * 80)
print()

# Import modules
from generate_data import generate_dataset
from experiment import run_experiment, load_documents
from analyze_results import analyze_and_visualize

try:
    # Step 1: Generate data
    print("\n" + "=" * 80)
    print("STEP 1: GENERATING SYNTHETIC DOCUMENTS")
    print("=" * 80)
    documents = generate_dataset(num_docs=15, words_per_doc=200, output_dir="lab1/data")
    
    # Step 2: Run experiment
    print("\n" + "=" * 80)
    print("STEP 2: RUNNING EXPERIMENT")
    print("=" * 80)
    print("\n⚠️  This will make 15 API calls to Azure OpenAI...")
    print("Estimated time: 2-5 minutes depending on API latency\n")
    
    results = run_experiment(documents, output_file="lab1/results/experiment_results.json")
    
    # Step 3: Analyze and visualize
    print("\n" + "=" * 80)
    print("STEP 3: ANALYZING RESULTS")
    print("=" * 80)
    analyze_and_visualize(results_file="lab1/results/experiment_results.json")
    
    # Final summary
    print("\n" + "=" * 80)
    print("LAB 1 COMPLETE! ✓")
    print("=" * 80)
    print("\nGenerated files:")
    print("  - lab1/data/documents.json")
    print("  - lab1/results/experiment_results.json")
    print("  - lab1/results/accuracy_by_position.png")
    print("  - lab1/results/detailed_analysis.png")
    print("  - lab1/results/analysis_report.txt")
    print("\nNext steps:")
    print("  1. Review the plots to visualize the 'lost in the middle' effect")
    print("  2. Read analysis_report.txt for detailed findings")
    print("  3. Check experiment_results.json for raw data")
    print()
    
except KeyboardInterrupt:
    print("\n\n⚠️  Experiment interrupted by user.")
    sys.exit(1)
except Exception as e:
    print(f"\n\n❌ Error running experiment: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

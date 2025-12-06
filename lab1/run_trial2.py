"""
Lab 1 - Trial 2: Complex Needle-in-Haystack

This script generates and runs a more challenging version of the experiment:
- Longer documents (1000 words)
- Distractor facts with similar numbers
- Same evaluation to compare with Trial 1 baseline
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

print("=" * 80)
print("LAB 1 - TRIAL 2: COMPLEX NEEDLE-IN-HAYSTACK")
print("=" * 80)
print()
print("Building on Trial 1 (baseline: 200 words, no distractors, 100% accuracy)")
print()
print("Trial 2 Parameters:")
print("  - Document length: ~1000 words (5x longer)")
print("  - Distractor facts: 3 per document (similar numbers)")
print("  - Same facts and positions as Trial 1")
print()
print("Hypothesis: Longer documents + distractors will reveal 'lost in middle' effect")
print("=" * 80)
print()

from generate_data import generate_dataset
from experiment import run_experiment
from analyze_results import analyze_and_visualize

try:
    # Step 1: Generate complex dataset
    print("\n" + "=" * 80)
    print("STEP 1: GENERATING COMPLEX DOCUMENTS")
    print("=" * 80)
    documents = generate_dataset(
        num_docs=15,
        words_per_doc=1000,  # 5x longer
        output_dir="lab1/data",
        add_distractors=True,  # Add confusing facts
        dataset_name="documents_complex"
    )
    
    # Step 2: Run experiment on complex data
    print("\n" + "=" * 80)
    print("STEP 2: RUNNING EXPERIMENT ON COMPLEX DATA")
    print("=" * 80)
    print("\n⚠️  This will make 15 API calls to Azure OpenAI...")
    print("Testing longer contexts with distractors...\n")
    
    results = run_experiment(
        documents,
        output_file="lab1/results/experiment_results_complex.json"
    )
    
    # Step 3: Analyze complex results
    print("\n" + "=" * 80)
    print("STEP 3: ANALYZING COMPLEX RESULTS")
    print("=" * 80)
    
    # Create separate analysis for complex trial
    from analyze_results import load_results, analyze_position_effect, generate_report
    import json
    
    complex_results = load_results("lab1/results/experiment_results_complex.json")
    complex_analysis = analyze_position_effect(complex_results)
    
    # Generate visualizations with different naming
    from analyze_results import generate_accuracy_plot, generate_detailed_plot
    generate_accuracy_plot(complex_results, "lab1/results/accuracy_by_position_complex.png")
    generate_detailed_plot(complex_results, "lab1/results/detailed_analysis_complex.png")
    generate_report(complex_results, complex_analysis, "lab1/results/analysis_report_complex.txt")
    
    # Step 4: Compare with baseline
    print("\n" + "=" * 80)
    print("STEP 4: COMPARING TRIAL 1 (BASELINE) vs TRIAL 2 (COMPLEX)")
    print("=" * 80)
    
    # Load baseline results
    baseline_results = load_results("lab1/results/experiment_results.json")
    
    print("\nTRIAL 1 (Baseline - 200 words, no distractors):")
    print(f"  Overall Accuracy: {baseline_results['overall_accuracy']:.1%}")
    print(f"  START:  {baseline_results['accuracy_by_position']['start']:.1%}")
    print(f"  MIDDLE: {baseline_results['accuracy_by_position']['middle']:.1%}")
    print(f"  END:    {baseline_results['accuracy_by_position']['end']:.1%}")
    
    print("\nTRIAL 2 (Complex - 1000 words, 3 distractors):")
    print(f"  Overall Accuracy: {complex_results['overall_accuracy']:.1%}")
    print(f"  START:  {complex_results['accuracy_by_position']['start']:.1%}")
    print(f"  MIDDLE: {complex_results['accuracy_by_position']['middle']:.1%}")
    print(f"  END:    {complex_results['accuracy_by_position']['end']:.1%}")
    
    # Calculate changes
    overall_drop = baseline_results['overall_accuracy'] - complex_results['overall_accuracy']
    start_drop = baseline_results['accuracy_by_position']['start'] - complex_results['accuracy_by_position']['start']
    middle_drop = baseline_results['accuracy_by_position']['middle'] - complex_results['accuracy_by_position']['middle']
    end_drop = baseline_results['accuracy_by_position']['end'] - complex_results['accuracy_by_position']['end']
    
    print("\nACCURACY CHANGES (Trial 1 → Trial 2):")
    print(f"  Overall: {overall_drop:+.1%}")
    print(f"  START:   {start_drop:+.1%}")
    print(f"  MIDDLE:  {middle_drop:+.1%}")
    print(f"  END:     {end_drop:+.1%}")
    
    # Detect if middle suffered more
    if middle_drop > start_drop and middle_drop > end_drop:
        print("\n🔍 LOST IN THE MIDDLE DETECTED!")
        print(f"   Middle position suffered {middle_drop:.1%} accuracy loss")
        print(f"   vs {start_drop:.1%} (start) and {end_drop:.1%} (end)")
    
    # Save comparison data
    comparison = {
        "baseline": {
            "params": {"words_per_doc": 200, "distractors": False},
            "overall_accuracy": baseline_results['overall_accuracy'],
            "accuracy_by_position": baseline_results['accuracy_by_position']
        },
        "complex": {
            "params": {"words_per_doc": 1000, "distractors": True},
            "overall_accuracy": complex_results['overall_accuracy'],
            "accuracy_by_position": complex_results['accuracy_by_position']
        },
        "changes": {
            "overall": overall_drop,
            "start": start_drop,
            "middle": middle_drop,
            "end": end_drop
        }
    }
    
    with open("lab1/results/trial_comparison.json", 'w') as f:
        json.dump(comparison, f, indent=2)
    
    print("\n" + "=" * 80)
    print("TRIAL 2 COMPLETE! ✓")
    print("=" * 80)
    print("\nGenerated files:")
    print("  - lab1/data/documents_complex.json")
    print("  - lab1/results/experiment_results_complex.json")
    print("  - lab1/results/accuracy_by_position_complex.png")
    print("  - lab1/results/detailed_analysis_complex.png")
    print("  - lab1/results/analysis_report_complex.txt")
    print("  - lab1/results/trial_comparison.json")
    print()
    
except KeyboardInterrupt:
    print("\n\n⚠️  Experiment interrupted by user.")
    sys.exit(1)
except Exception as e:
    print(f"\n\n❌ Error running experiment: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

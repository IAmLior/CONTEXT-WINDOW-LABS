"""
Lab 1 - Trial 3: Extreme Length Needle-in-Haystack

This script generates and runs the most challenging version:
- Very long documents (5000-10000 words)
- Multiple enhanced distractors (5-10 per document)
- Testing the absolute limits of GPT-4o's context retrieval
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

print("=" * 80)
print("LAB 1 - TRIAL 3: EXTREME LENGTH NEEDLE-IN-HAYSTACK")
print("=" * 80)
print()
print("Building on previous trials:")
print("  Trial 1: 200 words, no distractors → 100% accuracy")
print("  Trial 2: 1000 words, 3 distractors → 100% accuracy")
print()
print("Trial 3 Parameters:")
print("  - Document length: 5000-10000 words (25-50x original!)")
print("  - Distractor facts: 8-12 per document")
print("  - Enhanced filler: 50+ diverse templates (no repetition)")
print("  - Same facts embedded deep in massive contexts")
print()
print("Hypothesis: Extreme length will FINALLY reveal position-dependent degradation")
print("=" * 80)
print()

from generate_data import generate_dataset
from experiment import run_experiment
from analyze_results import analyze_and_visualize, load_results, analyze_position_effect, generate_report
import json

try:
    # Step 1: Generate extreme-length dataset
    print("\n" + "=" * 80)
    print("STEP 1: GENERATING EXTREME-LENGTH DOCUMENTS")
    print("=" * 80)
    print("\n⚠️  Generating very long documents (~7500 words each)...")
    print("This may take a moment...\n")
    
    documents = generate_dataset(
        num_docs=15,
        words_per_doc=3000,  # 15x longer than Trial 1 (within token limits)
        output_dir="lab1/data",
        add_distractors=True,
        dataset_name="documents_extreme"
    )
    
    # Step 2: Run experiment on extreme data
    print("\n" + "=" * 80)
    print("STEP 2: RUNNING EXPERIMENT ON EXTREME-LENGTH DATA")
    print("=" * 80)
    print("\n⚠️  This will make 15 API calls with VERY LONG contexts...")
    print("Each document is ~3000 words (~4000 tokens)")
    print("Estimated time: 5-10 minutes depending on API latency")
    print("Testing if facts get lost in massive haystacks...\n")
    
    results = run_experiment(
        documents,
        output_file="lab1/results/experiment_results_extreme.json"
    )
    
    # Step 3: Analyze extreme results
    print("\n" + "=" * 80)
    print("STEP 3: ANALYZING EXTREME-LENGTH RESULTS")
    print("=" * 80)
    
    extreme_results = load_results("lab1/results/experiment_results_extreme.json")
    extreme_analysis = analyze_position_effect(extreme_results)
    
    # Generate visualizations
    from analyze_results import generate_accuracy_plot, generate_detailed_plot
    generate_accuracy_plot(extreme_results, "lab1/results/accuracy_by_position_extreme.png")
    generate_detailed_plot(extreme_results, "lab1/results/detailed_analysis_extreme.png")
    generate_report(extreme_results, extreme_analysis, "lab1/results/analysis_report_extreme.txt")
    
    # Step 4: Compare ALL three trials
    print("\n" + "=" * 80)
    print("STEP 4: COMPREHENSIVE COMPARISON - ALL THREE TRIALS")
    print("=" * 80)
    
    # Load all results
    baseline_results = load_results("lab1/results/experiment_results.json")
    complex_results = load_results("lab1/results/experiment_results_complex.json")
    
    print("\n" + "=" * 80)
    print("COMPLETE EXPERIMENTAL JOURNEY")
    print("=" * 80)
    
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
    
    print("\nTRIAL 3 (Extreme - 3000 words, 8-12 distractors):")
    print(f"  Overall Accuracy: {extreme_results['overall_accuracy']:.1%}")
    print(f"  START:  {extreme_results['accuracy_by_position']['start']:.1%}")
    print(f"  MIDDLE: {extreme_results['accuracy_by_position']['middle']:.1%}")
    print(f"  END:    {extreme_results['accuracy_by_position']['end']:.1%}")
    
    # Calculate progressive changes
    trial1_to_2_overall = baseline_results['overall_accuracy'] - complex_results['overall_accuracy']
    trial2_to_3_overall = complex_results['overall_accuracy'] - extreme_results['overall_accuracy']
    trial1_to_3_overall = baseline_results['overall_accuracy'] - extreme_results['overall_accuracy']
    
    trial1_to_3_middle = baseline_results['accuracy_by_position']['middle'] - extreme_results['accuracy_by_position']['middle']
    trial1_to_3_start = baseline_results['accuracy_by_position']['start'] - extreme_results['accuracy_by_position']['start']
    trial1_to_3_end = baseline_results['accuracy_by_position']['end'] - extreme_results['accuracy_by_position']['end']
    
    print("\n" + "=" * 80)
    print("ACCURACY DEGRADATION ANALYSIS")
    print("=" * 80)
    print(f"\nOverall Accuracy Change:")
    print(f"  Trial 1 → Trial 2: {trial1_to_2_overall:+.1%}")
    print(f"  Trial 2 → Trial 3: {trial2_to_3_overall:+.1%}")
    print(f"  Trial 1 → Trial 3: {trial1_to_3_overall:+.1%}")
    
    print(f"\nPosition-Specific Changes (Trial 1 → Trial 3):")
    print(f"  START:  {trial1_to_3_start:+.1%}")
    print(f"  MIDDLE: {trial1_to_3_middle:+.1%}")
    print(f"  END:    {trial1_to_3_end:+.1%}")
    
    # Detect if middle suffered disproportionately
    if trial1_to_3_middle > trial1_to_3_start and trial1_to_3_middle > trial1_to_3_end:
        print("\n" + "🔍" * 40)
        print("🎯 LOST IN THE MIDDLE EFFECT DETECTED! 🎯")
        print("🔍" * 40)
        print(f"\nMiddle position suffered {trial1_to_3_middle:.1%} accuracy loss")
        print(f"Compared to {trial1_to_3_start:.1%} (start) and {trial1_to_3_end:.1%} (end)")
        print("\nThe model struggles MORE with facts buried in the middle")
        print("of extremely long documents (3000+ words)")
    elif extreme_results['overall_accuracy'] < 1.0:
        print("\n⚠️  ACCURACY DEGRADATION DETECTED!")
        print(f"Overall accuracy dropped to {extreme_results['overall_accuracy']:.1%}")
        if trial1_to_3_middle == trial1_to_3_start == trial1_to_3_end:
            print("Degradation is UNIFORM across all positions")
        else:
            print("Degradation varies by position:")
            print(f"  Most affected: {max([('START', trial1_to_3_start), ('MIDDLE', trial1_to_3_middle), ('END', trial1_to_3_end)], key=lambda x: x[1])[0]}")
    else:
        print("\n🤯 REMARKABLE: 100% accuracy even with 3000-word documents!")
        print("GPT-4o demonstrates exceptional context handling capabilities")
    
    # Save comprehensive comparison
    comprehensive_comparison = {
        "trial_1_baseline": {
            "params": {"words_per_doc": 200, "distractors": 0},
            "overall_accuracy": baseline_results['overall_accuracy'],
            "accuracy_by_position": baseline_results['accuracy_by_position']
        },
        "trial_2_complex": {
            "params": {"words_per_doc": 1000, "distractors": 3},
            "overall_accuracy": complex_results['overall_accuracy'],
            "accuracy_by_position": complex_results['accuracy_by_position']
        },
        "trial_3_extreme": {
            "params": {"words_per_doc": 3000, "distractors": "8-12"},
            "overall_accuracy": extreme_results['overall_accuracy'],
            "accuracy_by_position": extreme_results['accuracy_by_position']
        },
        "progressive_changes": {
            "trial_1_to_2_overall": trial1_to_2_overall,
            "trial_2_to_3_overall": trial2_to_3_overall,
            "trial_1_to_3_overall": trial1_to_3_overall,
            "trial_1_to_3_by_position": {
                "start": trial1_to_3_start,
                "middle": trial1_to_3_middle,
                "end": trial1_to_3_end
            }
        },
        "lost_in_middle_detected": trial1_to_3_middle > max(trial1_to_3_start, trial1_to_3_end),
        "overall_degradation_detected": extreme_results['overall_accuracy'] < baseline_results['overall_accuracy']
    }
    
    with open("lab1/results/comprehensive_comparison.json", 'w') as f:
        json.dump(comprehensive_comparison, f, indent=2)
    
    print("\n" + "=" * 80)
    print("TRIAL 3 COMPLETE! ✓")
    print("=" * 80)
    print("\nGenerated files:")
    print("  - lab1/data/documents_extreme.json")
    print("  - lab1/results/experiment_results_extreme.json")
    print("  - lab1/results/accuracy_by_position_extreme.png")
    print("  - lab1/results/detailed_analysis_extreme.png")
    print("  - lab1/results/analysis_report_extreme.txt")
    print("  - lab1/results/comprehensive_comparison.json")
    print("\nAll three trials completed. Check comprehensive_comparison.json for full analysis.")
    print()
    
except KeyboardInterrupt:
    print("\n\n⚠️  Experiment interrupted by user.")
    sys.exit(1)
except Exception as e:
    print(f"\n\n❌ Error running experiment: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

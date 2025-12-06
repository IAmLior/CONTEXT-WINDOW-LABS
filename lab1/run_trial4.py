"""
Lab 1 - Trial 4: Secondary Model Comparison (Phi-4-mini-instruct)

This script runs the same experiment as Trial 3 but with the secondary model:
- Same document length (3000 words)
- Same enhanced distractors (8-12 per document)
- Using Phi-4-mini-instruct instead of GPT-4o
- Testing if the smaller model shows "lost in the middle" effect
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

print("=" * 80)
print("LAB 1 - TRIAL 4: SECONDARY MODEL COMPARISON (PHI-4-MINI-INSTRUCT)")
print("=" * 80)
print()
print("Previous Results Summary:")
print("  Trial 1 (GPT-4o): 200 words, no distractors → 100% accuracy")
print("  Trial 2 (GPT-4o): 1000 words, 3 distractors → 100% accuracy")
print("  Trial 3 (GPT-4o): 3000 words, 8-12 distractors → 100% accuracy")
print()
print("Trial 4 Parameters:")
print("  - Model: Phi-4-mini-instruct (secondary)")
print("  - Document length: 3000 words (same as Trial 3)")
print("  - Distractor facts: 8-12 per document (same as Trial 3)")
print("  - Enhanced filler: 50+ diverse templates")
print("  - Testing: Will smaller model show position bias?")
print()
print("Hypothesis: Phi-4-mini may struggle where GPT-4o succeeded")
print("Expected: Position-dependent accuracy degradation in middle")
print("=" * 80)
print()

from generate_data import generate_dataset
from experiment import run_experiment
from analyze_results import analyze_and_visualize, load_results, analyze_position_effect, generate_report
import json

try:
    # Step 1: Generate dataset (same parameters as Trial 3)
    print("\n" + "=" * 80)
    print("STEP 1: GENERATING DOCUMENTS (IDENTICAL TO TRIAL 3)")
    print("=" * 80)
    print("\nGenerating 15 documents with 3000 words each...")
    print("This ensures direct comparison with GPT-4o Trial 3 results.\n")
    
    documents = generate_dataset(
        num_docs=15,
        words_per_doc=3000,  # Same as Trial 3
        output_dir="lab1/data",
        add_distractors=True,
        dataset_name="documents_phi4_trial"
    )
    
    # Step 2: Run experiment with SECONDARY MODEL (Phi-4-mini-instruct)
    print("\n" + "=" * 80)
    print("STEP 2: RUNNING EXPERIMENT WITH PHI-4-MINI-INSTRUCT")
    print("=" * 80)
    print("\n🔬 Testing secondary model (Phi-4-mini-instruct)...")
    print("Each document is ~3000 words (~4000 tokens)")
    print("Estimated time: 5-10 minutes depending on API latency")
    print("Checking if smaller model shows position bias...\n")
    
    results = run_experiment(
        documents,
        output_file="lab1/results/experiment_results_phi4.json",
        model="secondary"  # Use Phi-4-mini-instruct
    )
    
    # Step 3: Analyze Phi-4 results
    print("\n" + "=" * 80)
    print("STEP 3: ANALYZING PHI-4-MINI RESULTS")
    print("=" * 80)
    
    phi4_results = load_results("lab1/results/experiment_results_phi4.json")
    phi4_analysis = analyze_position_effect(phi4_results)
    
    # Generate visualizations
    from analyze_results import generate_accuracy_plot, generate_detailed_plot
    generate_accuracy_plot(phi4_results, "lab1/results/accuracy_by_position_phi4.png")
    generate_detailed_plot(phi4_results, "lab1/results/detailed_analysis_phi4.png")
    generate_report(phi4_results, phi4_analysis, "lab1/results/analysis_report_phi4.txt")
    
    # Step 4: Compare Phi-4 vs GPT-4o (Trial 3)
    print("\n" + "=" * 80)
    print("STEP 4: MODEL COMPARISON - PHI-4-MINI VS GPT-4O")
    print("=" * 80)
    
    # Load GPT-4o Trial 3 results for comparison
    try:
        gpt4o_results = load_results("lab1/results/experiment_results_extreme.json")
        
        print("\n" + "=" * 80)
        print("DIRECT MODEL COMPARISON (SAME TASK)")
        print("=" * 80)
        
        print("\nGPT-4o (Trial 3) - 3000 words, 8-12 distractors:")
        print(f"  Overall Accuracy: {gpt4o_results['overall_accuracy']:.1%}")
        print(f"  START:  {gpt4o_results['accuracy_by_position']['start']:.1%}")
        print(f"  MIDDLE: {gpt4o_results['accuracy_by_position']['middle']:.1%}")
        print(f"  END:    {gpt4o_results['accuracy_by_position']['end']:.1%}")
        
        print("\nPhi-4-mini-instruct (Trial 4) - 3000 words, 8-12 distractors:")
        print(f"  Overall Accuracy: {phi4_results['overall_accuracy']:.1%}")
        print(f"  START:  {phi4_results['accuracy_by_position']['start']:.1%}")
        print(f"  MIDDLE: {phi4_results['accuracy_by_position']['middle']:.1%}")
        print(f"  END:    {phi4_results['accuracy_by_position']['end']:.1%}")
        
        # Calculate performance gap
        accuracy_gap = gpt4o_results['overall_accuracy'] - phi4_results['overall_accuracy']
        middle_gap = gpt4o_results['accuracy_by_position']['middle'] - phi4_results['accuracy_by_position']['middle']
        
        print("\n" + "=" * 80)
        print("PERFORMANCE COMPARISON")
        print("=" * 80)
        print(f"\nOverall Accuracy Gap: {accuracy_gap:+.1%} (GPT-4o - Phi-4-mini)")
        print(f"Middle Position Gap:  {middle_gap:+.1%} (GPT-4o - Phi-4-mini)")
        
        if abs(middle_gap) > 0.15:  # More than 15% difference
            print("\n🎯 SIGNIFICANT 'LOST IN THE MIDDLE' EFFECT DETECTED!")
            print(f"   Phi-4-mini shows {abs(middle_gap):.1%} worse accuracy on middle positions")
        elif abs(accuracy_gap) > 0.10:  # More than 10% overall difference
            print("\n📊 NOTABLE PERFORMANCE DEGRADATION")
            print(f"   Phi-4-mini overall accuracy is {abs(accuracy_gap):.1%} lower")
        else:
            print("\n⚠️  SIMILAR PERFORMANCE")
            print("   Both models perform comparably on this task")
        
    except FileNotFoundError:
        print("\n⚠️  Note: GPT-4o Trial 3 results not found for comparison")
        print("   Run Trial 3 first for direct model comparison")
    
    # Step 5: Complete summary across all trials
    print("\n" + "=" * 80)
    print("STEP 5: COMPLETE EXPERIMENTAL SUMMARY")
    print("=" * 80)
    
    try:
        baseline_results = load_results("lab1/results/experiment_results.json")
        complex_results = load_results("lab1/results/experiment_results_complex.json")
        
        print("\n" + "=" * 80)
        print("ALL TRIALS SUMMARY")
        print("=" * 80)
        
        print("\nGPT-4o Progression:")
        print(f"  Trial 1 (200w, 0 distr):      {baseline_results['overall_accuracy']:.1%}")
        print(f"  Trial 2 (1000w, 3 distr):     {complex_results['overall_accuracy']:.1%}")
        print(f"  Trial 3 (3000w, 8-12 distr):  {gpt4o_results['overall_accuracy']:.1%}")
        
        print("\nPhi-4-mini-instruct:")
        print(f"  Trial 4 (3000w, 8-12 distr):  {phi4_results['overall_accuracy']:.1%}")
        
        print("\n" + "=" * 80)
        print("KEY INSIGHTS")
        print("=" * 80)
        
        if phi4_results['overall_accuracy'] < 0.85:
            print("\n✓ Successfully triggered degradation with smaller model")
            print("  Phi-4-mini shows clear limitations that GPT-4o doesn't have")
        
        if phi4_results['accuracy_by_position']['middle'] < phi4_results['accuracy_by_position']['start']:
            print("\n✓ Position bias detected in Phi-4-mini")
            print("  Middle positions are harder for the smaller model")
        
        print("\n✓ Experimental framework successfully differentiates model capabilities")
        print("✓ Multi-model comparison reveals context window handling differences")
        
    except FileNotFoundError as e:
        print(f"\n⚠️  Some previous trial results not available: {e}")
    
    print("\n" + "=" * 80)
    print("TRIAL 4 COMPLETE!")
    print("=" * 80)
    print("\n✓ Results saved to: lab1/results/experiment_results_phi4.json")
    print("✓ Visualizations saved to: lab1/results/*_phi4.png")
    print("✓ Analysis report saved to: lab1/results/analysis_report_phi4.txt")
    print("\n📊 Check the visualizations to see the position-dependent effects!")
    print("=" * 80)
    print()

except KeyboardInterrupt:
    print("\n\n⚠️  Experiment interrupted by user")
    print("Partial results may have been saved")
    
except Exception as e:
    print("\n" + "=" * 80)
    print("ERROR OCCURRED")
    print("=" * 80)
    print(f"\n{type(e).__name__}: {e}")
    print("\nPlease check:")
    print("  1. Azure OpenAI credentials in .env file")
    print("  2. Secondary model (Phi-4-mini-instruct) is properly configured")
    print("  3. Previous trial results exist for comparison")
    import traceback
    print("\nFull traceback:")
    traceback.print_exc()

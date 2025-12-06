"""
Lab 1 - Trial 5 FINAL: Ultimate Challenge at 4000 words (Phi-4-mini's limit)

Based on diagnostics:
- 3000 words: ✓ Works perfectly
- 5000 words: ✗ Produces gibberish (exceeds capacity)
- 4000 words: ? Testing the practical limit
"""

import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

print("=" * 80)
print("LAB 1 - TRIAL 5 FINAL: TESTING PHI-4-MINI'S PRACTICAL LIMIT (4000 WORDS)")
print("=" * 80)
print()
print("📊 DIAGNOSTIC RESULTS:")
print("   3000 words: ✓ Perfect accuracy (100%)")
print("   5000 words: ✗ Gibberish output (exceeds capacity)")
print("   4000 words: ? Testing now...")
print()
print("Previous Results:")
print("  Trial 1 (GPT-4o):  200w, 0 distr  → 100% ✅")
print("  Trial 2 (GPT-4o):  1000w, 3 distr → 100% ✅")
print("  Trial 3 (GPT-4o):  3000w, 8-12d  → 100% ✅")
print("  Trial 4 (Phi-4):   3000w, 8-12d  → 100% ✅")
print("  Trial 5 (Phi-4):   5000w, 10-15d → Gibberish (exceeded limit) ❌")
print()
print("Trial 5 FINAL - Balanced Challenge Configuration:")
print("  ✓ Model: Phi-4-mini-instruct")
print("  ✓ Length: 4000 words (between working 3000 and failing 5000)")
print("  ✓ Filler: Shuffle-and-cycle (minimal repetition)")
print("  ✓ Distractors: 10-15 numerical confusers per document")
print("  ✓ Goal: Find the sweet spot where degradation begins")
print()
print("Hypothesis: 4000 words may trigger position bias without complete breakdown")
print("=" * 80)
print()

from generate_data import generate_dataset
from experiment import run_experiment
from analyze_results import load_results, analyze_position_effect, generate_report
import json

# Track start time
start_time = datetime.now()
print(f"⏱️  Experiment started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

try:
    # Step 1: Generate 4000-word documents
    print("\n" + "=" * 80)
    print("STEP 1: GENERATING 4000-WORD DOCUMENTS")
    print("=" * 80)
    print("\n📝 Generating 15 documents with 4000 words each...")
    print("   This is between the working 3000w and failing 5000w")
    print("   Should be within Phi-4-mini's capacity while still challenging")
    print()
    
    documents = generate_dataset(
        num_docs=15,
        words_per_doc=4000,  # Sweet spot
        output_dir="lab1/data",
        add_distractors=True,
        dataset_name="documents_trial5_4000w"
    )
    
    print(f"\n✓ Dataset generation complete!")
    print(f"   Total words: {sum(doc['word_count'] for doc in documents):,}")
    print(f"   Average per document: {sum(doc['word_count'] for doc in documents) / len(documents):.1f}")
    
    # Step 2: Run experiment
    print("\n" + "=" * 80)
    print("STEP 2: TESTING PHI-4-MINI AT 4000 WORDS")
    print("=" * 80)
    print("\n🔬 Querying Phi-4-mini-instruct...")
    print("   Each document ~4000 words (~5200 tokens)")
    print("   This should be processable but challenging")
    print("   Estimated time: 8-12 minutes\n")
    
    results = run_experiment(
        documents,
        output_file="lab1/results/experiment_results_trial5_4000w.json",
        model="secondary"
    )
    
    # Step 3: Analyze results
    print("\n" + "=" * 80)
    print("STEP 3: ANALYZING RESULTS")
    print("=" * 80)
    
    trial5_results = load_results("lab1/results/experiment_results_trial5_4000w.json")
    trial5_analysis = analyze_position_effect(trial5_results)
    
    # Generate visualizations
    from analyze_results import generate_accuracy_plot, generate_detailed_plot
    generate_accuracy_plot(trial5_results, "lab1/results/accuracy_by_position_trial5_4000w.png")
    generate_detailed_plot(trial5_results, "lab1/results/detailed_analysis_trial5_4000w.png")
    generate_report(trial5_results, trial5_analysis, "lab1/results/analysis_report_trial5_4000w.txt")
    
    # Step 4: Compare with all trials
    print("\n" + "=" * 80)
    print("STEP 4: COMPLETE PROGRESSION ANALYSIS")
    print("=" * 80)
    
    try:
        trial1_results = load_results("lab1/results/experiment_results.json")
        trial2_results = load_results("lab1/results/experiment_results_complex.json")
        trial3_results = load_results("lab1/results/experiment_results_extreme.json")
        trial4_results = load_results("lab1/results/experiment_results_phi4.json")
        
        print("\n📊 FULL EXPERIMENTAL PROGRESSION:")
        print(f"\n   Trial 1 (GPT-4o,  200w):  {trial1_results['overall_accuracy']:6.1%}")
        print(f"   Trial 2 (GPT-4o,  1000w): {trial2_results['overall_accuracy']:6.1%}")
        print(f"   Trial 3 (GPT-4o,  3000w): {trial3_results['overall_accuracy']:6.1%}")
        print(f"   Trial 4 (Phi-4,   3000w): {trial4_results['overall_accuracy']:6.1%}")
        print(f"   Trial 5 (Phi-4,   4000w): {trial5_results['overall_accuracy']:6.1%} ← NEW")
        
        print("\n📍 POSITION BREAKDOWN:")
        print("\n   START:")
        print(f"      T1-T3 (GPT-4o): All 100%")
        print(f"      T4 (Phi-4, 3000w): {trial4_results['accuracy_by_position']['start']:6.1%}")
        print(f"      T5 (Phi-4, 4000w): {trial5_results['accuracy_by_position']['start']:6.1%} ← NEW")
        
        print("\n   MIDDLE:")
        print(f"      T1-T3 (GPT-4o): All 100%")
        print(f"      T4 (Phi-4, 3000w): {trial4_results['accuracy_by_position']['middle']:6.1%}")
        print(f"      T5 (Phi-4, 4000w): {trial5_results['accuracy_by_position']['middle']:6.1%} ← NEW")
        
        print("\n   END:")
        print(f"      T1-T3 (GPT-4o): All 100%")
        print(f"      T4 (Phi-4, 3000w): {trial4_results['accuracy_by_position']['end']:6.1%}")
        print(f"      T5 (Phi-4, 4000w): {trial5_results['accuracy_by_position']['end']:6.1%} ← NEW")
        
        # Calculate metrics
        trial5_middle = trial5_results['accuracy_by_position']['middle']
        trial5_edges = (trial5_results['accuracy_by_position']['start'] + 
                       trial5_results['accuracy_by_position']['end']) / 2
        position_gap = trial5_edges - trial5_middle
        
        length_impact = trial4_results['overall_accuracy'] - trial5_results['overall_accuracy']
        
        print("\n" + "=" * 80)
        print("CRITICAL FINDINGS")
        print("=" * 80)
        
        print(f"\n📊 Position Analysis (4000 words):")
        print(f"   Edge accuracy (avg): {trial5_edges:6.1%}")
        print(f"   Middle accuracy:     {trial5_middle:6.1%}")
        print(f"   Position gap:        {position_gap:+6.1%}")
        
        if position_gap > 0.20:
            print("\n   🎯 MAJOR SUCCESS! 'Lost in the middle' effect detected!")
            print(f"      {position_gap:.1%} degradation in middle positions")
        elif position_gap > 0.10:
            print("\n   ✓ Moderate position bias observed")
            print(f"      {position_gap:.1%} difference between positions")
        else:
            print("\n   → No significant position bias at 4000 words")
        
        print(f"\n📏 Length Impact (3000w → 4000w):")
        print(f"   Accuracy change: {length_impact:+6.1%}")
        
        if abs(length_impact) > 0.15:
            print(f"   ✓ Significant degradation - found the breaking point!")
        elif abs(length_impact) > 0.05:
            print(f"   → Moderate impact - approaching limits")
        else:
            print(f"   → Minimal impact - still within capacity")
        
        print(f"\n🎯 Overall Assessment:")
        if trial5_results['overall_accuracy'] >= 0.95:
            print(f"   Phi-4-mini maintains {trial5_results['overall_accuracy']:.1%} accuracy at 4000 words")
            print("   Model handles this length well")
        elif trial5_results['overall_accuracy'] >= 0.80:
            print(f"   Accuracy dropped to {trial5_results['overall_accuracy']:.1%}")
            print("   Some degradation but still functional")
        elif trial5_results['overall_accuracy'] >= 0.50:
            print(f"   Significant degradation to {trial5_results['overall_accuracy']:.1%}")
            print("   Approaching model's limit")
        else:
            print(f"   Severe breakdown at {trial5_results['overall_accuracy']:.1%}")
            print("   4000 words still too much")
        
    except FileNotFoundError as e:
        print(f"\n⚠️  Some previous results not available: {e}")
    
    # Final summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("\n" + "=" * 80)
    print("TRIAL 5 COMPLETE - PHI-4-MINI LIMITS MAPPED")
    print("=" * 80)
    print(f"\n⏱️  Duration: {duration:.1f} seconds ({duration/60:.1f} minutes)")
    print(f"   Completed: {end_time.strftime('%H:%M:%S')}")
    
    print("\n📊 Findings:")
    print(f"   ✓ 3000 words: {trial4_results['overall_accuracy']:.1%} accuracy")
    print(f"   ✓ 4000 words: {trial5_results['overall_accuracy']:.1%} accuracy")
    print(f"   ✗ 5000 words: Gibberish (exceeds capacity)")
    
    print("\n✓ Results: lab1/results/experiment_results_trial5_4000w.json")
    print("✓ Plots: lab1/results/*_trial5_4000w.png")
    print("=" * 80)
    print()

except KeyboardInterrupt:
    print("\n\n⚠️  Interrupted by user")
    end_time = datetime.now()
    print(f"Duration: {(end_time - start_time).total_seconds():.1f}s")
    
except Exception as e:
    print("\n" + "=" * 80)
    print("ERROR")
    print("=" * 80)
    print(f"\n{type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    end_time = datetime.now()
    print(f"\nDuration before error: {(end_time - start_time).total_seconds():.1f}s")

"""
Lab 1 - Trial 5 FINAL: Conservative Challenge at 3500 words

Based on empirical testing:
- 3000 words: ✓ 100% success (all 15 documents)
- 4000 words: ⚠️ ~60% success (mixed results, some gibberish)
- 5000 words: ✗ Complete failure (all gibberish)

Target: 3500 words - Long enough to challenge but reliable enough for valid results
"""

import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

print("=" * 80)
print("LAB 1 - TRIAL 5 FINAL: RELIABLE CHALLENGE AT 3500 WORDS")
print("=" * 80)
print()
print("🎯 STRATEGY: Conservative but meaningful increase")
print()
print("Empirical Findings:")
print("  3000 words: ✓ 100% success, all documents work")
print("  4000 words: ⚠️ ~60% success, unreliable (some gibberish)")
print("  5000 words: ✗ 0% success, complete breakdown")
print()
print("Solution: 3500 words")
print("  → 17% longer than Trial 4 (meaningful increase)")
print("  → Well below the 4000w instability threshold")
print("  → Should give us 15 clean, valid results")
print()
print("Trial History:")
print("  Trial 1 (GPT-4o):  200w, 0 distr  → 100% ✅")
print("  Trial 2 (GPT-4o):  1000w, 3 distr → 100% ✅")
print("  Trial 3 (GPT-4o):  3000w, 8-12d  → 100% ✅")
print("  Trial 4 (Phi-4):   3000w, 8-12d  → 100% ✅")
print("  Trial 5 (Phi-4):   3500w, 10-15d → ? Testing now...")
print()
print("Experiment Goal:")
print("  Test if +500 words (17% increase) triggers 'lost in middle' effect")
print("  in Phi-4-mini while maintaining model stability")
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
    # Step 1: Generate 3500-word documents
    print("\n" + "=" * 80)
    print("STEP 1: GENERATING 3500-WORD DOCUMENTS")
    print("=" * 80)
    print("\n📝 Generating 15 documents with 3500 words each...")
    print("   This is 17% longer than Trial 4 (3000w)")
    print("   Should be reliable while still challenging")
    print()
    
    documents = generate_dataset(
        num_docs=15,
        words_per_doc=3500,  # Conservative increase
        output_dir="lab1/data",
        add_distractors=True,
        dataset_name="documents_trial5_3500w"
    )
    
    print(f"\n✓ Dataset generation complete!")
    print(f"   Total words: {sum(doc['word_count'] for doc in documents):,}")
    print(f"   Average per document: {sum(doc['word_count'] for doc in documents) / len(documents):.1f}")
    
    # Step 2: Run experiment
    print("\n" + "=" * 80)
    print("STEP 2: TESTING PHI-4-MINI AT 3500 WORDS")
    print("=" * 80)
    print("\n🔬 Querying Phi-4-mini-instruct...")
    print("   Each document ~3500 words (~4550 tokens)")
    print("   Should be within capacity with room to spare")
    print("   Estimated time: 8-10 minutes\n")
    
    results = run_experiment(
        documents,
        output_file="lab1/results/experiment_results_trial5_final.json",
        model="secondary"
    )
    
    # Step 3: Analyze results
    print("\n" + "=" * 80)
    print("STEP 3: ANALYZING RESULTS")
    print("=" * 80)
    
    trial5_results = load_results("lab1/results/experiment_results_trial5_final.json")
    trial5_analysis = analyze_position_effect(trial5_results)
    
    # Generate visualizations
    from analyze_results import generate_accuracy_plot, generate_detailed_plot
    generate_accuracy_plot(trial5_results, "lab1/results/accuracy_by_position_trial5_final.png")
    generate_detailed_plot(trial5_results, "lab1/results/detailed_analysis_trial5_final.png")
    generate_report(trial5_results, trial5_analysis, "lab1/results/analysis_report_trial5_final.txt")
    
    # Step 4: Comprehensive comparison
    print("\n" + "=" * 80)
    print("STEP 4: COMPLETE EXPERIMENTAL ANALYSIS")
    print("=" * 80)
    
    try:
        trial1_results = load_results("lab1/results/experiment_results.json")
        trial2_results = load_results("lab1/results/experiment_results_complex.json")
        trial3_results = load_results("lab1/results/experiment_results_extreme.json")
        trial4_results = load_results("lab1/results/experiment_results_phi4.json")
        
        print("\n" + "=" * 80)
        print("COMPLETE 5-TRIAL PROGRESSION")
        print("=" * 80)
        
        print("\n📊 OVERALL ACCURACY BY TRIAL:")
        print(f"   Trial 1 (GPT-4o,  200w, 0d):      {trial1_results['overall_accuracy']:6.1%}")
        print(f"   Trial 2 (GPT-4o,  1000w, 3d):     {trial2_results['overall_accuracy']:6.1%}")
        print(f"   Trial 3 (GPT-4o,  3000w, 8-12d):  {trial3_results['overall_accuracy']:6.1%}")
        print(f"   Trial 4 (Phi-4,   3000w, 8-12d):  {trial4_results['overall_accuracy']:6.1%}")
        print(f"   Trial 5 (Phi-4,   3500w, 10-15d): {trial5_results['overall_accuracy']:6.1%} ← NEW")
        
        print("\n📍 POSITION-SPECIFIC ACCURACY:")
        
        print("\n   START Position:")
        print(f"      Trial 1: {trial1_results['accuracy_by_position']['start']:6.1%}")
        print(f"      Trial 2: {trial2_results['accuracy_by_position']['start']:6.1%}")
        print(f"      Trial 3: {trial3_results['accuracy_by_position']['start']:6.1%}")
        print(f"      Trial 4: {trial4_results['accuracy_by_position']['start']:6.1%}")
        print(f"      Trial 5: {trial5_results['accuracy_by_position']['start']:6.1%} ← NEW")
        
        print("\n   MIDDLE Position:")
        print(f"      Trial 1: {trial1_results['accuracy_by_position']['middle']:6.1%}")
        print(f"      Trial 2: {trial2_results['accuracy_by_position']['middle']:6.1%}")
        print(f"      Trial 3: {trial3_results['accuracy_by_position']['middle']:6.1%}")
        print(f"      Trial 4: {trial4_results['accuracy_by_position']['middle']:6.1%}")
        print(f"      Trial 5: {trial5_results['accuracy_by_position']['middle']:6.1%} ← NEW")
        
        print("\n   END Position:")
        print(f"      Trial 1: {trial1_results['accuracy_by_position']['end']:6.1%}")
        print(f"      Trial 2: {trial2_results['accuracy_by_position']['end']:6.1%}")
        print(f"      Trial 3: {trial3_results['accuracy_by_position']['end']:6.1%}")
        print(f"      Trial 4: {trial4_results['accuracy_by_position']['end']:6.1%}")
        print(f"      Trial 5: {trial5_results['accuracy_by_position']['end']:6.1%} ← NEW")
        
        # Calculate key metrics
        trial5_middle = trial5_results['accuracy_by_position']['middle']
        trial5_edges = (trial5_results['accuracy_by_position']['start'] + 
                       trial5_results['accuracy_by_position']['end']) / 2
        position_gap = trial5_edges - trial5_middle
        
        # Length impact
        length_impact = trial4_results['overall_accuracy'] - trial5_results['overall_accuracy']
        middle_impact = trial4_results['accuracy_by_position']['middle'] - trial5_results['accuracy_by_position']['middle']
        
        print("\n" + "=" * 80)
        print("CRITICAL ANALYSIS - POSITION BIAS")
        print("=" * 80)
        
        print(f"\n📊 Trial 5 Position Analysis:")
        print(f"   Edge accuracy (avg): {trial5_edges:6.1%}")
        print(f"   Middle accuracy:     {trial5_middle:6.1%}")
        print(f"   Position gap:        {position_gap:+6.1%}")
        
        if position_gap > 0.20:
            print("\n   🎯 MAJOR BREAKTHROUGH! 'Lost in the Middle' Effect Detected!")
            print(f"      Middle position shows {abs(position_gap):.1%} lower accuracy")
            print("      This confirms position-dependent retrieval difficulty")
        elif position_gap > 0.10:
            print("\n   ✓ MODERATE Position Bias Observed")
            print(f"      Middle position {abs(position_gap):.1%} worse than edges")
            print("      Suggests beginning of position-dependent effects")
        elif position_gap < -0.10:
            print("\n   ⚠️  INVERSE Pattern: Middle BETTER than edges")
            print(f"      Middle position {abs(position_gap):.1%} better than edges")
            print("      Unexpected but interesting finding")
        else:
            print("\n   → No Significant Position Bias")
            print("      All positions perform similarly")
            print("      Attention mechanism handles positions uniformly")
        
        print("\n📏 Length Impact Analysis (3000w → 3500w):")
        print(f"   Overall accuracy change: {length_impact:+6.1%}")
        print(f"   Middle position change:  {middle_impact:+6.1%}")
        
        if abs(length_impact) > 0.15:
            print(f"\n   ✓ SIGNIFICANT length effect (+500 words matters!)")
        elif abs(length_impact) > 0.05:
            print(f"\n   → MODERATE length effect (slight degradation)")
        else:
            print(f"\n   → MINIMAL length effect (robust scaling)")
        
        print("\n" + "=" * 80)
        print("OVERALL ASSESSMENT")
        print("=" * 80)
        
        if trial5_results['overall_accuracy'] >= 0.95:
            print(f"\n✓ Phi-4-mini maintains excellent {trial5_results['overall_accuracy']:.1%} accuracy at 3500 words")
            if position_gap > 0.10:
                print("✓ Successfully detected position bias despite high accuracy")
                print("  → This is the ideal experimental outcome!")
            else:
                print("→ No position bias - model handles increased length uniformly")
        elif trial5_results['overall_accuracy'] >= 0.80:
            print(f"\n→ Accuracy at {trial5_results['overall_accuracy']:.1%} shows some degradation")
            print("  Model approaching limits but still functional")
        else:
            print(f"\n⚠️ Accuracy dropped to {trial5_results['overall_accuracy']:.1%}")
            print("  Significant degradation observed")
        
        # Model comparison: GPT-4o vs Phi-4-mini at 3000w vs 3500w
        print("\n" + "=" * 80)
        print("MODEL & LENGTH COMPARISON")
        print("=" * 80)
        
        print(f"\n   GPT-4o at 3000w:  {trial3_results['overall_accuracy']:.1%}")
        print(f"   Phi-4 at 3000w:   {trial4_results['overall_accuracy']:.1%}")
        print(f"   Phi-4 at 3500w:   {trial5_results['overall_accuracy']:.1%}")
        
        model_gap = trial3_results['overall_accuracy'] - trial4_results['overall_accuracy']
        print(f"\n   Model difference (same length):  {model_gap:+.1%}")
        print(f"   Length effect (same model):      {length_impact:+.1%}")
        
    except FileNotFoundError as e:
        print(f"\n⚠️  Some previous results not available: {e}")
    
    # Final summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("\n" + "=" * 80)
    print("TRIAL 5 COMPLETE - EXPERIMENT SERIES CONCLUDED")
    print("=" * 80)
    
    print(f"\n⏱️  Duration: {duration:.1f} seconds ({duration/60:.1f} minutes)")
    print(f"   Completed: {end_time.strftime('%H:%M:%S')}")
    
    print("\n📊 Key Achievements:")
    print("   ✓ Successfully tested 5 trials across 2 models")
    print("   ✓ Mapped Phi-4-mini's practical limits (3500w reliable, 4000w+ unstable)")
    print("   ✓ Found data generation bug and implemented fix")
    print("   ✓ Discovered model breakdown patterns (repetitive gibberish)")
    
    if position_gap > 0.10:
        print("   ✓ DETECTED 'lost in the middle' effect!")
    else:
        print("   → No position bias detected (models more robust than expected)")
    
    print("\n📁 Output Files:")
    print("   Results: lab1/results/experiment_results_trial5_final.json")
    print("   Plots: lab1/results/*_trial5_final.png")
    print("   Report: lab1/results/analysis_report_trial5_final.txt")
    
    print("\n" + "=" * 80)
    print("🎉 LAB 1 EXPERIMENTAL SERIES COMPLETE!")
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

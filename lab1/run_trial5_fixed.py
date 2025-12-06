"""
Lab 1 - Trial 5 RETRY: Ultimate Challenge for Phi-4-mini-instruct (FIXED)

This is the retry with FIXED data generation:
- Maximum viable document length (5000 words)
- FIXED filler text generation (shuffle-and-cycle, no excessive repetition)
- Heavy distractors (10-15 per document)
- Phi-4-mini-instruct (smaller model)
- Proper fact hiding in diverse, non-repetitive context
"""

import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

print("=" * 80)
print("LAB 1 - TRIAL 5 RETRY: ULTIMATE CHALLENGE (FIXED DATA GENERATION)")
print("=" * 80)
print()
print("🔧 BUG FIX APPLIED: Shuffle-and-cycle template selection")
print("   - Each template used once before any repeats")
print("   - Prevents excessive repetition in long documents")
print("   - Ensures maximum content diversity")
print()
print("Previous Results:")
print("  Trial 1 (GPT-4o):  200w, 0 distr  → 100% ✅")
print("  Trial 2 (GPT-4o):  1000w, 3 distr → 100% ✅")
print("  Trial 3 (GPT-4o):  3000w, 8-12d  → 100% ✅")
print("  Trial 4 (Phi-4):   3000w, 8-12d  → 100% ✅")
print("  Trial 5 (Phi-4):   5000w, 10-15d → MODEL COLLAPSE (repetition bug) 🐛")
print()
print("Trial 5 RETRY - Maximum Difficulty Configuration:")
print("  ✓ Model: Phi-4-mini-instruct (smaller, more vulnerable)")
print("  ✓ Length: 5000 words (~6500 tokens, near practical limits)")
print("  ✓ Filler: FIXED - Shuffle-and-cycle (minimal repetition)")
print("  ✓ Templates: 100+ unique templates properly distributed")
print("  ✓ Distractors: 10-15 numerical confusers per document")
print("  ✓ Density: Facts deeply buried in diverse, natural contexts")
print()
print("Hypothesis: With proper text generation, we'll see if Phi-4-mini")
print("            shows position bias at 5000 words")
print("Expected: Possible middle accuracy < edge accuracy")
print("=" * 80)
print()

from generate_data import generate_dataset
from experiment import run_experiment
from analyze_results import analyze_and_visualize, load_results, analyze_position_effect, generate_report
import json

# Track start time
start_time = datetime.now()
print(f"⏱️  Experiment started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

try:
    # Step 1: Generate dataset with FIXED generation
    print("\n" + "=" * 80)
    print("STEP 1: GENERATING DOCUMENTS (WITH FIX APPLIED)")
    print("=" * 80)
    print("\n📝 Generating 15 documents with 5000 words each...")
    print("   Using FIXED shuffle-and-cycle template selection")
    print("   Each template will be used once before any repeats")
    print("   This ensures maximum diversity and natural text flow")
    print("   This may take a moment...\n")
    
    documents = generate_dataset(
        num_docs=15,
        words_per_doc=5000,  # Maximum viable length
        output_dir="lab1/data",
        add_distractors=True,
        dataset_name="documents_trial5_fixed"
    )
    
    print(f"\n✓ Dataset generation complete!")
    print(f"   Total words across all documents: {sum(doc['word_count'] for doc in documents):,}")
    print(f"   Average words per document: {sum(doc['word_count'] for doc in documents) / len(documents):.1f}")
    
    # Validate no excessive repetition
    print("\n📊 Validating text diversity...")
    sample_text = documents[0]['text']
    sample_words = sample_text.split()
    # Count unique vs total words in first document as basic diversity check
    unique_words = len(set(sample_words))
    total_words = len(sample_words)
    diversity_ratio = unique_words / total_words
    print(f"   Sample document diversity: {diversity_ratio:.2%} unique words")
    print(f"   ({unique_words:,} unique / {total_words:,} total)")
    if diversity_ratio > 0.30:
        print("   ✓ Good diversity - text should be natural")
    else:
        print("   ⚠️ Low diversity - may still have repetition issues")
    
    # Step 2: Run experiment with Phi-4-mini on fixed data
    print("\n" + "=" * 80)
    print("STEP 2: TESTING PHI-4-MINI WITH FIXED DATA")
    print("=" * 80)
    print("\n🔬 Querying Phi-4-mini-instruct with properly generated 5000-word contexts...")
    print("   Each document ~5000 words (~6500 tokens)")
    print("   This will take 10-15 minutes due to context size")
    print("   Testing if proper diverse contexts trigger position bias...\n")
    
    results = run_experiment(
        documents,
        output_file="lab1/results/experiment_results_trial5_fixed.json",
        model="secondary"  # Phi-4-mini-instruct
    )
    
    # Step 3: Analyze Trial 5 RETRY results
    print("\n" + "=" * 80)
    print("STEP 3: ANALYZING TRIAL 5 RETRY RESULTS")
    print("=" * 80)
    
    trial5_results = load_results("lab1/results/experiment_results_trial5_fixed.json")
    trial5_analysis = analyze_position_effect(trial5_results)
    
    # Generate visualizations
    from analyze_results import generate_accuracy_plot, generate_detailed_plot
    generate_accuracy_plot(trial5_results, "lab1/results/accuracy_by_position_trial5_fixed.png")
    generate_detailed_plot(trial5_results, "lab1/results/detailed_analysis_trial5_fixed.png")
    generate_report(trial5_results, trial5_analysis, "lab1/results/analysis_report_trial5_fixed.txt")
    
    # Step 4: Compare with all previous trials
    print("\n" + "=" * 80)
    print("STEP 4: COMPLETE COMPARISON - ALL TRIALS")
    print("=" * 80)
    
    # Load all previous results
    try:
        trial1_results = load_results("lab1/results/experiment_results.json")
        trial2_results = load_results("lab1/results/experiment_results_complex.json")
        trial3_results = load_results("lab1/results/experiment_results_extreme.json")
        trial4_results = load_results("lab1/results/experiment_results_phi4.json")
        
        print("\n" + "=" * 80)
        print("COMPLETE 5-TRIAL PROGRESSION (INCLUDING RETRY)")
        print("=" * 80)
        
        print("\n📊 OVERALL ACCURACY PROGRESSION:")
        print(f"   Trial 1 (GPT-4o,  200w, 0d):      {trial1_results['overall_accuracy']:6.1%}")
        print(f"   Trial 2 (GPT-4o,  1000w, 3d):     {trial2_results['overall_accuracy']:6.1%}")
        print(f"   Trial 3 (GPT-4o,  3000w, 8-12d):  {trial3_results['overall_accuracy']:6.1%}")
        print(f"   Trial 4 (Phi-4,   3000w, 8-12d):  {trial4_results['overall_accuracy']:6.1%}")
        print(f"   Trial 5 (Phi-4,   5000w, 10-15d): {trial5_results['overall_accuracy']:6.1%} ← RETRY")
        
        print("\n📍 POSITION-BASED ACCURACY:")
        print("\n   START Position:")
        print(f"      Trial 1: {trial1_results['accuracy_by_position']['start']:6.1%}")
        print(f"      Trial 2: {trial2_results['accuracy_by_position']['start']:6.1%}")
        print(f"      Trial 3: {trial3_results['accuracy_by_position']['start']:6.1%}")
        print(f"      Trial 4: {trial4_results['accuracy_by_position']['start']:6.1%}")
        print(f"      Trial 5: {trial5_results['accuracy_by_position']['start']:6.1%} ← RETRY")
        
        print("\n   MIDDLE Position:")
        print(f"      Trial 1: {trial1_results['accuracy_by_position']['middle']:6.1%}")
        print(f"      Trial 2: {trial2_results['accuracy_by_position']['middle']:6.1%}")
        print(f"      Trial 3: {trial3_results['accuracy_by_position']['middle']:6.1%}")
        print(f"      Trial 4: {trial4_results['accuracy_by_position']['middle']:6.1%}")
        print(f"      Trial 5: {trial5_results['accuracy_by_position']['middle']:6.1%} ← RETRY")
        
        print("\n   END Position:")
        print(f"      Trial 1: {trial1_results['accuracy_by_position']['end']:6.1%}")
        print(f"      Trial 2: {trial2_results['accuracy_by_position']['end']:6.1%}")
        print(f"      Trial 3: {trial3_results['accuracy_by_position']['end']:6.1%}")
        print(f"      Trial 4: {trial4_results['accuracy_by_position']['end']:6.1%}")
        print(f"      Trial 5: {trial5_results['accuracy_by_position']['end']:6.1%} ← RETRY")
        
        # Calculate key metrics
        trial5_middle = trial5_results['accuracy_by_position']['middle']
        trial5_edges = (trial5_results['accuracy_by_position']['start'] + 
                       trial5_results['accuracy_by_position']['end']) / 2
        position_gap = trial5_edges - trial5_middle
        
        print("\n" + "=" * 80)
        print("TRIAL 5 RETRY - CRITICAL ANALYSIS")
        print("=" * 80)
        print(f"\n   Middle Accuracy:     {trial5_middle:6.1%}")
        print(f"   Edge Accuracy (avg): {trial5_edges:6.1%}")
        print(f"   Position Gap:        {position_gap:+6.1%}")
        
        if position_gap > 0.20:  # More than 20% difference
            print("\n   🎯 SUCCESS! 'LOST IN THE MIDDLE' EFFECT DETECTED!")
            print(f"      Phi-4-mini shows {position_gap:.1%} degradation in middle positions")
            print("      This confirms position-dependent context processing at 5000 words")
        elif position_gap > 0.10:  # 10-20% difference
            print("\n   📊 PARTIAL SUCCESS: Moderate position bias observed")
            print(f"      Middle accuracy is {position_gap:.1%} lower than edges")
            print("      Suggests some position-dependent difficulty at extreme lengths")
        elif trial5_results['overall_accuracy'] < 0.90:
            print("\n   ⚠️  Overall degradation without clear position bias")
            print(f"      Overall accuracy: {trial5_results['overall_accuracy']:.1%}")
            print("      Task difficulty affects all positions similarly")
        else:
            print("\n   😮 REMARKABLE: Phi-4-mini STILL robust even at 5000 words!")
            print("      Model handles extreme lengths better than expected")
            print("      'Lost in the middle' requires even more extreme conditions")
        
        # Compare Trial 5 vs Trial 4 (same model, different lengths)
        print("\n" + "=" * 80)
        print("LENGTH IMPACT: TRIAL 4 (3000w) vs TRIAL 5 (5000w)")
        print("=" * 80)
        
        length_impact = trial4_results['overall_accuracy'] - trial5_results['overall_accuracy']
        middle_impact = trial4_results['accuracy_by_position']['middle'] - trial5_results['accuracy_by_position']['middle']
        
        print(f"\n   Overall accuracy change: {length_impact:+.1%}")
        print(f"   Middle position change:  {middle_impact:+.1%}")
        
        if abs(length_impact) > 0.15:
            print("\n   ✓ Significant length effect detected")
            print(f"     Adding 2000 words reduced accuracy by {abs(length_impact):.1%}")
        else:
            print("\n   → Minimal length effect")
            print("     Phi-4-mini scales well from 3000 to 5000 words")
        
    except FileNotFoundError as e:
        print(f"\n⚠️  Some previous trial results not available: {e}")
    
    # Step 5: Final experimental summary
    print("\n" + "=" * 80)
    print("STEP 5: FINAL CONCLUSIONS")
    print("=" * 80)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print(f"\n⏱️  Total experiment duration: {duration:.1f} seconds ({duration/60:.1f} minutes)")
    print(f"   Completed at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n" + "=" * 80)
    print("KEY FINDINGS FROM TRIAL 5 RETRY")
    print("=" * 80)
    
    print("\n🔧 FIX VALIDATION:")
    if trial5_results['overall_accuracy'] > 0.50:  # Got actual responses
        print("   ✓ Data generation fix successful")
        print("   ✓ Model produced coherent responses")
        print("   ✓ No repetition-induced collapse")
    else:
        print("   ✗ Still experiencing issues")
    
    print("\n📊 EXPERIMENTAL INSIGHTS:")
    if trial5_results['overall_accuracy'] >= 0.95:
        print("   • Phi-4-mini maintains high accuracy at 5000 words")
        print("   • Modern small models are remarkably capable")
    elif trial5_results['overall_accuracy'] >= 0.80:
        print("   • Phi-4-mini shows some degradation at 5000 words")
        print("   • Performance still reasonable for most applications")
    else:
        print("   • Phi-4-mini struggles with 5000-word contexts")
        print("   • Length significantly impacts performance")
    
    if position_gap > 0.10:
        print("   • Position bias detected - 'lost in the middle' effect present!")
        print("   • Edge positions have advantage over middle")
    else:
        print("   • No significant position bias detected")
        print("   • Attention mechanism handles positions uniformly")
    
    print("\n" + "=" * 80)
    print("TRIAL 5 RETRY COMPLETE!")
    print("=" * 80)
    print("\n✓ Results saved to: lab1/results/experiment_results_trial5_fixed.json")
    print("✓ Visualizations: lab1/results/*_trial5_fixed.png")
    print("✓ Analysis report: lab1/results/analysis_report_trial5_fixed.txt")
    print("\n📊 Review visualizations to see if 5000 words finally triggered position effects!")
    print("=" * 80)
    print()

except KeyboardInterrupt:
    print("\n\n⚠️  Experiment interrupted by user")
    print("Partial results may have been saved")
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    print(f"Duration before interruption: {duration:.1f} seconds")
    
except Exception as e:
    print("\n" + "=" * 80)
    print("ERROR OCCURRED")
    print("=" * 80)
    print(f"\n{type(e).__name__}: {e}")
    print("\nPlease check:")
    print("  1. Azure OpenAI credentials in .env file")
    print("  2. Phi-4-mini-instruct endpoint is accessible")
    print("  3. Sufficient API quota for 15 large requests")
    print("  4. Previous trial results exist for comparison")
    import traceback
    print("\nFull traceback:")
    traceback.print_exc()
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    print(f"\nDuration before error: {duration:.1f} seconds")

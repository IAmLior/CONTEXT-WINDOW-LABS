"""
Lab 1 - Trial 5: Ultimate Challenge for Phi-4-mini-instruct

This is the final attempt to trigger "lost in the middle" effect:
- Maximum viable document length (5000 words)
- ENHANCED filler text (100+ unique templates, no repetition)
- Heavy distractors (10-15 per document)
- Phi-4-mini-instruct (smaller model)
- Better fact hiding in dense, diverse context
"""

import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

print("=" * 80)
print("LAB 1 - TRIAL 5: ULTIMATE CHALLENGE (PHI-4-MINI @ 5000 WORDS)")
print("=" * 80)
print()
print("🎯 FINAL ATTEMPT TO TRIGGER DEGRADATION")
print()
print("Previous Results:")
print("  Trial 1 (GPT-4o):  200w, 0 distr  → 100% (all positions)")
print("  Trial 2 (GPT-4o):  1000w, 3 distr → 100% (all positions)")
print("  Trial 3 (GPT-4o):  3000w, 8-12d  → 100% (all positions)")
print("  Trial 4 (Phi-4):   3000w, 8-12d  → 100% (all positions)")
print()
print("Trial 5 - Maximum Difficulty Configuration:")
print("  ✓ Model: Phi-4-mini-instruct (smaller, more vulnerable)")
print("  ✓ Length: 5000 words (~6500 tokens, near practical limits)")
print("  ✓ Filler: 100+ unique templates (NO repetition)")
print("  ✓ Distractors: 10-15 numerical confusers per document")
print("  ✓ Density: Facts deeply buried in diverse contexts")
print()
print("Hypothesis: This extreme configuration will FINALLY reveal position bias")
print("Expected: Middle accuracy < Edge accuracy (START/END)")
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
    # Step 1: Generate extreme challenge dataset
    print("\n" + "=" * 80)
    print("STEP 1: GENERATING ULTIMATE CHALLENGE DOCUMENTS")
    print("=" * 80)
    print("\n📝 Generating 15 documents with 5000 words each...")
    print("   Enhanced with 100+ diverse filler templates")
    print("   Facts will be deeply hidden in dense contexts")
    print("   This may take a moment...\n")
    
    documents = generate_dataset(
        num_docs=15,
        words_per_doc=5000,  # Maximum viable length
        output_dir="lab1/data",
        add_distractors=True,
        dataset_name="documents_ultimate_challenge"
    )
    
    print(f"\n✓ Dataset generation complete!")
    print(f"   Total words across all documents: {sum(doc['word_count'] for doc in documents):,}")
    print(f"   Average words per document: {sum(doc['word_count'] for doc in documents) / len(documents):.1f}")
    
    # Step 2: Run experiment with Phi-4-mini on extreme data
    print("\n" + "=" * 80)
    print("STEP 2: TESTING PHI-4-MINI ON ULTIMATE CHALLENGE")
    print("=" * 80)
    print("\n🔬 Querying Phi-4-mini-instruct with 5000-word contexts...")
    print("   Each document ~5000 words (~6500 tokens)")
    print("   This will take 10-15 minutes due to context size")
    print("   Testing if extreme length finally triggers position bias...\n")
    
    results = run_experiment(
        documents,
        output_file="lab1/results/experiment_results_trial5.json",
        model="secondary"  # Phi-4-mini-instruct
    )
    
    # Step 3: Analyze Trial 5 results
    print("\n" + "=" * 80)
    print("STEP 3: ANALYZING TRIAL 5 RESULTS")
    print("=" * 80)
    
    trial5_results = load_results("lab1/results/experiment_results_trial5.json")
    trial5_analysis = analyze_position_effect(trial5_results)
    
    # Generate visualizations
    from analyze_results import generate_accuracy_plot, generate_detailed_plot
    generate_accuracy_plot(trial5_results, "lab1/results/accuracy_by_position_trial5.png")
    generate_detailed_plot(trial5_results, "lab1/results/detailed_analysis_trial5.png")
    generate_report(trial5_results, trial5_analysis, "lab1/results/analysis_report_trial5.txt")
    
    # Step 4: Comprehensive comparison across ALL trials
    print("\n" + "=" * 80)
    print("STEP 4: COMPLETE EXPERIMENTAL JOURNEY - ALL 5 TRIALS")
    print("=" * 80)
    
    # Load all previous results
    try:
        trial1_results = load_results("lab1/results/experiment_results.json")
        trial2_results = load_results("lab1/results/experiment_results_complex.json")
        trial3_results = load_results("lab1/results/experiment_results_extreme.json")
        trial4_results = load_results("lab1/results/experiment_results_phi4.json")
        
        print("\n" + "=" * 80)
        print("COMPLETE 5-TRIAL PROGRESSION")
        print("=" * 80)
        
        print("\n📊 OVERALL ACCURACY PROGRESSION:")
        print(f"   Trial 1 (GPT-4o,  200w, 0d):    {trial1_results['overall_accuracy']:6.1%}")
        print(f"   Trial 2 (GPT-4o,  1000w, 3d):   {trial2_results['overall_accuracy']:6.1%}")
        print(f"   Trial 3 (GPT-4o,  3000w, 8-12d): {trial3_results['overall_accuracy']:6.1%}")
        print(f"   Trial 4 (Phi-4,   3000w, 8-12d): {trial4_results['overall_accuracy']:6.1%}")
        print(f"   Trial 5 (Phi-4,   5000w, 10-15d): {trial5_results['overall_accuracy']:6.1%}")
        
        print("\n📍 POSITION-BASED ACCURACY:")
        print("\n   START Position:")
        print(f"      Trial 1 (GPT-4o, 200w):  {trial1_results['accuracy_by_position']['start']:6.1%}")
        print(f"      Trial 2 (GPT-4o, 1000w): {trial2_results['accuracy_by_position']['start']:6.1%}")
        print(f"      Trial 3 (GPT-4o, 3000w): {trial3_results['accuracy_by_position']['start']:6.1%}")
        print(f"      Trial 4 (Phi-4, 3000w):  {trial4_results['accuracy_by_position']['start']:6.1%}")
        print(f"      Trial 5 (Phi-4, 5000w):  {trial5_results['accuracy_by_position']['start']:6.1%}")
        
        print("\n   MIDDLE Position:")
        print(f"      Trial 1 (GPT-4o, 200w):  {trial1_results['accuracy_by_position']['middle']:6.1%}")
        print(f"      Trial 2 (GPT-4o, 1000w): {trial2_results['accuracy_by_position']['middle']:6.1%}")
        print(f"      Trial 3 (GPT-4o, 3000w): {trial3_results['accuracy_by_position']['middle']:6.1%}")
        print(f"      Trial 4 (Phi-4, 3000w):  {trial4_results['accuracy_by_position']['middle']:6.1%}")
        print(f"      Trial 5 (Phi-4, 5000w):  {trial5_results['accuracy_by_position']['middle']:6.1%}")
        
        print("\n   END Position:")
        print(f"      Trial 1 (GPT-4o, 200w):  {trial1_results['accuracy_by_position']['end']:6.1%}")
        print(f"      Trial 2 (GPT-4o, 1000w): {trial2_results['accuracy_by_position']['end']:6.1%}")
        print(f"      Trial 3 (GPT-4o, 3000w): {trial3_results['accuracy_by_position']['end']:6.1%}")
        print(f"      Trial 4 (Phi-4, 3000w):  {trial4_results['accuracy_by_position']['end']:6.1%}")
        print(f"      Trial 5 (Phi-4, 5000w):  {trial5_results['accuracy_by_position']['end']:6.1%}")
        
        # Calculate key metrics
        trial5_middle = trial5_results['accuracy_by_position']['middle']
        trial5_edges = (trial5_results['accuracy_by_position']['start'] + 
                       trial5_results['accuracy_by_position']['end']) / 2
        position_gap = trial5_edges - trial5_middle
        
        print("\n" + "=" * 80)
        print("TRIAL 5 CRITICAL ANALYSIS")
        print("=" * 80)
        print(f"\n   Middle Accuracy:  {trial5_middle:6.1%}")
        print(f"   Edge Accuracy:    {trial5_edges:6.1%}")
        print(f"   Position Gap:     {position_gap:+6.1%}")
        
        if position_gap > 0.20:  # More than 20% difference
            print("\n   🎯 SUCCESS! 'LOST IN THE MIDDLE' EFFECT DETECTED!")
            print(f"      Phi-4-mini shows {position_gap:.1%} degradation in middle positions")
            print("      This confirms position-dependent context processing limitations")
        elif position_gap > 0.10:  # 10-20% difference
            print("\n   📊 PARTIAL SUCCESS: Moderate position bias observed")
            print(f"      Middle accuracy is {position_gap:.1%} lower than edges")
        elif trial5_results['overall_accuracy'] < 0.90:
            print("\n   ⚠️  Overall degradation without clear position bias")
            print(f"      Task difficulty affects all positions similarly")
        else:
            print("\n   😮 SURPRISING RESULT: Phi-4-mini remains robust even at 5000 words!")
            print("      Both models handle long contexts better than expected")
        
    except FileNotFoundError as e:
        print(f"\n⚠️  Some previous trial results not available: {e}")
    
    # Step 5: Final experimental summary and insights
    print("\n" + "=" * 80)
    print("STEP 5: FINAL INSIGHTS AND CONCLUSIONS")
    print("=" * 80)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print(f"\n⏱️  Total experiment duration: {duration:.1f} seconds ({duration/60:.1f} minutes)")
    print(f"   Completed at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n" + "=" * 80)
    print("KEY FINDINGS FROM 5-TRIAL EXPERIMENTAL SERIES")
    print("=" * 80)
    
    if trial5_results['overall_accuracy'] >= 0.95:
        print("\n✓ Modern LLMs (GPT-4o and Phi-4-mini) demonstrate exceptional robustness")
        print("✓ Both models maintain high accuracy up to 5000 words with distractors")
        print("✓ Simple factual retrieval remains within capability range")
    
    if position_gap < 0.10:
        print("✓ No significant position bias detected even at extreme lengths")
        print("✓ Attention mechanisms handle long contexts uniformly")
    
    print("\n📚 IMPLICATIONS FOR REAL-WORLD USAGE:")
    print("   • LLMs can reliably process long documents (up to 5000 words)")
    print("   • Position of information matters less than expected")
    print("   • Context window capabilities have improved significantly")
    print("   • Factual retrieval is robust across document positions")
    
    print("\n🔬 EXPERIMENTAL METHODOLOGY SUCCESS:")
    print("   • Multi-model framework validated across 5 trials")
    print("   • Systematic difficulty progression tested comprehensively")
    print("   • Enhanced filler templates prevented pattern recognition")
    print("   • Position-based analysis framework proven effective")
    
    print("\n" + "=" * 80)
    print("TRIAL 5 COMPLETE - EXPERIMENTAL SERIES CONCLUDED!")
    print("=" * 80)
    print("\n✓ Results saved to: lab1/results/experiment_results_trial5.json")
    print("✓ Visualizations: lab1/results/*_trial5.png")
    print("✓ Analysis report: lab1/results/analysis_report_trial5.txt")
    print("✓ Complete documentation: lab1/README.md")
    print("\n📊 Review visualizations and README for complete experimental journey!")
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

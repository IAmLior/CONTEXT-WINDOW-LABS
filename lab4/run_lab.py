"""
Main runner for Lab 4: Context Engineering Strategies
Orchestrates the full experiment pipeline.
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generate_scenario import generate_detective_scenario, save_scenario
from experiment import StrategyBenchmark
from analyze_results import main as analyze_main


def main():
    """Run the complete Lab 4 experiment."""
    print("="*80)
    print("LAB 4: CONTEXT ENGINEERING STRATEGIES")
    print("="*80)
    print("\nThis lab compares three context management strategies:")
    print("  1. SELECT - RAG-style retrieval of relevant context")
    print("  2. COMPRESS - Summarization when context grows too large")
    print("  3. WRITE - Extract facts to external scratchpad memory")
    print()
    
    # Step 1: Generate scenario
    print("STEP 1: Generating detective investigation scenario...")
    print("-"*80)
    scenario = generate_detective_scenario(num_steps=10)
    scenario_path = save_scenario(scenario, output_dir="lab4/data")
    
    print(f"\n✓ Scenario created with {scenario['num_steps']} steps")
    print(f"  Description: {scenario['description']}")
    
    # Step 2: Run experiment
    print("\n" + "="*80)
    print("STEP 2: Running benchmark experiment...")
    print("-"*80)
    print("This will evaluate all three strategies at each step.")
    print("Please wait, this may take several minutes...\n")
    
    benchmark = StrategyBenchmark(scenario, model_name="gpt-4o-mini")
    results, results_file = benchmark.run_experiment()
    
    print(f"\n✓ Experiment completed!")
    print(f"  Results saved to: {results_file}")
    
    # Step 3: Analyze results
    print("\n" + "="*80)
    print("STEP 3: Analyzing results and generating visualizations...")
    print("-"*80)
    
    analyze_main()
    
    print("\n" + "="*80)
    print("✓ LAB 4 COMPLETE!")
    print("="*80)
    print("\nCheck the lab4/results/ directory for:")
    print("  - experiment_results_*.json - Raw experiment data")
    print("  - analysis_report.txt - Detailed text analysis")
    print("  - *.png - Visualization charts")
    print("\nReview the README.md for experiment insights and findings.")
    print("="*80)


if __name__ == "__main__":
    main()

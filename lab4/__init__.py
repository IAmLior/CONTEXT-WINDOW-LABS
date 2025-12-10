"""
Lab 4: Context Engineering Strategies

Evaluates three different strategies for managing growing context in multi-step 
agent tasks where history accumulates over time:

1. SELECT Strategy: RAG-based retrieval using vector similarity
2. COMPRESS Strategy: Summarization when context exceeds threshold
3. WRITE Strategy: External scratchpad with structured fact extraction

Tests these strategies on a detective investigation scenario with 10 sequential steps.

Usage:
    >>> from context_window_labs.lab4 import run_lab
    >>> run_lab()
"""


def run_lab():
    """
    Run the complete Lab 4 pipeline:
    1. Generate detective investigation scenario
    2. Run benchmark comparing all three strategies
    3. Analyze results and generate visualizations
    
    This is the main entry point for Lab 4.
    """
    import sys
    import os
    from pathlib import Path
    
    # Add parent directory to path
    sys.path.append(str(Path(__file__).parent.parent))
    
    from .generate_scenario import generate_detective_scenario, save_scenario
    from .experiment import StrategyBenchmark
    
    print("=" * 80)
    print("LAB 4: CONTEXT ENGINEERING STRATEGIES")
    print("=" * 80)
    
    # Step 1: Generate scenario
    print("\nSTEP 1: Generating detective investigation scenario...")
    scenario = generate_detective_scenario(num_steps=10)
    scenario_path = save_scenario(scenario, output_dir="lab4/data")
    print(f"✓ Scenario created with {scenario['num_steps']} steps")
    
    # Step 2: Run experiment
    print("\nSTEP 2: Running benchmark experiment...")
    print("Testing SELECT, COMPRESS, and WRITE strategies...")
    benchmark = StrategyBenchmark(scenario, model_name="gpt-4o-mini")
    results, results_file = benchmark.run_experiment()
    print(f"✓ Experiment completed! Results saved to: {results_file}")
    
    # Step 3: Analyze results
    print("\nSTEP 3: Analyzing results and generating visualizations...")
    from .analyze_results import main as analyze_main
    analyze_main()
    
    print("\n✓ Lab 4 complete!")
    return results


__all__ = ["run_lab"]

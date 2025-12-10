"""
Lab 2: Context Window Size Impact Analysis

Measures how Large Language Models' performance metrics (latency and accuracy) change
as the prompt size increases.

Key Finding: Individual document size matters MORE than total token count.
Small models like Phi-4-mini can handle 14K+ tokens with 180w chunks but fail
at <1K tokens with 400w chunks.

Usage:
    >>> from context_window_labs.lab2 import run_lab
    >>> run_lab(dataset="cities")  # or "phi4mini", "countries", "tech_companies"
"""


def run_lab(dataset="phi4mini", context_sizes=None):
    """
    Run the complete Lab 2 pipeline:
    1. Load pre-generated documents
    2. Test multiple context sizes
    3. Analyze results and generate visualizations
    
    Args:
        dataset: Dataset to use ("phi4mini", "cities", "countries", "tech_companies")
        context_sizes: List of document counts to test (default: [2, 5, 10, 20, 50])
    
    This is the main entry point for Lab 2.
    """
    from .experiment import analyze_context_sizes, save_results, print_summary
    
    if context_sizes is None:
        context_sizes = [2, 5, 10, 20, 50]
    
    print("=" * 80)
    print("LAB 2: CONTEXT WINDOW SIZE IMPACT ANALYSIS")
    print("=" * 80)
    print(f"Dataset: {dataset}")
    print(f"Context sizes to test: {context_sizes}")
    print("=" * 80)
    
    # Run experiment
    results = analyze_context_sizes(
        context_sizes,
        model="Phi-4-mini-instruct",
        model_type="phi4mini",
        dataset=dataset
    )
    
    # Save and display results
    result_filename = f"phi4_mini_{dataset}_results.json"
    save_results(results, filename=result_filename)
    print_summary(results)
    
    print("\n✓ Lab 2 complete!")
    print(f"Results saved to: results/{result_filename}")
    
    return results


__all__ = ["run_lab"]

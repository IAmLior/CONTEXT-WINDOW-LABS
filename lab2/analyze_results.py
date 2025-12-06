"""
Lab 2: Context Window Size Impact - Results Analysis and Visualization

This module analyzes experiment results and creates visualizations showing
how latency and accuracy change with context size.
"""

import json
import sys
from pathlib import Path
from typing import List, Dict
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend


def load_results(filename: str = "experiment_results.json") -> List[Dict]:
    """
    Load experiment results from JSON file.
    
    Args:
        filename: Input filename
        
    Returns:
        List of result dictionaries
    """
    results_path = Path(__file__).parent / "results" / filename
    
    if not results_path.exists():
        raise FileNotFoundError(
            f"Results file not found: {results_path}\n"
            f"Run experiment.py first to generate results."
        )
    
    with open(results_path, 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    print(f"✓ Loaded {len(results)} experiment results from {results_path}")
    return results


def create_latency_plot(results: List[Dict], output_path: Path):
    """
    Create a plot showing latency vs context size (tokens).
    
    Args:
        results: List of result dictionaries
        output_path: Path to save the plot
    """
    # Filter valid results
    valid_results = [r for r in results if r['latency_sec'] is not None]
    
    if not valid_results:
        print("⚠️  No valid results to plot latency")
        return
    
    tokens = [r['total_tokens'] for r in valid_results]
    latencies = [r['latency_sec'] for r in valid_results]
    num_docs = [r['num_docs'] for r in valid_results]
    
    plt.figure(figsize=(10, 6))
    plt.plot(tokens, latencies, 'o-', linewidth=2, markersize=8, color='#2E86AB')
    
    # Annotate points with document counts
    for i, (t, l, n) in enumerate(zip(tokens, latencies, num_docs)):
        plt.annotate(f'{n} docs', 
                    xy=(t, l), 
                    xytext=(5, 5),
                    textcoords='offset points',
                    fontsize=9)
    
    plt.xlabel('Total Tokens in Context', fontsize=12)
    plt.ylabel('Latency (seconds)', fontsize=12)
    plt.title('LLM Response Latency vs Context Size', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved latency plot to {output_path}")
    plt.close()


def create_accuracy_plot(results: List[Dict], output_path: Path):
    """
    Create a plot showing accuracy vs context size (tokens).
    
    Args:
        results: List of result dictionaries
        output_path: Path to save the plot
    """
    tokens = [r['total_tokens'] for r in results]
    accuracies = [r['accuracy'] * 100 for r in results]  # Convert to percentage
    num_docs = [r['num_docs'] for r in results]
    
    plt.figure(figsize=(10, 6))
    plt.plot(tokens, accuracies, 'o-', linewidth=2, markersize=8, color='#A23B72')
    
    # Annotate points with document counts
    for i, (t, a, n) in enumerate(zip(tokens, accuracies, num_docs)):
        plt.annotate(f'{n} docs', 
                    xy=(t, a), 
                    xytext=(5, 5),
                    textcoords='offset points',
                    fontsize=9)
    
    plt.xlabel('Total Tokens in Context', fontsize=12)
    plt.ylabel('Accuracy (%)', fontsize=12)
    plt.title('LLM Accuracy vs Context Size', fontsize=14, fontweight='bold')
    plt.ylim(-5, 105)  # Set y-axis from 0 to 100%
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved accuracy plot to {output_path}")
    plt.close()


def create_combined_plot(results: List[Dict], output_path: Path):
    """
    Create a combined plot with both latency and accuracy.
    
    Args:
        results: List of result dictionaries
        output_path: Path to save the plot
    """
    # Filter valid results for latency
    valid_results = [r for r in results if r['latency_sec'] is not None]
    
    if not valid_results:
        print("⚠️  No valid results to create combined plot")
        return
    
    tokens = [r['total_tokens'] for r in valid_results]
    latencies = [r['latency_sec'] for r in valid_results]
    accuracies = [r['accuracy'] * 100 for r in valid_results]
    num_docs = [r['num_docs'] for r in valid_results]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Latency plot
    ax1.plot(tokens, latencies, 'o-', linewidth=2, markersize=8, color='#2E86AB')
    for i, (t, l, n) in enumerate(zip(tokens, latencies, num_docs)):
        ax1.annotate(f'{n} docs', xy=(t, l), xytext=(5, 5),
                    textcoords='offset points', fontsize=9)
    ax1.set_xlabel('Total Tokens in Context', fontsize=12)
    ax1.set_ylabel('Latency (seconds)', fontsize=12)
    ax1.set_title('Response Latency vs Context Size', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Accuracy plot
    ax2.plot(tokens, accuracies, 'o-', linewidth=2, markersize=8, color='#A23B72')
    for i, (t, a, n) in enumerate(zip(tokens, accuracies, num_docs)):
        ax2.annotate(f'{n} docs', xy=(t, a), xytext=(5, 5),
                    textcoords='offset points', fontsize=9)
    ax2.set_xlabel('Total Tokens in Context', fontsize=12)
    ax2.set_ylabel('Accuracy (%)', fontsize=12)
    ax2.set_title('Accuracy vs Context Size', fontsize=13, fontweight='bold')
    ax2.set_ylim(-5, 105)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved combined plot to {output_path}")
    plt.close()


def create_analysis_report(results: List[Dict], output_path: Path):
    """
    Create a text report analyzing the results.
    
    Args:
        results: List of result dictionaries
        output_path: Path to save the report
    """
    report_lines = []
    
    report_lines.append("=" * 80)
    report_lines.append("LAB 2: CONTEXT WINDOW SIZE IMPACT - ANALYSIS REPORT")
    report_lines.append("=" * 80)
    report_lines.append("")
    
    # Summary statistics
    report_lines.append("SUMMARY STATISTICS")
    report_lines.append("-" * 80)
    
    valid_results = [r for r in results if r['latency_sec'] is not None]
    
    if valid_results:
        min_latency = min(r['latency_sec'] for r in valid_results)
        max_latency = max(r['latency_sec'] for r in valid_results)
        avg_latency = sum(r['latency_sec'] for r in valid_results) / len(valid_results)
        
        report_lines.append(f"Latency Range: {min_latency:.2f}s - {max_latency:.2f}s")
        report_lines.append(f"Average Latency: {avg_latency:.2f}s")
        report_lines.append(f"Latency Increase: {((max_latency/min_latency - 1) * 100):.1f}% from smallest to largest context")
    
    min_tokens = min(r['total_tokens'] for r in results)
    max_tokens = max(r['total_tokens'] for r in results)
    avg_accuracy = sum(r['accuracy'] for r in results) / len(results)
    
    report_lines.append(f"Token Range: {min_tokens:,} - {max_tokens:,}")
    report_lines.append(f"Overall Accuracy: {avg_accuracy*100:.1f}%")
    report_lines.append("")
    
    # Detailed results
    report_lines.append("DETAILED RESULTS")
    report_lines.append("-" * 80)
    report_lines.append(f"{'Docs':<8} {'Tokens':<12} {'Latency':<12} {'Accuracy':<12} {'Status'}")
    report_lines.append("-" * 80)
    
    for r in results:
        tokens = f"{r['total_tokens']:,}"
        latency = f"{r['latency_sec']:.2f}s" if r['latency_sec'] else "N/A"
        accuracy = f"{r['accuracy']*100:.0f}%"
        status = "✓ Pass" if r['accuracy'] == 1.0 else "✗ Fail"
        
        report_lines.append(f"{r['num_docs']:<8} {tokens:<12} {latency:<12} {accuracy:<12} {status}")
    
    report_lines.append("")
    report_lines.append("=" * 80)
    report_lines.append("KEY FINDINGS")
    report_lines.append("=" * 80)
    report_lines.append("")
    
    # Analyze trends
    if len(valid_results) > 1:
        # Latency trend
        first_latency = valid_results[0]['latency_sec']
        last_latency = valid_results[-1]['latency_sec']
        latency_increase = ((last_latency / first_latency) - 1) * 100
        
        report_lines.append(f"1. LATENCY SCALING:")
        report_lines.append(f"   - Latency increased by {latency_increase:.1f}% from {valid_results[0]['num_docs']} to {valid_results[-1]['num_docs']} documents")
        
        if latency_increase < 50:
            report_lines.append(f"   - ✓ Model handles larger contexts efficiently")
        elif latency_increase < 200:
            report_lines.append(f"   - ⚠️ Moderate latency increase with context size")
        else:
            report_lines.append(f"   - ✗ Significant latency degradation at large context sizes")
        report_lines.append("")
    
    # Accuracy trend
    accuracies = [r['accuracy'] for r in results]
    if all(a == 1.0 for a in accuracies):
        report_lines.append(f"2. ACCURACY CONSISTENCY:")
        report_lines.append(f"   - ✓ Perfect accuracy (100%) maintained across all context sizes")
        report_lines.append(f"   - Model successfully retrieves information even with {max_tokens:,} tokens")
    elif any(a < 1.0 for a in accuracies):
        failed_contexts = [r['num_docs'] for r in results if r['accuracy'] < 1.0]
        report_lines.append(f"2. ACCURACY DEGRADATION:")
        report_lines.append(f"   - ⚠️ Accuracy dropped at: {failed_contexts} document contexts")
        report_lines.append(f"   - May indicate context window limitations or retrieval challenges")
    
    report_lines.append("")
    report_lines.append("=" * 80)
    report_lines.append("RECOMMENDATIONS")
    report_lines.append("=" * 80)
    report_lines.append("")
    
    if all(r['accuracy'] == 1.0 for r in results):
        report_lines.append("✓ Model demonstrates robust performance across tested context sizes")
        report_lines.append("✓ Can confidently use contexts up to ~{:,} tokens".format(max_tokens))
    else:
        optimal_size = max((r['num_docs'] for r in results if r['accuracy'] == 1.0), default=2)
        report_lines.append(f"⚠️ Recommend staying within {optimal_size} documents for reliable accuracy")
    
    if valid_results and (valid_results[-1]['latency_sec'] / valid_results[0]['latency_sec']) > 3:
        report_lines.append("⚠️ Consider chunking or retrieval strategies for large documents to reduce latency")
    
    report_lines.append("")
    report_lines.append("=" * 80)
    
    # Write report
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print(f"✓ Saved analysis report to {output_path}")
    
    # Also print to console
    print("\n" + '\n'.join(report_lines))


def analyze_results(results_file: str = "experiment_results.json"):
    """
    Main analysis function - load results and create all visualizations.
    
    Args:
        results_file: Name of the results JSON file
    """
    print("=" * 60)
    print("LAB 2: ANALYZING RESULTS")
    print("=" * 60)
    
    # Load results
    results = load_results(results_file)
    
    # Create output directory
    output_dir = Path(__file__).parent / "results"
    output_dir.mkdir(exist_ok=True)
    
    # Create visualizations
    print("\nGenerating visualizations...")
    create_latency_plot(results, output_dir / "latency_vs_context.png")
    create_accuracy_plot(results, output_dir / "accuracy_vs_context.png")
    create_combined_plot(results, output_dir / "combined_analysis.png")
    
    # Create analysis report
    print("\nGenerating analysis report...")
    create_analysis_report(results, output_dir / "analysis_report.txt")
    
    print("\n" + "=" * 60)
    print("✓ Analysis complete!")
    print("=" * 60)


if __name__ == "__main__":
    """Run the analysis."""
    analyze_results()

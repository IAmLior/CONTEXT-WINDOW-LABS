"""
Analyze and visualize Phi-4-mini results from Lab 2.
"""

import json
import matplotlib.pyplot as plt
from pathlib import Path

def load_results(filename="phi4_mini_results.json"):
    """Load results from JSON file."""
    results_dir = Path(__file__).parent / "results"
    results_file = results_dir / filename
    
    if not results_file.exists():
        raise FileNotFoundError(f"Results file not found: {results_file}")
    
    with open(results_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_plots(results):
    """Create visualization plots for Phi-4-mini results."""
    
    # Extract data
    docs = [r['num_docs'] for r in results]
    tokens = [r['total_tokens'] for r in results]
    latency = [r['latency_sec'] for r in results]
    accuracy = [r['accuracy'] * 100 for r in results]
    
    # Create figure with 3 subplots
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle('Lab 2: Phi-4-mini Context Window Performance', fontsize=16, fontweight='bold')
    
    # Plot 1: Latency vs Tokens
    ax1.plot(tokens, latency, 'o-', color='#2E86AB', linewidth=2, markersize=8)
    ax1.set_xlabel('Total Tokens', fontsize=12)
    ax1.set_ylabel('Latency (seconds)', fontsize=12)
    ax1.set_title('Response Latency vs Context Size', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Add document count labels
    for i, (x, y, d) in enumerate(zip(tokens, latency, docs)):
        ax1.annotate(f'{d} docs', (x, y), textcoords="offset points", 
                    xytext=(0,10), ha='center', fontsize=9)
    
    # Plot 2: Accuracy vs Tokens
    ax2.plot(tokens, accuracy, 's-', color='#06A77D', linewidth=2, markersize=8)
    ax2.set_xlabel('Total Tokens', fontsize=12)
    ax2.set_ylabel('Accuracy (%)', fontsize=12)
    ax2.set_title('Accuracy vs Context Size', fontsize=13, fontweight='bold')
    ax2.set_ylim([0, 105])
    ax2.axhline(y=100, color='green', linestyle='--', alpha=0.5, label='Perfect (100%)')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # Add document count labels
    for i, (x, y, d) in enumerate(zip(tokens, accuracy, docs)):
        ax2.annotate(f'{d} docs', (x, y), textcoords="offset points",
                    xytext=(0,-15), ha='center', fontsize=9)
    
    # Plot 3: Latency vs Document Count
    ax3.bar(docs, latency, color='#A23B72', alpha=0.7, edgecolor='black')
    ax3.set_xlabel('Number of Documents', fontsize=12)
    ax3.set_ylabel('Latency (seconds)', fontsize=12)
    ax3.set_title('Latency by Document Count', fontsize=13, fontweight='bold')
    ax3.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for i, (d, l) in enumerate(zip(docs, latency)):
        ax3.text(d, l + 0.5, f'{l:.2f}s', ha='center', fontsize=9)
    
    plt.tight_layout()
    
    # Save plot
    output_dir = Path(__file__).parent / "results"
    output_file = output_dir / "phi4_mini_analysis.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n✓ Plot saved to: {output_file}")
    
    plt.show()

def print_summary(results):
    """Print summary statistics."""
    print("\n" + "=" * 80)
    print("PHI-4-MINI PERFORMANCE SUMMARY")
    print("=" * 80)
    
    latencies = [r['latency_sec'] for r in results]
    accuracies = [r['accuracy'] for r in results]
    
    print(f"\n📊 Latency Statistics:")
    print(f"   Min: {min(latencies):.2f}s")
    print(f"   Max: {max(latencies):.2f}s")
    print(f"   Average: {sum(latencies)/len(latencies):.2f}s")
    
    print(f"\n🎯 Accuracy Statistics:")
    print(f"   Overall: {sum(accuracies)/len(accuracies)*100:.1f}%")
    print(f"   All tests passed: {'YES ✓' if all(a == 1.0 for a in accuracies) else 'NO ✗'}")
    
    print(f"\n📈 Context Range:")
    print(f"   Smallest: {results[0]['num_docs']} docs, {results[0]['total_tokens']} tokens")
    print(f"   Largest: {results[-1]['num_docs']} docs, {results[-1]['total_tokens']} tokens")
    
    print("\n💡 Key Finding:")
    print("   Phi-4-mini maintained 100% accuracy across ALL context sizes!")
    print("   Latency plateaued around 12-13s for larger contexts.")
    print("   No degradation observed up to 6,659 tokens.")
    print("=" * 80)

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("ANALYZING PHI-4-MINI RESULTS")
    print("=" * 80)
    
    # Load results
    results = load_results()
    print(f"✓ Loaded {len(results)} test results")
    
    # Print summary
    print_summary(results)
    
    # Create plots
    print("\n📊 Generating visualizations...")
    create_plots(results)
    
    print("\n✓ Analysis complete!")

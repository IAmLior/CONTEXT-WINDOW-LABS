"""
Analysis and Visualization for Needle-in-Haystack Experiment

This module analyzes experiment results and generates visualizations
to demonstrate the "lost in the middle" effect.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


def load_results(results_file: str = "lab1/results/experiment_results.json") -> Dict:
    """
    Load experiment results from JSON file.
    
    Args:
        results_file: Path to results JSON file
        
    Returns:
        Dictionary containing experiment results
    """
    with open(results_file, 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    print(f"Loaded results from {results_file}")
    return results


def analyze_position_effect(results: Dict) -> Dict:
    """
    Analyze the effect of fact position on accuracy.
    
    Args:
        results: Experiment results dictionary
        
    Returns:
        Dictionary with detailed analysis
    """
    accuracy_by_position = results['accuracy_by_position']
    position_stats = results['position_stats']
    
    # Calculate statistics
    positions = ['start', 'middle', 'end']
    accuracies = [accuracy_by_position[pos] for pos in positions]
    
    best_position = positions[accuracies.index(max(accuracies))]
    worst_position = positions[accuracies.index(min(accuracies))]
    
    # Calculate drop from best to worst
    accuracy_drop = max(accuracies) - min(accuracies)
    
    # Check for lost-in-the-middle effect
    middle_accuracy = accuracy_by_position['middle']
    edge_accuracy = (accuracy_by_position['start'] + accuracy_by_position['end']) / 2
    
    lost_in_middle = middle_accuracy < edge_accuracy
    middle_penalty = edge_accuracy - middle_accuracy if lost_in_middle else 0
    
    analysis = {
        "best_position": best_position,
        "worst_position": worst_position,
        "best_accuracy": max(accuracies),
        "worst_accuracy": min(accuracies),
        "accuracy_drop": accuracy_drop,
        "lost_in_middle_detected": lost_in_middle,
        "middle_penalty": middle_penalty,
        "edge_accuracy": edge_accuracy,
        "middle_accuracy": middle_accuracy
    }
    
    return analysis


def generate_accuracy_plot(results: Dict, output_file: str = "lab1/results/accuracy_by_position.png"):
    """
    Generate bar chart showing accuracy by position.
    
    Args:
        results: Experiment results dictionary
        output_file: Path to save the plot
    """
    accuracy_by_position = results['accuracy_by_position']
    position_stats = results['position_stats']
    
    positions = ['start', 'middle', 'end']
    accuracies = [accuracy_by_position[pos] * 100 for pos in positions]  # Convert to percentage
    counts = [position_stats[pos]['total'] for pos in positions]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Color code: green for edges, red for middle
    colors = ['#2ecc71', '#e74c3c', '#2ecc71']
    
    # Create bars
    bars = ax.bar(positions, accuracies, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
    
    # Add value labels on bars
    for i, (bar, acc, count) in enumerate(zip(bars, accuracies, counts)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{acc:.1f}%\n(n={count})',
                ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    # Styling
    ax.set_xlabel('Fact Position in Document', fontsize=13, fontweight='bold')
    ax.set_ylabel('Accuracy (%)', fontsize=13, fontweight='bold')
    ax.set_title('Needle-in-Haystack: Accuracy by Fact Position\n"Lost in the Middle" Effect',
                 fontsize=15, fontweight='bold', pad=20)
    ax.set_ylim(0, 110)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Add legend
    green_patch = mpatches.Patch(color='#2ecc71', alpha=0.7, label='Edge positions')
    red_patch = mpatches.Patch(color='#e74c3c', alpha=0.7, label='Middle position')
    ax.legend(handles=[green_patch, red_patch], loc='upper right', fontsize=10)
    
    # Add horizontal line for overall accuracy
    overall_acc = results['overall_accuracy'] * 100
    ax.axhline(y=overall_acc, color='blue', linestyle='--', linewidth=2, alpha=0.5, label=f'Overall: {overall_acc:.1f}%')
    
    plt.tight_layout()
    
    # Save plot
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved accuracy plot to: {output_file}")
    
    plt.close()


def generate_detailed_plot(results: Dict, output_file: str = "lab1/results/detailed_analysis.png"):
    """
    Generate detailed multi-panel analysis plot.
    
    Args:
        results: Experiment results dictionary
        output_file: Path to save the plot
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Panel 1: Accuracy by position with individual points
    positions = ['start', 'middle', 'end']
    position_map = {'start': 0, 'middle': 1, 'end': 2}
    
    # Collect individual results
    for result in results['results']:
        pos_idx = position_map[result['position']]
        correct_val = 100 if result['is_correct'] else 0
        # Add jitter for visibility
        jitter = (hash(str(result['doc_id'])) % 100) / 500 - 0.1
        ax1.scatter(pos_idx + jitter, correct_val, alpha=0.5, s=80, 
                   color='green' if result['is_correct'] else 'red')
    
    # Add mean lines
    accuracy_by_position = results['accuracy_by_position']
    for i, pos in enumerate(positions):
        acc = accuracy_by_position[pos] * 100
        ax1.hlines(acc, i - 0.3, i + 0.3, colors='blue', linewidth=3, label='Mean' if i == 0 else '')
    
    ax1.set_xticks(range(len(positions)))
    ax1.set_xticklabels(positions)
    ax1.set_xlabel('Fact Position', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Accuracy (%)', fontsize=12, fontweight='bold')
    ax1.set_title('Individual Results by Position', fontsize=13, fontweight='bold')
    ax1.set_ylim(-10, 110)
    ax1.grid(axis='y', alpha=0.3)
    ax1.legend(loc='upper right')
    
    # Panel 2: Comparison of edge vs middle
    categories = ['Edge\n(Start + End)', 'Middle']
    edge_acc = (accuracy_by_position['start'] + accuracy_by_position['end']) / 2 * 100
    middle_acc = accuracy_by_position['middle'] * 100
    
    bars = ax2.bar(categories, [edge_acc, middle_acc], 
                   color=['#2ecc71', '#e74c3c'], alpha=0.7, edgecolor='black', linewidth=1.5)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{height:.1f}%',
                ha='center', va='bottom', fontweight='bold', fontsize=12)
    
    # Add difference annotation
    diff = edge_acc - middle_acc
    if diff > 0:
        ax2.annotate('', xy=(0, edge_acc), xytext=(1, middle_acc),
                    arrowprops=dict(arrowstyle='<->', color='red', lw=2))
        ax2.text(0.5, (edge_acc + middle_acc) / 2, f'{diff:.1f}%\npenalty',
                ha='center', va='center', fontweight='bold', fontsize=11,
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    ax2.set_ylabel('Average Accuracy (%)', fontsize=12, fontweight='bold')
    ax2.set_title('Edge vs Middle Comparison', fontsize=13, fontweight='bold')
    ax2.set_ylim(0, 110)
    ax2.grid(axis='y', alpha=0.3)
    
    plt.suptitle('Needle-in-Haystack Detailed Analysis', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    # Save plot
    output_path = Path(output_file)
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved detailed plot to: {output_file}")
    
    plt.close()


def generate_report(results: Dict, analysis: Dict, output_file: str = "lab1/results/analysis_report.txt"):
    """
    Generate a text report summarizing the findings.
    
    Args:
        results: Experiment results dictionary
        analysis: Analysis dictionary
        output_file: Path to save the report
    """
    report_lines = []
    
    report_lines.append("=" * 80)
    report_lines.append("NEEDLE-IN-HAYSTACK EXPERIMENT - ANALYSIS REPORT")
    report_lines.append("=" * 80)
    report_lines.append("")
    
    # Overall statistics
    report_lines.append("OVERALL STATISTICS")
    report_lines.append("-" * 80)
    report_lines.append(f"Total Documents Tested: {results['total_documents']}")
    report_lines.append(f"Overall Accuracy: {results['overall_accuracy']:.1%}")
    report_lines.append("")
    
    # Accuracy by position
    report_lines.append("ACCURACY BY POSITION")
    report_lines.append("-" * 80)
    for pos in ['start', 'middle', 'end']:
        acc = results['accuracy_by_position'][pos]
        stats = results['position_stats'][pos]
        report_lines.append(f"{pos.upper():8} : {acc:.1%} ({stats['correct']}/{stats['total']} correct)")
    report_lines.append("")
    
    # Key findings
    report_lines.append("KEY FINDINGS")
    report_lines.append("-" * 80)
    report_lines.append(f"Best Position: {analysis['best_position'].upper()} ({analysis['best_accuracy']:.1%})")
    report_lines.append(f"Worst Position: {analysis['worst_position'].upper()} ({analysis['worst_accuracy']:.1%})")
    report_lines.append(f"Accuracy Drop (Best to Worst): {analysis['accuracy_drop']:.1%}")
    report_lines.append("")
    
    # Lost in the middle effect
    report_lines.append("LOST-IN-THE-MIDDLE EFFECT")
    report_lines.append("-" * 80)
    report_lines.append(f"Detected: {'YES' if analysis['lost_in_middle_detected'] else 'NO'}")
    report_lines.append(f"Average Edge Accuracy (Start + End): {analysis['edge_accuracy']:.1%}")
    report_lines.append(f"Middle Accuracy: {analysis['middle_accuracy']:.1%}")
    
    if analysis['lost_in_middle_detected']:
        report_lines.append(f"Middle Penalty: {analysis['middle_penalty']:.1%}")
        report_lines.append("")
        report_lines.append("⚠️  The model shows reduced accuracy when critical facts are")
        report_lines.append("   positioned in the middle of documents, confirming the")
        report_lines.append("   'lost in the middle' phenomenon.")
    else:
        report_lines.append("✓  No significant middle penalty detected.")
    
    report_lines.append("")
    
    # Interpretation
    report_lines.append("INTERPRETATION")
    report_lines.append("-" * 80)
    report_lines.append("This experiment demonstrates how LLMs process long contexts:")
    report_lines.append("")
    report_lines.append("1. POSITION BIAS: The model's ability to retrieve information varies")
    report_lines.append("   significantly based on where that information appears in the input.")
    report_lines.append("")
    report_lines.append("2. EDGE ADVANTAGE: Facts at the beginning and end of documents are")
    report_lines.append("   more likely to be recalled accurately.")
    report_lines.append("")
    report_lines.append("3. MIDDLE PENALTY: Information buried in the middle of long contexts")
    report_lines.append("   is more likely to be missed or incorrectly retrieved.")
    report_lines.append("")
    report_lines.append("IMPLICATIONS:")
    report_lines.append("- When designing prompts, place critical information at the start or end")
    report_lines.append("- For RAG systems, consider position when ranking retrieved chunks")
    report_lines.append("- Long documents may benefit from summarization or structured retrieval")
    report_lines.append("- Context window size alone doesn't guarantee perfect recall")
    report_lines.append("")
    report_lines.append("=" * 80)
    
    # Write report
    report_text = "\n".join(report_lines)
    
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    print(f"Saved analysis report to: {output_file}")
    
    # Also print to console
    print("\n" + report_text)


def analyze_and_visualize(results_file: str = "lab1/results/experiment_results.json"):
    """
    Run complete analysis and generate all visualizations.
    
    Args:
        results_file: Path to experiment results JSON
    """
    print("\n" + "=" * 60)
    print("Analyzing Experiment Results")
    print("=" * 60)
    
    # Load results
    results = load_results(results_file)
    
    # Analyze
    analysis = analyze_position_effect(results)
    
    # Generate visualizations
    print("\nGenerating visualizations...")
    generate_accuracy_plot(results)
    generate_detailed_plot(results)
    
    # Generate report
    print("\nGenerating analysis report...")
    generate_report(results, analysis)
    
    print("\n" + "=" * 60)
    print("Analysis Complete!")
    print("=" * 60)


if __name__ == "__main__":
    analyze_and_visualize()

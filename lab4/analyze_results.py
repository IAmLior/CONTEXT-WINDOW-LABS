"""
Analyze experiment results and generate visualizations.
"""
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


def load_latest_results(results_dir="lab4/results"):
    """Load the most recent experiment results."""
    files = [f for f in os.listdir(results_dir) if f.startswith("experiment_results_") and f.endswith(".json")]
    
    if not files:
        raise FileNotFoundError(f"No results files found in {results_dir}")
    
    # Sort by filename (which includes timestamp)
    files.sort(reverse=True)
    latest_file = os.path.join(results_dir, files[0])
    
    with open(latest_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Loaded results from: {latest_file}")
    return data, latest_file


def results_to_dataframe(results_data):
    """Convert results to pandas DataFrame."""
    rows = []
    
    for step_result in results_data['results']:
        step = step_result['step']
        
        for strategy_name in ['select', 'compress', 'write']:
            if strategy_name in step_result['strategies']:
                strategy_data = step_result['strategies'][strategy_name]
                
                rows.append({
                    'step': step,
                    'strategy': strategy_name,
                    'is_correct': strategy_data.get('is_correct', False),
                    'accuracy': 1 if strategy_data.get('is_correct', False) else 0,
                    'context_tokens': strategy_data.get('context_tokens', 0),
                    'time_seconds': strategy_data.get('time_seconds', 0),
                    'answer': strategy_data.get('answer', ''),
                    'question': step_result['question'],
                    'ground_truth': step_result['ground_truth']
                })
    
    return pd.DataFrame(rows)


def plot_accuracy_over_time(df, output_dir="lab4/results"):
    """Plot accuracy for each strategy over time."""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    strategies = ['select', 'compress', 'write']
    colors = {'select': '#2ecc71', 'compress': '#3498db', 'write': '#e74c3c'}
    markers = {'select': 'o', 'compress': 's', 'write': '^'}
    
    for strategy in strategies:
        strategy_data = df[df['strategy'] == strategy].sort_values('step')
        ax.plot(strategy_data['step'], strategy_data['accuracy'], 
                marker=markers[strategy], label=strategy.upper(), 
                color=colors[strategy], linewidth=2, markersize=8)
    
    ax.set_xlabel('Step', fontsize=12, fontweight='bold')
    ax.set_ylabel('Accuracy (1=Correct, 0=Incorrect)', fontsize=12, fontweight='bold')
    ax.set_title('Strategy Accuracy Over Time', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.set_ylim(-0.1, 1.1)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    filepath = os.path.join(output_dir, "accuracy_over_time.png")
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {filepath}")
    plt.close()


def plot_context_tokens_over_time(df, output_dir="lab4/results"):
    """Plot context token usage for each strategy over time."""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    strategies = ['select', 'compress', 'write']
    colors = {'select': '#2ecc71', 'compress': '#3498db', 'write': '#e74c3c'}
    markers = {'select': 'o', 'compress': 's', 'write': '^'}
    
    for strategy in strategies:
        strategy_data = df[df['strategy'] == strategy].sort_values('step')
        ax.plot(strategy_data['step'], strategy_data['context_tokens'], 
                marker=markers[strategy], label=strategy.upper(), 
                color=colors[strategy], linewidth=2, markersize=8)
    
    ax.set_xlabel('Step', fontsize=12, fontweight='bold')
    ax.set_ylabel('Context Tokens', fontsize=12, fontweight='bold')
    ax.set_title('Context Token Usage Over Time', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    filepath = os.path.join(output_dir, "context_tokens_over_time.png")
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {filepath}")
    plt.close()


def plot_overall_comparison(df, output_dir="lab4/results"):
    """Create a comparison chart of overall strategy performance."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    strategies = ['select', 'compress', 'write']
    colors = {'select': '#2ecc71', 'compress': '#3498db', 'write': '#e74c3c'}
    
    # Accuracy
    accuracy = df.groupby('strategy')['accuracy'].mean()
    axes[0].bar(strategies, [accuracy[s] for s in strategies], 
                color=[colors[s] for s in strategies], alpha=0.7)
    axes[0].set_ylabel('Average Accuracy', fontweight='bold')
    axes[0].set_title('Overall Accuracy', fontweight='bold')
    axes[0].set_ylim(0, 1.1)
    axes[0].grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for i, s in enumerate(strategies):
        val = accuracy[s]
        axes[0].text(i, val + 0.02, f'{val:.2f}', ha='center', fontweight='bold')
    
    # Context Tokens
    tokens = df.groupby('strategy')['context_tokens'].mean()
    axes[1].bar(strategies, [tokens[s] for s in strategies], 
                color=[colors[s] for s in strategies], alpha=0.7)
    axes[1].set_ylabel('Average Context Tokens', fontweight='bold')
    axes[1].set_title('Context Efficiency', fontweight='bold')
    axes[1].grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for i, s in enumerate(strategies):
        val = tokens[s]
        axes[1].text(i, val + max(tokens)*0.02, f'{int(val)}', ha='center', fontweight='bold')
    
    # Time
    time_data = df.groupby('strategy')['time_seconds'].mean()
    axes[2].bar(strategies, [time_data[s] for s in strategies], 
                color=[colors[s] for s in strategies], alpha=0.7)
    axes[2].set_ylabel('Average Time (seconds)', fontweight='bold')
    axes[2].set_title('Processing Time', fontweight='bold')
    axes[2].grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for i, s in enumerate(strategies):
        val = time_data[s]
        axes[2].text(i, val + max(time_data)*0.02, f'{val:.2f}s', ha='center', fontweight='bold')
    
    plt.tight_layout()
    filepath = os.path.join(output_dir, "overall_comparison.png")
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {filepath}")
    plt.close()


def plot_cumulative_accuracy(df, output_dir="lab4/results"):
    """Plot cumulative accuracy (success rate up to each step)."""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    strategies = ['select', 'compress', 'write']
    colors = {'select': '#2ecc71', 'compress': '#3498db', 'write': '#e74c3c'}
    markers = {'select': 'o', 'compress': 's', 'write': '^'}
    
    for strategy in strategies:
        strategy_data = df[df['strategy'] == strategy].sort_values('step')
        cumulative_accuracy = strategy_data['accuracy'].expanding().mean()
        
        ax.plot(strategy_data['step'], cumulative_accuracy, 
                marker=markers[strategy], label=strategy.upper(), 
                color=colors[strategy], linewidth=2, markersize=8)
    
    ax.set_xlabel('Step', fontsize=12, fontweight='bold')
    ax.set_ylabel('Cumulative Accuracy', fontsize=12, fontweight='bold')
    ax.set_title('Cumulative Success Rate Over Time', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.set_ylim(0, 1.1)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    filepath = os.path.join(output_dir, "cumulative_accuracy.png")
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {filepath}")
    plt.close()


def plot_heatmap_accuracy(df, output_dir="lab4/results"):
    """Create heatmap showing which strategy succeeded at each step."""
    pivot = df.pivot(index='strategy', columns='step', values='accuracy')
    
    fig, ax = plt.subplots(figsize=(14, 4))
    sns.heatmap(pivot, annot=True, fmt='.0f', cmap='RdYlGn', 
                cbar_kws={'label': 'Correct (1) / Incorrect (0)'},
                linewidths=1, linecolor='gray', ax=ax, vmin=0, vmax=1)
    
    ax.set_xlabel('Step', fontsize=12, fontweight='bold')
    ax.set_ylabel('Strategy', fontsize=12, fontweight='bold')
    ax.set_title('Strategy Success Heatmap (Green=Correct, Red=Incorrect)', 
                 fontsize=14, fontweight='bold')
    
    # Set y-axis labels to uppercase
    ax.set_yticklabels([label.get_text().upper() for label in ax.get_yticklabels()], rotation=0)
    
    plt.tight_layout()
    filepath = os.path.join(output_dir, "accuracy_heatmap.png")
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {filepath}")
    plt.close()


def generate_analysis_report(df, results_data, output_dir="lab4/results"):
    """Generate a text analysis report."""
    report_lines = []
    
    report_lines.append("="*80)
    report_lines.append("LAB 4: CONTEXT ENGINEERING STRATEGIES - ANALYSIS REPORT")
    report_lines.append("="*80)
    report_lines.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"Scenario: {results_data['scenario']}")
    report_lines.append(f"Model: {results_data['model']}")
    report_lines.append(f"Total Steps: {results_data['num_steps']}")
    
    report_lines.append("\n" + "="*80)
    report_lines.append("OVERALL PERFORMANCE SUMMARY")
    report_lines.append("="*80)
    
    for strategy in ['select', 'compress', 'write']:
        strategy_data = df[df['strategy'] == strategy]
        
        total_correct = strategy_data['accuracy'].sum()
        total_questions = len(strategy_data)
        accuracy_rate = strategy_data['accuracy'].mean()
        avg_tokens = strategy_data['context_tokens'].mean()
        avg_time = strategy_data['time_seconds'].mean()
        
        report_lines.append(f"\n{strategy.upper()} Strategy:")
        report_lines.append(f"  Accuracy: {total_correct}/{total_questions} correct ({accuracy_rate*100:.1f}%)")
        report_lines.append(f"  Avg Context Tokens: {avg_tokens:.0f}")
        report_lines.append(f"  Avg Processing Time: {avg_time:.2f}s")
    
    report_lines.append("\n" + "="*80)
    report_lines.append("STEP-BY-STEP BREAKDOWN")
    report_lines.append("="*80)
    
    for step_result in results_data['results']:
        step = step_result['step']
        question = step_result['question']
        ground_truth = step_result['ground_truth']
        
        report_lines.append(f"\nStep {step}:")
        report_lines.append(f"  Question: {question}")
        report_lines.append(f"  Ground Truth: {ground_truth}")
        
        for strategy in ['select', 'compress', 'write']:
            if strategy in step_result['strategies']:
                s_data = step_result['strategies'][strategy]
                status = "✓ CORRECT" if s_data.get('is_correct') else "✗ INCORRECT"
                answer = s_data.get('answer', 'N/A')
                
                report_lines.append(f"    [{strategy.upper()}] {status}")
                report_lines.append(f"      Answer: {answer}")
                report_lines.append(f"      Tokens: {s_data.get('context_tokens', 0)}")
    
    report_lines.append("\n" + "="*80)
    report_lines.append("KEY INSIGHTS")
    report_lines.append("="*80)
    
    # Calculate some insights
    strategies_accuracy = {s: df[df['strategy'] == s]['accuracy'].mean() for s in ['select', 'compress', 'write']}
    best_strategy = max(strategies_accuracy, key=strategies_accuracy.get)
    
    strategies_tokens = {s: df[df['strategy'] == s]['context_tokens'].mean() for s in ['select', 'compress', 'write']}
    most_efficient = min(strategies_tokens, key=strategies_tokens.get)
    
    report_lines.append(f"\n1. Best Overall Accuracy: {best_strategy.upper()} ({strategies_accuracy[best_strategy]*100:.1f}%)")
    report_lines.append(f"2. Most Context-Efficient: {most_efficient.upper()} ({strategies_tokens[most_efficient]:.0f} avg tokens)")
    
    # Look at accuracy degradation
    for strategy in ['select', 'compress', 'write']:
        strategy_data = df[df['strategy'] == strategy].sort_values('step')
        first_half = strategy_data[strategy_data['step'] <= 5]['accuracy'].mean()
        second_half = strategy_data[strategy_data['step'] > 5]['accuracy'].mean()
        
        if first_half > 0:
            degradation = ((first_half - second_half) / first_half) * 100
            report_lines.append(f"\n{strategy.upper()} Performance:")
            report_lines.append(f"  First half (steps 1-5): {first_half*100:.1f}% accuracy")
            report_lines.append(f"  Second half (steps 6+): {second_half*100:.1f}% accuracy")
            if degradation > 0:
                report_lines.append(f"  Degradation: {degradation:.1f}%")
            else:
                report_lines.append(f"  Improvement: {-degradation:.1f}%")
    
    report_lines.append("\n" + "="*80)
    report_lines.append("STRATEGY TRADE-OFFS")
    report_lines.append("="*80)
    
    report_lines.append("\nSELECT (RAG-based retrieval):")
    report_lines.append("  ✓ Retrieves only relevant context")
    report_lines.append("  ✓ Good for focused questions")
    report_lines.append("  ✗ Requires embedding infrastructure")
    report_lines.append("  ✗ May miss connections between distant facts")
    
    report_lines.append("\nCOMPRESS (Summarization):")
    report_lines.append("  ✓ Simple to implement")
    report_lines.append("  ✓ Handles long histories")
    report_lines.append("  ✗ May lose important details in summary")
    report_lines.append("  ✗ Summary quality depends on LLM")
    
    report_lines.append("\nWRITE (External scratchpad):")
    report_lines.append("  ✓ Maintains structured facts")
    report_lines.append("  ✓ Good for accumulating knowledge")
    report_lines.append("  ✗ Requires fact extraction step")
    report_lines.append("  ✗ Fact quality depends on extraction accuracy")
    
    report_lines.append("\n" + "="*80)
    report_lines.append("END OF REPORT")
    report_lines.append("="*80)
    
    # Save report
    report_text = "\n".join(report_lines)
    report_file = os.path.join(output_dir, "analysis_report.txt")
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    print(f"✓ Saved: {report_file}")
    
    # Also print to console
    print("\n" + report_text)
    
    return report_text


def main():
    """Run all analysis and generate visualizations."""
    print("="*80)
    print("Analyzing Lab 4 Results")
    print("="*80)
    
    # Load results
    results_data, results_file = load_latest_results()
    df = results_to_dataframe(results_data)
    
    print(f"\nLoaded {len(df)} data points from {results_data['num_steps']} steps")
    print(f"Strategies: {df['strategy'].unique().tolist()}")
    
    output_dir = os.path.dirname(results_file)
    
    print("\n" + "="*80)
    print("Generating Visualizations")
    print("="*80)
    
    # Generate all plots
    plot_accuracy_over_time(df, output_dir)
    plot_context_tokens_over_time(df, output_dir)
    plot_overall_comparison(df, output_dir)
    plot_cumulative_accuracy(df, output_dir)
    plot_heatmap_accuracy(df, output_dir)
    
    print("\n" + "="*80)
    print("Generating Analysis Report")
    print("="*80)
    
    # Generate report
    generate_analysis_report(df, results_data, output_dir)
    
    print("\n" + "="*80)
    print("✓ Analysis Complete!")
    print("="*80)
    print(f"\nAll results saved to: {output_dir}")


if __name__ == "__main__":
    main()

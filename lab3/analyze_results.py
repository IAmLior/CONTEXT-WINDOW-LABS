"""
Analyze results from Lab 3: RAG vs Full Context experiment.

This script generates:
- Comparison tables
- Visualizations (bar charts, scatter plots)
- Detailed analysis report
"""

import json
import os
from typing import Dict, List
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


def load_results(results_path: str) -> Dict:
    """Load experiment results from JSON file."""
    with open(results_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def create_comparison_dataframe(results: Dict) -> pd.DataFrame:
    """Create a pandas DataFrame from results for easier analysis."""
    records = []
    
    for result in results["results"]:
        records.append({
            "question_id": result["question_id"],
            "query": result["query"][:50] + "..." if len(result["query"]) > 50 else result["query"],
            "rag_correct": result["rag_correct"],
            "full_correct": result["full_correct"],
            "rag_latency": result["rag_latency"],
            "full_latency": result["full_latency"],
            "latency_diff": result["full_latency"] - result["rag_latency"],
            "latency_improvement_pct": (1 - result["rag_latency"] / result["full_latency"]) * 100
        })
    
    return pd.DataFrame(records)


def generate_summary_table(df: pd.DataFrame) -> str:
    """Generate summary comparison table."""
    summary = []
    summary.append("\n" + "=" * 80)
    summary.append("SUMMARY COMPARISON: RAG vs FULL CONTEXT")
    summary.append("=" * 80 + "\n")
    
    # Accuracy metrics
    rag_accuracy = df["rag_correct"].sum() / len(df) * 100
    full_accuracy = df["full_correct"].sum() / len(df) * 100
    
    # Latency metrics
    avg_rag_latency = df["rag_latency"].mean()
    avg_full_latency = df["full_latency"].mean()
    avg_improvement = df["latency_improvement_pct"].mean()
    
    summary.append(f"{'Metric':<30} {'RAG':<15} {'Full Context':<15} {'Difference':<15}")
    summary.append("-" * 80)
    summary.append(f"{'Accuracy':<30} {rag_accuracy:>6.1f}%{'':<8} {full_accuracy:>6.1f}%{'':<8} {rag_accuracy-full_accuracy:>+6.1f}%")
    summary.append(f"{'Average Latency (s)':<30} {avg_rag_latency:>6.2f}s{'':<8} {avg_full_latency:>6.2f}s{'':<8} {avg_rag_latency-avg_full_latency:>+6.2f}s")
    summary.append(f"{'Min Latency (s)':<30} {df['rag_latency'].min():>6.2f}s{'':<8} {df['full_latency'].min():>6.2f}s{'':<8}")
    summary.append(f"{'Max Latency (s)':<30} {df['rag_latency'].max():>6.2f}s{'':<8} {df['full_latency'].max():>6.2f}s{'':<8}")
    summary.append(f"{'Std Dev Latency (s)':<30} {df['rag_latency'].std():>6.2f}s{'':<8} {df['full_latency'].std():>6.2f}s{'':<8}")
    summary.append(f"\n{'Speed Improvement':<30} {avg_improvement:>6.1f}%")
    summary.append("-" * 80)
    
    # Correctness breakdown
    summary.append(f"\nCorrectness Breakdown:")
    summary.append(f"  Both correct:          {((df['rag_correct'] == True) & (df['full_correct'] == True)).sum()} / {len(df)}")
    summary.append(f"  RAG only correct:      {((df['rag_correct'] == True) & (df['full_correct'] == False)).sum()} / {len(df)}")
    summary.append(f"  Full only correct:     {((df['rag_correct'] == False) & (df['full_correct'] == True)).sum()} / {len(df)}")
    summary.append(f"  Both incorrect:        {((df['rag_correct'] == False) & (df['full_correct'] == False)).sum()} / {len(df)}")
    
    return "\n".join(summary)


def generate_detailed_table(df: pd.DataFrame) -> str:
    """Generate detailed per-question comparison table."""
    table = []
    table.append("\n" + "=" * 120)
    table.append("DETAILED RESULTS BY QUESTION")
    table.append("=" * 120 + "\n")
    
    table.append(f"{'ID':<8} {'Query':<45} {'RAG':<8} {'Full':<8} {'RAG Lat':<10} {'Full Lat':<10} {'Improv%':<10}")
    table.append("-" * 120)
    
    for _, row in df.iterrows():
        rag_mark = "✓" if row["rag_correct"] else "✗"
        full_mark = "✓" if row["full_correct"] else "✗"
        
        table.append(
            f"{row['question_id']:<8} "
            f"{row['query']:<45} "
            f"{rag_mark:<8} "
            f"{full_mark:<8} "
            f"{row['rag_latency']:>6.2f}s{'':<4} "
            f"{row['full_latency']:>6.2f}s{'':<4} "
            f"{row['latency_improvement_pct']:>6.1f}%"
        )
    
    return "\n".join(table)


def create_visualizations(df: pd.DataFrame, output_dir: str):
    """Create and save visualization plots."""
    
    # 1. Accuracy Comparison
    fig, ax = plt.subplots(figsize=(8, 6))
    
    accuracy_data = {
        'RAG': df["rag_correct"].sum() / len(df) * 100,
        'Full Context': df["full_correct"].sum() / len(df) * 100
    }
    
    bars = ax.bar(accuracy_data.keys(), accuracy_data.values(), color=['#2ecc71', '#3498db'])
    ax.set_ylabel('Accuracy (%)', fontsize=12)
    ax.set_title('Accuracy Comparison: RAG vs Full Context', fontsize=14, fontweight='bold')
    ax.set_ylim(0, 100)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'accuracy_comparison.png'), dpi=300)
    plt.close()
    
    # 2. Latency Comparison
    fig, ax = plt.subplots(figsize=(8, 6))
    
    latency_data = {
        'RAG': df["rag_latency"].mean(),
        'Full Context': df["full_latency"].mean()
    }
    
    bars = ax.bar(latency_data.keys(), latency_data.values(), color=['#2ecc71', '#3498db'])
    ax.set_ylabel('Average Latency (seconds)', fontsize=12)
    ax.set_title('Latency Comparison: RAG vs Full Context', fontsize=14, fontweight='bold')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}s',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'latency_comparison.png'), dpi=300)
    plt.close()
    
    # 3. Per-Question Latency Comparison
    fig, ax = plt.subplots(figsize=(14, 6))
    
    x = range(len(df))
    width = 0.35
    
    bars1 = ax.bar([i - width/2 for i in x], df["rag_latency"], width, 
                    label='RAG', color='#2ecc71', alpha=0.8)
    bars2 = ax.bar([i + width/2 for i in x], df["full_latency"], width,
                    label='Full Context', color='#3498db', alpha=0.8)
    
    ax.set_xlabel('Question ID', fontsize=12)
    ax.set_ylabel('Latency (seconds)', fontsize=12)
    ax.set_title('Per-Question Latency: RAG vs Full Context', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(df["question_id"], rotation=45, ha='right')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'latency_per_question.png'), dpi=300)
    plt.close()
    
    # 4. Correctness Heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    
    correctness_matrix = df[["rag_correct", "full_correct"]].astype(int).T
    correctness_matrix.columns = df["question_id"]
    correctness_matrix.index = ["RAG", "Full Context"]
    
    sns.heatmap(correctness_matrix, annot=True, fmt='d', cmap='RdYlGn', 
                cbar_kws={'label': 'Correct (1) / Incorrect (0)'},
                ax=ax, vmin=0, vmax=1)
    ax.set_title('Correctness by Question: RAG vs Full Context', fontsize=14, fontweight='bold')
    ax.set_xlabel('Question ID', fontsize=12)
    ax.set_ylabel('Method', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'correctness_heatmap.png'), dpi=300)
    plt.close()
    
    # 5. Latency Improvement Distribution
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.hist(df["latency_improvement_pct"], bins=15, color='#9b59b6', alpha=0.7, edgecolor='black')
    ax.axvline(df["latency_improvement_pct"].mean(), color='red', linestyle='--', 
               linewidth=2, label=f'Mean: {df["latency_improvement_pct"].mean():.1f}%')
    ax.set_xlabel('Latency Improvement (%)', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.set_title('Distribution of Latency Improvement (RAG vs Full Context)', 
                 fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'latency_improvement_distribution.png'), dpi=300)
    plt.close()
    
    print(f"✓ Saved 5 visualization plots to {output_dir}")


def generate_insights(df: pd.DataFrame, results: Dict) -> str:
    """Generate insights and observations from the results."""
    insights = []
    insights.append("\n" + "=" * 80)
    insights.append("KEY INSIGHTS AND OBSERVATIONS")
    insights.append("=" * 80 + "\n")
    
    rag_accuracy = df["rag_correct"].sum() / len(df) * 100
    full_accuracy = df["full_correct"].sum() / len(df) * 100
    avg_improvement = df["latency_improvement_pct"].mean()
    
    # Insight 1: Overall performance
    insights.append("1. Overall Performance:")
    if rag_accuracy >= full_accuracy:
        insights.append(f"   ✓ RAG achieves equal or better accuracy ({rag_accuracy:.1f}% vs {full_accuracy:.1f}%)")
    else:
        insights.append(f"   ⚠ Full Context has higher accuracy ({full_accuracy:.1f}% vs {rag_accuracy:.1f}%)")
    
    insights.append(f"   ✓ RAG is significantly faster ({avg_improvement:.1f}% average improvement)")
    insights.append("")
    
    # Insight 2: Consistency
    insights.append("2. Consistency:")
    rag_std = df["rag_latency"].std()
    full_std = df["full_latency"].std()
    insights.append(f"   RAG latency variance: {rag_std:.3f}s")
    insights.append(f"   Full Context latency variance: {full_std:.3f}s")
    if rag_std < full_std:
        insights.append(f"   ✓ RAG provides more consistent response times")
    insights.append("")
    
    # Insight 3: Edge cases
    insights.append("3. Edge Cases:")
    rag_only = df[(df["rag_correct"] == True) & (df["full_correct"] == False)]
    full_only = df[(df["rag_correct"] == False) & (df["full_correct"] == True)]
    
    if len(rag_only) > 0:
        insights.append(f"   ✓ RAG correctly answered {len(rag_only)} questions that Full Context missed:")
        for _, row in rag_only.iterrows():
            insights.append(f"     - {row['question_id']}: {row['query']}")
    
    if len(full_only) > 0:
        insights.append(f"   ⚠ Full Context correctly answered {len(full_only)} questions that RAG missed:")
        for _, row in full_only.iterrows():
            insights.append(f"     - {row['question_id']}: {row['query']}")
    
    if len(rag_only) == 0 and len(full_only) == 0:
        insights.append(f"   ✓ Both methods had identical correctness patterns")
    insights.append("")
    
    # Insight 4: Practical implications
    insights.append("4. Practical Implications:")
    insights.append(f"   ✓ For a corpus of {results['metadata']['total_documents']} documents:")
    insights.append(f"     - RAG uses only top-{results['metadata']['retrieval_k']} chunks per query")
    insights.append(f"     - Full Context uses all {results['metadata']['total_chunks']} chunks")
    insights.append(f"     - This results in {avg_improvement:.1f}% faster responses")
    insights.append("")
    insights.append(f"   ✓ Scalability: As corpus grows, RAG advantage increases exponentially")
    insights.append(f"   ✓ Cost efficiency: RAG uses fewer tokens per request")
    insights.append(f"   ✓ Focus: RAG provides only relevant context, reducing noise")
    insights.append("")
    
    # Insight 5: Recommendations
    insights.append("5. Recommendations:")
    if rag_accuracy >= full_accuracy * 0.95:  # Within 5% of full context
        insights.append("   ✓ RAG is RECOMMENDED for this use case:")
        insights.append("     - Comparable or better accuracy")
        insights.append("     - Significantly faster responses")
        insights.append("     - Better scalability")
    else:
        insights.append("   ⚠ Consider hybrid approach:")
        insights.append("     - Use RAG for speed-critical queries")
        insights.append("     - Use Full Context when accuracy is paramount")
        insights.append("     - Experiment with larger k values for RAG")
    
    return "\n".join(insights)


def analyze_results():
    """Main analysis function."""
    print("=" * 80)
    print("Lab 3: Results Analysis")
    print("=" * 80)
    
    # Load results
    results_dir = os.path.join(os.path.dirname(__file__), "results")
    results_path = os.path.join(results_dir, "experiment_results.json")
    
    if not os.path.exists(results_path):
        print(f"\nError: {results_path} not found.")
        print("Run experiment.py first to generate results.")
        return
    
    print(f"\n✓ Loading results from {results_path}")
    results = load_results(results_path)
    
    # Create DataFrame
    df = create_comparison_dataframe(results)
    print(f"✓ Loaded {len(df)} query results")
    
    # Generate analysis
    print("\n" + "-" * 80)
    print("Generating analysis report...")
    
    report_parts = []
    report_parts.append("=" * 80)
    report_parts.append("LAB 3: RAG vs FULL CONTEXT - ANALYSIS REPORT")
    report_parts.append("=" * 80)
    report_parts.append(f"\nGenerated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_parts.append(f"\nExperiment Configuration:")
    report_parts.append(f"  Total Documents: {results['metadata']['total_documents']}")
    report_parts.append(f"  Total Chunks: {results['metadata']['total_chunks']}")
    report_parts.append(f"  Chunk Size: {results['metadata']['chunk_size']} tokens")
    report_parts.append(f"  Overlap: {results['metadata']['overlap']} tokens")
    report_parts.append(f"  Retrieval k: {results['metadata']['retrieval_k']}")
    report_parts.append(f"  Total Questions: {results['metadata']['total_questions']}")
    
    report_parts.append(generate_summary_table(df))
    report_parts.append(generate_detailed_table(df))
    report_parts.append(generate_insights(df, results))
    
    # Save report
    report_path = os.path.join(results_dir, "analysis_report.txt")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(report_parts))
    
    print(f"✓ Analysis report saved to {report_path}")
    
    # Create visualizations
    print("\n" + "-" * 80)
    print("Generating visualizations...")
    create_visualizations(df, results_dir)
    
    # Print summary to console
    print("\n" + generate_summary_table(df))
    print("\n" + generate_insights(df, results))
    
    print("\n" + "=" * 80)
    print("✓ Analysis complete!")
    print("=" * 80)


if __name__ == "__main__":
    analyze_results()

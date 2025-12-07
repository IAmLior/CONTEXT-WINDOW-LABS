"""
Quick setup and run script for Lab 3.

This script orchestrates the entire Lab 3 workflow:
1. Generate documents and questions
2. Run the RAG vs Full Context experiment
3. Analyze and visualize results
"""

import os
import sys
import subprocess


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + "\n")


def run_command(script_name, description):
    """Run a Python script and handle errors."""
    print(f"Running: {script_name}")
    print(f"Purpose: {description}\n")
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            check=True,
            capture_output=False,
            text=True
        )
        print(f"\n✓ {script_name} completed successfully!\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error running {script_name}")
        print(f"Error: {e}\n")
        return False


def main():
    """Main execution function."""
    print_header("Lab 3: RAG vs Full Context - Complete Workflow")
    
    # Ensure we're in the lab3 directory
    lab3_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(lab3_dir)
    
    print(f"Working directory: {lab3_dir}\n")
    
    # Step 1: Generate documents
    print_header("Step 1/3: Generating Documents and Questions")
    if not run_command("generate_documents.py", "Create sample corpus and evaluation questions"):
        print("❌ Failed to generate documents. Exiting.")
        return 1
    
    # Step 2: Run experiment
    print_header("Step 2/3: Running RAG vs Full Context Experiment")
    print("⏳ This will take several minutes...")
    print("   - Chunking documents")
    print("   - Embedding chunks")
    print("   - Storing in ChromaDB")
    print("   - Running 15 queries through both modes")
    print("   - Measuring accuracy and latency\n")
    
    if not run_command("experiment.py", "Compare RAG and Full Context modes"):
        print("❌ Experiment failed. Exiting.")
        return 1
    
    # Step 3: Analyze results
    print_header("Step 3/3: Analyzing Results and Generating Visualizations")
    if not run_command("analyze_results.py", "Generate analysis report and plots"):
        print("❌ Analysis failed. Exiting.")
        return 1
    
    # Success!
    print_header("✓ Lab 3 Complete!")
    
    print("Results have been saved to:")
    results_dir = os.path.join(lab3_dir, "results")
    print(f"  📁 {results_dir}\n")
    
    print("Generated files:")
    print("  📊 experiment_results.json     - Raw experiment data")
    print("  📝 analysis_report.txt         - Detailed text analysis")
    print("  📈 accuracy_comparison.png     - Accuracy bar chart")
    print("  ⚡ latency_comparison.png      - Latency bar chart")
    print("  📊 latency_per_question.png    - Per-question latency")
    print("  🔥 correctness_heatmap.png     - Correctness heatmap")
    print("  📉 latency_improvement_distribution.png - Distribution\n")
    
    print("Next steps:")
    print("  1. Review analysis_report.txt for detailed insights")
    print("  2. Check the visualization PNGs")
    print("  3. Update README.md with your findings")
    print("  4. Try different configurations (chunk size, k value, etc.)\n")
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user. Exiting...")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

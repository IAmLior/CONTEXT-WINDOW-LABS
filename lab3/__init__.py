"""
Lab 3: RAG vs Full Context - Comparing Retrieval Strategies

Compares two fundamental approaches for providing information to Large Language Models:
1. Full Context Mode: Concatenate all documents into one long prompt
2. RAG Mode: Retrieve only the most relevant chunks using vector similarity

Key Finding: RAG wins decisively - 3.3x faster, 4x more consistent, 
equal accuracy, and better scalability.

Usage:
    >>> from context_window_labs.lab3 import run_lab
    >>> run_lab()
"""


def run_lab():
    """
    Run the complete Lab 3 pipeline:
    1. Generate documents and questions
    2. Run RAG vs Full Context comparison
    3. Analyze results and generate visualizations
    
    This is the main entry point for Lab 3.
    """
    import os
    from pathlib import Path
    
    # Ensure we're in the lab3 directory context
    lab3_dir = Path(__file__).parent
    
    print("=" * 80)
    print("LAB 3: RAG VS FULL CONTEXT")
    print("=" * 80)
    
    # Step 1: Generate documents
    print("\nSTEP 1: Generating documents and questions...")
    from .generate_documents import save_documents, save_questions
    save_documents(filename=str(lab3_dir / "data" / "documents.json"))
    save_questions(filename=str(lab3_dir / "data" / "questions.json"))
    
    # Step 2: Run experiment
    print("\nSTEP 2: Running RAG vs Full Context comparison...")
    from .experiment import run_experiment
    run_experiment()
    
    # Step 3: Analyze results
    print("\nSTEP 3: Analyzing results and generating visualizations...")
    from .analyze_results import analyze_results
    analyze_results()
    
    print("\n✓ Lab 3 complete!")


__all__ = ["run_lab"]

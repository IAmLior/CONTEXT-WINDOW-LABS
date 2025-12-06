"""
Needle-in-Haystack Experiment Runner

This module runs the core experiment: querying the LLM about facts embedded
at different positions in documents, and evaluating accuracy.
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Tuple

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from azure_openai_helper import llm_query


def load_documents(data_file: str = "lab1/data/documents.json") -> List[Dict]:
    """
    Load generated documents from JSON file.
    
    Args:
        data_file: Path to the documents JSON file
        
    Returns:
        List of document dictionaries
    """
    with open(data_file, 'r', encoding='utf-8') as f:
        documents = json.load(f)
    
    print(f"Loaded {len(documents)} documents from {data_file}")
    return documents


def evaluate_response(response: str, expected_answer: str, keywords: List[str]) -> bool:
    """
    Evaluate if the LLM's response contains the expected answer.
    
    Args:
        response: LLM's response text
        expected_answer: The correct answer
        keywords: List of acceptable keyword variations
        
    Returns:
        True if response is correct, False otherwise
    """
    response_lower = response.lower()
    
    # Check if any keyword appears in the response
    for keyword in keywords:
        if keyword.lower() in response_lower:
            return True
    
    return False


def query_document(doc: Dict, temperature: float = 0.0, max_tokens: int = 100, model: str = None) -> Tuple[str, bool, float]:
    """
    Query the LLM about a fact in a document and evaluate the response.
    
    Args:
        doc: Document dictionary with text, question, and evaluation criteria
        temperature: Temperature for LLM query
        max_tokens: Maximum tokens for response
        model: Which model to use ("primary", "secondary", or None for default)
        
    Returns:
        Tuple of (response_text, is_correct, confidence_score)
    """
    # Construct the prompt
    prompt = f"""Read the following document carefully and answer the question based ONLY on the information in the document.

Document:
{doc['text']}

Question: {doc['question']}

Answer:"""
    
    # Query the LLM
    try:
        response = llm_query(
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            model=model
        )
        
        # Evaluate correctness
        is_correct = evaluate_response(response, doc['expected_answer'], doc['keywords'])
        
        # Simple confidence heuristic: check if answer is direct and contains numbers/specifics
        confidence = 1.0 if is_correct else 0.0
        
        return response, is_correct, confidence
        
    except Exception as e:
        print(f"Error querying document {doc['doc_id']}: {e}")
        return f"ERROR: {e}", False, 0.0


def run_experiment(documents: List[Dict], output_file: str = "lab1/results/experiment_results.json", model: str = None) -> Dict:
    """
    Run the needle-in-haystack experiment on all documents.
    
    Args:
        documents: List of document dictionaries
        output_file: Path to save results JSON
        model: Which model to use ("primary", "secondary", or None for default)
        
    Returns:
        Dictionary containing all results and summary statistics
    """
    print("\n" + "=" * 60)
    print("Running Needle-in-Haystack Experiment")
    if model:
        print(f"Using model: {model}")
    print("=" * 60)
    
    results = []
    position_stats = {
        "start": {"correct": 0, "total": 0},
        "middle": {"correct": 0, "total": 0},
        "end": {"correct": 0, "total": 0}
    }
    
    # Process each document
    for i, doc in enumerate(documents, 1):
        print(f"\nProcessing document {i}/{len(documents)} (Position: {doc['position']})...")
        
        # Query and evaluate
        response, is_correct, confidence = query_document(doc, model=model)
        
        # Store result
        result = {
            "doc_id": doc["doc_id"],
            "position": doc["position"],
            "question": doc["question"],
            "expected_answer": doc["expected_answer"],
            "llm_response": response,
            "is_correct": is_correct,
            "confidence": confidence,
            "word_count": doc["word_count"]
        }
        results.append(result)
        
        # Update stats
        position_stats[doc['position']]['total'] += 1
        if is_correct:
            position_stats[doc['position']]['correct'] += 1
        
        # Print result
        status = "✓ CORRECT" if is_correct else "✗ INCORRECT"
        print(f"  {status}")
        print(f"  Response: {response[:100]}...")
    
    # Calculate accuracy by position
    accuracy_by_position = {}
    for position, stats in position_stats.items():
        if stats['total'] > 0:
            accuracy = stats['correct'] / stats['total']
            accuracy_by_position[position] = accuracy
        else:
            accuracy_by_position[position] = 0.0
    
    # Compile final results
    experiment_results = {
        "total_documents": len(documents),
        "results": results,
        "position_stats": position_stats,
        "accuracy_by_position": accuracy_by_position,
        "overall_accuracy": sum(r['is_correct'] for r in results) / len(results) if results else 0.0
    }
    
    # Save results
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(experiment_results, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print("\n" + "=" * 60)
    print("EXPERIMENT SUMMARY")
    print("=" * 60)
    print(f"Total Documents: {len(documents)}")
    print(f"Overall Accuracy: {experiment_results['overall_accuracy']:.1%}")
    print("\nAccuracy by Position:")
    for position in ["start", "middle", "end"]:
        accuracy = accuracy_by_position[position]
        count = position_stats[position]['total']
        print(f"  {position.upper():8} : {accuracy:.1%} ({position_stats[position]['correct']}/{count})")
    
    print(f"\nResults saved to: {output_file}")
    
    return experiment_results


if __name__ == "__main__":
    # Load documents
    documents = load_documents()
    
    # Run experiment
    results = run_experiment(documents)

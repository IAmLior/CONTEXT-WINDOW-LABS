"""
Lab 2: Context Window Size Impact - Experiment Runner

This module measures how LLM performance (latency and accuracy) changes 
as the prompt size (number of concatenated documents) increases.
"""

import json
import sys
import time
from pathlib import Path
from typing import List, Dict, Tuple
import tiktoken

# Add parent directory to path to import azure_openai_helper
sys.path.append(str(Path(__file__).parent.parent))
from azure_openai_helper import llm_query


def count_tokens(text: str, model: str = "gpt-4") -> int:
    """
    Count the number of tokens in a text string.
    
    Args:
        text: Input text to tokenize
        model: Model name for tokenizer (default: gpt-4)
        
    Returns:
        Number of tokens
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        # Fallback to cl100k_base for newer models
        encoding = tiktoken.get_encoding("cl100k_base")
    
    return len(encoding.encode(text))


def load_documents(num_docs: int, model_type: str = "gpt4o", dataset: str = "phi4mini") -> List[Dict[str, str]]:
    """
    Load pre-generated documents for a specific context size and model.
    
    Args:
        num_docs: Number of documents to load
        model_type: Model type identifier ("phi4mini" or "gpt4o")
        dataset: Dataset type ("phi4mini" for animals, "cities" for cities)
        
    Returns:
        List of document dictionaries
    """
    data_path = Path(__file__).parent / "data" / f"documents_{num_docs}_{dataset}.json"
    
    if not data_path.exists():
        raise FileNotFoundError(
            f"Documents not found: {data_path}\n"
            f"Run generate_documents.py or generate_cities.py first to create the data."
        )
    
    with open(data_path, 'r', encoding='utf-8') as f:
        documents = json.load(f)
    
    return documents


def concatenate_documents(documents: List[Dict[str, str]]) -> str:
    """
    Concatenate multiple documents into a single context string.
    
    Args:
        documents: List of document dictionaries
        
    Returns:
        Concatenated text of all documents
    """
    separator = "\n\n" + "=" * 80 + "\n\n"
    # Support both 'text' (animals) and 'content' (cities) fields
    doc_texts = [doc.get('text', doc.get('content', '')) for doc in documents]
    return separator.join(doc_texts)


def insert_test_fact(context: str, fact: str, position: str = "middle") -> str:
    """
    Insert a test fact into the context at a specific position.
    
    Args:
        context: Full concatenated context
        fact: Fact to insert
        position: Where to insert ('start', 'middle', or 'end')
        
    Returns:
        Modified context with inserted fact
    """
    test_sentence = f"\n\n[CRITICAL INFO] {fact}\n\n"
    
    if position == "start":
        return test_sentence + context
    elif position == "end":
        return context + test_sentence
    else:  # middle
        # Insert in the middle of the context
        mid_point = len(context) // 2
        return context[:mid_point] + test_sentence + context[mid_point:]


def create_query_prompt(context: str, question: str) -> str:
    """
    Create a complete prompt with context and question.
    
    Args:
        context: Full document context
        question: Question to ask
        
    Returns:
        Formatted prompt for the LLM
    """
    prompt = f"""Below is a collection of documents about various animals. Read through them carefully and answer the question that follows.

DOCUMENTS:
{context}

QUESTION: {question}

Please provide a concise answer based on the information in the documents above."""
    
    return prompt


def evaluate_response(response: str, expected_answer: str, use_llm: bool = True) -> bool:
    """
    Check if the LLM response contains the expected answer.
    Uses LLM-powered evaluation for semantic matching.
    
    Args:
        response: LLM response text
        expected_answer: Expected answer or key phrase
        use_llm: Whether to use LLM for evaluation (default: True)
        
    Returns:
        True if answer is correct, False otherwise
    """
    if not use_llm:
        # Fallback: simple string matching
        response_lower = response.lower()
        expected_lower = expected_answer.lower()
        return expected_lower in response_lower
    
    # LLM-powered evaluation
    evaluation_prompt = f"""You are an accuracy evaluator. Compare these two answers and determine if they convey the same factual information.

EXPECTED ANSWER: {expected_answer}

MODEL'S ANSWER: {response}

Question: Do these answers have more than 85% semantic similarity (i.e., do they convey essentially the same fact)?
- Consider paraphrasing, different wording, and elaboration as valid matches
- Ignore minor differences in phrasing or additional context
- Focus on whether the core factual claim is the same

Respond with ONLY "YES" or "NO"."""

    try:
        evaluation_response = llm_query(evaluation_prompt, model="gpt-4o")
        evaluation_result = evaluation_response.strip().upper()
        
        # Check if response contains YES
        return "YES" in evaluation_result
        
    except Exception as e:
        print(f"[WARNING] LLM evaluation failed: {e}. Falling back to string matching.")
        # Fallback to simple string matching
        response_lower = response.lower()
        expected_lower = expected_answer.lower()
        return expected_lower in response_lower


def run_single_experiment(
    num_docs: int,
    model: str = "gpt-4o",
    model_type: str = "gpt4o",
    dataset: str = "phi4mini"
) -> Dict:
    """
    Run a single experiment with a specific number of documents.
    
    Args:
        num_docs: Number of documents to use
        model: Model to use (default: gpt-4o)
        model_type: Model type for loading docs ("phi4mini" or "gpt4o")
        dataset: Dataset type ("phi4mini" for animals, "cities" for cities)
        
    Returns:
        Dictionary with experiment results
    """
    print(f"\n{'='*60}")
    print(f"Testing with {num_docs} documents (Model: {model}, Dataset: {dataset})")
    print(f"{'='*60}")
    
    # Load documents (model-specific sizes)
    documents = load_documents(num_docs, model_type, dataset)
    print(f"✓ Loaded {len(documents)} documents")
    
    # Concatenate all documents
    context = concatenate_documents(documents)
    print(f"✓ Concatenated documents")
    
    # Select a random document and use its fact as the test
    import random
    test_doc = random.choice(documents)
    
    # Support animals, cities, countries, and tech_companies datasets
    if 'animal' in test_doc:
        test_fact = test_doc['key_fact']
        test_subject = test_doc['animal']
        question = f"What special characteristic or ability does the {test_subject} have?"
    elif 'city' in test_doc:
        test_fact = test_doc['unique_fact']
        test_subject = test_doc['city']
        question = f"What is a unique or fascinating fact about {test_subject}?"
    elif 'country' in test_doc:
        test_fact = test_doc['unique_fact']
        test_subject = test_doc['country']
        question = f"What is a remarkable characteristic or fact about {test_subject}?"
    else:  # tech_companies dataset
        test_fact = test_doc['key_fact']
        test_subject = test_doc['company']
        question = f"What is a notable or unique fact about {test_subject}?"
    
    # Insert the test fact in the middle of context
    # (Actually, it's already in one of the documents, so we just use the context as-is)
    
    # Create full prompt
    full_prompt = create_query_prompt(context, question)
    
    # Count tokens
    token_count = count_tokens(full_prompt, model)
    print(f"✓ Token count: {token_count:,}")
    
    # Measure latency and query LLM with retry logic for rate limits
    print(f"🤖 Querying {model}...")
    start_time = time.time()
    
    max_retries = 3
    retry_delay = 5  # seconds
    
    for attempt in range(max_retries):
        try:
            # Set max_tokens to 100K to avoid any output length limitations
            response = llm_query(full_prompt, model=model, max_tokens=100000)
            latency = time.time() - start_time
            
            print(f"✓ Response received in {latency:.2f}s")
            
            # Clean up response if it contains formatting artifacts
            response = response.strip()
            if response.startswith("<|assistant|>"):
                response = response.replace("<|assistant|>", "").strip()
            
            # Check if response looks like garbage (contains too many special chars or parentheses)
            special_char_ratio = sum(1 for c in response[:200] if c in '()_.,;') / max(len(response[:200]), 1)
            if special_char_ratio > 0.3:  # More than 30% special characters
                print(f"⚠️  WARNING: Response appears to be corrupted/garbage")
                print(f"   Special char ratio: {special_char_ratio:.2%}")
                is_correct = False
            elif len(response) < 10:
                print(f"⚠️  WARNING: Response too short or empty: '{response}'")
                is_correct = False
            else:
                # Evaluate accuracy using LLM
                print(f"🔍 Evaluating response with LLM...")
                is_correct = evaluate_response(response, test_fact)
            
            print(f"\nTest Subject: {test_subject}")
            print(f"Key Fact: {test_fact}")
            print(f"Response: {response[:200]}...")
            print(f"Accuracy: {'✓ CORRECT' if is_correct else '✗ INCORRECT'}")
            
            return {
                "num_docs": num_docs,
                "total_tokens": token_count,
                "latency_sec": round(latency, 2),
                "accuracy": 1.0 if is_correct else 0.0,
                "test_subject": test_subject,
                "key_fact": test_fact,
                "response": response,
                "model": model,
                "dataset": dataset
            }
            
        except Exception as e:
            import traceback
            error_msg = str(e)
            last_error = e  # Store error for return
            
            # Print full traceback for debugging
            print(f"\n⚠️  Exception details:")
            print(f"   Type: {type(e).__name__}")
            print(f"   Message: {error_msg}")
            print(f"   Full traceback:")
            traceback.print_exc()
            
            # Check if it's a rate limit error
            if "429" in error_msg or "Too Many Requests" in error_msg:
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (attempt + 1)
                    print(f"⚠️  Rate limit hit. Waiting {wait_time}s before retry {attempt + 2}/{max_retries}...")
                    time.sleep(wait_time)
                    continue
                else:
                    print(f"✗ Rate limit error after {max_retries} attempts: {e}")
                    break
            else:
                print(f"✗ Error during query: {e}")
                break
    
    # If we get here, all retries failed
    return {
        "num_docs": num_docs,
        "total_tokens": token_count,
        "latency_sec": None,
        "accuracy": 0.0,
        "error": str(last_error) if 'last_error' in locals() else "Unknown error",
        "model": model
    }


def analyze_context_sizes(
    doc_counts: List[int] = [2, 5, 10, 20, 50],
    model: str = "gpt-4o",
    model_type: str = "gpt4o",
    dataset: str = "phi4mini"
) -> List[Dict]:
    """
    Run experiments across multiple context sizes.
    
    Args:
        doc_counts: List of document counts to test
        model: Model to use for all experiments
        model_type: Model type for loading docs ("phi4mini" or "gpt4o")
        dataset: Dataset type ("phi4mini" for animals, "cities" for cities)
        
    Returns:
        List of result dictionaries
    """
    print("=" * 60)
    print("LAB 2: CONTEXT WINDOW SIZE IMPACT ANALYSIS")
    print("=" * 60)
    print(f"Model: {model}")
    print(f"Model type: {model_type}")
    print(f"Dataset: {dataset}")
    print(f"Context sizes to test: {doc_counts}")
    print("=" * 60)
    
    results = []
    
    for i, num_docs in enumerate(doc_counts):
        result = run_single_experiment(num_docs, model, model_type, dataset)
        results.append(result)
        
        # Save incrementally after each test
        if i < len(doc_counts) - 1:  # Don't wait after the last test
            # Longer delay between experiments to avoid rate limits
            # Especially important for Azure OpenAI rate limiting
            print(f"\n⏱️  Waiting 10 seconds before next test to avoid rate limits...\n")
            time.sleep(10)
    
    return results


def save_results(results: List[Dict], filename: str = "experiment_results.json"):
    """
    Save experiment results to JSON file.
    
    Args:
        results: List of result dictionaries
        filename: Output filename
    """
    output_dir = Path(__file__).parent / "results"
    output_dir.mkdir(exist_ok=True)
    
    output_path = output_dir / filename
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Results saved to {output_path}")


def print_summary(results: List[Dict]):
    """
    Print a summary table of results.
    
    Args:
        results: List of result dictionaries
    """
    print("\n" + "=" * 80)
    print("EXPERIMENT SUMMARY")
    print("=" * 80)
    print(f"{'Docs':<8} {'Tokens':<12} {'Latency (s)':<15} {'Accuracy':<10} {'Status'}")
    print("-" * 80)
    
    for r in results:
        tokens = f"{r['total_tokens']:,}" if r['total_tokens'] else "N/A"
        latency = f"{r['latency_sec']:.2f}" if r['latency_sec'] else "N/A"
        accuracy = f"{r['accuracy']*100:.0f}%"
        status = "✓" if r['accuracy'] == 1.0 else "✗"
        
        print(f"{r['num_docs']:<8} {tokens:<12} {latency:<15} {accuracy:<10} {status}")
    
    print("=" * 80)
    
    # Calculate averages
    valid_results = [r for r in results if r['latency_sec'] is not None]
    if valid_results:
        avg_latency = sum(r['latency_sec'] for r in valid_results) / len(valid_results)
        avg_accuracy = sum(r['accuracy'] for r in results) / len(results)
        
        print(f"\nAverage Latency: {avg_latency:.2f}s")
        print(f"Overall Accuracy: {avg_accuracy*100:.1f}%")


if __name__ == "__main__":
    """Run the Phi-4-mini experiment with animals, cities, or countries dataset."""
    
    # Check for command-line argument to specify dataset
    import sys
    if len(sys.argv) > 1:
        dataset = sys.argv[1]
    else:
        dataset = "phi4mini"  # Default to animals
    
    # Test with standard context sizes: 2, 5, 10, 20, 50 documents
    context_sizes = [2, 5, 10, 20, 50]
    
    if dataset == "tech_companies":
        print("\n🏢 LAB 2: PHI-4-MINI CONTEXT WINDOW ANALYSIS - TECH COMPANIES DATASET (TRIAL 4)")
        print("=" * 80)
        print("ULTIMATE TEST: 400 words/doc - Beyond the instability threshold!")
        print("\n  PREVIOUS TESTS:")
        print("    Animals (90w/doc):    6,636 tokens  → ✅ 100% accurate")
        print("    Cities (180w/doc):    14,328 tokens → ✅ 100% accurate")
        print("    Countries (300w/doc): 21,915 tokens → ⚠️  60-80% accurate (UNSTABLE)")
        print("\n  THIS TEST - Tech Companies (400 words/doc - 4.4x animals):")
        print("    2 docs = 800 words     (~1,040 tokens)")
        print("    5 docs = 2,000 words   (~2,600 tokens)")
        print("    10 docs = 4,000 words  (~5,200 tokens)")
        print("    20 docs = 8,000 words  (~10,400 tokens)")
        print("    50 docs = 20,000 words (~26,000 tokens) ❌ EXTREME!")
        print("\n❓ HYPOTHESIS: Will 400w/doc cause COMPLETE failure or just more instability?")
    elif dataset == "countries":
        print("\n🌍 LAB 2: PHI-4-MINI CONTEXT WINDOW ANALYSIS - COUNTRIES DATASET (TRIAL 3)")
        print("=" * 80)
        print("EXTREME TEST: Will 300 words/doc finally break Phi-4-mini?")
        print("\n  PREVIOUS TESTS:")
        print("    Animals (90w/doc):  6,636 tokens  → ✅ 100% accurate")
        print("    Cities (180w/doc):  14,328 tokens → ✅ 100% accurate")
        print("\n  THIS TEST - Countries (300 words/doc - 3.3x animals):")
        print("    2 docs = 600 words     (~780 tokens)")
        print("    5 docs = 1,500 words   (~1,950 tokens)")
        print("    10 docs = 3,000 words  (~3,900 tokens)")
        print("    20 docs = 6,000 words  (~7,800 tokens)")
        print("    50 docs = 15,000 words (~19,500 tokens) ❌ EXTREME!")
        print("\n❓ HYPOTHESIS: Will ~25K tokens reveal Phi-4-mini's TRUE limit?")
    elif dataset == "cities":
        print("\n🏙️  LAB 2: PHI-4-MINI CONTEXT WINDOW ANALYSIS - CITIES DATASET")
        print("=" * 80)
        print("Testing if LARGER documents (180 words) stress Phi-4-mini more:")
        print("\n  PREVIOUS TEST - Animals (90 words/doc):")
        print("    50 docs = 4,700 words (~6,636 tokens): ✅ 100% accurate")
        print("\n  THIS TEST - Cities (180 words/doc - 2x larger):")
        print("    2 docs = 360 words    (~468 tokens)")
        print("    5 docs = 900 words    (~1,170 tokens)")
        print("    10 docs = 1,800 words (~2,340 tokens)")
        print("    20 docs = 3,600 words (~4,680 tokens)")
        print("    50 docs = 9,000 words (~11,700 tokens) ❓ UNCHARTED TERRITORY!")
        print("\n❓ HYPOTHESIS: Will 2x larger docs push Phi-4-mini past its limits?")
    else:
        print("\n🎯 LAB 2: PHI-4-MINI CONTEXT WINDOW ANALYSIS - ANIMALS DATASET")
        print("=" * 80)
        print("Based on Lab 1 findings:")
        print("  - Phi-4-mini: Perfect up to 3,500 words, unstable at 4,000, fails at 5,000+")
        print("  - Task type: Complex position-based retrieval")
        print("\nLab 2 tests SIMPLE fact retrieval with:")
        print("\n  PHI-4-MINI (90 words/doc):")
        print("    2 docs = 180 words    (~310 tokens)")
        print("    5 docs = 450 words    (~679 tokens)")
        print("    10 docs = 900 words   (~1,383 tokens)")
        print("    20 docs = 1,800 words (~2,691 tokens)")
        print("    50 docs = 4,500 words (~6,659 tokens) ⚠️ Beyond Lab 1 limit!")
    
    print("=" * 80)
    
    # Test Phi-4-mini
    if dataset == "tech_companies":
        emoji = "🏢 "
    elif dataset == "countries":
        emoji = "🌍 "
    elif dataset == "cities":
        emoji = "🏙️  "
    else:
        emoji = "🤖 "
    
    print("\n\n" + emoji * 20)
    print(f"TESTING PHI-4-MINI-INSTRUCT - {dataset.upper()} DATASET")
    print(emoji * 20)
    phi_results = analyze_context_sizes(
        context_sizes, 
        model="Phi-4-mini-instruct", 
        model_type="phi4mini",
        dataset=dataset
    )
    
    result_filename = f"phi4_mini_{dataset}_results.json"
    save_results(phi_results, filename=result_filename)
    print_summary(phi_results)
    
    print("\n" + "=" * 80)
    print("✓ Lab 2 experiment complete!")
    print("=" * 80)
    print(f"\nResults saved to: results/{result_filename}")
    print("Next step: Run analyze_phi_results.py to generate visualizations")
    print("\nResults saved to: results/phi4_mini_results.json")
    print("Next step: Run analyze_phi_results.py to generate visualizations")

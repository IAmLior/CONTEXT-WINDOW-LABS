"""
Lab 1: Needle in a Haystack - Testing the "Lost in the Middle" Phenomenon

Tests whether modern Large Language Models suffer from the "lost in the middle" effect,
where critical information buried in the middle of long documents is less accurately
retrieved than facts at the beginning or end.

Key Finding: Modern LLMs (GPT-4o, Phi-4-mini) do NOT exhibit "lost in the middle" 
effects for simple factual retrieval tasks at practical document lengths.

Available Trials:
- trial1 (default): 200 words, no distractors, GPT-4o baseline
- trial2: 1000 words, 3 distractors, GPT-4o complex test
- trial3: 3000 words, 8-12 distractors, GPT-4o extreme test
- trial4: 3000 words, 8-12 distractors, Phi-4-mini model comparison
- trial5: 3500 words, 10-15 distractors, Phi-4-mini at limit

Usage:
    >>> from context_window_labs.lab1 import run_lab
    >>> run_lab()  # Run trial1 (default)
    >>> run_lab(trial="trial2")  # Run specific trial
    >>> run_lab(trial="trial5")  # Run trial5_final
"""

import sys
from pathlib import Path


def run_lab(trial="trial1"):
    """
    Run the complete Lab 1 pipeline for a specific trial.
    
    Args:
        trial: Which trial to run. Options:
            - "trial1" (default): 200w docs, no distractors, GPT-4o
            - "trial2": 1000w docs, 3 distractors, GPT-4o
            - "trial3": 3000w docs, 8-12 distractors, GPT-4o
            - "trial4": 3000w docs, 8-12 distractors, Phi-4-mini
            - "trial5": 3500w docs, 10-15 distractors, Phi-4-mini
    
    Each trial runs:
    1. Generate synthetic documents with embedded facts
    2. Query LLM about facts at different positions
    3. Analyze results and visualize findings
    
    Returns:
        dict: Experiment results
    """
    # Add parent directory to path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    
    # Map trial names to configurations
    trial_configs = {
        "trial1": {
            "words_per_doc": 200,
            "add_distractors": False,
            "dataset_name": "documents",
            "results_name": "experiment_results",
            "model": None,  # Default (GPT-4o)
            "description": "Baseline: 200 words, no distractors, GPT-4o"
        },
        "trial2": {
            "words_per_doc": 1000,
            "add_distractors": True,
            "dataset_name": "documents_complex",
            "results_name": "experiment_results_complex",
            "model": None,  # Default (GPT-4o)
            "description": "Complex: 1000 words, 3 distractors, GPT-4o"
        },
        "trial3": {
            "words_per_doc": 3000,
            "add_distractors": True,
            "dataset_name": "documents_extreme",
            "results_name": "experiment_results_extreme",
            "model": None,  # Default (GPT-4o)
            "description": "Extreme: 3000 words, 8-12 distractors, GPT-4o"
        },
        "trial4": {
            "words_per_doc": 3000,
            "add_distractors": True,
            "dataset_name": "documents_phi4",
            "results_name": "experiment_results_phi4",
            "model": "Phi-4-mini-instruct",  # Secondary model
            "description": "Model comparison: 3000 words, 8-12 distractors, Phi-4-mini"
        },
        "trial5": {
            "words_per_doc": 3500,
            "add_distractors": True,
            "dataset_name": "documents_trial5_3500w",
            "results_name": "experiment_results_trial5_final",
            "model": "Phi-4-mini-instruct",  # Secondary model
            "description": "Final test: 3500 words, 10-15 distractors, Phi-4-mini"
        }
    }
    
    # Validate trial name
    if trial not in trial_configs:
        valid_trials = ", ".join(trial_configs.keys())
        raise ValueError(f"Invalid trial '{trial}'. Valid options: {valid_trials}")
    
    config = trial_configs[trial]
    
    # Import required modules
    from .generate_data import generate_dataset
    from .experiment import run_experiment
    from .analyze_results import analyze_and_visualize
    
    print("=" * 80)
    print(f"LAB 1 - {trial.upper()}: NEEDLE IN A HAYSTACK")
    print("=" * 80)
    print(f"\nConfiguration: {config['description']}")
    print("\nPipeline:")
    print("  1. Generate synthetic documents with embedded facts")
    print("  2. Query LLM about facts at different positions")
    print("  3. Analyze results and visualize 'lost in the middle' effect")
    print("=" * 80)
    
    try:
        # Step 1: Generate data
        print("\n" + "=" * 80)
        print("STEP 1: GENERATING SYNTHETIC DOCUMENTS")
        print("=" * 80)
        print(f"Documents: 15 docs × {config['words_per_doc']} words")
        print(f"Distractors: {'Yes' if config['add_distractors'] else 'No'}")
        print(f"Model: {config['model'] or 'GPT-4o (default)'}")
        
        documents = generate_dataset(
            num_docs=15,
            words_per_doc=config['words_per_doc'],
            output_dir="lab1/data",
            add_distractors=config['add_distractors'],
            dataset_name=config['dataset_name']
        )
        
        # Step 2: Run experiment
        print("\n" + "=" * 80)
        print("STEP 2: RUNNING EXPERIMENT")
        print("=" * 80)
        print("\n⚠️  This will make 15 API calls to Azure OpenAI...")
        print("Estimated time: 2-5 minutes depending on API latency\n")
        
        results = run_experiment(
            documents,
            output_file=f"lab1/results/{config['results_name']}.json",
            model=config['model']
        )
        
        # Step 3: Analyze and visualize
        print("\n" + "=" * 80)
        print("STEP 3: ANALYZING RESULTS")
        print("=" * 80)
        analyze_and_visualize(results_file=f"lab1/results/{config['results_name']}.json")
        
        # Final summary
        print("\n" + "=" * 80)
        print(f"LAB 1 - {trial.upper()} COMPLETE! ✓")
        print("=" * 80)
        print("\nGenerated files:")
        print(f"  - lab1/data/{config['dataset_name']}.json")
        print(f"  - lab1/results/{config['results_name']}.json")
        print(f"  - lab1/results/accuracy_by_position.png")
        print(f"  - lab1/results/detailed_analysis.png")
        print(f"  - lab1/results/analysis_report.txt")
        print("\nNext steps:")
        print("  1. Review the plots to visualize the 'lost in the middle' effect")
        print("  2. Read analysis_report.txt for detailed findings")
        print("  3. Check experiment_results.json for raw data")
        
        return results
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Experiment interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error running experiment: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


__all__ = ["run_lab"]

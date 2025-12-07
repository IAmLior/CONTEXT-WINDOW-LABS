"""
Main experiment: Benchmark all three strategies over multi-step scenario.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import time
from datetime import datetime
import pandas as pd
from strategies import create_strategy
from azure_openai_helper import llm_query


class StrategyBenchmark:
    """
    Benchmark context management strategies over a multi-step scenario.
    """
    
    def __init__(self, scenario, model_name="gpt-4o-mini"):
        self.scenario = scenario
        self.model_name = model_name
        self.results = []
        
        # Initialize strategies
        self.strategies = {
            "select": create_strategy("select", model_name=model_name, top_k=3),
            "compress": create_strategy("compress", model_name=model_name, max_tokens=2000),
            "write": create_strategy("write", model_name=model_name)
        }
    
    def evaluate_answer(self, answer, ground_truth, question):
        """
        Use LLM to evaluate if answer is correct compared to ground truth.
        
        Returns:
            dict with is_correct (bool) and explanation
        """
        eval_prompt = f"""You are evaluating whether an answer to a question is correct.

Question: {question}

Ground Truth Answer: {ground_truth}

Given Answer: {answer}

Is the given answer essentially correct compared to the ground truth? The answer doesn't need to be word-for-word identical, but should convey the same key information.

Respond in this format:
CORRECT: [YES or NO]
EXPLANATION: [brief explanation]"""

        eval_text = llm_query(
            prompt=eval_prompt,
            temperature=0,
            max_tokens=200
        )
        
        # Parse response
        is_correct = "YES" in eval_text.split('\n')[0].upper()
        
        lines = eval_text.split('\n')
        explanation = ""
        for line in lines:
            if line.startswith("EXPLANATION:"):
                explanation = line.replace("EXPLANATION:", "").strip()
                break
        
        return {
            "is_correct": is_correct,
            "explanation": explanation,
            "eval_response": eval_text
        }
    
    def run_experiment(self, output_dir="lab4/results"):
        """
        Run the full experiment: evaluate all strategies at each step.
        """
        os.makedirs(output_dir, exist_ok=True)
        
        print("="*80)
        print("LAB 4: Context Engineering Strategies Benchmark")
        print("="*80)
        print(f"\nScenario: {self.scenario['description']}")
        print(f"Model: {self.model_name}")
        print(f"Total Steps: {self.scenario['num_steps']}")
        print(f"Strategies: {list(self.strategies.keys())}")
        print()
        
        # Simulate the multi-step process
        for step_idx in range(self.scenario['num_steps']):
            step_num = step_idx + 1
            current_history = self.scenario['steps'][:step_num]
            question = self.scenario['questions'][step_idx]
            ground_truth = self.scenario['ground_truth'][step_idx]
            
            print(f"\n{'='*80}")
            print(f"STEP {step_num}/{self.scenario['num_steps']}")
            print(f"{'='*80}")
            print(f"Action: {self.scenario['steps'][step_idx]['action']}")
            print(f"Question: {question}")
            print(f"Ground Truth: {ground_truth}")
            print()
            
            step_results = {
                "step": step_num,
                "question": question,
                "ground_truth": ground_truth,
                "history_length": len(current_history),
                "strategies": {}
            }
            
            # Evaluate each strategy
            for strategy_name, strategy in self.strategies.items():
                print(f"\n  [{strategy_name.upper()}]")
                
                try:
                    start_time = time.time()
                    
                    # Get answer from strategy
                    result = strategy.answer_question(current_history, question)
                    answer = result['answer']
                    context_tokens = result['context_tokens']
                    
                    # Evaluate correctness
                    evaluation = self.evaluate_answer(answer, ground_truth, question)
                    
                    elapsed = time.time() - start_time
                    
                    # Store results
                    step_results['strategies'][strategy_name] = {
                        "answer": answer,
                        "is_correct": evaluation['is_correct'],
                        "explanation": evaluation['explanation'],
                        "context_tokens": context_tokens,
                        "time_seconds": round(elapsed, 2)
                    }
                    
                    # Print results
                    status = "✓ CORRECT" if evaluation['is_correct'] else "✗ INCORRECT"
                    print(f"    Answer: {answer}")
                    print(f"    Status: {status}")
                    print(f"    Context Tokens: {context_tokens}")
                    print(f"    Time: {elapsed:.2f}s")
                    
                except Exception as e:
                    print(f"    ERROR: {str(e)}")
                    step_results['strategies'][strategy_name] = {
                        "answer": None,
                        "is_correct": False,
                        "explanation": f"Error: {str(e)}",
                        "context_tokens": 0,
                        "time_seconds": 0,
                        "error": str(e)
                    }
            
            self.results.append(step_results)
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = os.path.join(output_dir, f"experiment_results_{timestamp}.json")
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump({
                "scenario": self.scenario['scenario_type'],
                "model": self.model_name,
                "num_steps": self.scenario['num_steps'],
                "timestamp": timestamp,
                "results": self.results
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'='*80}")
        print(f"✓ Results saved to {results_file}")
        
        return self.results, results_file
    
    def create_summary_dataframe(self):
        """
        Create a DataFrame summarizing strategy performance over time.
        """
        rows = []
        
        for step_result in self.results:
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
                        'question': step_result['question']
                    })
        
        df = pd.DataFrame(rows)
        return df


def load_scenario(scenario_path="lab4/data/scenario_detective_investigation_10steps.json"):
    """Load scenario from JSON file."""
    with open(scenario_path, 'r', encoding='utf-8') as f:
        return json.load(f)


if __name__ == "__main__":
    # Load scenario
    print("Loading scenario...")
    scenario = load_scenario()
    
    # Run experiment
    benchmark = StrategyBenchmark(scenario, model_name="gpt-4o-mini")
    results, results_file = benchmark.run_experiment()
    
    # Create summary
    df = benchmark.create_summary_dataframe()
    
    print("\n" + "="*80)
    print("SUMMARY STATISTICS")
    print("="*80)
    
    # Overall accuracy by strategy
    print("\nOverall Accuracy by Strategy:")
    accuracy_by_strategy = df.groupby('strategy')['accuracy'].agg(['mean', 'sum', 'count'])
    print(accuracy_by_strategy)
    
    # Average context tokens by strategy
    print("\nAverage Context Tokens by Strategy:")
    tokens_by_strategy = df.groupby('strategy')['context_tokens'].mean()
    print(tokens_by_strategy)
    
    # Average time by strategy
    print("\nAverage Time (seconds) by Strategy:")
    time_by_strategy = df.groupby('strategy')['time_seconds'].mean()
    print(time_by_strategy)
    
    print("\n" + "="*80)
    print("Experiment complete! Run analyze_results.py to generate visualizations.")
    print("="*80)

# Lab 4 - Prompt Log

## Overview
This document tracks all prompts used in Lab 4: Context Engineering Strategies experiment.

---

## Prompt 1
```
Lets continue to Lab 4 - Context Engineering Strategies (Select / Compress / Write) 

Idea:
You simulate an agent doing a sequence of actions (10 steps). After each step, history grows, and you apply three different strategies to manage context:

SELECT – use retrieval (RAG) to pull only relevant parts of the history.

COMPRESS – summarize the history once it gets too long.

WRITE – extract key facts into a separate “scratchpad” / memory and query from there.

Then you benchmark the strategies over the sequence.

Lab pseudocode:

# Strategy 1: SELECT – RAG over history
def select_strategy(history, query):
    relevant = rag_search(history, query, k=5)
    return query_llm(relevant, query)

# Strategy 2: COMPRESS – summarize history when too long
def compress_strategy(history, query):
    if token_len(history) > MAX_TOKENS:
        history = summarize(history)
    return query_llm(history, query)

# Strategy 3: WRITE – maintain external scratchpad
def write_strategy(history, query, scratchpad):
    key_facts = extract_key_facts(history)
    scratchpad.store(key_facts)
    context_for_llm = scratchpad.retrieve(query)
    return query_llm(context_for_llm, query)

# Compare strategies over several actions
def benchmark_strategies(num_actions=10):
    results = {"select": [], "compress": [], "write": []}
    history = []
    for step in range(num_actions):
        output = agent.execute(step)      # simulate one action
        history.append(output)

        # evaluate each strategy on current history
        for name in results.keys():
            score = evaluate_strategy(name, history)
            results[name].append(score)
    return results

You then create plots/tables comparing strategy vs score over time and discuss trade-offs:

SELECT: accurate, but needs retrieval infra.

COMPRESS: cheap, but may lose details.

WRITE: good for accumulating structured facts.

Deeper explenation:

## Goal of this lab
We want to evaluate how different **context-management strategies** affect an LLM’s ability to answer questions during a multi-step task where the “history” grows over time.

LLMs have limited attention and become less reliable as the context becomes longer and noisier.  
To handle this, we compare three widely used strategies:

1. **SELECT** – retrieve only the most relevant pieces of the history (RAG-style retrieval).
2. **COMPRESS** – when history becomes too long, replace it with a summary.
3. **WRITE** – extract structured key facts after each step and store them in an external “scratchpad” memory.

The goal is to observe:
- how each strategy maintains answer quality as the task progresses,
- how each strategy deals with long histories,
- what trade-offs (accuracy, stability, degradation patterns) emerge over the sequence.

## What we need to do

### 1. Simulate a multi-step process
Create a simple loop of ~10 steps that produces short text outputs (e.g., agent actions, state updates, or fact statements).  
After each step, append the new output to a growing **history** list.

This history is the input all strategies must work with.

### 2. Implement the three strategies

### (A) SELECT Strategy (RAG-style)
- Split history items into chunks.
- Embed all chunks once.
- For each query:
  - Run vector similarity search to retrieve top-k relevant chunks.
  - Build a prompt using *only* these retrieved chunks.
  - Ask the LLM and record the answer.

### (B) COMPRESS Strategy
- Maintain a running text history.
- When history exceeds a token threshold:
  - Generate a summary of the entire history using the LLM.
  - Replace the full history with the summary.
- Ask the LLM using this compressed representation.

### (C) WRITE Strategy (External Memory)
- After each step:
  - Use the LLM to extract **key facts** from the newly generated content.
  - Store these facts in an external "scratchpad" structure.
- For each query:
  - Retrieve relevant facts from the scratchpad (e.g., via simple filtering or embedding retrieval).
  - Provide these structured facts as the context for the question.

### 3. Benchmark all strategies over time
For each step in the sequence:

1. Update the history.
2. Run each strategy to answer a fixed evaluation query.
3. Compare correctness against a known expected answer.
4. Log:
   - accuracy (True/False)
   - which strategy succeeded or failed at each step.

### 4. Output and visualization
Produce:
- A DataFrame showing accuracy per strategy per step.
- A line plot with:
  - x-axis = step number
  - y-axis = accuracy (0 or 1)
  - separate line for SELECT, COMPRESS, WRITE
- Another some plots to explain the results and interesting insights

### Expected behaviors:
- SELECT should maintain high accuracy as long as retrieval is good.
- COMPRESS may lose details over time, especially after repeated summaries.
- WRITE should preserve key information well if fact extraction is reliable.

## Expected final deliverables
Copilot should generate:
- Clean, modular Python code with:
  - history simulation
  - three strategy implementations
  - evaluation loop
  - result aggregation
  - a plot comparing strategy performance
- Reusable functions for future labs.

Follow the description above and generate well-structured code.
**Note you have to create Readme.md file that will follow our experiment progress and log every result and insight**
```

## Prompt 2
```
run it in an existing terminal as venv is already enabled there
```

---
## Prompt 3
```
wait, it seems like you have errors calling the llm, look on the returned response:
  [WRITE]
    ERROR: Error code: 404 - {'error': {'code': 'DeploymentNotFound', 'message': 'The API deployment for this resource does not exist. If you created the deployment within the last 5 minutes, please wait a moment and try again.'}}
```

---

## Prompt 4
```
we are using the llm helper for this case?
```

---

## Prompt 5
```
Experiment complete! Run analyze_results.py to generate visualizations.
```

---

## Prompt 6
```
extand our readme with all those great results and insights!
add this  LAB 4 - COMPREHENSIVE REPORT (terminal output) to the end of the readme file
```

---


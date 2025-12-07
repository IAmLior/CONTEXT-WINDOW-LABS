# Lab 3 - Prompt Log

## Overview
This document tracks all prompts used in Lab 3: RAG vs Full Context experiment.

---

## Prompt 1
```
Lets continue to Lab3 – RAG vs Full Context 
Idea:
Same documents, same questions, two modes:
1. Full context: concatenate all docs and ask the model.
2. RAG: chunk docs, embed, store in Chroma, retrieve only the top-k relevant chunks and ask with those.

You compare accuracy + latency.

Lab pseudocode:

# Step 1: split docs into chunks
chunks = split_documents(documents, chunk_size=500)

# Step 2: embed the chunks
embeddings = nomic_embed_text(chunks)

# Step 3: store in Chroma
vector_store = ChromaDB()
vector_store.add(chunks, embeddings)

# Step 4: compare full-context vs RAG
def compare_modes(query):
    # Mode A: full context (all docs together)
    full_response = query_with_full_context(all_documents, query)

    # Mode B: RAG (only retrieved chunks)
    relevant_chunks = vector_store.similarity_search(query, k=3)
    rag_response = query_with_context(relevant_chunks, query)

    return {
        "full_accuracy": evaluate(full_response),
        "rag_accuracy": evaluate(rag_response),
        "full_latency": full_response.latency,
        "rag_latency": rag_response.latency,
    }


You typically show a small table:

Mode	Accuracy	Latency
Full	…	…
RAG	…	…

and explain that RAG is usually both faster and cleaner for larger corpora.

Detailed explenation:
## Goal of this lab
We want to compare two different ways of giving information to an LLM:

1. **Full Context** – concatenate *all* documents into one long prompt and ask the question directly.
2. **RAG (Retrieval-Augmented Generation)** – break documents into chunks, embed them, store in a vector store, retrieve only the most relevant chunks for a query, and ask the LLM using only those retrieved chunks.

The main goal is to measure how these two modes differ in terms of:
- **Answer quality / accuracy**
- **Latency / response time**
- Practical behavior when the number of documents grows.

We expect:
- Full Context → noisy, slow, may miss the answer when context is huge.
- RAG → more focused, faster, and usually more accurate for the same corpus. :contentReference[oaicite:0]{index=0}

## What we need to do

1. **Prepare data**
   - Use a small corpus of around ~20 short documents on mixed topics (e.g., health, law, technology). :contentReference[oaicite:1]{index=1}  
   - Each document contains factual information that can be asked about with a question.

2. **Full Context mode**
   - Concatenate all documents into a single long string (`all_documents`).
   - For a given query, build a prompt using the entire concatenated context.
   - Send this to the LLM and capture:
     - The answer text.
     - Latency (time from request to response).
     - A simple correctness flag (whether the answer contains the expected fact).

3. **RAG mode**
   - **Chunking:** split the documents into reasonably sized chunks (e.g. `chunk_size = 500` tokens/words). :contentReference[oaicite:2]{index=2}  
   - **Embedding:** compute embeddings for each chunk (e.g. using an embedding model like `nomic-embed-text`).  
   - **Vector store:** store chunks + embeddings in a vector database (e.g. ChromaDB).  
   - **Retrieval:** for each query, run a similarity search (e.g. `similarity_search(query, k=3)`) to get top-k relevant chunks. :contentReference[oaicite:3]{index=3}  
   - Build a prompt with only these retrieved chunks as the context and ask the LLM.
   - Capture answer text, latency, and correctness.

4. **Comparison function**
   - Implement a function (e.g. `compare_modes(query)`) that:
     - Runs the query once in **Full Context** mode.
     - Runs the same query in **RAG** mode.
     - Returns a structured result with:
       - `full_accuracy`, `rag_accuracy`
       - `full_latency`, `rag_latency`   

5. **Evaluation**
   - Define a small set of evaluation questions whose answers appear in the corpus.
   - For each question, call `compare_modes`.
   - Aggregate results into a table (DataFrame) with columns like:
     - `query`, `full_accuracy`, `rag_accuracy`, `full_latency`, `rag_latency`.
   - Optionally produce simple plots (e.g. bar charts) comparing:
     - Full vs RAG accuracy
     - Full vs RAG latency

## Expected outcome
- A clear empirical comparison showing that **RAG** provides:
  - Focused, high-quality answers.
  - Lower latency than pushing all documents as a single full-context prompt.
- A reusable code structure that we can extend later (e.g. for chunking variations, reranking, etc.).

Please generate clean, modular Python code following this plan, with helpful docstrings and clear function boundaries.
**Note you have to create Readme.md file that will follow our experiment progress and log every result and insight**
```

## Prompt 2
```
go on and run our experiment, summarize and log the process, results and interesting insights.
```

---
## Prompt 3
```
I see within /lab3 great content in various .md files.
Except of PROMPT_LOG.md please unite the content of all readme files to one well structered readme that will contain all the knowledge process insights and concludtions and anything alse about our experiment
```

---

# Lab 2 - Prompt Log

This file contains all user prompts related to Lab 2 experiments, in chronological order.

---

## Session Date: December 6-7, 2025

### Initial Setup

#### Prompt 1
```
Great! lets continue to lab 2!

2️⃣ Experiment 2 – Context Window Size Impact 
Idea:
You gradually increase the number of documents (and thus the total tokens in the prompt), send everything as one huge context, and measure latency and accuracy. This shows the cost of large context windows.

# Measure performance across different context sizes
def analyze_context_sizes(doc_counts=[2, 5, 10, 20, 50]):
    results = []
    for num_docs in doc_counts:
        docs = load_documents(num_docs)              # load N docs
        context = concatenate_documents(docs)        # single long prompt

        start_time = time.time()
        response = langchain_query(context, query)   # call LLM via LangChain
        latency = time.time() - start_time

        results.append({
            "num_docs": num_docs,
            "tokens_used": count_tokens(context),
            "latency": latency,
            "accuracy": evaluate_accuracy(response),
        })
    return results


From results you plot, for example:
tokens_used vs latency
tokens_used vs accuracy
to show: more context → slower, and eventually less accurate.

Deeper explenation:
Goal of this lab
We want to measure how an LLM’s **accuracy** and **latency** change as the **prompt size increases**.  
This experiment shows the practical limits of large context windows and helps us understand how long inputs affect model behavior.

## What we need to do
1. Generate synthetic documents of increasing total length (e.g., simulate context sizes for 2, 5, 10, 20, 50 documents). You can take a subject - for example animals, and generate a document per animal telling about the animal.
2. Insert a simple fact into the full context so we can test whether the model still finds it.
3. Query the LLM with the entire concatenated context (no retrieval; pure full-context mode).
4. Measure:
   - total tokens in the prompt  
   - model **latency**  
   - whether the model returned the **correct answer**  
5. Aggregate results and plot:
   - **tokens vs latency**
   - **tokens vs accuracy**

Execution plan (based on lab description)
- Create a function that loads or generates `N` filler documents.
- Concatenate them into a single long prompt.
- Insert a known fact and ask a direct question about it.
- Call the LLM using our Azure helper (`llm.query`).
- Record:
  - token count  
  - response time  
  - correctness  
- Repeat this over multiple context sizes.
- Produce a results DataFrame and simple Matplotlib plots.

Expected output
- A reusable function `analyze_context_sizes()` that returns a table with:
  - num_docs  
  - tokens_used  
  - latency_sec  
  - accuracy  

- Two plots:
  - Latency vs context size  
  - Accuracy vs context size  

Follow these requirements and generate clean, modular Python code with docstrings and clear structure.


Implement everything in /lab2 dir. note that every llm usage should be using our helper. 
this time we will have to use our primry model?
```

---

#### Prompt 2
```
before running the experiment, as we understand from lab1, this is not sufficient enough for a big model such like gpt4o, 
suggest:
1. use phi for this experiment as well
2. much expand the docs for much bigger context (I think it still wont be enough, am I wrong?)
```

---

#### Prompt 3
```
we saw the context window of the phi was around 4000 words am I wrong? does this makes sense?

but the lab states 2,5,10,20,50
pls rearrange the number of word of the 2 models
```

---

#### Prompt 4
```
before running the experiment, please update the readme with our preprocess thinking and why we decide to preform the experiment this way.

next run the experiment, do not forget to save run logs and outputs and shw the logs as part of the readme (as thay are very intuitive)
```

---

### Trial 1 - Animals Dataset

#### Prompt 5
```
I have manually stop the last run of the experiment as I want us to validate the answers a bit differently, llm can sometimes answer correctly but in a different words, so our evaluation should be also powered by llm.
So - 
1. implement evaluation by llm (you can ask a model itself if the answer you wanted to see and model's answer have more than 85% in common)
2. remove last's run results (as it was manually stopped)
3. re run the experiment
```

---

#### Prompt 6
```
again - Iv'e stopped it manually cause i saw errors
look at the outputs, some of them contains api errors, lets:
1. understand what might happen and fix if there is a need.
2. remove last run results and rerun
```

---

#### Prompt 7
```
summarize our key findings and phi model process into the readme file.
before finishing the lab, lets try to create new dataset, instead of animals, about cities. each doc will be sized with *2 words than the animal doc word count, again we will create items of 2,5,10,20,50 and rerun the experiment. we will see if bigger items will create bigger context and will make the model furstrate in answering correctly
```

---

### Trial 2 - Cities & Countries & Tech companies Datasets

#### Prompt 8
```
lets rerun the countries test, for validating errors are not transient, the last results file will be the objective
```

---

#### Prompt 9
```
ok, add those interesting insights from the 3 times countries run to our readme file. and an explenations and the running logs.
please unite the readme and the summary into one readme file.
I see too much md files within lab2 dir, please add the needed parts to readme.md (it should contain all)
experiments process, goals, process per trial results per trial and insigths
```


---

#### Prompt 10
```
lets now create one last trial, we will generate tech companies data, and will contains 400w per doc, same 2,5,10,20,50 run, lets see what happns
```
---

#### Prompt 11
```
1. lets run it again to see nothing was transient
2. dont create specific readme for results, add it to the general readme (remove the tech companies results you have already generated)
```


---

#### Prompt 12
```
I see we still have 2 .md files within /lab2.
unite them into readme.md in a well structured format what will contain all the sata regarding our lab in one file
```
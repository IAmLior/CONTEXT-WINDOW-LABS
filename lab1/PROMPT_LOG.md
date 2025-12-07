# Lab 1 - Prompt Log

This file contains all user prompts related to Lab 1 experiments, in chronological order.

---

## Session Date: December 6, 2025

### Prompt 1
```
Experiment 1 – Needle in a Haystack / Lost in the Middle

Idea:
You generate several synthetic documents, hide a single critical fact in each one (either at the start, middle, or end), and ask the model about that fact. Then you measure accuracy per position to show the lost-in-the-middle effect.

Lab pseudocode:

# Create synthetic documents and embed the critical fact
def create_documents(num_docs=5, words_per_doc=200):
    documents = []
    for i in range(num_docs):
        filler = generate_filler_text(words_per_doc)
        position = random.choice(["start", "middle", "end"])
        doc_with_fact = embed_critical_fact(filler, fact, position)
        documents.append((doc_with_fact, position))
    return documents

# Ask the LLM and compute accuracy grouped by fact position
def measure_accuracy_by_position(documents, query):
    results = {"start": [], "middle": [], "end": []}
    for doc, position in documents:
        response = ollama_query(doc, query)
        accuracy = evaluate_response(response, expected_answer)
        results[position].append(accuracy)
    return average_per_bucket(results)


You’ll then plot or tabulate accuracy vs {start, middle, end} and show accuracy is worst for middle.


More detailed explenation:
**Goal of this experiment**

We want to test how an LLM behaves when a single important fact (“the needle”) is placed at different positions inside a long document (“the haystack”): at the **start**, **middle**, and **end**.  
For each position, we will generate several synthetic documents, query the LLM about the fact, and measure **accuracy per position**.  
We expect to see a “lost-in-the-middle” effect: the model tends to do worse when the fact is buried in the middle.

Feel free to add more interesting insights or plots regarding our experiment results.

Environment assumptions
- We already have an LLM helper module that talks to Azure OpenAI.
- all relevant files will be written under lab1 dir
- You can create data dir which will contain generated data as explained before that will help us show the experiment goals. Data should be 5 sinthetic docs with ~200 words per doc. each one will contain one "critical" fact in start/middle/end of doc.
```

---

### Prompt 2
```
great, as we see that our model is well preforming on this "lost in the middle problem" lets go on and take the problem one stem further.
lets create sume problem on a much complex form - much longer input against much hidden facts, and see if there will be accuracy change.

- do not remove the past ran of the lab - its a great beginning of our experiment
- log our experiment steps as part of our readme, this should include our tries, results, understandings and new tryings as a cycle...
```

---

### Prompt 3
```
before conntinuation to trial 3 - please note:
- you should share all of our running logs from console to the lab readme, its very informative!
- trial 3 should be much longer files than 1000, something around 5000-10000 word files. in order to do it well, please much expand your filler sentences in order no to repeat same sentences again and again
```

---

### Prompt 4
```
ok Ive deployed the Llama-3.2-1B-Instruct for our experiment.
lets add to our helper the option to select between 2 models (gpt4o as default in order to be backward compatible to our existing code), remember you should add some params to the .env file and add another unittest validating this model, let me know which params I should send you as values for the .env
```

---

### Prompt 5
```
endpoint

**************

key

**********************

model_name = "Phi-4-mini-instruct"
deployment_name = "Phi-4-mini-instruct"


add this to our .env and test the new model using the helper unit tests
run tests for validation
```

---

### Prompt 6
```
lets run trial 4 of our experiment, this trial will be similar to trial 3 () with the 3000word doc ) but with our new secondary model
```

---

### Prompt 7
```
lets try trial5, last chance with phi model and 5000 word doc, pls enhance your filler sentences to avoid repetative sentences and hide the facts as possible. log the whole process into our readme
```

---

### Promprt8
``
Look at the logs - seems like a bug - isnt it?

Processing document 1/15 (Position: end)...
  ✗ INCORRECT
  Response: ..am.str. The. The. The.. and and and and and the. The. and and. The. The.. and.and. and and- and- a...

Processing document 2/15 (Position: end)...
  ✗ INCORRECT
  Response: .... and. .prim.prim.prim.... and. and. and... and... and. and... and. and.prim.. and.str... and. an...

Processing document 3/15 (Position: middle)...
  ✗ INCORRECT
  Response: .ord..ord.ord.ord.ale.ord..ord.ord.ord..ord.ord.ord.and. andord.ord.bale and and and.ord and and and...

Processing document 4/15 (Position: end)...
  ✗ INCORRECT
  Response: .. The....am...str. and..arch... and..ale.ord. and and and and.....mo....

Processing document 5/15 (Position: middle)...
  ✗ INCORRECT
  Response: . and and and... and. and. and. and. and. The.the.the....

Processing document 6/15 (Position: start)...
  ✗ INCORRECT
  Response: . and. and. and. and. and and and and and and. and.. and. and.ord. and.op.ad. to to. to. and and. Th...

Processing document 7/15 (Position: middle)...
  ✗ INCORRECT
  Response: .ter.ter.am.ordurac.hegale.ord.hegam.am.orma.am. The.rough.gam.orma.am.ale.ale.terale. and and.ale.a...

Processing document 8/15 (Position: middle)...
```

---

### Prompt 9
```
maybe retry trial 5?
```

### Prompt 9
```
same wierd answers, rerun the phi test on the inputs we are sending..

Processing document 1/15 (Position: start)...
  ✗ INCORRECT
  Response: .. and and and and and and and and and and and and. and and. and and...................ro.....*. and...

Processing document 2/15 (Position: middle)...
Error querying document 1: 'NoneType' object has no attribute 'lower'
  ✗ INCORRECT
  Response: ERROR: 'NoneType' object has no attribute 'lower'...

Processing document 3/15 (Position: end)...
  ✗ INCORRECT
  Response: ... and.rough. and and and and and and and and andhe.ow.ter. and and... and.preca. and.ter.. and and...

Processing document 4/15 (Position: end)...
  ✗ INCORRECT
  Response: ......ter..ter.ter.ter.temartemop.......t.ter..ter.t and and and and and and and...ter.ter...ter.ter...

Processing document 5/15 (Position: end)...
  ✗ INCORRECT
  Response: .d. and and andale.....ord....ord..ful.ter.... and.. and.ter.... and and...ter and and and and... an...

Processing document 6/15 (Position: middle)...


maybe lower a bit so we have successful 15 runs and validate our experiment goal something like 3500-3800 words
```

### Prompt 7
```
great! so we have got an interesting findings, modern models are not suffering from 'lost in the middle' phenomeneon, of coarse not openai big models, bet also a limited model such like pur secondary was answering with 100% accuracy! even when it was close to its context window limit!

before we finishing this lab, take your time to rearrange the readme to conclude the whole process.
start with goal, continue to the progress and trials concepts step by step, explain about the findings on the road and the final understanding.
show the logs of the 5 trials at the end of the readme.
```

---
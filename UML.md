# Architecture Document
## Context Window Labs - Scientific Framework for LLM Context Window Testing

**Version:** 1.0  
**Date:** December 11, 2025  
**Author:** Lior Abuhav

---

## Table of Contents
1. [System Overview](#1-system-overview)
2. [C4 Model Architecture](#2-c4-model-architecture)
3. [Component Architecture](#3-component-architecture)
4. [Data Flow Architecture](#4-data-flow-architecture)
5. [Module Details](#5-module-details)
6. [External Dependencies](#6-external-dependencies)
7. [Architecture Decision Records (ADRs)](#7-architecture-decision-records-adrs)
8. [Design Patterns](#8-design-patterns)
9. [Quality Attributes](#9-quality-attributes)
10. [Deployment Architecture](#10-deployment-architecture)

---

## 1. System Overview

### 1.1 Purpose
Context Window Labs is a scientific research framework designed to systematically test and measure Large Language Model (LLM) behavior across different context window scenarios. The system provides reproducible experiments, statistical analysis, and production-ready insights for LLM-based applications.

### 1.2 Architectural Characteristics
- **Modularity**: Four independent lab modules with clear separation of concerns
- **Reproducibility**: Deterministic data generation and experiment execution
- **Extensibility**: Plugin-based architecture for new experiments and models
- **Scientific Rigor**: Comprehensive metrics, statistical validation, and visualization
- **Production-Ready**: Installable Python package with stable API

### 1.3 Key Design Principles
1. **Separation of Concerns**: Data generation, experimentation, and analysis are isolated
2. **Configuration over Code**: Environment-based configuration for flexibility
3. **Fail-Safe Operations**: Comprehensive error handling and validation
4. **Observable Behavior**: Extensive logging and progress tracking
5. **Testability**: Unit and integration tests for all critical components

---

## 2. C4 Model Architecture

### 2.1 Level 1: System Context Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                    External Context                             │
│                                                                 │
│  ┌──────────┐                                   ┌─────────────┐│
│  │          │    API Requests                  │             ││
│  │  User/   │ ────────────────────────────────>│   Context   ││
│  │Researcher│                                  │   Window    ││
│  │          │<────────────────────────────────│    Labs     ││
│  │          │    Results & Reports             │   System    ││
│  └──────────┘                                   └──────┬──────┘│
│                                                        │       │
│                                                        │       │
│                                          ┌─────────────▼──────┐│
│                                          │  Azure OpenAI API  ││
│                                          │  - GPT-4o          ││
│                                          │  - Phi-4-mini      ││
│                                          │  - Embeddings      ││
│                                          └────────────────────┘│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Key Relationships:**
- **Users/Researchers** interact via Python API (function calls) or CLI
- **Context Window Labs System** orchestrates experiments
- **Azure OpenAI API** provides LLM inference and embeddings

---

### 2.2 Level 2: Container Diagram

```
┌────────────────────────────────────────────────────────────────────┐
│                    Context Window Labs System                      │
│                                                                    │
│  ┌────────────────────┐         ┌──────────────────────────────┐  │
│  │                    │         │  Azure OpenAI Helper Module  │  │
│  │   Package API      │────────>│  - Client Management         │──┼──> Azure
│  │   (context_window  │         │  - Configuration             │  │    OpenAI
│  │    _labs.py)       │         │  - Error Handling            │  │
│  │                    │         │  - Prompt Logging            │  │
│  └─────────┬──────────┘         └──────────────────────────────┘  │
│            │                                                       │
│            │ Orchestrates                                          │
│            │                                                       │
│  ┌─────────▼──────────────────────────────────────────────────┐   │
│  │                   Laboratory Modules                        │   │
│  │                                                             │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │   │
│  │  │  Lab 1   │  │  Lab 2   │  │  Lab 3   │  │  Lab 4   │   │   │
│  │  │ Position │  │ Context  │  │   RAG    │  │ Context  │   │   │
│  │  │   Bias   │  │   Size   │  │    vs    │  │ Engineer │   │   │
│  │  │  Testing │  │  Impact  │  │   Full   │  │   -ing   │   │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │   │
│  │       │             │             │             │          │   │
│  └───────┼─────────────┼─────────────┼─────────────┼──────────┘   │
│          │             │             │             │              │
│          └─────────────┴─────────────┴─────────────┘              │
│                        │                                          │
│              ┌─────────▼─────────────┐                            │
│              │  Data & Results       │                            │
│              │  - JSON Storage       │                            │
│              │  - Vector Database    │                            │
│              │  - Analysis Reports   │                            │
│              │  - Visualizations     │                            │
│              └───────────────────────┘                            │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

**Container Responsibilities:**
- **Package API**: Entry point, lab orchestration, public interface
- **Azure OpenAI Helper**: Centralized LLM client, config management
- **Laboratory Modules**: Independent experiments with data generation, execution, analysis
- **Data & Results**: Persistent storage for inputs, outputs, and analytics

---

### 2.3 Level 3: Component Diagram

#### Lab Module Internal Architecture (Common Pattern)

```
┌─────────────────────────────────────────────────────────────────┐
│                        Lab Module (Generic)                     │
│                                                                 │
│  ┌───────────────────┐        ┌──────────────────────────────┐ │
│  │  Data Generation  │        │    Experiment Execution       │ │
│  │  Component        │        │    Component                  │ │
│  │                   │        │                               │ │
│  │  - generate_*.py  │───────>│  - experiment.py              │ │
│  │  - Templates      │ JSON   │  - Query orchestration        │ │
│  │  - Fact libraries │ Files  │  - Response evaluation        │ │
│  │  - Random seed    │        │  - Metrics collection         │ │
│  └───────────────────┘        └────────────┬──────────────────┘ │
│                                            │                    │
│                                            │ Results JSON       │
│                                            │                    │
│  ┌────────────────────────────────────────▼──────────────────┐ │
│  │             Analysis & Visualization Component            │ │
│  │                                                            │ │
│  │  - analyze_results.py                                     │ │
│  │  - Statistical calculations                               │ │
│  │  - Matplotlib/Seaborn charts                              │ │
│  │  - Report generation                                      │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Component Architecture

### 3.1 Package-Level Components

#### 3.1.1 Context Window Labs Main Module
**File:** `context_window_labs.py`

```python
┌──────────────────────────────────────────┐
│   context_window_labs.py                 │
│                                          │
│  Exports:                                │
│  ├── run_lab1(trial="trial1")           │
│  ├── run_lab2(dataset="cities")         │
│  ├── run_lab3()                          │
│  ├── run_lab4()                          │
│  ├── llm_query()                         │
│  ├── validate_configuration()            │
│  └── get_client()                        │
│                                          │
│  Responsibilities:                       │
│  - Public API definition                 │
│  - Lab orchestration                     │
│  - Version management                    │
└──────────────────────────────────────────┘
```

---

#### 3.1.2 Azure OpenAI Helper Module
**Directory:** `azure_openai_helper/`

```
azure_openai_helper/
├── __init__.py                    # Module exports
├── llm_client.py                  # Core client implementation
├── PROMPT_LOG.md                  # Prompt logging
└── tests/                         # Unit tests
    ├── test_multi_model.py
    └── test_validation.py
```

**Class Diagram:**

```
┌─────────────────────────────────────────────────────┐
│           Azure OpenAI Helper Module                │
│                                                     │
│  Functions:                                         │
│  ┌────────────────────────────────────────────┐    │
│  │ _load_configuration() -> dict              │    │
│  │ ├── Load .env variables                    │    │
│  │ ├── Validate required fields               │    │
│  │ └── Support primary + secondary models     │    │
│  └────────────────────────────────────────────┘    │
│                                                     │
│  ┌────────────────────────────────────────────┐    │
│  │ validate_configuration() -> dict           │    │
│  │ └── Public config validation               │    │
│  └────────────────────────────────────────────┘    │
│                                                     │
│  ┌────────────────────────────────────────────┐    │
│  │ get_client(model: str) -> AzureOpenAI      │    │
│  │ ├── Initialize Azure OpenAI client         │    │
│  │ ├── Support model selection                │    │
│  │ └── Return configured client               │    │
│  └────────────────────────────────────────────┘    │
│                                                     │
│  ┌────────────────────────────────────────────┐    │
│  │ llm_query(prompt, temp, tokens, model)     │    │
│  │ ├── Call chat.completions API              │    │
│  │ ├── Handle errors (rate limit, API)        │    │
│  │ ├── Log prompts to PROMPT_LOG.md           │    │
│  │ └── Return response text                   │    │
│  └────────────────────────────────────────────┘    │
│                                                     │
│  Exception:                                         │
│  └── ConfigurationError (custom exception)         │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

### 3.2 Lab-Specific Components

#### 3.2.1 Lab 1: Position Bias Testing

**Directory Structure:**
```
lab1/
├── __init__.py                    # Lab exports (run_lab)
├── generate_data.py               # Synthetic document generation
├── experiment.py                  # Experiment execution
├── analyze_results.py             # Statistical analysis
├── run_lab.py                     # Convenience runner
├── data/                          # Generated JSON files
└── results/                       # Experiment outputs
```

**Component Interaction Flow:**

```
┌────────────────┐        ┌─────────────────┐        ┌──────────────────┐
│  Data          │  JSON  │   Experiment    │ JSON   │   Analysis       │
│  Generation    │───────>│   Execution     │───────>│   & Reporting    │
│                │        │                 │        │                  │
│ - Templates    │        │ - Load docs     │        │ - Statistics     │
│ - Facts        │        │ - Query LLM     │        │ - Visualizations │
│ - Positions    │        │ - Evaluate      │        │ - Findings       │
│ - Distractors  │        │ - Collect metrics│       │ - Recommendations│
└────────────────┘        └────────┬────────┘        └──────────────────┘
                                   │
                                   │ llm_query()
                                   ▼
                          ┌─────────────────┐
                          │ Azure OpenAI    │
                          │ Helper          │
                          └─────────────────┘
```

**Key Classes/Functions:**

```python
# generate_data.py
def generate_documents(target_word_count, positions, add_distractors)
def create_document(fact_data, position, word_count, distractors)
def get_filler_text(word_count)

# experiment.py
def load_documents(data_file)
def query_document(doc, temperature, max_tokens, model)
def evaluate_response(response, expected_answer, keywords)
def run_experiment(data_file, model)

# analyze_results.py
def load_results(results_file)
def analyze_position_effect(results)
def plot_position_accuracy(results)
def generate_analysis_report(results, analysis)
```

---

#### 3.2.2 Lab 2: Context Size Impact

**Directory Structure:**
```
lab2/
├── __init__.py
├── generate_documents.py          # Multiple generators
├── generate_cities.py
├── generate_countries.py
├── generate_tech_companies.py
├── experiment.py
├── analyze_results.py
├── data/                          # Size-varied datasets
└── results/
```

**Unique Features:**
- **Multi-dataset support**: Animals, cities, countries, tech companies
- **Token counting**: Integration with tiktoken library
- **Latency tracking**: Time-based performance metrics

**Token Counting Architecture:**

```
┌───────────────────────────────────────────────────┐
│         Token Counting Component                  │
│                                                   │
│  ┌─────────────────────────────────────────┐     │
│  │  import tiktoken                        │     │
│  │                                         │     │
│  │  encoding = tiktoken.encoding_for_model│     │
│  │             ("gpt-4")                   │     │
│  │                                         │     │
│  │  token_count = len(encoding.encode(txt))│    │
│  └─────────────────────────────────────────┘     │
│                                                   │
│  Used for:                                        │
│  - Pre-query token estimation                    │
│  - Cost calculation                               │
│  - Context limit validation                       │
└───────────────────────────────────────────────────┘
```

---

#### 3.2.3 Lab 3: RAG vs Full Context

**Directory Structure:**
```
lab3/
├── __init__.py
├── generate_documents.py          # Domain-specific corpus
├── experiment.py                  # Dual-mode execution
├── analyze_results.py
├── data/
└── results/
```

**Architecture Highlights:**

```
┌────────────────────────────────────────────────────────────┐
│                Lab 3 Architecture                          │
│                                                            │
│  ┌──────────────────────┐      ┌──────────────────────┐   │
│  │   Full Context Mode  │      │     RAG Mode         │   │
│  │                      │      │                      │   │
│  │  1. Concatenate all │      │  1. Chunk documents  │   │
│  │     documents        │      │  2. Generate embeddings│ │
│  │  2. Single LLM query│      │  3. Vector search    │   │
│  │  3. High token usage│      │  4. Retrieve top-k   │   │
│  │                      │      │  5. Query with chunks│   │
│  └──────────────────────┘      └──────────┬───────────┘   │
│                                           │               │
│                                           ▼               │
│                              ┌─────────────────────────┐  │
│                              │   ChromaDB              │  │
│                              │   (Vector Database)     │  │
│                              │                         │  │
│                              │  - Persistent storage   │  │
│                              │  - Cosine similarity    │  │
│                              │  - OpenAI embeddings    │  │
│                              └─────────────────────────┘  │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

**Key Classes:**

```python
class DocumentChunker:
    """Utility for splitting documents into fixed-size chunks"""
    def __init__(self, chunk_size, overlap)
    def chunk_text(text, doc_id) -> List[Dict]
    def chunk_documents(documents) -> List[Dict]

class RAGEngine:
    """Vector-based retrieval engine"""
    def __init__(self, collection_name, persist_directory)
    def initialize_collection(documents)
    def retrieve(query, top_k) -> List[str]
    def _get_embeddings(texts) -> List[List[float]]
```

---

#### 3.2.4 Lab 4: Context Engineering Strategies

**Directory Structure:**
```
lab4/
├── __init__.py
├── generate_scenario.py           # Detective scenario
├── experiment.py
├── strategies.py                  # Strategy implementations
├── analyze_results.py
├── data/
└── results/
```

**Strategy Pattern Architecture:**

```
┌─────────────────────────────────────────────────────────────┐
│                  Strategy Pattern                           │
│                                                             │
│              ┌───────────────────────┐                      │
│              │  ContextStrategy      │                      │
│              │  (Abstract Base)      │                      │
│              │                       │                      │
│              │ + process_history()   │                      │
│              │ + answer_question()   │                      │
│              │ + count_tokens()      │                      │
│              └───────────┬───────────┘                      │
│                          │                                  │
│          ┌───────────────┼───────────────┐                  │
│          │               │               │                  │
│  ┌───────▼─────┐  ┌──────▼──────┐  ┌────▼──────┐           │
│  │   SELECT    │  │  COMPRESS   │  │   WRITE   │           │
│  │  Strategy   │  │  Strategy   │  │ Strategy  │           │
│  │             │  │             │  │           │           │
│  │ Keyword-    │  │ Summarize   │  │ Extract   │           │
│  │ based       │  │ when >      │  │ facts to  │           │
│  │ retrieval   │  │ threshold   │  │ scratchpad│           │
│  └─────────────┘  └─────────────┘  └───────────┘           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Strategy Classes:**

```python
class ContextStrategy:
    """Base class for context management strategies"""
    def process_history(history, query) -> str
    def answer_question(history, query) -> dict
    def count_tokens(text) -> int

class SelectStrategy(ContextStrategy):
    """RAG-style keyword retrieval (top-k relevant steps)"""
    def calculate_relevance(text, query) -> float
    def process_history(history, query) -> str

class CompressStrategy(ContextStrategy):
    """Summarization when exceeding token threshold"""
    def process_history(history, query) -> str
    # Maintains: compressed_history, last_summarized_step

class WriteStrategy(ContextStrategy):
    """External scratchpad with fact extraction"""
    def extract_facts(history) -> List[str]
    def process_history(history, query) -> str
```

---

## 4. Data Flow Architecture

### 4.1 High-Level Data Flow

```
┌────────────────────────────────────────────────────────────────┐
│                    Data Flow Pipeline                          │
│                                                                │
│  ┌──────────────┐     ┌───────────────┐     ┌──────────────┐  │
│  │   Config     │────>│   Lab Module  │────>│   Results    │  │
│  │   (.env)     │     │               │     │   (JSON/PNG) │  │
│  └──────────────┘     │  1. Generate  │     └──────────────┘  │
│                       │     Data      │                       │
│                       │               │                       │
│                       │  2. Execute   │                       │
│                       │     Experiment│                       │
│                       │       ↓       │                       │
│  ┌──────────────┐     │    [LLM API]  │                       │
│  │  Azure       │<────│       ↑       │                       │
│  │  OpenAI      │     │  3. Analyze   │                       │
│  │  API         │     │     Results   │                       │
│  └──────────────┘     └───────────────┘                       │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### 4.2 Detailed Experiment Flow

```
User Request
    │
    ▼
┌─────────────────┐
│  run_labX()     │  Entry point function
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Load/Generate   │  Data preparation
│ Documents       │  - Read JSON or generate
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ For each doc/   │  Iteration loop
│ question:       │
│   │             │
│   ├─> Construct│  Prompt engineering
│   │   Prompt   │
│   │            │
│   ├─> Query    │  LLM API call
│   │   LLM      │  via azure_openai_helper
│   │            │
│   ├─> Evaluate │  Response validation
│   │   Response │
│   │            │
│   └─> Collect  │  Metrics aggregation
│       Metrics  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Save Results    │  Persistence
│ (JSON)          │  - Timestamp
└────────┬────────┘  - Metadata
         │           - Raw data
         ▼
┌─────────────────┐
│ Analyze &       │  Post-processing
│ Visualize       │  - Statistics
└────────┬────────┘  - Charts
         │           - Reports
         ▼
┌─────────────────┐
│ Generate Report │  Output
│ (TXT/PNG)       │
└─────────────────┘
```

### 4.3 Configuration Flow

```
┌──────────────┐
│  .env file   │
│              │
│  Variables:  │
│  - ENDPOINT  │
│  - API_KEY   │
│  - DEPLOY    │
│  - VERSION   │
└──────┬───────┘
       │
       │ load_dotenv()
       ▼
┌──────────────────────┐
│ _load_configuration()│
│                      │
│ Validates:           │
│ ✓ Required vars      │
│ ✓ Secondary model    │
│ ✓ Format             │
└──────┬───────────────┘
       │
       │ Returns config dict
       ▼
┌──────────────────┐
│  get_client()    │
│                  │
│ Creates:         │
│ - AzureOpenAI    │
│   client         │
│ - Model routing  │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  llm_query()     │
│                  │
│ Executes:        │
│ - API call       │
│ - Error handling │
│ - Logging        │
└──────────────────┘
```

---

## 5. Module Details

### 5.1 Azure OpenAI Helper - Deep Dive

**Responsibility:** Centralized abstraction over Azure OpenAI API

**Key Design Decisions:**
1. **Single Responsibility**: Only handles LLM communication
2. **Configuration Isolation**: Environment-based, no hardcoded values
3. **Multi-Model Support**: Primary/secondary model routing
4. **Comprehensive Logging**: All prompts logged to PROMPT_LOG.md
5. **Error Classification**: Specific handling for rate limits, API errors, connection issues

**Error Handling Strategy:**

```python
try:
    response = client.chat.completions.create(...)
except RateLimitError as e:
    # Exponential backoff or user notification
    raise
except APIConnectionError as e:
    # Network issues - suggest retry
    raise
except APIError as e:
    # API-level errors - log and fail gracefully
    raise
except Exception as e:
    # Unexpected errors - comprehensive logging
    raise
```

**Logging Mechanism:**

```python
# PROMPT_LOG.md structure:
## [TIMESTAMP] Model: <deployment_name>
### Prompt:
<full_prompt_text>

### Response:
<llm_response>

### Metadata:
- Temperature: X
- Max Tokens: Y
- Model: Z
---
```

---

### 5.2 Lab Module Common Patterns

All lab modules follow a consistent three-phase architecture:

#### Phase 1: Data Generation
```python
# Consistent interface across all labs
def generate_<dataset_type>(
    count: int,
    size: int,
    **kwargs
) -> List[Dict]:
    """
    Generate synthetic data with:
    - Fixed random seed (reproducibility)
    - Validation checks
    - Metadata annotation
    - JSON serialization
    """
    random.seed(42)  # Fixed seed
    data = []
    # Generation logic
    return data
```

#### Phase 2: Experiment Execution
```python
def run_experiment(
    data_file: str,
    model: str = None
) -> Dict:
    """
    Execute experiment with:
    - Progress tracking
    - Error handling per item
    - Metrics collection
    - Result aggregation
    """
    results = {
        "timestamp": datetime.now().isoformat(),
        "model": model,
        "data": []
    }
    # Execution logic
    return results
```

#### Phase 3: Analysis
```python
def analyze_results(
    results_file: str
) -> None:
    """
    Analyze with:
    - Statistical calculations
    - Visualization generation
    - Report writing
    - Insights extraction
    """
    # Analysis logic
    # Save plots and reports
```

---

## 6. External Dependencies

### 6.1 Dependency Map

```
┌────────────────────────────────────────────────────────────┐
│                  External Dependencies                     │
│                                                            │
│  ┌──────────────────────────────────────────────────┐     │
│  │  Azure Services                                  │     │
│  │                                                  │     │
│  │  ┌────────────────────────────────────────┐     │     │
│  │  │  Azure OpenAI Service                  │     │     │
│  │  │  - GPT-4o deployment                   │     │     │
│  │  │  - text-embedding-ada-002              │     │     │
│  │  └────────────────────────────────────────┘     │     │
│  │                                                  │     │
│  │  ┌────────────────────────────────────────┐     │     │
│  │  │  Azure AI Foundry                      │     │     │
│  │  │  - Phi-4-mini-instruct deployment      │     │     │
│  │  └────────────────────────────────────────┘     │     │
│  └──────────────────────────────────────────────────┘     │
│                                                            │
│  ┌──────────────────────────────────────────────────┐     │
│  │  Python Libraries (Core)                         │     │
│  │  - openai >= 1.0.0 (Azure SDK)                   │     │
│  │  - python-dotenv (configuration)                 │     │
│  │  - tiktoken (token counting)                     │     │
│  └──────────────────────────────────────────────────┘     │
│                                                            │
│  ┌──────────────────────────────────────────────────┐     │
│  │  Python Libraries (Experiments)                  │     │
│  │  - chromadb (vector database)                    │     │
│  │  - pandas (data analysis)                        │     │
│  │  - matplotlib (visualization)                    │     │
│  │  - seaborn (enhanced charts)                     │     │
│  │  - numpy (numerical operations)                  │     │
│  │  - scikit-learn (similarity metrics)             │     │
│  └──────────────────────────────────────────────────┘     │
│                                                            │
│  ┌──────────────────────────────────────────────────┐     │
│  │  Python Libraries (Development)                  │     │
│  │  - pytest (testing)                              │     │
│  │  - black (formatting)                            │     │
│  │  - flake8 (linting)                              │     │
│  │  - mypy (type checking)                          │     │
│  └──────────────────────────────────────────────────┘     │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### 6.2 Dependency Rationale

| Dependency | Purpose | Alternatives Considered | Decision Rationale |
|------------|---------|------------------------|-------------------|
| Azure OpenAI | LLM inference | OpenAI API, Anthropic, HuggingFace | Enterprise features, managed service, multi-model support |
| ChromaDB | Vector storage | Pinecone, Weaviate, FAISS | Lightweight, embeddable, open-source, no server required |
| tiktoken | Token counting | Transformers, manual | Official OpenAI library, accurate for GPT models |
| matplotlib | Visualization | Plotly, Seaborn only | Widely adopted, publication-quality, extensive documentation |
| python-dotenv | Configuration | configparser, YAML | Simple, standard for .env files, minimal dependencies |

---

## 7. Architecture Decision Records (ADRs)

### ADR-001: Package-Based Distribution

**Status:** Accepted  
**Date:** 2024-12

**Context:**  
Need to provide reusable, installable framework for experiments.

**Decision:**  
Implement as installable Python package with setup.py/pyproject.toml.

**Consequences:**
- ✅ Easy installation via pip
- ✅ Version management
- ✅ Dependency resolution
- ✅ Distribution via PyPI or Git
- ⚠️ Requires proper package structure
- ⚠️ More complex than standalone scripts

**Alternatives Considered:**
1. Standalone scripts - Too difficult to reuse
2. Jupyter notebooks - Not reproducible enough
3. Docker containers - Overkill for Python-only project

---

### ADR-002: Centralized Azure OpenAI Helper

**Status:** Accepted  
**Date:** 2024-12

**Context:**  
Multiple labs need LLM access with consistent configuration and error handling.

**Decision:**  
Create shared `azure_openai_helper` module with single responsibility.

**Consequences:**
- ✅ DRY principle (no duplication)
- ✅ Consistent error handling
- ✅ Centralized logging
- ✅ Easy to update API version
- ⚠️ Single point of failure
- ⚠️ Labs coupled to this module

**Implementation:**
```python
# All labs import from same source
from azure_openai_helper import llm_query
```

---

### ADR-003: Lab Independence

**Status:** Accepted  
**Date:** 2024-12

**Context:**  
Four different experiments with different goals and methodologies.

**Decision:**  
Each lab is self-contained with own data/, results/, and scripts.

**Consequences:**
- ✅ Run labs independently
- ✅ Different data structures per lab
- ✅ Isolated failures
- ✅ Easy to extend with new labs
- ⚠️ Some code duplication (analyze patterns)
- ⚠️ Larger total codebase

**Structure:**
```
lab1/ lab2/ lab3/ lab4/  # Separate namespaces
```

---

### ADR-004: JSON for Data Persistence

**Status:** Accepted  
**Date:** 2024-12

**Context:**  
Need human-readable, version-controllable storage format.

**Decision:**  
Use JSON for documents, results, and configuration.

**Consequences:**
- ✅ Human-readable
- ✅ Git-friendly (diffs)
- ✅ Universal support
- ✅ No database required
- ⚠️ Large files for big datasets
- ⚠️ No indexing/querying

**Alternatives Considered:**
1. SQLite - Too complex for read-once data
2. CSV - Doesn't handle nested structures
3. Pickle - Not human-readable
4. YAML - Less standard for data

---

### ADR-005: Temperature = 0.0 for Reproducibility

**Status:** Accepted  
**Date:** 2024-12

**Context:**  
Scientific experiments require reproducibility.

**Decision:**  
Default temperature to 0.0 for deterministic outputs.

**Consequences:**
- ✅ Reproducible results
- ✅ Easier to compare across runs
- ✅ Fair model comparison
- ⚠️ May not reflect real-world usage
- ⚠️ Less creative responses

**Configuration:**
```python
llm_query(prompt, temperature=0.0)  # Default
```

---

### ADR-006: Strategy Pattern for Lab 4

**Status:** Accepted  
**Date:** 2024-12

**Context:**  
Need to compare three different context management approaches.

**Decision:**  
Implement Strategy pattern with base class and three concrete strategies.

**Consequences:**
- ✅ Clean separation of strategies
- ✅ Easy to add new strategies
- ✅ Consistent interface
- ✅ Testable in isolation
- ⚠️ More abstraction overhead

**Class Hierarchy:**
```
ContextStrategy (abstract)
├── SelectStrategy
├── CompressStrategy
└── WriteStrategy
```

---

### ADR-007: ChromaDB for Vector Storage (Lab 3)

**Status:** Accepted  
**Date:** 2024-12

**Context:**  
Lab 3 requires vector similarity search for RAG implementation.

**Decision:**  
Use ChromaDB as embedded vector database.

**Consequences:**
- ✅ No server setup required
- ✅ Persistent storage
- ✅ Simple Python API
- ✅ Suitable for experiment scale
- ⚠️ Not production-grade at scale
- ⚠️ Additional dependency

**Alternative:** FAISS (rejected - more complex, no persistence by default)

---

### ADR-008: Multi-Model Support via Configuration

**Status:** Accepted  
**Date:** 2024-12

**Context:**  
Need to compare GPT-4o vs Phi-4-mini on same experiments.

**Decision:**  
Support primary and secondary model configurations.

**Consequences:**
- ✅ Fair comparisons
- ✅ Model selection at runtime
- ✅ No code changes to switch models
- ⚠️ More complex configuration
- ⚠️ Need to manage multiple deployments

**Usage:**
```python
llm_query(prompt, model="primary")  # GPT-4o
llm_query(prompt, model="secondary")  # Phi-4-mini
```

---

### ADR-009: Progressive Trials (Lab 1)

**Status:** Accepted  
**Date:** 2024-12

**Context:**  
Unknown context window limits require systematic testing.

**Decision:**  
Implement multiple trials with increasing document sizes.

**Consequences:**
- ✅ Discover breaking points empirically
- ✅ Gradual difficulty increase
- ✅ Document model capabilities
- ⚠️ More experiment runs required
- ⚠️ More data files to manage

**Implementation:**
```
trial1: 200 words
trial2: 500 words
trial3: 1000 words
trial4: 2000 words
trial5: 3500 words
```

---

### ADR-010: Prompt Logging to PROMPT_LOG.md

**Status:** Accepted  
**Date:** 2024-12

**Context:**  
Need visibility into exact prompts sent to LLM for debugging and documentation.

**Decision:**  
Log all prompts and responses to markdown files.

**Consequences:**
- ✅ Full transparency
- ✅ Debugging aid
- ✅ Documentation of experiments
- ✅ Audit trail
- ⚠️ Large log files
- ⚠️ May contain sensitive data

**Format:**
```markdown
## [Timestamp] Model: deployment_name
### Prompt:
...
### Response:
...
```

---

## 8. Design Patterns

### 8.1 Patterns Used

#### 8.1.1 **Strategy Pattern**
**Where:** Lab 4 context management strategies  
**Purpose:** Encapsulate interchangeable algorithms (SELECT, COMPRESS, WRITE)

```python
class ContextStrategy(ABC):
    @abstractmethod
    def process_history(self, history, query):
        pass

# Concrete strategies
class SelectStrategy(ContextStrategy): ...
class CompressStrategy(ContextStrategy): ...
class WriteStrategy(ContextStrategy): ...
```

---

#### 8.1.2 **Template Method Pattern**
**Where:** Lab experiment execution  
**Purpose:** Define skeleton with customizable steps

```python
def run_lab():
    # Template steps (same across all labs)
    1. Load/generate data
    2. Execute experiments
    3. Save results
    4. Analyze
    5. Generate reports
    
    # Customizable: what data, how to evaluate, etc.
```

---

#### 8.1.3 **Facade Pattern**
**Where:** `context_window_labs.py` module  
**Purpose:** Simplified interface to complex subsystem

```python
# Complex subsystem hidden behind simple functions
def run_lab1(trial="trial1"):
    # Internally handles:
    # - Data loading
    # - Configuration
    # - Experiment execution
    # - Analysis
```

---

#### 8.1.4 **Factory Pattern** (Implicit)
**Where:** Model client creation  
**Purpose:** Encapsulate object creation logic

```python
def get_client(model: str) -> AzureOpenAI:
    # Factory decides which configuration to use
    if model == "primary":
        return AzureOpenAI(endpoint1, key1, ...)
    elif model == "secondary":
        return AzureOpenAI(endpoint2, key2, ...)
```

---

#### 8.1.5 **Singleton Pattern** (Lazy)
**Where:** Configuration loading  
**Purpose:** Single configuration instance per run

```python
_config_cache = None

def _load_configuration():
    global _config_cache
    if _config_cache is None:
        _config_cache = load_dotenv(...)
    return _config_cache
```

---

### 8.2 Anti-Patterns Avoided

| Anti-Pattern | How Avoided |
|--------------|-------------|
| **God Object** | Separated concerns into azure_openai_helper, labs, analysis |
| **Hardcoded Values** | All config in .env, no magic numbers in API calls |
| **Copy-Paste Code** | Shared helper module for LLM access |
| **Tight Coupling** | Labs don't depend on each other, only on helper |
| **Premature Optimization** | Simple JSON storage, optimize only if needed |

---

## 9. Quality Attributes

### 9.1 Reproducibility ⭐⭐⭐⭐⭐

**Mechanisms:**
- Fixed random seeds in data generation
- Temperature=0.0 for deterministic LLM responses
- Version-controlled data files
- Timestamped results with metadata

**Validation:**
```python
random.seed(42)  # Fixed seed
np.random.seed(42)
```

---

### 9.2 Testability ⭐⭐⭐⭐

**Mechanisms:**
- Unit tests for azure_openai_helper
- Integration tests for package installation
- Mock-friendly design (dependency injection)

**Test Structure:**
```
tests/
├── test_installation.py
├── test_package.py
└── test_quick_start.py

azure_openai_helper/tests/
├── test_multi_model.py
└── test_validation.py
```

---

### 9.3 Maintainability ⭐⭐⭐⭐

**Mechanisms:**
- Consistent structure across labs
- Clear separation of concerns
- Comprehensive documentation
- Type hints where applicable

---

### 9.4 Extensibility ⭐⭐⭐⭐⭐

**Extension Points:**
1. **New Labs:** Add `lab5/` directory with same structure
2. **New Models:** Add to .env configuration
3. **New Strategies:** Inherit from `ContextStrategy`
4. **New Analysis:** Add to analyze_results.py

---

### 9.5 Performance ⭐⭐⭐

**Considerations:**
- Sequential API calls (not optimized for speed)
- Local storage (no database overhead)
- Token counting is fast (tiktoken)

**Known Limitations:**
- No parallel execution
- Large prompts may be slow
- No caching of responses

---

### 9.6 Security ⭐⭐⭐⭐

**Mechanisms:**
- API keys in .env (not version controlled)
- No hardcoded credentials
- .gitignore for sensitive files

**Best Practices:**
```
.env          # Ignored by git
.env.example  # Template (no real keys)
```

---

## 10. Deployment Architecture

### 10.1 Local Development Setup

```
Developer Machine
│
├── Python 3.9+ Environment
│   ├── Virtual environment (venv/conda)
│   └── Installed dependencies
│
├── Project Directory
│   ├── context-window-labs/
│   ├── .env (local configuration)
│   └── Git repository
│
└── External Services
    └── Azure OpenAI
        ├── GPT-4o endpoint
        └── Phi-4-mini endpoint
```

---

### 10.2 Installation Flow

```
┌─────────────────────────────────────────────────┐
│          Installation Process                   │
│                                                 │
│  1. Clone repository                            │
│     git clone <repo>                            │
│                                                 │
│  2. Create .env file                            │
│     cp .env.example .env                        │
│     # Edit with real credentials                │
│                                                 │
│  3. Install package                             │
│     pip install -e .                            │
│     # Or: pip install -e ".[dev]"               │
│                                                 │
│  4. Verify installation                         │
│     python -c "import context_window_labs"      │
│                                                 │
│  5. Run labs                                    │
│     python -c "from context_window_labs..."     │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

### 10.3 Production Considerations

⚠️ **Note:** This is a research framework, not production-ready software.

**If adapting for production:**

1. **API Rate Limiting**
   - Implement exponential backoff
   - Add request queuing
   - Monitor rate limit headers

2. **Error Recovery**
   - Retry failed requests
   - Save partial results
   - Resume from checkpoint

3. **Scalability**
   - Parallel execution with asyncio
   - Distributed processing
   - Database instead of JSON

4. **Monitoring**
   - Add logging framework (e.g., structlog)
   - Metrics collection (e.g., Prometheus)
   - Alert on failures

5. **Security**
   - Use Azure Key Vault for secrets
   - Implement RBAC
   - Audit logging

---

## 11. UML Diagrams

### 11.1 High-Level Package Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                    context_window_labs                         │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │              azure_openai_helper                         │ │
│  │                                                          │ │
│  │  + llm_query(prompt, temp, tokens, model) -> str        │ │
│  │  + validate_configuration() -> dict                     │ │
│  │  + get_client(model) -> AzureOpenAI                     │ │
│  │  + ConfigurationError                                   │ │
│  └──────────────────────────────────────────────────────────┘ │
│                             ▲                                  │
│                             │ uses                             │
│                             │                                  │
│  ┌──────────────┬──────────┴┬──────────────┬──────────────┐   │
│  │    lab1      │    lab2   │    lab3      │    lab4      │   │
│  │              │           │              │              │   │
│  │ + run_lab()  │ + run_lab()│ + run_lab() │ + run_lab() │   │
│  │              │           │              │              │   │
│  │ Components:  │Components:│ Components:  │ Components:  │   │
│  │ - generate   │ - generate│ - generate   │ - generate   │   │
│  │ - experiment │ - experim.│ - experiment │ - experiment │   │
│  │ - analyze    │ - analyze │ - analyze    │ - strategies │   │
│  │              │           │ - RAGEngine  │ - analyze    │   │
│  └──────────────┴───────────┴──────────────┴──────────────┘   │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

### 11.2 Sequence Diagram: Running an Experiment

```
User          Package API      Lab Module      Azure Helper    Azure OpenAI
  │                │               │                 │               │
  │ run_lab1()     │               │                 │               │
  │───────────────>│               │                 │               │
  │                │               │                 │               │
  │                │ load_docs()   │                 │               │
  │                │──────────────>│                 │               │
  │                │               │                 │               │
  │                │  documents    │                 │               │
  │                │<──────────────│                 │               │
  │                │               │                 │               │
  │                │ for each doc: │                 │               │
  │                │──────────────>│                 │               │
  │                │               │                 │               │
  │                │               │ llm_query()     │               │
  │                │               │────────────────>│               │
  │                │               │                 │               │
  │                │               │                 │ API call      │
  │                │               │                 │──────────────>│
  │                │               │                 │               │
  │                │               │                 │   response    │
  │                │               │                 │<──────────────│
  │                │               │                 │               │
  │                │               │   response      │               │
  │                │               │<────────────────│               │
  │                │               │                 │               │
  │                │               │ evaluate()      │               │
  │                │               │ ─ ─ ─ ─ ─ ─ ─ ─│               │
  │                │               │                 │               │
  │                │  results      │                 │               │
  │                │<──────────────│                 │               │
  │                │               │                 │               │
  │                │ analyze()     │                 │               │
  │                │──────────────>│                 │               │
  │                │               │                 │               │
  │                │  report       │                 │               │
  │                │<──────────────│                 │               │
  │                │               │                 │               │
  │    success     │               │                 │               │
  │<───────────────│               │                 │               │
```

---

### 11.3 Class Diagram: Lab 4 Strategies

```
┌─────────────────────────────────────────────────┐
│           <<abstract>>                          │
│          ContextStrategy                        │
├─────────────────────────────────────────────────┤
│ # model_name: str                               │
│ # encoding: tiktoken.Encoding                   │
├─────────────────────────────────────────────────┤
│ + __init__(model_name: str)                     │
│ + count_tokens(text: str) -> int                │
│ + process_history(history, query) -> str*       │
│ + answer_question(history, query) -> dict       │
└────────────────┬────────────────────────────────┘
                 │
                 │ inherits
       ┌─────────┼──────────┐
       │         │          │
       ▼         ▼          ▼
┌──────────┐ ┌───────────┐ ┌────────────┐
│ SELECT   │ │ COMPRESS  │ │   WRITE    │
│ Strategy │ │ Strategy  │ │  Strategy  │
├──────────┤ ├───────────┤ ├────────────┤
│ + top_k  │ │+ max_tokens│ │+ scratchpad│
│          │ │+ compressed│ │            │
├──────────┤ ├───────────┤ ├────────────┤
│+ process_│ │+ process_ │ │+ extract_  │
│  history │ │  history  │ │  facts     │
│          │ │           │ │+ process_  │
│+ calc_   │ │           │ │  history   │
│  relevance│ │           │ │            │
└──────────┘ └───────────┘ └────────────┘

* Abstract method (must implement)
```

---

### 11.4 Component Diagram: Lab 3 RAG Architecture

```
┌──────────────────────────────────────────────────────┐
│                   Lab 3 Module                       │
│                                                      │
│  ┌────────────────┐         ┌──────────────────┐    │
│  │ Experiment     │         │  Analysis        │    │
│  │ Runner         │────────>│  Component       │    │
│  │                │ results │                  │    │
│  └────────┬───────┘         └──────────────────┘    │
│           │                                          │
│           │ orchestrates                             │
│           │                                          │
│  ┌────────▼────────────────────────────┐            │
│  │      Evaluation Loop                │            │
│  │                                     │            │
│  │  For each question:                 │            │
│  │    ├─> Full Context Mode            │            │
│  │    │   └─> Concatenate all docs     │            │
│  │    │                                │            │
│  │    └─> RAG Mode                     │            │
│  │        ├─> Query Embedding          │            │
│  │        ├─> Vector Search            │            │
│  │        └─> Retrieve Top-K           │            │
│  └────────┬────────────────────────────┘            │
│           │                                          │
│           │ uses                                     │
│           │                                          │
│  ┌────────▼────────────┐  ┌─────────────────────┐   │
│  │  DocumentChunker    │  │   RAGEngine         │   │
│  │                     │  │                     │   │
│  │  - chunk_size       │  │  - ChromaDB client  │   │
│  │  - overlap          │  │  - collection       │   │
│  │  - encoding         │  │  - embeddings API   │   │
│  │                     │  │                     │   │
│  │  + chunk_text()     │  │  + initialize()     │   │
│  │  + chunk_documents()│  │  + retrieve()       │   │
│  └─────────────────────┘  │  + get_embeddings() │   │
│                           └──────────┬──────────┘   │
│                                      │              │
└──────────────────────────────────────┼──────────────┘
                                       │
                                       │ persists to
                                       ▼
                              ┌─────────────────┐
                              │  ChromaDB       │
                              │  (Vector Store) │
                              │                 │
                              │  - Documents    │
                              │  - Embeddings   │
                              │  - Metadata     │
                              └─────────────────┘
```

---

## 12. Summary

### Key Architectural Strengths
1. ✅ **Modularity**: Clean separation between labs and shared components
2. ✅ **Reproducibility**: Fixed seeds, deterministic execution, version control
3. ✅ **Extensibility**: Easy to add new labs, models, or strategies
4. ✅ **Scientific Rigor**: Comprehensive metrics, analysis, and visualization
5. ✅ **Usability**: Simple API, clear documentation, installable package

### Architectural Trade-offs
| Benefit | Trade-off |
|---------|-----------|
| Lab independence | Some code duplication |
| Simple JSON storage | No query optimization |
| Sequential execution | Slower than parallel |
| Single-threaded | Simpler but not scalable |
| Embedded vector DB | Not production-scale |

### Future Architectural Evolution

**Near-term:**
- Add async/await for parallel API calls
- Implement caching layer for responses
- Add streaming support for large documents

**Long-term:**
- Microservice architecture for distributed experiments
- Web dashboard for real-time monitoring
- Plugin system for community-contributed labs
- Support for non-Azure LLM providers

---

## Appendix: File Structure

```
context-window-labs/
├── context_window_labs.py         # Main package module
├── pyproject.toml                 # Package configuration
├── setup.py                       # Setup script
├── requirements.txt               # Dependencies
├── .env.example                   # Configuration template
├── README.md                      # User documentation
├── PRD.md                         # Product requirements
├── ARCHITECTURE.md                # This document
│
├── azure_openai_helper/           # Shared LLM client
│   ├── __init__.py
│   ├── llm_client.py
│   ├── PROMPT_LOG.md
│   └── tests/
│       ├── test_multi_model.py
│       └── test_validation.py
│
├── lab1/                          # Position bias testing
│   ├── __init__.py
│   ├── generate_data.py
│   ├── experiment.py
│   ├── analyze_results.py
│   ├── run_lab.py
│   ├── data/
│   │   └── documents_*.json
│   └── results/
│       ├── experiment_results_*.json
│       └── analysis_report_*.txt
│
├── lab2/                          # Context size impact
│   ├── __init__.py
│   ├── generate_documents.py
│   ├── generate_cities.py
│   ├── experiment.py
│   ├── analyze_results.py
│   ├── data/
│   └── results/
│
├── lab3/                          # RAG vs Full Context
│   ├── __init__.py
│   ├── generate_documents.py
│   ├── experiment.py
│   ├── analyze_results.py
│   ├── data/
│   └── results/
│
├── lab4/                          # Context engineering
│   ├── __init__.py
│   ├── generate_scenario.py
│   ├── experiment.py
│   ├── strategies.py
│   ├── analyze_results.py
│   ├── data/
│   └── results/
│
└── tests/                         # Package-level tests
    ├── __init__.py
    ├── test_installation.py
    ├── test_package.py
    └── test_quick_start.py
```

---

**Document Version:** 1.0  
**Last Updated:** December 11, 2025  
**Maintainer:** Lior Abuhav  
**Status:** Living Document

# Product Requirements Document (PRD)
## Project: Context Window Labs - Systematic LLM Context Window Testing Framework
## Author: Lior Abuhav

---

## 1. Purpose
The purpose of this project is to design and implement a comprehensive, modular Python package for systematically testing Large Language Model (LLM) context window limitations and strategies through hands-on experiments. The system demonstrates how modern LLMs handle different context sizes, retrieval strategies, and context management techniques through four independent, reproducible laboratory experiments.

This PRD defines the **goals, requirements, constraints, and acceptance criteria** of the system.  
*Implementation details, setup instructions, experiment descriptions, and architectural explanations are intentionally kept out of this PRD because they appear in the README.*

---

## 2. Objectives

### Functional Objectives
- Implement four independent laboratory experiments:
  - **Lab 1**: Position Bias Testing ("Needle in a Haystack")
  - **Lab 2**: Context Size Impact Analysis
  - **Lab 3**: RAG vs Full Context Comparison
  - **Lab 4**: Context Engineering Strategies Evaluation
- Each lab must:
  - Generate synthetic test data programmatically
  - Execute experiments against Azure OpenAI models
  - Measure multiple performance metrics (accuracy, latency, token usage)
  - Produce statistical analysis and visualizations
  - Generate comprehensive reports
- Provide installable Python package with simple API
- Support multiple LLM models (GPT-4o, Phi-4-mini-instruct)
- Enable reproducible experiments with deterministic configurations

### Non‑Functional Objectives
- Scientific rigor and reproducibility
- Comprehensive documentation
- Modular and extensible architecture
- Clear separation of data generation, experimentation, and analysis
- Production-ready guidelines based on empirical findings

---

## 3. Scope

### In Scope
- Four complete laboratory experiments with different research questions
- Synthetic data generation for controlled experiments
- Azure OpenAI integration via standardized helper module
- Multi-model comparison framework
- Statistical analysis and visualization tools
- Performance metrics tracking (accuracy, latency, token count)
- Vector database integration for RAG experiments (ChromaDB)
- Comprehensive test coverage
- Package installation and distribution

### Out of Scope
- Support for non-Azure OpenAI providers (OpenAI API, Anthropic, etc.)
- Real-time or streaming response handling
- Production deployment infrastructure
- Web UI or interactive dashboard
- Parallel or distributed experiment execution
- Advanced embedding models beyond OpenAI's offerings
- Multi-language support (non-English experiments)

---

## 4. System Overview
The system functions as a scientific research framework with four distinct experimental modules:

```
Context Window Labs Package
│
├── Azure OpenAI Helper Module (shared)
│   ├── Client initialization and configuration
│   ├── Multi-model support
│   └── Prompt logging and validation
│
├── Lab 1: Position Bias Testing
│   ├── Data: Synthetic documents with embedded facts
│   ├── Experiment: Test START/MIDDLE/END positions
│   └── Analysis: Position-based accuracy curves
│
├── Lab 2: Context Size Impact
│   ├── Data: Progressively larger document sets
│   ├── Experiment: Measure latency vs. context size
│   └── Analysis: Degradation curves and thresholds
│
├── Lab 3: RAG vs Full Context
│   ├── Data: Domain-specific document corpus
│   ├── Experiment: Compare retrieval vs. full context
│   └── Analysis: Performance comparison across metrics
│
└── Lab 4: Context Engineering Strategies
    ├── Data: Multi-step scenario with growing context
    ├── Experiment: Compare SELECT/COMPRESS/WRITE strategies
    └── Analysis: Strategy effectiveness over time
```

(See README for detailed architecture explanation, diagrams, and implementation details.)

---

## 5. User Stories

### Researchers
- As a researcher, I can run controlled experiments to understand LLM context window behavior
- As a researcher, I can reproduce published results and extend experiments with new parameters
- As a researcher, I can generate publication-quality visualizations and statistical analyses

### System Architects
- As a system architect, I can determine optimal chunk sizes for RAG implementations
- As a system architect, I can understand practical context window limits for production systems
- As a system architect, I can compare different context management strategies empirically

### Developers
- As a developer, I can install the package with pip and run experiments via simple Python functions
- As a developer, I can extend the framework with new experiments or models
- As a developer, I can validate Azure OpenAI configurations before running experiments

### Educators
- As an educator, I can use these labs to teach students about LLM limitations and capabilities
- As an educator, I can modify experiments to demonstrate different concepts
- As an educator, I can generate clear visualizations to explain complex behaviors

---

## 6. Functional Requirements

### FR1 – Package Installation & Configuration
- FR1.1: Package must be installable via `pip install -e .` in development mode
- FR1.2: Package must be installable from Git repository URL
- FR1.3: Package must support optional dev dependencies (pytest, black, flake8, mypy)
- FR1.4: Configuration must be managed via `.env` file with Azure OpenAI credentials
- FR1.5: Package must provide configuration validation function

### FR2 – Azure OpenAI Helper Module
- FR2.1: Must support multiple deployment names (primary and secondary models)
- FR2.2: Must provide simple query interface with temperature and max_tokens parameters
- FR2.3: Must log all prompts and responses to PROMPT_LOG.md files
- FR2.4: Must handle API errors gracefully with informative error messages
- FR2.5: Must support both GPT-4o and Phi-4-mini-instruct models

### FR3 – Lab 1: Position Bias Testing
- FR3.1: Generate synthetic documents with facts at START/MIDDLE/END positions
- FR3.2: Support multiple trials with progressive difficulty (200w → 3500w)
- FR3.3: Add numerical distractors to increase task difficulty
- FR3.4: Test both GPT-4o and Phi-4-mini models on identical datasets
- FR3.5: Measure accuracy by position and overall
- FR3.6: Identify practical context window limits through systematic testing
- FR3.7: Generate analysis reports showing position-based accuracy curves

### FR4 – Lab 2: Context Size Impact Analysis
- FR4.1: Generate document sets of varying sizes (90w, 180w, 300w, 400w per document)
- FR4.2: Test multiple document counts (2, 5, 10, 20, 50 documents)
- FR4.3: Measure token count, latency, and accuracy for each context size
- FR4.4: Use tiktoken for accurate token counting
- FR4.5: Generate degradation curve showing accuracy vs. context size
- FR4.6: Identify safe, caution, and danger zones for production use
- FR4.7: Produce production guidelines based on empirical findings

### FR5 – Lab 3: RAG vs Full Context Comparison
- FR5.1: Generate domain-specific document corpus (health, law, technology)
- FR5.2: Create evaluation questions with ground truth answers
- FR5.3: Implement full context mode (concatenate all documents)
- FR5.4: Implement RAG mode using ChromaDB vector database
- FR5.5: Measure accuracy, latency, consistency (standard deviation), and token usage
- FR5.6: Generate comparative visualizations (latency, accuracy, token usage)
- FR5.7: Provide statistical validation and confidence intervals
- FR5.8: Produce "When to Use What" decision guidelines

### FR6 – Lab 4: Context Engineering Strategies
- FR6.1: Generate multi-step scenario with growing context (detective investigation)
- FR6.2: Implement SELECT strategy (RAG-based retrieval)
- FR6.3: Implement COMPRESS strategy (summarization)
- FR6.4: Implement WRITE strategy (external scratchpad with fact extraction)
- FR6.5: Measure accuracy, context tokens, and processing time per step
- FR6.6: Generate visualizations showing strategy performance over time
- FR6.7: Produce heatmap showing which strategy succeeds at which step
- FR6.8: Calculate cumulative success rates for each strategy

### FR7 – Data Generation
- FR7.1: All data generation must be reproducible with fixed random seeds
- FR7.2: Synthetic data must avoid repetition using shuffle-and-cycle algorithms
- FR7.3: Generated documents must be saved in JSON format
- FR7.4: Each lab must have separate data generation scripts
- FR7.5: Data must be stored in lab-specific `data/` subdirectories

### FR8 – Experiment Execution
- FR8.1: Each lab must have dedicated experiment runner script
- FR8.2: Experiments must save raw results in JSON format with timestamps
- FR8.3: Results must include metadata (model, timestamp, configuration)
- FR8.4: Experiments must handle API errors and retry when appropriate
- FR8.5: Progress must be logged to console during execution

### FR9 – Analysis & Visualization
- FR9.1: Each lab must generate statistical analysis reports
- FR9.2: Visualizations must be saved as PNG files
- FR9.3: Analysis must calculate summary statistics (mean, median, std dev)
- FR9.4: Charts must include proper labels, legends, and titles
- FR9.5: Reports must be saved as human-readable text files
- FR9.6: Analysis must highlight key findings and actionable insights

### FR10 – Testing
- FR10.1: Package must include installation verification tests
- FR10.2: Azure OpenAI helper must have comprehensive test coverage
- FR10.3: Tests must validate configuration loading
- FR10.4: Tests must validate multi-model support
- FR10.5: All tests must be executable via `pytest`

---

## 7. Non‑Functional Requirements

### NFR1: Scientific Reproducibility
- NFR1.1: All experiments must be reproducible with identical inputs
- NFR1.2: Random seeds must be fixed for deterministic data generation
- NFR1.3: Model temperature must be set to 0.0 for reproducible responses
- NFR1.4: All experiment parameters must be documented in results files

### NFR2: Code Quality
- NFR2.1: Code must follow PEP 8 style guidelines
- NFR2.2: Functions must have descriptive docstrings
- NFR2.3: Complex logic must include inline comments
- NFR2.4: No hardcoded credentials or API keys in source code

### NFR3: Performance
- NFR3.1: Data generation must complete in reasonable time (<5 minutes per lab)
- NFR3.2: Experiments should handle API rate limits gracefully
- NFR3.3: Large result files must be formatted efficiently (JSON with minimal whitespace)

### NFR4: Usability
- NFR4.1: Package must provide simple top-level functions (run_lab1, run_lab2, etc.)
- NFR4.2: Error messages must be clear and actionable
- NFR4.3: Console output must show progress for long-running experiments
- NFR4.4: README must provide step-by-step instructions for each lab

### NFR5: Maintainability
- NFR5.1: Each lab must be independent and runnable separately
- NFR5.2: Shared code must be in reusable modules (azure_openai_helper)
- NFR5.3: File structure must be consistent across all labs
- NFR5.4: Dependencies must be pinned in requirements.txt

### NFR6: Documentation
- NFR6.1: Main README must document all four labs comprehensively
- NFR6.2: Each lab must have detailed findings and conclusions
- NFR6.3: All prompts must be logged to PROMPT_LOG.md files
- NFR6.4: Production guidelines must be included based on empirical results

---

## 8. Key Research Questions

### Lab 1: Position Bias
- **RQ1.1**: Do modern LLMs exhibit "lost in the middle" phenomenon?
- **RQ1.2**: At what document length does position bias emerge?
- **RQ1.3**: Do smaller models show degradation where larger models succeed?
- **RQ1.4**: What are the practical context window limits for factual retrieval?

### Lab 2: Context Size Impact
- **RQ2.1**: How does individual document size affect accuracy?
- **RQ2.2**: Is total token count or individual chunk size the limiting factor?
- **RQ2.3**: What are the safe/caution/danger zones for production systems?
- **RQ2.4**: How does latency scale with context size?

### Lab 3: RAG vs Full Context
- **RQ3.1**: Does RAG provide equal or better accuracy than full context?
- **RQ3.2**: How much faster is RAG compared to full context?
- **RQ3.3**: How do token costs compare between approaches?
- **RQ3.4**: Which approach has better performance consistency?

### Lab 4: Context Engineering
- **RQ4.1**: Which strategy best handles growing context in multi-step tasks?
- **RQ4.2**: How does accuracy degrade over time for each strategy?
- **RQ4.3**: What are the trade-offs between SELECT, COMPRESS, and WRITE?
- **RQ4.4**: Which strategy is most suitable for different use cases?

---

## 9. Success Metrics

### Lab 1 Metrics
- Position-based accuracy (START, MIDDLE, END)
- Overall accuracy across all documents
- Context window breaking points identified
- Multi-model comparison completed

### Lab 2 Metrics
- Accuracy at different document sizes (90w, 180w, 300w, 400w)
- Latency measurements across context sizes
- Token count tracking
- Production guidelines defined

### Lab 3 Metrics
- Accuracy comparison (RAG vs Full Context)
- Latency comparison (mean, max, standard deviation)
- Token usage comparison
- Cost-benefit analysis

### Lab 4 Metrics
- Per-strategy accuracy across 10 steps
- Context token growth tracking
- Processing time per strategy
- Cumulative success rates

---

## 10. Technical Dependencies

### Core Dependencies
- Python 3.9 or higher
- openai >= 1.0.0 (Azure OpenAI SDK)
- python-dotenv (environment configuration)
- tiktoken (token counting)

### Experiment Dependencies
- chromadb (vector database for Lab 3)
- pandas (data analysis)
- matplotlib (visualization)
- seaborn (enhanced visualization)

### Development Dependencies
- pytest (testing framework)
- black (code formatting)
- flake8 (linting)
- mypy (type checking)

### External Services
- Azure OpenAI Service with GPT-4o deployment
- Azure AI Foundry with Phi-4-mini-instruct deployment

---

## 11. Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Azure OpenAI rate limits | Experiment failure | Implement retry logic, add sleep between calls |
| API cost overruns | Budget issues | Use smaller models (Phi-4-mini) for development testing |
| Non-reproducible results | Scientific validity | Fix random seeds, use temperature=0.0, document all parameters |
| Model availability changes | Deployment breakage | Support multiple models, make deployment names configurable |
| Large result files | Storage issues | Use efficient JSON formatting, implement result compression |
| Long experiment runtime | User frustration | Show progress indicators, allow partial result saving |
| Embedding API failures | Lab 3/4 failures | Implement fallback to keyword-based retrieval |
| Token counting inaccuracies | Cost miscalculation | Use official tiktoken library matching OpenAI |

---

## 12. Acceptance Criteria

### Package-Level Acceptance
- ✔ Package installable via `pip install -e .`
- ✔ Package installable from Git repository URL
- ✔ Configuration validation function works correctly
- ✔ All tests pass with pytest
- ✔ Package exports run_lab1, run_lab2, run_lab3, run_lab4 functions

### Lab 1 Acceptance
- ✔ Five progressive trials completed (200w → 3500w)
- ✔ Both GPT-4o and Phi-4-mini tested
- ✔ Position-based accuracy calculated for START/MIDDLE/END
- ✔ Context window limits empirically identified (3500w safe, 5000w fails)
- ✔ "Lost in the middle" hypothesis tested and conclusion documented
- ✔ Multi-model comparison framework validated

### Lab 2 Acceptance
- ✔ Four trials completed with different document sizes (90w, 180w, 300w, 400w)
- ✔ Degradation curve showing accuracy vs. document size
- ✔ Key finding documented: individual chunk size matters more than total tokens
- ✔ Production guidelines defined (safe: ≤200w, caution: 250-300w, danger: 300-400w)
- ✔ Token counting validated using tiktoken

### Lab 3 Acceptance
- ✔ 20-document corpus generated across 3 domains
- ✔ 15 evaluation questions with ground truth answers
- ✔ Both RAG and Full Context modes implemented and tested
- ✔ RAG shows 3.3x faster latency, equal accuracy, 4x better consistency
- ✔ Statistical validation with confidence intervals
- ✔ Five visualization plots generated
- ✔ "When to Use What" decision guidelines provided

### Lab 4 Acceptance
- ✔ 10-step detective scenario generated
- ✔ SELECT, COMPRESS, and WRITE strategies implemented
- ✔ All strategies tested across all 10 steps
- ✔ COMPRESS achieves 100% accuracy in experiment
- ✔ Accuracy heatmap shows strategy performance patterns
- ✔ Cumulative success rates calculated
- ✔ Strategy recommendations documented

### Documentation Acceptance
- ✔ Main README documents all four labs comprehensively
- ✔ Each lab includes: objective, methodology, results, conclusions
- ✔ Installation instructions are clear and complete
- ✔ Quick start examples work as documented
- ✔ All prompts logged to PROMPT_LOG.md files
- ✔ Production recommendations based on empirical findings

---

## 13. Out-of-Scope Future Enhancements

While not part of the initial release, these enhancements may be considered for future versions:

### Additional Labs
- Lab 5: Multi-document reasoning and synthesis
- Lab 6: Adversarial context injection testing
- Lab 7: Cross-lingual context window behavior
- Lab 8: Structured data extraction at scale

### Technical Enhancements
- Support for OpenAI API (non-Azure)
- Support for Anthropic Claude models
- Parallel experiment execution
- Real-time experiment monitoring dashboard
- Automated result comparison across runs
- Docker containerization for reproducibility

### Analysis Improvements
- Advanced statistical tests (t-tests, ANOVA)
- Confidence intervals on all metrics
- Cost optimization recommendations
- Automated report generation in multiple formats (PDF, HTML)

---

## 14. Success Criteria Summary

The Context Window Labs project will be considered successful when:

1. **Scientific Rigor**: All four labs produce reproducible, statistically valid results that answer their respective research questions
2. **Usability**: Any researcher or developer can install the package and run all experiments following README instructions
3. **Impact**: Results provide actionable insights for production LLM system design (chunk sizes, retrieval strategies, context management)
4. **Quality**: Code is well-documented, tested, and maintainable
5. **Completeness**: All labs include data generation, experimentation, analysis, and visualization
6. **Documentation**: README comprehensively documents findings, methodology, and practical implications

---

This PRD defines **what** the Context Window Labs system must achieve across its four experimental modules.  
The README explains **how** to install, run, and interpret each experiment.  
Together, they provide a complete specification and documentation set for the project.

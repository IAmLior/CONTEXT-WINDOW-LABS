"""
Context management strategies: SELECT, COMPRESS, and WRITE.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from azure_openai_helper import llm_query, get_client
import tiktoken
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class ContextStrategy:
    """Base class for context management strategies."""
    
    def __init__(self, model_name="gpt-4o-mini"):
        self.model_name = model_name
        self.encoding = tiktoken.encoding_for_model("gpt-4")
        
    def count_tokens(self, text):
        """Count tokens in text."""
        return len(self.encoding.encode(text))
    
    def process_history(self, history, query):
        """
        Process history and prepare context for answering query.
        Must be implemented by subclasses.
        
        Args:
            history: List of step dictionaries
            query: Question to answer
            
        Returns:
            Prepared context string
        """
        raise NotImplementedError
    
    def answer_question(self, history, query):
        """
        Answer a question given the history.
        
        Args:
            history: List of step dictionaries
            query: Question to answer
            
        Returns:
            dict with answer, token_count, and context_used
        """
        context = self.process_history(history, query)
        
        prompt = f"""Based on the following information, answer the question concisely and accurately.

Context:
{context}

Question: {query}

Answer (be brief and specific):"""
        
        # Use llm_query for simplicity
        answer = llm_query(
            prompt=prompt,
            temperature=0,
            max_tokens=150
        )
        
        tokens_used = self.count_tokens(context)
        
        return {
            "answer": answer,
            "context_tokens": tokens_used,
            "context_preview": context[:200] + "..." if len(context) > 200 else context
        }


class SelectStrategy(ContextStrategy):
    """
    SELECT Strategy: Use keyword-based retrieval to get only relevant parts of history.
    Note: This is a simplified version that uses keyword matching instead of embeddings.
    """
    
    def __init__(self, model_name="gpt-4o-mini", top_k=3):
        super().__init__(model_name)
        self.top_k = top_k
        
    def calculate_relevance(self, text, query):
        """Calculate relevance score based on keyword overlap."""
        # Simple keyword-based relevance scoring
        text_lower = text.lower()
        query_words = query.lower().split()
        
        # Count how many query words appear in text
        score = sum(1 for word in query_words if len(word) > 3 and word in text_lower)
        
        # Boost score for exact phrases
        if query.lower() in text_lower:
            score += 5
        
        return score
    
    def process_history(self, history, query):
        """
        Retrieve top-k most relevant history items using keyword matching.
        """
        if not history:
            return ""
        
        # Create chunks from history with relevance scores
        chunks_with_scores = []
        for step_data in history:
            chunk = f"Step {step_data['step']}: {step_data['action']}\n{step_data['observations']}\nTime: {step_data['time']}"
            score = self.calculate_relevance(chunk, query)
            chunks_with_scores.append((chunk, score))
        
        # Sort by relevance score and take top-k
        chunks_with_scores.sort(key=lambda x: x[1], reverse=True)
        relevant_chunks = [chunk for chunk, score in chunks_with_scores[:self.top_k]]
        
        return "\n\n".join(relevant_chunks)


class CompressStrategy(ContextStrategy):
    """
    COMPRESS Strategy: Summarize history when it exceeds token threshold.
    """
    
    def __init__(self, model_name="gpt-4o-mini", max_tokens=2000):
        super().__init__(model_name)
        self.max_tokens = max_tokens
        self.compressed_history = None
        self.last_summarized_step = 0
        
    def process_history(self, history, query):
        """
        Compress history if it exceeds max_tokens, otherwise use full history.
        """
        if not history:
            return ""
        
        # Build full history text
        full_history = []
        for step_data in history:
            full_history.append(
                f"Step {step_data['step']}: {step_data['action']}\n"
                f"{step_data['observations']}\n"
                f"Time: {step_data['time']}"
            )
        
        history_text = "\n\n".join(full_history)
        token_count = self.count_tokens(history_text)
        
        # If under threshold, return as is
        if token_count <= self.max_tokens:
            return history_text
        
        # Need to compress - check if we need a new summary
        current_step = history[-1]['step']
        
        if self.compressed_history is None or current_step > self.last_summarized_step:
            # Generate new summary
            summary_prompt = f"""Summarize the following investigation steps concisely, preserving all key facts, names, times, locations, and evidence. Be specific and retain important details.

Investigation Steps:
{history_text}

Summary:"""
            
            self.compressed_history = llm_query(
                prompt=summary_prompt,
                temperature=0,
                max_tokens=800
            )
            self.last_summarized_step = current_step
        
        return self.compressed_history


class WriteStrategy(ContextStrategy):
    """
    WRITE Strategy: Extract key facts into external scratchpad and retrieve from there.
    Note: This is a simplified version that uses keyword matching instead of embeddings.
    """
    
    def __init__(self, model_name="gpt-4o-mini"):
        super().__init__(model_name)
        self.scratchpad = []  # List of extracted facts
        self.processed_steps = set()
        
    def extract_key_facts(self, step_data):
        """
        Extract key facts from a single step using LLM.
        """
        step_text = f"""Step {step_data['step']}: {step_data['action']}
{step_data['observations']}
Time: {step_data['time']}"""
        
        extract_prompt = f"""Extract key facts from this investigation step. List each fact as a separate bullet point. Include names, times, locations, actions, and evidence.

Step:
{step_text}

Key Facts (one per line, be specific):"""
        
        facts_text = llm_query(
            prompt=extract_prompt,
            temperature=0,
            max_tokens=300
        )
        
        # Parse facts (each line is a fact)
        facts = [line.strip() for line in facts_text.split('\n') if line.strip() and (line.strip().startswith('-') or line.strip().startswith('•') or line.strip()[0].isdigit())]
        
        return facts
    
    def calculate_relevance(self, fact, query):
        """Calculate relevance score based on keyword overlap."""
        fact_lower = fact.lower()
        query_words = query.lower().split()
        
        # Count how many query words appear in fact
        score = sum(1 for word in query_words if len(word) > 3 and word in fact_lower)
        
        # Boost score for exact phrases
        if query.lower() in fact_lower:
            score += 5
        
        return score
    
    def process_history(self, history, query):
        """
        Extract facts from new steps and retrieve relevant facts for the query.
        """
        if not history:
            return ""
        
        # Process any new steps
        for step_data in history:
            step_num = step_data['step']
            if step_num not in self.processed_steps:
                facts = self.extract_key_facts(step_data)
                self.scratchpad.extend(facts)
                self.processed_steps.add(step_num)
        
        # Now retrieve relevant facts for the query using keyword matching
        if not self.scratchpad:
            return ""
        
        # Score all facts
        facts_with_scores = [(fact, self.calculate_relevance(fact, query)) for fact in self.scratchpad]
        
        # Sort by relevance and take top 10
        facts_with_scores.sort(key=lambda x: x[1], reverse=True)
        top_k = min(10, len(self.scratchpad))
        relevant_facts = [fact for fact, score in facts_with_scores[:top_k]]
        
        return "Key Facts:\n" + "\n".join(relevant_facts)


def create_strategy(strategy_name, model_name="gpt-4o-mini", **kwargs):
    """
    Factory function to create strategy instances.
    
    Args:
        strategy_name: "select", "compress", or "write"
        model_name: LLM model to use
        **kwargs: Additional strategy-specific parameters
        
    Returns:
        Strategy instance
    """
    strategies = {
        "select": SelectStrategy,
        "compress": CompressStrategy,
        "write": WriteStrategy
    }
    
    if strategy_name.lower() not in strategies:
        raise ValueError(f"Unknown strategy: {strategy_name}. Choose from {list(strategies.keys())}")
    
    return strategies[strategy_name.lower()](model_name=model_name, **kwargs)

"""
Lab 3: RAG vs Full Context Experiment

This module compares two approaches for question answering:
1. Full Context: Use all documents concatenated as context
2. RAG: Retrieve only relevant chunks using vector similarity search

Measures: accuracy and latency for both approaches.
"""

import json
import os
import sys
import time
from typing import List, Dict, Any, Tuple
import tiktoken
from dotenv import load_dotenv
from openai import AzureOpenAI

# Add parent directory to path to import azure_openai_helper
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from azure_openai_helper.llm_client import llm_query

try:
    import chromadb
    from chromadb.config import Settings
except ImportError:
    print("ChromaDB not installed. Please run: pip install chromadb")
    sys.exit(1)

# Load environment variables
load_dotenv()


class DocumentChunker:
    """Utility for splitting documents into fixed-size chunks."""
    
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        """
        Initialize chunker.
        
        Args:
            chunk_size: Target size of each chunk in tokens
            overlap: Number of tokens to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def chunk_text(self, text: str, doc_id: str = None) -> List[Dict[str, Any]]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Text to chunk
            doc_id: Optional document identifier
            
        Returns:
            List of chunk dictionaries with text and metadata
        """
        tokens = self.encoding.encode(text)
        chunks = []
        
        start = 0
        chunk_idx = 0
        
        while start < len(tokens):
            end = start + self.chunk_size
            chunk_tokens = tokens[start:end]
            chunk_text = self.encoding.decode(chunk_tokens)
            
            chunks.append({
                "text": chunk_text,
                "chunk_id": f"{doc_id}_chunk_{chunk_idx}" if doc_id else f"chunk_{chunk_idx}",
                "doc_id": doc_id,
                "chunk_index": chunk_idx,
                "token_count": len(chunk_tokens)
            })
            
            chunk_idx += 1
            start += (self.chunk_size - self.overlap)
        
        return chunks
    
    def chunk_documents(self, documents: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """
        Chunk multiple documents.
        
        Args:
            documents: List of document dictionaries with 'id' and 'content'
            
        Returns:
            List of all chunks from all documents
        """
        all_chunks = []
        
        for doc in documents:
            doc_id = doc.get("id", "unknown")
            content = doc.get("content", "")
            title = doc.get("title", "")
            category = doc.get("category", "")
            
            # Include title in content for better context
            full_text = f"{title}\n\n{content}" if title else content
            
            chunks = self.chunk_text(full_text, doc_id)
            
            # Add document metadata to each chunk
            for chunk in chunks:
                chunk["title"] = title
                chunk["category"] = category
            
            all_chunks.extend(chunks)
        
        return all_chunks


class RAGSystem:
    """RAG system using ChromaDB for vector storage and retrieval."""
    
    def __init__(self, collection_name: str = "lab3_docs"):
        """
        Initialize RAG system.
        
        Args:
            collection_name: Name for the ChromaDB collection
        """
        self.collection_name = collection_name
        
        # Initialize ChromaDB with default embedding function (sentence-transformers)
        self.chroma_client = chromadb.Client(Settings(
            anonymized_telemetry=False,
            allow_reset=True
        ))
        
        # Reset collection if it exists
        try:
            self.chroma_client.delete_collection(name=collection_name)
        except:
            pass
        
        # Create collection - ChromaDB will use default embedding function
        self.collection = self.chroma_client.create_collection(
            name=collection_name,
            metadata={"description": "Lab 3 document chunks"}
        )
        
        self.chunks = []
        print("✓ Using ChromaDB's default embedding function (sentence-transformers)")
    
    def add_documents(self, chunks: List[Dict[str, Any]]) -> None:
        """
        Add document chunks to vector store.
        
        Args:
            chunks: List of chunk dictionaries
        """
        print(f"Embedding and storing {len(chunks)} chunks...")
        
        self.chunks = chunks
        
        # Process in batches
        batch_size = 10
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i+batch_size]
            
            # Prepare data for ChromaDB
            texts = [chunk["text"] for chunk in batch]
            
            # Prepare metadata
            metadatas = [
                {
                    "chunk_id": chunk["chunk_id"],
                    "doc_id": chunk["doc_id"],
                    "title": chunk.get("title", ""),
                    "category": chunk.get("category", ""),
                    "chunk_index": str(chunk["chunk_index"]),
                    "token_count": str(chunk["token_count"])
                }
                for chunk in batch
            ]
            
            # Add to collection - ChromaDB will automatically generate embeddings
            self.collection.add(
                documents=texts,
                metadatas=metadatas,
                ids=[chunk["chunk_id"] for chunk in batch]
            )
            
            print(f"  Processed {min(i+batch_size, len(chunks))}/{len(chunks)} chunks")
        
        print(f"✓ Added {len(chunks)} chunks to vector store")
    
    def similarity_search(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieve top-k most relevant chunks for a query.
        
        Args:
            query: Search query
            k: Number of chunks to retrieve
            
        Returns:
            List of relevant chunks with metadata
        """
        # Search using query text - ChromaDB will embed it automatically
        results = self.collection.query(
            query_texts=[query],
            n_results=k
        )
        
        # Format results
        retrieved_chunks = []
        for i in range(len(results["ids"][0])):
            retrieved_chunks.append({
                "chunk_id": results["ids"][0][i],
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i] if "distances" in results else None
            })
        
        return retrieved_chunks
    
    def query_with_rag(self, query: str, k: int = 3) -> Tuple[str, float, List[Dict]]:
        """
        Answer query using RAG approach.
        
        Args:
            query: Question to answer
            k: Number of chunks to retrieve
            
        Returns:
            Tuple of (answer, latency, retrieved_chunks)
        """
        start_time = time.time()
        
        # Retrieve relevant chunks
        retrieved_chunks = self.similarity_search(query, k=k)
        
        # Build context from retrieved chunks
        context_parts = []
        for i, chunk in enumerate(retrieved_chunks, 1):
            context_parts.append(f"[Document {i}]\n{chunk['text']}")
        
        context = "\n\n".join(context_parts)
        
        # Build prompt
        prompt = f"""Answer the following question based ONLY on the provided context. Be concise and specific.

Context:
{context}

Question: {query}

Answer:"""
        
        # Query LLM using function-based API
        response = llm_query(
            prompt=prompt,
            temperature=0.0,
            max_tokens=200
        )
        
        latency = time.time() - start_time
        
        return response, latency, retrieved_chunks


class FullContextSystem:
    """System for querying with full document context."""
    
    def __init__(self):
        """Initialize full context system."""
        self.full_context = ""
    
    def set_documents(self, documents: List[Dict[str, str]]) -> None:
        """
        Concatenate all documents into full context.
        
        Args:
            documents: List of document dictionaries
        """
        context_parts = []
        for doc in documents:
            title = doc.get("title", "")
            content = doc.get("content", "")
            doc_text = f"[{title}]\n{content}" if title else content
            context_parts.append(doc_text)
        
        self.full_context = "\n\n".join(context_parts)
        
        encoding = tiktoken.get_encoding("cl100k_base")
        token_count = len(encoding.encode(self.full_context))
        print(f"✓ Full context prepared: {token_count} tokens")
    
    def query_with_full_context(self, query: str) -> Tuple[str, float]:
        """
        Answer query using all documents as context.
        
        Args:
            query: Question to answer
            
        Returns:
            Tuple of (answer, latency)
        """
        start_time = time.time()
        
        # Build prompt with full context
        prompt = f"""Answer the following question based on the provided documents. Be concise and specific.

Documents:
{self.full_context}

Question: {query}

Answer:"""
        
        # Query LLM using function-based API
        response = llm_query(
            prompt=prompt,
            temperature=0.0,
            max_tokens=200
        )
        
        latency = time.time() - start_time
        
        return response, latency


def evaluate_answer(answer: str, expected: str) -> bool:
    """
    Simple evaluation: check if expected answer is in the response.
    
    Args:
        answer: Model's answer
        expected: Expected answer text
        
    Returns:
        True if answer contains expected text (case-insensitive)
    """
    return expected.lower() in answer.lower()


def compare_modes(
    query: str,
    expected_answer: str,
    rag_system: RAGSystem,
    full_context_system: FullContextSystem,
    k: int = 3
) -> Dict[str, Any]:
    """
    Compare RAG and Full Context modes for a single query.
    
    Args:
        query: Question to ask
        expected_answer: Expected answer for evaluation
        rag_system: RAG system instance
        full_context_system: Full context system instance
        k: Number of chunks to retrieve for RAG
        
    Returns:
        Dictionary with comparison results
    """
    print(f"\nQuery: {query}")
    
    # RAG mode
    print("  Running RAG mode...")
    rag_answer, rag_latency, retrieved_chunks = rag_system.query_with_rag(query, k=k)
    rag_correct = evaluate_answer(rag_answer, expected_answer)
    
    print(f"    Latency: {rag_latency:.2f}s")
    print(f"    Correct: {rag_correct}")
    print(f"    Answer: {rag_answer[:100]}...")
    
    # Full Context mode
    print("  Running Full Context mode...")
    full_answer, full_latency = full_context_system.query_with_full_context(query)
    full_correct = evaluate_answer(full_answer, expected_answer)
    
    print(f"    Latency: {full_latency:.2f}s")
    print(f"    Correct: {full_correct}")
    print(f"    Answer: {full_answer[:100]}...")
    
    return {
        "query": query,
        "expected_answer": expected_answer,
        "rag_answer": rag_answer,
        "rag_latency": rag_latency,
        "rag_correct": rag_correct,
        "rag_retrieved_chunks": [
            {
                "chunk_id": chunk["chunk_id"],
                "doc_id": chunk["metadata"]["doc_id"],
                "title": chunk["metadata"]["title"]
            }
            for chunk in retrieved_chunks
        ],
        "full_answer": full_answer,
        "full_latency": full_latency,
        "full_correct": full_correct
    }


def run_experiment():
    """Main experiment runner."""
    print("=" * 80)
    print("Lab 3: RAG vs Full Context Experiment")
    print("=" * 80)
    
    # Load documents and questions
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    docs_path = os.path.join(data_dir, "documents.json")
    questions_path = os.path.join(data_dir, "questions.json")
    
    if not os.path.exists(docs_path):
        print(f"\nError: {docs_path} not found.")
        print("Run generate_documents.py first to create the dataset.")
        return
    
    with open(docs_path, 'r', encoding='utf-8') as f:
        docs_data = json.load(f)
    
    with open(questions_path, 'r', encoding='utf-8') as f:
        questions_data = json.load(f)
    
    documents = docs_data["documents"]
    questions = questions_data["questions"]
    
    print(f"\n✓ Loaded {len(documents)} documents")
    print(f"✓ Loaded {len(questions)} evaluation questions")
    
    # Setup chunking
    print("\n" + "-" * 80)
    print("Chunking documents...")
    chunker = DocumentChunker(chunk_size=500, overlap=50)
    chunks = chunker.chunk_documents(documents)
    print(f"✓ Created {len(chunks)} chunks from {len(documents)} documents")
    
    # Setup RAG system
    print("\n" + "-" * 80)
    print("Setting up RAG system...")
    rag_system = RAGSystem()
    rag_system.add_documents(chunks)
    
    # Setup Full Context system
    print("\n" + "-" * 80)
    print("Setting up Full Context system...")
    full_context_system = FullContextSystem()
    full_context_system.set_documents(documents)
    
    # Run comparisons
    print("\n" + "=" * 80)
    print("Running Comparisons")
    print("=" * 80)
    
    results = []
    for i, question in enumerate(questions, 1):
        print(f"\n[{i}/{len(questions)}]")
        
        result = compare_modes(
            query=question["question"],
            expected_answer=question["expected_answer"],
            rag_system=rag_system,
            full_context_system=full_context_system,
            k=3
        )
        
        result["question_id"] = question["id"]
        result["relevant_doc"] = question["relevant_doc"]
        results.append(result)
    
    # Save results
    results_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(results_dir, exist_ok=True)
    
    output = {
        "metadata": {
            "total_questions": len(questions),
            "total_documents": len(documents),
            "total_chunks": len(chunks),
            "chunk_size": 500,
            "overlap": 50,
            "retrieval_k": 3
        },
        "results": results
    }
    
    output_path = os.path.join(results_dir, "experiment_results.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 80)
    print(f"✓ Experiment complete!")
    print(f"✓ Results saved to {output_path}")
    print("=" * 80)
    
    # Print summary
    rag_correct = sum(1 for r in results if r["rag_correct"])
    full_correct = sum(1 for r in results if r["full_correct"])
    avg_rag_latency = sum(r["rag_latency"] for r in results) / len(results)
    avg_full_latency = sum(r["full_latency"] for r in results) / len(results)
    
    print("\nSummary:")
    print(f"  RAG Accuracy:          {rag_correct}/{len(results)} ({rag_correct/len(results)*100:.1f}%)")
    print(f"  Full Context Accuracy: {full_correct}/{len(results)} ({full_correct/len(results)*100:.1f}%)")
    print(f"  RAG Avg Latency:       {avg_rag_latency:.2f}s")
    print(f"  Full Context Latency:  {avg_full_latency:.2f}s")
    print(f"  Latency Improvement:   {(1 - avg_rag_latency/avg_full_latency)*100:.1f}%")


if __name__ == "__main__":
    run_experiment()

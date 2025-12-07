"""
Generate mixed-topic documents for Lab 3: RAG vs Full Context experiment.

This script creates a small corpus of ~20 documents covering different domains:
- Health & Medicine
- Law & Legal
- Technology & Computing

Each document contains factual information that can be queried with specific questions.
"""

import json
from typing import List, Dict

def generate_health_documents() -> List[Dict[str, str]]:
    """Generate health and medicine related documents."""
    return [
        {
            "id": "health_001",
            "title": "Vitamin D Benefits",
            "content": "Vitamin D is essential for bone health and immune function. The recommended daily intake for adults is 600-800 IU. Vitamin D deficiency can lead to osteoporosis and weakened immunity. Main sources include sunlight exposure, fatty fish like salmon, and fortified dairy products.",
            "category": "health"
        },
        {
            "id": "health_002",
            "title": "Sleep and Health",
            "content": "Adults need 7-9 hours of sleep per night for optimal health. Sleep deprivation can lead to increased risk of heart disease, diabetes, and obesity. During sleep, the body repairs tissues and consolidates memories. The sleep hormone melatonin is produced in the pineal gland.",
            "category": "health"
        },
        {
            "id": "health_003",
            "title": "Cardiovascular Exercise",
            "content": "The American Heart Association recommends at least 150 minutes of moderate-intensity aerobic exercise per week. Cardiovascular exercise strengthens the heart, improves circulation, and reduces blood pressure. Activities include brisk walking, cycling, swimming, and jogging.",
            "category": "health"
        },
        {
            "id": "health_004",
            "title": "Diabetes Management",
            "content": "Type 2 diabetes affects how the body processes blood sugar. Management includes monitoring blood glucose levels, maintaining a healthy diet, regular exercise, and sometimes medication. The target fasting blood sugar level is typically 80-130 mg/dL. Hemoglobin A1C should be below 7% for most patients.",
            "category": "health"
        },
        {
            "id": "health_005",
            "title": "Nutrition and Fiber",
            "content": "Dietary fiber is crucial for digestive health. Adults should consume 25-30 grams of fiber daily. High-fiber foods include whole grains, legumes, fruits, and vegetables. Fiber helps regulate blood sugar, lowers cholesterol, and promotes healthy gut bacteria.",
            "category": "health"
        },
    ]

def generate_law_documents() -> List[Dict[str, str]]:
    """Generate law and legal related documents."""
    return [
        {
            "id": "law_001",
            "title": "Contract Formation",
            "content": "A valid contract requires three essential elements: offer, acceptance, and consideration. The offer must be definite and communicated to the offeree. Acceptance must be unequivocal and mirror the terms of the offer. Consideration is something of value exchanged between parties.",
            "category": "law"
        },
        {
            "id": "law_002",
            "title": "Intellectual Property",
            "content": "Copyright protection lasts for the author's lifetime plus 70 years. Patents protect inventions for 20 years from the filing date. Trademarks can be renewed indefinitely every 10 years. Trade secrets have no expiration but require reasonable efforts to maintain secrecy.",
            "category": "law"
        },
        {
            "id": "law_003",
            "title": "Employment Law Basics",
            "content": "The Fair Labor Standards Act (FLSA) establishes minimum wage, overtime pay, and child labor standards. Non-exempt employees must receive overtime pay at 1.5 times their regular rate for hours worked over 40 per week. The federal minimum wage is currently $7.25 per hour.",
            "category": "law"
        },
        {
            "id": "law_004",
            "title": "Tort Law - Negligence",
            "content": "To prove negligence, a plaintiff must establish four elements: duty of care, breach of duty, causation, and damages. The reasonable person standard determines if a duty was breached. Proximate cause requires that damages were a foreseeable result of the breach.",
            "category": "law"
        },
        {
            "id": "law_005",
            "title": "Criminal Burden of Proof",
            "content": "In criminal cases, the prosecution must prove guilt beyond a reasonable doubt. This is the highest burden of proof in the legal system. In civil cases, the standard is preponderance of the evidence, meaning more likely than not. Administrative proceedings often use the clear and convincing evidence standard.",
            "category": "law"
        },
        {
            "id": "law_006",
            "title": "Real Estate Transactions",
            "content": "A deed transfers ownership of real property and must be in writing per the Statute of Frauds. Title insurance protects buyers against defects in title. Closing costs typically range from 2-5% of the purchase price. The escrow period usually lasts 30-60 days.",
            "category": "law"
        },
    ]

def generate_technology_documents() -> List[Dict[str, str]]:
    """Generate technology and computing related documents."""
    return [
        {
            "id": "tech_001",
            "title": "REST API Design",
            "content": "REST APIs use HTTP methods: GET for retrieval, POST for creation, PUT for updates, and DELETE for removal. Status codes indicate results: 200 for success, 404 for not found, 500 for server errors. RESTful APIs are stateless and use standard HTTP protocols.",
            "category": "technology"
        },
        {
            "id": "tech_002",
            "title": "Database Normalization",
            "content": "First Normal Form (1NF) requires atomic values and unique rows. Second Normal Form (2NF) eliminates partial dependencies. Third Normal Form (3NF) removes transitive dependencies. Normalization reduces data redundancy and improves data integrity.",
            "category": "technology"
        },
        {
            "id": "tech_003",
            "title": "Cryptography Basics",
            "content": "AES-256 is a symmetric encryption algorithm using 256-bit keys. RSA is an asymmetric algorithm commonly using 2048 or 4096-bit keys. Hash functions like SHA-256 produce fixed-size outputs and are one-way. TLS 1.3 is the current secure communication protocol standard.",
            "category": "technology"
        },
        {
            "id": "tech_004",
            "title": "Machine Learning Fundamentals",
            "content": "Supervised learning uses labeled training data to predict outcomes. Unsupervised learning finds patterns in unlabeled data. Common algorithms include linear regression, decision trees, and neural networks. The training set is typically 70-80% of the data, with the rest for testing.",
            "category": "technology"
        },
        {
            "id": "tech_005",
            "title": "Cloud Computing Models",
            "content": "IaaS provides virtualized computing resources over the internet. PaaS offers a platform for developing and deploying applications. SaaS delivers software applications over the internet. Major cloud providers include AWS, Azure, and Google Cloud Platform.",
            "category": "technology"
        },
        {
            "id": "tech_006",
            "title": "Agile Methodology",
            "content": "Scrum is an agile framework with 2-4 week sprints. Sprint planning defines the work for the upcoming sprint. Daily standups are 15-minute sync meetings. Sprint retrospectives identify process improvements. The Product Owner prioritizes the backlog.",
            "category": "technology"
        },
        {
            "id": "tech_007",
            "title": "Network Protocols",
            "content": "TCP provides reliable, ordered delivery of data packets. UDP is faster but doesn't guarantee delivery. IP addresses identify devices on a network. IPv4 uses 32-bit addresses while IPv6 uses 128-bit addresses. DNS translates domain names to IP addresses.",
            "category": "technology"
        },
        {
            "id": "tech_008",
            "title": "Version Control with Git",
            "content": "Git is a distributed version control system. Branches allow parallel development. Commits are snapshots of the repository at a point in time. Merging combines changes from different branches. Pull requests facilitate code review before merging.",
            "category": "technology"
        },
        {
            "id": "tech_009",
            "title": "Container Orchestration",
            "content": "Kubernetes orchestrates containerized applications across clusters. Pods are the smallest deployable units containing one or more containers. Services provide stable networking for pods. Deployments manage replicated pods. The default namespace is used unless specified otherwise.",
            "category": "technology"
        },
    ]

def generate_all_documents() -> List[Dict[str, str]]:
    """Generate all documents across all categories."""
    all_docs = []
    all_docs.extend(generate_health_documents())
    all_docs.extend(generate_law_documents())
    all_docs.extend(generate_technology_documents())
    return all_docs

def generate_evaluation_questions() -> List[Dict[str, str]]:
    """
    Generate evaluation questions with expected answers.
    Each question should have a clear factual answer present in the documents.
    """
    return [
        {
            "id": "q001",
            "question": "What is the recommended daily intake of Vitamin D for adults?",
            "expected_answer": "600-800 IU",
            "relevant_doc": "health_001"
        },
        {
            "id": "q002",
            "question": "How many hours of sleep do adults need per night?",
            "expected_answer": "7-9 hours",
            "relevant_doc": "health_002"
        },
        {
            "id": "q003",
            "question": "What are the three essential elements required for a valid contract?",
            "expected_answer": "offer, acceptance, and consideration",
            "relevant_doc": "law_001"
        },
        {
            "id": "q004",
            "question": "How long does copyright protection last?",
            "expected_answer": "lifetime plus 70 years",
            "relevant_doc": "law_002"
        },
        {
            "id": "q005",
            "question": "What is the federal minimum wage in the United States?",
            "expected_answer": "$7.25 per hour",
            "relevant_doc": "law_003"
        },
        {
            "id": "q006",
            "question": "What HTTP method is used for retrieving data in REST APIs?",
            "expected_answer": "GET",
            "relevant_doc": "tech_001"
        },
        {
            "id": "q007",
            "question": "What are the three normal forms in database normalization?",
            "expected_answer": "1NF, 2NF, 3NF",
            "relevant_doc": "tech_002"
        },
        {
            "id": "q008",
            "question": "What is the current standard for secure communication protocols?",
            "expected_answer": "TLS 1.3",
            "relevant_doc": "tech_003"
        },
        {
            "id": "q009",
            "question": "How many minutes per week of moderate-intensity aerobic exercise does the American Heart Association recommend?",
            "expected_answer": "150 minutes",
            "relevant_doc": "health_003"
        },
        {
            "id": "q010",
            "question": "What is the target Hemoglobin A1C level for most diabetes patients?",
            "expected_answer": "below 7%",
            "relevant_doc": "health_004"
        },
        {
            "id": "q011",
            "question": "What is the highest burden of proof in the legal system?",
            "expected_answer": "beyond a reasonable doubt",
            "relevant_doc": "law_005"
        },
        {
            "id": "q012",
            "question": "What are the three major cloud providers mentioned?",
            "expected_answer": "AWS, Azure, and Google Cloud Platform",
            "relevant_doc": "tech_005"
        },
        {
            "id": "q013",
            "question": "How long is a typical Scrum sprint?",
            "expected_answer": "2-4 weeks",
            "relevant_doc": "tech_006"
        },
        {
            "id": "q014",
            "question": "What is the smallest deployable unit in Kubernetes?",
            "expected_answer": "Pod",
            "relevant_doc": "tech_009"
        },
        {
            "id": "q015",
            "question": "How many grams of fiber should adults consume daily?",
            "expected_answer": "25-30 grams",
            "relevant_doc": "health_005"
        },
    ]

def save_documents(filename: str = "documents.json"):
    """Save generated documents to a JSON file."""
    documents = generate_all_documents()
    
    output = {
        "metadata": {
            "total_documents": len(documents),
            "categories": {
                "health": len([d for d in documents if d["category"] == "health"]),
                "law": len([d for d in documents if d["category"] == "law"]),
                "technology": len([d for d in documents if d["category"] == "technology"])
            }
        },
        "documents": documents
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Generated {len(documents)} documents")
    print(f"  - Health: {output['metadata']['categories']['health']}")
    print(f"  - Law: {output['metadata']['categories']['law']}")
    print(f"  - Technology: {output['metadata']['categories']['technology']}")
    print(f"✓ Saved to {filename}")

def save_questions(filename: str = "questions.json"):
    """Save evaluation questions to a JSON file."""
    questions = generate_evaluation_questions()
    
    output = {
        "metadata": {
            "total_questions": len(questions)
        },
        "questions": questions
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Generated {len(questions)} evaluation questions")
    print(f"✓ Saved to {filename}")

if __name__ == "__main__":
    import os
    
    # Ensure we're in the data directory
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(data_dir, exist_ok=True)
    
    docs_path = os.path.join(data_dir, "documents.json")
    questions_path = os.path.join(data_dir, "questions.json")
    
    save_documents(docs_path)
    print()
    save_questions(questions_path)

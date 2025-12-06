"""
Synthetic Document Generator for Needle-in-Haystack Experiment

This module generates synthetic documents with embedded critical facts
at different positions (start, middle, end) for testing LLM context retrieval.
"""

import random
import json
from pathlib import Path
from typing import List, Tuple, Dict


# Define critical facts with questions and expected answers
CRITICAL_FACTS = [
    {
        "fact": "The ancient library of Alexandria contained over 400,000 scrolls before its destruction.",
        "question": "How many scrolls did the ancient library of Alexandria contain?",
        "answer": "400,000 scrolls",
        "keywords": ["400,000", "400000", "four hundred thousand"]
    },
    {
        "fact": "The first commercial computer weighed 29,000 pounds and was called UNIVAC.",
        "question": "What was the weight of the first commercial computer called UNIVAC?",
        "answer": "29,000 pounds",
        "keywords": ["29,000", "29000", "twenty-nine thousand", "pounds"]
    },
    {
        "fact": "Mount Kilimanjaro rises 19,341 feet above sea level in Tanzania.",
        "question": "What is the elevation of Mount Kilimanjaro above sea level?",
        "answer": "19,341 feet",
        "keywords": ["19,341", "19341", "nineteen thousand", "feet"]
    },
    {
        "fact": "The human brain contains approximately 86 billion neurons.",
        "question": "How many neurons does the human brain contain?",
        "answer": "86 billion neurons",
        "keywords": ["86 billion", "86,000,000,000", "eighty-six billion", "neurons"]
    },
    {
        "fact": "The Panama Canal took 10 years to construct and opened in 1914.",
        "question": "In what year did the Panama Canal open?",
        "answer": "1914",
        "keywords": ["1914", "nineteen fourteen"]
    }
]


# ENHANCED: 100+ highly diverse filler templates for 5000+ word documents
# Each template is unique to avoid any repetition patterns
FILLER_TEMPLATES = [
    # History and Archaeology
    "The study of historical events provides valuable insights into human civilization. "
    "Researchers have documented various patterns across different time periods. "
    "Archaeological discoveries continue to reshape our understanding of the past. "
    "Ancient societies developed complex systems of governance and trade. "
    "Cultural exchange between regions influenced technological advancement.",
    
    "Medieval manuscripts reveal intricate details about daily life in past centuries. "
    "Historians analyze primary sources to construct narratives of forgotten eras. "
    "The rise and fall of empires follows recognizable patterns throughout history. "
    "Trade routes connected distant civilizations and facilitated cultural diffusion. "
    "Monumental architecture reflects the values and capabilities of ancient builders.",
    
    # Technology and Computing
    "Modern technology has transformed the way we communicate and work. "
    "Digital infrastructure connects billions of people worldwide. "
    "Innovation in computing has accelerated exponentially over recent decades. "
    "Software applications enable new forms of collaboration and creativity. "
    "The digital revolution continues to reshape industries and economies.",
    
    "Artificial intelligence systems demonstrate increasingly sophisticated capabilities. "
    "Cloud computing platforms provide scalable resources for diverse applications. "
    "Cybersecurity measures protect sensitive information from malicious actors. "
    "Mobile devices have become ubiquitous tools for personal and professional use. "
    "Quantum computing promises to revolutionize certain computational tasks.",
    
    # Environment and Climate
    "Environmental science examines the complex interactions in natural systems. "
    "Climate patterns affect ecosystems across the globe. "
    "Biodiversity plays a crucial role in maintaining ecological balance. "
    "Conservation efforts focus on protecting endangered species and habitats. "
    "Sustainable practices aim to preserve resources for future generations.",
    
    "Renewable energy sources offer alternatives to fossil fuel dependence. "
    "Deforestation threatens vital ecosystems and contributes to climate change. "
    "Ocean currents distribute heat and influence weather patterns worldwide. "
    "Wetlands provide crucial services including flood control and water filtration. "
    "Sustainable agriculture balances productivity with environmental stewardship.",
    
    # Medicine and Health
    "Medical research advances our understanding of human health and disease. "
    "Scientific breakthroughs have led to improved treatments and therapies. "
    "Healthcare systems around the world face various challenges and opportunities. "
    "Public health initiatives work to prevent illness and promote wellness. "
    "Ongoing studies investigate the mechanisms of cellular function.",
    
    "Genomic medicine enables personalized treatment approaches based on individual genetics. "
    "Immunotherapy harnesses the body's immune system to fight diseases. "
    "Telemedicine expands access to healthcare in remote and underserved areas. "
    "Preventive care strategies reduce the burden of chronic diseases. "
    "Mental health awareness has increased significantly in recent years.",
    
    # Economics and Finance
    "Economic theories attempt to explain market behavior and resource allocation. "
    "Global trade networks facilitate the exchange of goods and services. "
    "Financial systems enable investment and capital formation. "
    "Policy decisions impact employment, inflation, and economic growth. "
    "International cooperation addresses shared economic challenges.",
    
    "Cryptocurrency and blockchain technology challenge traditional financial models. "
    "Income inequality remains a persistent concern in many societies. "
    "Central banks use monetary policy to influence economic conditions. "
    "Supply chain optimization improves efficiency and reduces costs. "
    "Consumer behavior patterns shape market trends and business strategies.",
    
    # Arts and Culture
    "Artistic expression takes many forms across different cultures and eras. "
    "Creative works reflect the values and experiences of their time. "
    "Museums and galleries preserve important cultural artifacts. "
    "Literature captures human emotions and philosophical ideas. "
    "Music transcends language barriers and connects people emotionally.",
    
    "Contemporary art challenges traditional boundaries and conventions. "
    "Digital media enables new forms of creative expression and distribution. "
    "Cultural heritage preservation maintains connections to historical traditions. "
    "Performing arts bring communities together through shared experiences. "
    "Film and television shape popular culture and collective narratives.",
    
    # Education and Learning
    "Educational systems prepare individuals for participation in society. "
    "Learning theories explore how knowledge is acquired and retained. "
    "Curriculum development balances traditional subjects with emerging fields. "
    "Technology integration in classrooms offers new pedagogical possibilities. "
    "Lifelong learning becomes increasingly important in a changing world.",
    
    "Online learning platforms democratize access to educational resources. "
    "Critical thinking skills enable students to analyze complex problems. "
    "Collaborative learning environments foster peer-to-peer knowledge exchange. "
    "Standardized testing remains controversial in educational assessment. "
    "STEM education prepares students for careers in technical fields.",
    
    # Urban Development
    "Urban planning shapes the development of cities and communities. "
    "Infrastructure projects require careful consideration of multiple factors. "
    "Transportation networks enable mobility and economic activity. "
    "Public spaces contribute to quality of life and social interaction. "
    "Zoning regulations balance competing interests and land uses.",
    
    "Smart city initiatives leverage technology to improve urban services. "
    "Housing affordability challenges affect residents in many metropolitan areas. "
    "Green spaces provide environmental and psychological benefits to city dwellers. "
    "Mixed-use developments integrate residential, commercial, and recreational spaces. "
    "Public transportation reduces congestion and environmental impacts.",
    
    # Science and Research
    "Scientific inquiry follows rigorous methodologies to test hypotheses. "
    "Peer review ensures quality and validity of published research. "
    "Interdisciplinary collaboration produces innovative solutions to complex problems. "
    "Data analysis techniques extract meaningful patterns from large datasets. "
    "Experimental design controls variables to establish causal relationships.",
    
    "Space exploration expands our understanding of the universe beyond Earth. "
    "Nanotechnology manipulates matter at atomic and molecular scales. "
    "Particle physics investigates the fundamental building blocks of matter. "
    "Biotechnology applies biological systems to technological applications. "
    "Climate science integrates multiple disciplines to study environmental changes.",
    
    # Social Sciences
    "Sociology examines social structures and human interactions in groups. "
    "Psychology explores cognitive processes and behavioral patterns. "
    "Anthropology studies human cultures across time and geography. "
    "Political science analyzes power dynamics and governance systems. "
    "Demographics track population trends and societal changes.",
    
    "Social movements mobilize collective action for change. "
    "Identity formation involves complex interactions of personal and social factors. "
    "Communication patterns vary significantly across cultural contexts. "
    "Community development initiatives strengthen local social networks. "
    "Migration patterns reshape demographic compositions of regions.",
    
    # Philosophy and Ethics
    "Philosophical inquiry addresses fundamental questions about existence and knowledge. "
    "Ethical frameworks guide decision-making in complex moral situations. "
    "Logic provides tools for constructing and evaluating arguments. "
    "Metaphysics explores the nature of reality and being. "
    "Epistemology investigates the nature and limits of human knowledge.",
    
    "Applied ethics addresses moral questions in specific professional contexts. "
    "Bioethics examines ethical issues arising from medical and biological research. "
    "Environmental ethics considers moral obligations toward the natural world. "
    "Justice theories propose frameworks for fair distribution of resources. "
    "Free will debates question the nature of human agency and responsibility.",
    
    # Engineering and Innovation
    "Engineering disciplines apply scientific principles to practical problems. "
    "Materials science develops new substances with desired properties. "
    "Robotics combines mechanical engineering with artificial intelligence. "
    "Structural engineering ensures the safety and stability of buildings and bridges. "
    "Sustainable design minimizes environmental impact while meeting human needs.",
    
    "3D printing technology enables rapid prototyping and custom manufacturing. "
    "Automation increases efficiency but raises questions about employment. "
    "Renewable energy systems require innovative engineering solutions. "
    "Biomedical engineering creates devices that interface with biological systems. "
    "Civil engineering infrastructure supports economic development and quality of life.",
    
    # Agriculture and Food
    "Agricultural practices have evolved dramatically over human history. "
    "Crop rotation maintains soil fertility and reduces pest pressure. "
    "Precision agriculture uses data to optimize farming operations. "
    "Food security remains a critical challenge in many regions. "
    "Aquaculture provides an alternative source of protein production.",
    
    "Organic farming emphasizes natural processes and minimizes synthetic inputs. "
    "Genetic modification of crops raises both hopes and concerns. "
    "Food distribution systems connect producers with consumers globally. "
    "Nutritional science informs dietary recommendations and public health. "
    "Urban agriculture brings food production into city environments.",
    
    # Communication and Media
    "Mass media shapes public opinion and influences social discourse. "
    "Journalism investigates and reports on events of public interest. "
    "Social media platforms have transformed interpersonal communication. "
    "Information literacy helps individuals evaluate source credibility. "
    "Broadcasting technology evolved from radio to television to streaming.",
    
    "Advertising strategies employ psychological principles to influence behavior. "
    "News aggregation algorithms curate personalized information streams. "
    "Citizen journalism enables grassroots reporting and documentation. "
    "Media literacy education teaches critical consumption of information. "
    "Content moderation balances free expression with community standards.",
    
    # Law and Governance
    "Legal systems establish rules and procedures for resolving disputes. "
    "Constitutional frameworks define powers and limits of government. "
    "International law governs relations between sovereign states. "
    "Judicial interpretation shapes the application of legal principles. "
    "Regulatory agencies oversee compliance with established standards.",
    
    "Civil liberties protect individual rights against government overreach. "
    "Contract law enables voluntary agreements between parties. "
    "Property rights define ownership and use of resources. "
    "Criminal justice systems balance punishment, rehabilitation, and deterrence. "
    "Administrative law regulates the activities of government agencies.",
    
    # Psychology and Behavior
    "Cognitive psychology studies mental processes including perception and memory. "
    "Developmental psychology tracks changes across the human lifespan. "
    "Social psychology examines how individuals influence and are influenced by others. "
    "Personality theories attempt to explain individual differences in behavior. "
    "Clinical psychology addresses mental health disorders and treatments.",
    
    "Neuropsychology links brain function to psychological processes. "
    "Behavioral economics integrates psychological insights into economic models. "
    "Motivation theories explain what drives human action and persistence. "
    "Learning mechanisms include classical conditioning and observational learning. "
    "Emotional intelligence involves recognizing and managing one's own emotions.",
    
    # Additional diverse templates for 5000-word documents
    # Astronomy and Cosmology
    "The observable universe extends billions of light-years in all directions from Earth. "
    "Stellar evolution describes the lifecycle of stars from formation to death. "
    "Galaxies cluster together in vast cosmic structures connected by dark matter. "
    "Exoplanet detection methods reveal worlds orbiting distant stars. "
    "Cosmic microwave background radiation provides evidence for the Big Bang theory.",
    
    "Black holes warp spacetime through their immense gravitational fields. "
    "Nebulae serve as stellar nurseries where new stars ignite from collapsing gas clouds. "
    "Red shift measurements indicate galaxies are moving away from us uniformly. "
    "Asteroid composition reveals clues about the early solar system formation. "
    "Gravitational waves detected from merging neutron stars confirm Einstein's predictions.",
    
    # Marine Biology and Oceanography
    "Coral reefs host extraordinary biodiversity in tropical marine environments. "
    "Deep ocean trenches contain unique ecosystems adapted to extreme pressure. "
    "Phytoplankton form the base of marine food webs and produce atmospheric oxygen. "
    "Whale migration patterns span thousands of miles across ocean basins. "
    "Hydrothermal vents support chemosynthetic communities independent of sunlight.",
    
    "Ocean acidification threatens calcium carbonate shell formation in marine organisms. "
    "Tidal zones exhibit vertical stratification of species adapted to different conditions. "
    "Kelp forests provide habitat and food for diverse temperate marine species. "
    "Bioluminescence serves communication and predation functions in deep sea creatures. "
    "Mangrove ecosystems bridge terrestrial and marine environments in coastal areas.",
    
    # Linguistics and Language
    "Language acquisition in children follows predictable developmental stages worldwide. "
    "Phonetics analyzes the physical production and perception of speech sounds. "
    "Syntax governs how words combine to form grammatically correct sentences. "
    "Semantics studies meaning in language at various levels of analysis. "
    "Historical linguistics traces language evolution and relationships over time.",
    
    "Bilingualism affects cognitive development and executive function in complex ways. "
    "Sign languages possess full linguistic structure independent of spoken language. "
    "Pidgins and creoles emerge from contact between distinct language communities. "
    "Computational linguistics applies algorithms to natural language processing tasks. "
    "Sociolinguistics examines how language varies across social groups and contexts.",
    
    # Geology and Earth Sciences
    "Plate tectonics explains continental drift and seismic activity patterns globally. "
    "Rock formations preserve geological history spanning billions of years. "
    "Volcanic eruptions release magma from deep within Earth's mantle layers. "
    "Erosion processes gradually reshape landscapes through water, wind, and ice. "
    "Mineral deposits form through various geochemical processes under specific conditions.",
    
    "Sedimentary layers accumulate over time, creating stratified rock sequences. "
    "Earthquakes result from sudden release of accumulated tectonic stress. "
    "Glacial periods dramatically altered Earth's climate and surface features. "
    "Fossil records document the evolution of life across geological timescales. "
    "Geothermal energy taps heat from Earth's interior for power generation.",
    
    # Material Science and Chemistry
    "Atomic bonds determine the physical and chemical properties of materials. "
    "Polymers consist of long chains of repeating molecular units. "
    "Crystalline structures exhibit regular, repeating atomic arrangements. "
    "Catalysts accelerate chemical reactions without being consumed themselves. "
    "Phase transitions occur when materials change between solid, liquid, and gas states.",
    
    "Superconductors exhibit zero electrical resistance below critical temperatures. "
    "Composite materials combine multiple substances to achieve superior properties. "
    "Electrochemistry studies reactions involving electron transfer between substances. "
    "Spectroscopy reveals molecular composition through light absorption patterns. "
    "Thermodynamics governs energy transformations in chemical and physical processes.",
    
    # Architecture and Design
    "Architectural styles reflect cultural values and available construction technologies. "
    "Load-bearing structures must distribute weight safely to foundation systems. "
    "Interior design balances aesthetic appeal with functional space utilization. "
    "Historic preservation maintains buildings of cultural and architectural significance. "
    "Biophilic design incorporates natural elements into built environments.",
    
    "Sustainable architecture minimizes energy consumption and environmental impact. "
    "Modular construction allows prefabrication and rapid assembly on site. "
    "Acoustic design controls sound propagation and reverberation in spaces. "
    "Adaptive reuse transforms obsolete buildings for contemporary purposes. "
    "Universal design ensures accessibility for people with diverse abilities.",
    
    # Anthropology and Human Evolution
    "Hominid fossils trace human evolutionary lineage over millions of years. "
    "Tool use distinguishes humans and shaped cognitive development throughout prehistory. "
    "Hunter-gatherer societies developed diverse survival strategies across environments. "
    "Agricultural revolution transformed human social organization fundamentally. "
    "Cultural transmission passes knowledge and practices between generations.",
    
    "Kinship systems vary widely across cultures with different organizing principles. "
    "Burial practices reveal beliefs about death and afterlife in ancient societies. "
    "Cave art demonstrates early human symbolic thinking and creativity. "
    "Domestication of plants and animals enabled sedentary settlements. "
    "Migration patterns populated all continents with anatomically modern humans.",
    
    # Statistics and Data Science
    "Probability theory provides mathematical foundations for statistical inference. "
    "Sampling methods determine how representative data reflects larger populations. "
    "Hypothesis testing evaluates claims using statistical evidence and significance levels. "
    "Regression analysis models relationships between dependent and independent variables. "
    "Correlation measures association strength but does not establish causation.",
    
    "Machine learning algorithms identify patterns in complex datasets automatically. "
    "Data visualization techniques communicate quantitative information effectively. "
    "Bayesian statistics incorporates prior knowledge into probability calculations. "
    "Time series analysis examines data points collected at successive intervals. "
    "Experimental design optimization maximizes information gained from limited resources.",
    
    # Neuroscience and Brain Function
    "Neurons transmit electrical and chemical signals throughout the nervous system. "
    "Synaptic plasticity allows neural connections to strengthen or weaken with experience. "
    "Brain imaging techniques visualize activity patterns during cognitive tasks. "
    "Neurotransmitters facilitate communication between neurons across synaptic gaps. "
    "Cortical organization shows specialized regions for different functions.",
    
    "Memory consolidation transfers information from short-term to long-term storage. "
    "Neural networks process information through interconnected layers of neurons. "
    "Neurogenesis continues producing new neurons in specific brain regions. "
    "Circadian rhythms regulate physiological processes on roughly 24-hour cycles. "
    "Brain plasticity enables recovery and adaptation following injury or trauma.",
    
    # Music Theory and Acoustics
    "Musical scales organize pitches into systematic patterns across octaves. "
    "Harmonic relationships between frequencies create consonance or dissonance. "
    "Rhythm structures organize time into patterns of strong and weak beats. "
    "Timbre distinguishes sounds with identical pitch and loudness. "
    "Musical notation systems encode compositions for performance and preservation.",
    
    "Acoustic resonance amplifies certain frequencies in physical spaces. "
    "Melody contours create recognizable musical phrases and themes. "
    "Polyphony combines multiple independent melodic lines simultaneously. "
    "Temperament systems define pitch relationships in different musical traditions. "
    "Orchestration assigns musical parts to specific instruments for desired effects."
]


def generate_filler_text(target_words: int) -> str:
    """
    Generate filler text of approximately target_words length.
    
    FIXED: Uses shuffle-and-cycle approach to prevent excessive repetition
    in long documents. Each template is used once before any template repeats.
    
    Args:
        target_words: Target number of words to generate
        
    Returns:
        String of filler text with minimal repetition
    """
    text = []
    current_words = 0
    
    # Create a shuffled copy of templates for this document
    template_pool = FILLER_TEMPLATES.copy()
    random.shuffle(template_pool)
    template_index = 0
    
    while current_words < target_words:
        # Get next template from shuffled pool
        template = template_pool[template_index]
        text.append(template)
        current_words += len(template.split())
        
        # Move to next template, reshuffle when we've used all
        template_index += 1
        if template_index >= len(template_pool):
            # Reshuffle and restart (but we've now used all templates at least once)
            random.shuffle(template_pool)
            template_index = 0
    
    # Join and trim to approximately target length
    full_text = " ".join(text)
    words = full_text.split()
    
    if len(words) > target_words:
        words = words[:target_words]
    
    return " ".join(words)


def embed_fact_at_position(filler: str, fact: str, position: str) -> str:
    """
    Embed a critical fact at a specific position in the filler text.
    
    Args:
        filler: Background filler text
        fact: Critical fact to embed
        position: Where to place the fact ("start", "middle", or "end")
        
    Returns:
        Document with embedded fact
    """
    words = filler.split()
    total_words = len(words)
    
    if position == "start":
        # Insert at position 10-20 (after intro but clearly at start)
        insert_pos = random.randint(10, min(20, total_words // 4))
        words.insert(insert_pos, fact)
        
    elif position == "middle":
        # Insert in the middle third of the document
        middle_start = total_words // 3
        middle_end = 2 * total_words // 3
        insert_pos = random.randint(middle_start, middle_end)
        words.insert(insert_pos, fact)
        
    elif position == "end":
        # Insert near the end but not at the very last position
        insert_pos = random.randint(max(total_words - 20, 3 * total_words // 4), total_words - 5)
        words.insert(insert_pos, fact)
    
    return " ".join(words)


def add_distractor_facts(text: str, target_fact: str, num_distractors: int = 3) -> str:
    """
    Add distractor facts with similar numbers to make retrieval harder.
    
    Args:
        text: The document text
        target_fact: The actual fact to keep
        num_distractors: Number of distractor facts to add
        
    Returns:
        Text with distractors embedded
    """
    distractor_templates = [
        "Historical records indicate that approximately {num} items were catalogued in various collections.",
        "Studies have shown that roughly {num} specimens were analyzed in the research.",
        "Experts estimate that around {num} units were measured during the investigation.",
        "Reports suggest that nearly {num} instances were documented throughout the period.",
        "Archaeological findings reveal that close to {num} artifacts were discovered at the site.",
        "Scientific surveys calculated that about {num} samples were collected for analysis.",
        "Documentation shows that approximately {num} observations were recorded in total.",
        "Research indicates that roughly {num} examples were examined during the study.",
    ]
    
    words = text.split()
    
    # Generate random but plausible distractor numbers
    for _ in range(num_distractors):
        # Create numbers that are different but in similar ranges
        distractor_num = random.choice([
            f"{random.randint(100, 900) * 100:,}",
            f"{random.randint(10, 99)},{random.randint(100, 999):03d}",
            f"{random.randint(50, 150)} {random.choice(['thousand', 'million', 'billion'])}",
            str(random.randint(1800, 2020)),  # Years
        ])
        
        template = random.choice(distractor_templates)
        distractor = template.format(num=distractor_num)
        
        # Insert at random positions (avoiding the target fact position)
        insert_pos = random.randint(20, len(words) - 20)
        words.insert(insert_pos, distractor)
    
    return " ".join(words)


def generate_document(fact_data: Dict, position: str, words_per_doc: int = 200, 
                     add_distractors: bool = False) -> Dict:
    """
    Generate a single synthetic document with an embedded fact.
    
    Args:
        fact_data: Dictionary containing fact, question, answer, and keywords
        position: Where to place the fact ("start", "middle", or "end")
        words_per_doc: Approximate number of words in the document
        add_distractors: Whether to add distractor facts with similar numbers
        
    Returns:
        Dictionary with document text, metadata, and evaluation criteria
    """
    # Generate filler text
    filler = generate_filler_text(words_per_doc)
    
    # Embed the fact
    document_text = embed_fact_at_position(filler, fact_data["fact"], position)
    
    # Add distractor facts if requested
    if add_distractors:
        document_text = add_distractor_facts(document_text, fact_data["fact"], num_distractors=3)
    
    # Create document metadata
    doc_metadata = {
        "text": document_text,
        "fact": fact_data["fact"],
        "question": fact_data["question"],
        "expected_answer": fact_data["answer"],
        "keywords": fact_data["keywords"],
        "position": position,
        "word_count": len(document_text.split())
    }
    
    return doc_metadata


def generate_dataset(num_docs: int = 15, words_per_doc: int = 200, output_dir: str = "data",
                    add_distractors: bool = False, dataset_name: str = "documents") -> List[Dict]:
    """
    Generate a complete dataset of synthetic documents.
    
    Args:
        num_docs: Total number of documents to generate (should be divisible by 3)
        words_per_doc: Approximate words per document
        output_dir: Directory to save the generated data
        add_distractors: Whether to add distractor facts
        dataset_name: Name for the dataset file (without .json extension)
        
    Returns:
        List of document dictionaries
    """
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    documents = []
    positions = ["start", "middle", "end"]
    
    # Ensure balanced distribution across positions
    docs_per_position = num_docs // 3
    position_counts = {pos: 0 for pos in positions}
    
    for i in range(num_docs):
        # Select fact (cycle through available facts)
        fact_data = CRITICAL_FACTS[i % len(CRITICAL_FACTS)]
        
        # Select position (ensure balanced distribution)
        available_positions = [pos for pos in positions if position_counts[pos] < docs_per_position]
        if not available_positions:
            available_positions = positions
        
        position = random.choice(available_positions)
        position_counts[position] += 1
        
        # Generate document
        doc = generate_document(fact_data, position, words_per_doc, add_distractors=add_distractors)
        doc["doc_id"] = i
        documents.append(doc)
    
    # Save documents to JSON file
    output_file = output_path / f"{dataset_name}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(documents, f, indent=2, ensure_ascii=False)
    
    print(f"Generated {num_docs} documents:")
    print(f"  - {position_counts['start']} with fact at START")
    print(f"  - {position_counts['middle']} with fact at MIDDLE")
    print(f"  - {position_counts['end']} with fact at END")
    print(f"  - Average words per doc: {sum(d['word_count'] for d in documents) / len(documents):.1f}")
    print(f"  - Distractors: {'YES' if add_distractors else 'NO'}")
    print(f"  - Saved to: {output_file}")
    
    return documents


if __name__ == "__main__":
    # Generate dataset when run directly
    print("=" * 60)
    print("Generating Synthetic Dataset for Lab 1")
    print("=" * 60)
    
    # Generate 15 documents (5 per position)
    documents = generate_dataset(num_docs=15, words_per_doc=200, output_dir="lab1/data")
    
    # Print sample document
    print("\n" + "=" * 60)
    print("Sample Document (doc_id=0)")
    print("=" * 60)
    sample = documents[0]
    print(f"Position: {sample['position']}")
    print(f"Fact: {sample['fact']}")
    print(f"Question: {sample['question']}")
    print(f"Expected Answer: {sample['expected_answer']}")
    print(f"\nDocument Preview (first 300 chars):")
    print(sample['text'][:300] + "...")

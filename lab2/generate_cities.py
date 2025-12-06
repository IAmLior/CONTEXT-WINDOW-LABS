"""
Lab 2: Generate City Documents (180 words each - 2x animals)
Purpose: Test if larger documents stress Phi-4-mini more than smaller ones
"""

import json
import random
from pathlib import Path
from typing import List, Dict

# 50 unique cities with fascinating facts
CITIES = [
    {"name": "Tokyo", "country": "Japan", "fact": "Tokyo has more Michelin-starred restaurants than any other city in the world"},
    {"name": "Venice", "country": "Italy", "fact": "Venice is built on 118 small islands connected by over 400 bridges"},
    {"name": "Singapore", "country": "Singapore", "fact": "Singapore has the world's highest percentage of millionaires with one in six households being millionaire households"},
    {"name": "Reykjavik", "country": "Iceland", "fact": "Reykjavik is the world's northernmost capital city and uses geothermal energy to heat almost all its buildings"},
    {"name": "Dubai", "country": "UAE", "fact": "Dubai's Burj Khalifa is the tallest building in the world standing at 828 meters tall"},
    {"name": "Amsterdam", "country": "Netherlands", "fact": "Amsterdam has more bicycles than residents with over 880,000 bikes for 800,000 people"},
    {"name": "Copenhagen", "country": "Denmark", "fact": "Copenhagen aims to become the world's first carbon-neutral capital by 2025"},
    {"name": "Sydney", "country": "Australia", "fact": "Sydney Harbour Bridge took 1,400 workers eight years to build and uses 6 million hand-driven rivets"},
    {"name": "Barcelona", "country": "Spain", "fact": "Barcelona's Sagrada Familia has been under construction since 1882 and may be completed by 2026"},
    {"name": "Prague", "country": "Czech Republic", "fact": "Prague's Astronomical Clock has been operating since 1410 making it the oldest working astronomical clock"},
    {"name": "Marrakech", "country": "Morocco", "fact": "Marrakech's Jemaa el-Fnaa square transforms into the world's largest open-air restaurant every evening"},
    {"name": "Kyoto", "country": "Japan", "fact": "Kyoto has over 2,000 Buddhist temples and Shinto shrines including 17 UNESCO World Heritage sites"},
    {"name": "Istanbul", "country": "Turkey", "fact": "Istanbul is the only city in the world located on two continents Europe and Asia"},
    {"name": "Cairo", "country": "Egypt", "fact": "Cairo's population exceeds 20 million making it Africa's largest metropolitan area"},
    {"name": "Mumbai", "country": "India", "fact": "Mumbai's dabbawalas deliver 200,000 lunch boxes daily with a six sigma efficiency rating"},
    {"name": "Mexico City", "country": "Mexico", "fact": "Mexico City is sinking at a rate of 50 centimeters per year due to groundwater extraction"},
    {"name": "Rio de Janeiro", "country": "Brazil", "fact": "Rio's Christ the Redeemer statue stands 38 meters tall and is struck by lightning multiple times each year"},
    {"name": "St Petersburg", "country": "Russia", "fact": "St Petersburg has more bridges than Venice and Amsterdam combined with over 342 bridges"},
    {"name": "Vienna", "country": "Austria", "fact": "Vienna has been rated the world's most liveable city multiple times and has over 100 museums"},
    {"name": "Lisbon", "country": "Portugal", "fact": "Lisbon's Tram 28 travels through the city's narrowest streets some only 3 meters wide"},
    {"name": "Athens", "country": "Greece", "fact": "Athens has been continuously inhabited for over 3,400 years making it one of the world's oldest cities"},
    {"name": "Jerusalem", "country": "Israel", "fact": "Jerusalem is considered sacred by three major religions Judaism Christianity and Islam"},
    {"name": "Petra", "country": "Jordan", "fact": "Petra's Treasury is carved directly into rose-red sandstone cliffs and is over 2,000 years old"},
    {"name": "Dubrovnik", "country": "Croatia", "fact": "Dubrovnik's city walls are up to 25 meters high and 6 meters thick completely surrounding the old town"},
    {"name": "Edinburgh", "country": "Scotland", "fact": "Edinburgh has more trees per head of population than any other city in the UK"},
    {"name": "Stockholm", "country": "Sweden", "fact": "Stockholm is built on 14 islands connected by 57 bridges and has been called the Venice of the North"},
    {"name": "Helsinki", "country": "Finland", "fact": "Helsinki has over 300 islands within city limits and the world's only sea fortress still in use"},
    {"name": "Oslo", "country": "Norway", "fact": "Oslo is surrounded by forests and fjords with one-third of the city area being protected green space"},
    {"name": "Zurich", "country": "Switzerland", "fact": "Zurich has more than 1,200 drinking fountains with free potable water throughout the city"},
    {"name": "Geneva", "country": "Switzerland", "fact": "Geneva hosts 34 international organizations and is home to the European headquarters of the United Nations"},
    {"name": "Brussels", "country": "Belgium", "fact": "Brussels has more comic book writers and artists per square kilometer than anywhere else in Europe"},
    {"name": "Budapest", "country": "Hungary", "fact": "Budapest has 80 geothermal springs producing 70 million liters of thermal water daily"},
    {"name": "Warsaw", "country": "Poland", "fact": "Warsaw's Old Town was meticulously rebuilt after World War II using paintings and photographs"},
    {"name": "Dublin", "country": "Ireland", "fact": "Dublin's Phoenix Park is one of the largest urban parks in Europe covering 707 hectares"},
    {"name": "Tallinn", "country": "Estonia", "fact": "Tallinn offers free public transportation to all residents making it one of the largest free transit zones"},
    {"name": "Riga", "country": "Latvia", "fact": "Riga has the largest collection of Art Nouveau buildings in the world with over 800 structures"},
    {"name": "Vilnius", "country": "Lithuania", "fact": "Vilnius has one of the largest surviving medieval old towns in Northern Europe"},
    {"name": "Krakow", "country": "Poland", "fact": "Krakow's Main Market Square is one of the largest medieval town squares in Europe"},
    {"name": "Ljubljana", "country": "Slovenia", "fact": "Ljubljana was named European Green Capital for its commitment to sustainability and green spaces"},
    {"name": "Valletta", "country": "Malta", "fact": "Valletta is the smallest national capital in the European Union covering just 0.8 square kilometers"},
    {"name": "Nicosia", "country": "Cyprus", "fact": "Nicosia is the last divided capital in the world with a UN buffer zone separating north and south"},
    {"name": "Sarajevo", "country": "Bosnia", "fact": "Sarajevo is called the Jerusalem of Europe for its centuries of religious diversity and tolerance"},
    {"name": "Belgrade", "country": "Serbia", "fact": "Belgrade is one of the oldest cities in Europe dating back to the 4th century BC"},
    {"name": "Bucharest", "country": "Romania", "fact": "Bucharest's Palace of Parliament is the world's second-largest administrative building after the Pentagon"},
    {"name": "Sofia", "country": "Bulgaria", "fact": "Sofia is one of Europe's oldest cities with a history spanning over 7,000 years"},
    {"name": "Tirana", "country": "Albania", "fact": "Tirana's buildings are painted in vibrant colors as part of a project to bring life back after communism"},
    {"name": "Skopje", "country": "North Macedonia", "fact": "Skopje has over 130 statues and monuments erected in a controversial urban renewal project"},
    {"name": "Podgorica", "country": "Montenegro", "fact": "Podgorica is one of Europe's warmest cities and has been rebuilt three times throughout history"},
    {"name": "Bern", "country": "Switzerland", "fact": "Bern's Old Town has 6 kilometers of arcaded walkways called Lauben providing covered shopping"},
    {"name": "Vaduz", "country": "Liechtenstein", "fact": "Vaduz is one of the few capital cities without an airport and has a population under 6,000"},
]


def generate_city_document(city: Dict[str, str], word_target: int = 180) -> str:
    """
    Generate a rich document about a city.
    Target: 180 words (2x the animal documents to test if larger docs stress the model)
    
    Structure:
    - Introduction (20-25 words)
    - Location & Geography (30-35 words)
    - Population & Demographics (25-30 words)
    - Economy & Infrastructure (30-35 words)
    - Culture & Attractions (30-35 words)
    - Unique Fact (10-15 words)
    - Filler content to reach target (remaining words)
    """
    
    name = city["name"]
    country = city["country"]
    unique_fact = city["fact"]
    
    # Introduction
    intro = f"{name} is a remarkable city located in {country}. "
    intro += "It stands as a testament to urban development and cultural heritage. "
    intro += f"The city attracts millions of visitors annually who come to experience its unique character."
    
    # Location & Geography
    geography = f"Geographically {name} occupies a strategic position within {country}. "
    geography += "The city's landscape features distinctive terrain that shapes its identity. "
    geography += "Local climate conditions influence the lifestyle and architecture throughout the urban area. "
    geography += "Natural features surrounding the metropolis contribute to its scenic beauty and ecological diversity."
    
    # Population & Demographics
    demographics = f"The population of {name} represents a diverse multicultural community. "
    demographics += "Residents come from various backgrounds creating a rich social tapestry. "
    demographics += "The city continues to grow with urban development attracting new inhabitants. "
    demographics += "Educational institutions and employment opportunities drive demographic trends in the region."
    
    # Economy & Infrastructure
    economy = f"Economically {name} serves as a vital hub for commerce and industry in {country}. "
    economy += "The city's infrastructure supports modern transportation and communication networks. "
    economy += "Business districts house international corporations and innovative startups. "
    economy += "Tourism plays a significant role in the local economy generating substantial revenue annually. "
    economy += "Public services and utilities maintain high standards for residents and visitors alike."
    
    # Culture & Attractions
    culture = f"Culturally {name} offers numerous museums galleries theaters and concert halls. "
    culture += "Historic sites and modern attractions coexist throughout the cityscape. "
    culture += "Local festivals celebrate traditions and bring communities together throughout the year. "
    culture += "The culinary scene features both traditional dishes and international cuisine. "
    culture += "Art and architecture reflect centuries of historical development and contemporary innovation."
    
    # Unique fact
    fact_statement = f"A fascinating characteristic of {name}: {unique_fact}. "
    
    # Combine all sections
    document = intro + " " + geography + " " + demographics + " " + economy + " " + culture + " " + fact_statement
    
    # Add filler to reach word target
    current_words = len(document.split())
    words_needed = word_target - current_words
    
    if words_needed > 0:
        filler_sentences = [
            f"The city of {name} continues to evolve and adapt to changing global trends. ",
            "Urban planners focus on sustainability and improving quality of life for all inhabitants. ",
            "Transportation networks undergo constant upgrades to meet growing demands. ",
            "Green spaces and parks provide recreational opportunities for families and individuals. ",
            "Educational programs promote cultural awareness and environmental responsibility. ",
            "Community initiatives strengthen social bonds and neighborhood cohesion. ",
            "Technology integration enhances municipal services and citizen engagement. ",
            "Historic preservation efforts maintain connections to the city's rich past. ",
            "Future development projects aim to balance growth with environmental protection. ",
            f"Visitors to {name} discover new experiences with each visit to this dynamic city. ",
            "Local governance prioritizes transparency and responsive public administration. ",
            "International partnerships foster cultural exchange and economic cooperation. ",
            "The city's resilience shines through its ability to overcome challenges. ",
            "Innovation hubs attract talent from around the world seeking opportunities. ",
            "Public spaces serve as gathering points for celebrations and civic events. ",
        ]
        
        filler = ""
        while len(filler.split()) < words_needed:
            filler += random.choice(filler_sentences)
        
        # Trim to exact word count
        filler_words = filler.split()[:words_needed]
        filler = " ".join(filler_words)
        
        document += " " + filler
    
    return document.strip()


def generate_documents_set(num_documents: int, words_per_doc: int = 180) -> List[Dict[str, str]]:
    """
    Generate a set of city documents.
    Uses shuffle-and-cycle approach to ensure variety across different set sizes.
    """
    # Shuffle cities for randomness
    shuffled_cities = CITIES.copy()
    random.seed(42)  # Fixed seed for reproducibility
    random.shuffle(shuffled_cities)
    
    documents = []
    
    for i in range(num_documents):
        # Cycle through cities if we need more than 50
        city = shuffled_cities[i % len(shuffled_cities)]
        
        # Generate document
        content = generate_city_document(city, word_target=words_per_doc)
        word_count = len(content.split())
        
        documents.append({
            "id": i + 1,
            "city": city["name"],
            "country": city["country"],
            "unique_fact": city["fact"],
            "content": content,
            "word_count": word_count
        })
    
    return documents


def save_documents(documents: List[Dict[str, str]], filename: str):
    """Save documents to JSON file in data/ directory."""
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    output_path = data_dir / filename
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(documents, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Saved {len(documents)} documents to {output_path}")


def load_documents(filename: str) -> List[Dict[str, str]]:
    """Load documents from JSON file."""
    data_dir = Path(__file__).parent / "data"
    input_path = data_dir / filename
    
    with open(input_path, 'r', encoding='utf-8') as f:
        documents = json.load(f)
    
    print(f"✓ Loaded {len(documents)} documents from {input_path}")
    return documents


if __name__ == "__main__":
    """Generate city documents for Phi-4-mini context window testing."""
    
    print("=" * 80)
    print("LAB 2: CONTEXT WINDOW SIZE IMPACT - CITIES DATASET")
    print("Testing if LARGER documents stress Phi-4-mini more")
    print("=" * 80)
    
    # Generate document sets for different context sizes: 2, 5, 10, 20, 50 documents
    context_sizes = [2, 5, 10, 20, 50]
    
    # ============================================================================
    # PHI-4-MINI CITIES DOCUMENTS (180 words each - 2x animals)
    # ============================================================================
    print("\n" + "🏙️  " * 20)
    print("GENERATING CITY DOCUMENTS FOR PHI-4-MINI-INSTRUCT")
    print("🏙️  " * 20)
    print("\n📊 Previous test (Animals - 90 words/doc):")
    print("   ✅ 50 docs = 4,700 words (~6,636 tokens): 100% accurate")
    print("   ✅ All sizes: Perfect performance")
    
    phi_words_per_doc = 180  # 2x the animal documents
    print(f"\n📝 Using {phi_words_per_doc} words per document for Cities (2x Animals)")
    print(f"   This creates a progression from {context_sizes[0]*phi_words_per_doc:,} to {context_sizes[-1]*phi_words_per_doc:,} words")
    print(f"   Target: 50 docs (~9,000w / ~12K tokens) - Testing if LARGER docs cause issues\n")
    
    print("❓ HYPOTHESIS: Will bigger documents stress the model more?")
    print("   - Same number of documents (2, 5, 10, 20, 50)")
    print("   - But 2x word count per document (180 vs 90 words)")
    print("   - Will this push Phi-4-mini past its limits?\n")
    
    for num_docs in context_sizes:
        print(f"\nGenerating {num_docs} city documents...")
        documents = generate_documents_set(num_docs, words_per_doc=phi_words_per_doc)
        
        total_words = sum(doc['word_count'] for doc in documents)
        avg_words = total_words / num_docs
        approx_tokens = int(total_words * 1.3)
        
        # Status indicator
        if total_words <= 4700:
            status = "✅ BELOW ANIMAL TEST MAX"
        elif total_words <= 6500:
            status = "⚠️  CRITICAL ZONE"
        else:
            status = "❓ UNCHARTED TERRITORY"
        
        print(f"  Total words: {total_words:,} {status}")
        print(f"  Average words per doc: {avg_words:.1f}")
        print(f"  Estimated tokens: ~{approx_tokens:,}")
        
        save_documents(documents, f"documents_{num_docs}_cities.json")
    
    # ============================================================================
    # SUMMARY
    # ============================================================================
    print("\n" + "=" * 80)
    print("✓ City document sets generated successfully!")
    print("=" * 80)
    
    print("\n📊 CITIES CONTEXT SIZES (180 words/doc - 2x Animals):")
    for n in context_sizes:
        total = n * phi_words_per_doc
        tokens = int(total * 1.3)
        if total <= 4700:
            status = "✅"
        elif total <= 6500:
            status = "⚠️ "
        else:
            status = "❓"
        print(f"   {status} {n:2d} docs: {total:6,} words (~{tokens:6,} tokens)")
    
    print("\n💡 EXPERIMENTAL QUESTION:")
    print("   Animals (90w/doc): 100% accuracy at 4,700 words")
    print("   Cities (180w/doc): Will 9,000 words cause failure?")
    print("   Testing: Does DOCUMENT SIZE matter or just TOTAL TOKEN COUNT?")
    print("=" * 80)

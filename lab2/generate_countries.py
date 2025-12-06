"""
Lab 2: Generate Country Documents (300 words each - 3.3x animals)
Purpose: Push Phi-4-mini to the extreme - will 23K+ tokens finally break it?
"""

import json
import random
from pathlib import Path
from typing import List, Dict

# 50 unique countries with fascinating facts
COUNTRIES = [
    {"name": "Japan", "capital": "Tokyo", "fact": "Japan has the world's highest life expectancy at 85 years and is home to over 6800 islands"},
    {"name": "Brazil", "capital": "Brasilia", "fact": "Brazil covers nearly half of South America and contains 60 percent of the Amazon rainforest"},
    {"name": "Iceland", "capital": "Reykjavik", "fact": "Iceland runs almost entirely on renewable energy with 85 percent from hydroelectric and geothermal sources"},
    {"name": "Switzerland", "capital": "Bern", "fact": "Switzerland has remained neutral in every war since 1815 and has four official languages"},
    {"name": "New Zealand", "capital": "Wellington", "fact": "New Zealand was the first country to give women the right to vote in 1893"},
    {"name": "Norway", "capital": "Oslo", "fact": "Norway's sovereign wealth fund is the world's largest holding over 1.4 trillion dollars"},
    {"name": "Singapore", "capital": "Singapore", "fact": "Singapore has transformed from a third world country to first world in just one generation"},
    {"name": "Finland", "capital": "Helsinki", "fact": "Finland has more saunas than cars with approximately 3.3 million saunas for 5.5 million people"},
    {"name": "Netherlands", "capital": "Amsterdam", "fact": "Netherlands has more bicycles than people with 23 million bikes for 17 million residents"},
    {"name": "Sweden", "capital": "Stockholm", "fact": "Sweden recycles 99 percent of its household waste and imports garbage from other countries to fuel its power plants"},
    {"name": "Denmark", "capital": "Copenhagen", "fact": "Denmark consistently ranks as the happiest country in the world and invented LEGO"},
    {"name": "Canada", "capital": "Ottawa", "fact": "Canada has the longest coastline in the world at 202,080 kilometers and contains 20 percent of the world's fresh water"},
    {"name": "Australia", "capital": "Canberra", "fact": "Australia is the only country that is also a continent and has more deadly animals than any other nation"},
    {"name": "Germany", "capital": "Berlin", "fact": "Germany has over 1500 different types of beer and is the world's largest exporter of goods"},
    {"name": "South Korea", "capital": "Seoul", "fact": "South Korea has the fastest average internet speed in the world and invented the world's first metal movable type printing"},
    {"name": "Ireland", "capital": "Dublin", "fact": "Ireland has no snakes due to its isolation during the Ice Age and St Patrick gets credit in legend"},
    {"name": "Belgium", "capital": "Brussels", "fact": "Belgium produces 220,000 tons of chocolate per year and has over 1000 varieties of beer"},
    {"name": "Austria", "capital": "Vienna", "fact": "Austria has produced more Nobel Prize winners per capita than any other country"},
    {"name": "United Kingdom", "capital": "London", "fact": "The United Kingdom is made up of four countries England Scotland Wales and Northern Ireland"},
    {"name": "France", "capital": "Paris", "fact": "France is the most visited country in the world receiving over 89 million tourists annually"},
    {"name": "Spain", "capital": "Madrid", "fact": "Spain has the world's oldest restaurant Restaurante Botín founded in 1725 in Madrid"},
    {"name": "Italy", "capital": "Rome", "fact": "Italy has more UNESCO World Heritage Sites than any other country with 58 locations"},
    {"name": "Portugal", "capital": "Lisbon", "fact": "Portugal is the world's leading cork producer accounting for over 50 percent of global production"},
    {"name": "Greece", "capital": "Athens", "fact": "Greece has over 6000 islands of which only 227 are inhabited and invented democracy"},
    {"name": "Turkey", "capital": "Ankara", "fact": "Turkey straddles two continents Europe and Asia and Istanbul is the only city on two continents"},
    {"name": "Egypt", "capital": "Cairo", "fact": "Egypt is home to the only remaining ancient wonder the Great Pyramid of Giza built around 2560 BC"},
    {"name": "Morocco", "capital": "Rabat", "fact": "Morocco is the closest African country to Europe separated by only 13 kilometers at the Strait of Gibraltar"},
    {"name": "South Africa", "capital": "Pretoria", "fact": "South Africa has three capital cities Pretoria executive Bloemfontein judicial and Cape Town legislative"},
    {"name": "Kenya", "capital": "Nairobi", "fact": "Kenya is home to the Great Migration where over 1.5 million wildebeest migrate annually"},
    {"name": "India", "capital": "New Delhi", "fact": "India is the world's largest democracy with over 900 million eligible voters"},
    {"name": "China", "capital": "Beijing", "fact": "China has the world's largest population at 1.4 billion people and built the Great Wall over 2000 years"},
    {"name": "Russia", "capital": "Moscow", "fact": "Russia is the largest country in the world spanning 11 time zones and two continents"},
    {"name": "Indonesia", "capital": "Jakarta", "fact": "Indonesia is the world's largest archipelago with over 17,000 islands and 300 languages"},
    {"name": "Thailand", "capital": "Bangkok", "fact": "Thailand is the only Southeast Asian country never colonized by European powers"},
    {"name": "Vietnam", "capital": "Hanoi", "fact": "Vietnam is the world's largest exporter of cashew nuts and black pepper"},
    {"name": "Malaysia", "capital": "Kuala Lumpur", "fact": "Malaysia has the world's oldest rainforest at 130 million years old in Taman Negara"},
    {"name": "Philippines", "capital": "Manila", "fact": "Philippines is made up of 7641 islands and Filipinos send more text messages than any other nation"},
    {"name": "Mexico", "capital": "Mexico City", "fact": "Mexico City is built on the ruins of the ancient Aztec city of Tenochtitlan and sinks 10 inches per year"},
    {"name": "Argentina", "capital": "Buenos Aires", "fact": "Argentina has the highest consumption of red meat per capita in the world"},
    {"name": "Chile", "capital": "Santiago", "fact": "Chile is the longest north-south country in the world stretching 4270 kilometers"},
    {"name": "Peru", "capital": "Lima", "fact": "Peru is home to Machu Picchu one of the New Seven Wonders of the World built by the Incas"},
    {"name": "Colombia", "capital": "Bogota", "fact": "Colombia is the world's leading source of emeralds producing over 90 percent of the world's supply"},
    {"name": "Venezuela", "capital": "Caracas", "fact": "Venezuela has the world's largest oil reserves and Angel Falls the world's highest waterfall"},
    {"name": "Poland", "capital": "Warsaw", "fact": "Poland's capital Warsaw was rebuilt brick by brick after World War II using paintings and photographs"},
    {"name": "Czech Republic", "capital": "Prague", "fact": "Czech Republic has the highest beer consumption per capita in the world"},
    {"name": "Hungary", "capital": "Budapest", "fact": "Hungary has 1500 thermal springs and Budapest has the world's largest thermal water cave system"},
    {"name": "Romania", "capital": "Bucharest", "fact": "Romania is home to Dracula's castle Bran Castle and has the world's second largest building the Palace of Parliament"},
    {"name": "Bulgaria", "capital": "Sofia", "fact": "Bulgaria is the world's leading producer of rose oil used in perfumes"},
    {"name": "Croatia", "capital": "Zagreb", "fact": "Croatia invented the necktie originally worn by Croatian soldiers in the 17th century"},
    {"name": "Slovenia", "capital": "Ljubljana", "fact": "Slovenia is one of the world's most forested countries with forests covering 60 percent of its territory"},
]


def generate_country_document(country: Dict[str, str], word_target: int = 300) -> str:
    """
    Generate a comprehensive document about a country.
    Target: 300 words (3.3x the animal documents to really stress-test Phi-4-mini!)
    
    Structure:
    - Introduction (30-35 words)
    - Geography & Climate (50-55 words)
    - Population & Demographics (40-45 words)
    - Economy & Industry (50-55 words)
    - Culture & Traditions (45-50 words)
    - Government & Politics (35-40 words)
    - Unique Fact (15-20 words)
    - Filler content to reach target (remaining words)
    """
    
    name = country["name"]
    capital = country["capital"]
    unique_fact = country["fact"]
    
    # Introduction
    intro = f"{name} is a sovereign nation with its capital in {capital}. "
    intro += "This country represents a unique blend of historical heritage and modern development. "
    intro += f"The nation of {name} plays an important role in regional and global affairs. "
    intro += "Its distinctive character attracts international attention and cultural exchange opportunities."
    
    # Geography & Climate
    geography = f"Geographically {name} features diverse landscapes ranging from mountains to coastlines. "
    geography += "The country's topography has shaped settlement patterns and economic activities throughout history. "
    geography += f"Climate conditions in {name} vary by region creating distinct ecological zones. "
    geography += "Natural resources found within the territory support various industries and exports. "
    geography += "Rivers lakes and coastal areas provide essential water resources for agriculture and cities. "
    geography += "Environmental conservation efforts aim to protect biodiversity and natural habitats."
    
    # Population & Demographics
    demographics = f"The population of {name} consists of diverse ethnic and cultural groups. "
    demographics += f"Major urban centers include the capital {capital} along with other significant cities. "
    demographics += "Educational systems prepare citizens for participation in the modern economy. "
    demographics += "Healthcare infrastructure continues to develop with improvements in life expectancy. "
    demographics += "Migration patterns both internal and international affect demographic composition. "
    demographics += "Language and religious diversity contribute to the nation's cultural richness."
    
    # Economy & Industry  
    economy = f"The economy of {name} relies on multiple sectors including agriculture manufacturing and services. "
    economy += "International trade relationships connect the country to global markets. "
    economy += "Foreign investment flows support infrastructure development and job creation. "
    economy += "Technology adoption drives productivity gains across various industries. "
    economy += "Tourism represents a significant source of foreign exchange earnings. "
    economy += "Financial institutions and banking systems facilitate domestic and international transactions. "
    economy += "Transportation networks including roads railways and airports enable commerce."
    
    # Culture & Traditions
    culture = f"Culturally {name} boasts rich traditions in arts music dance and literature. "
    culture += "Historical monuments and museums preserve the nation's heritage for future generations. "
    culture += "Traditional festivals celebrate important events and bring communities together. "
    culture += "Culinary traditions feature distinctive flavors and cooking techniques. "
    culture += "Sports and recreational activities play important roles in social life. "
    culture += "Contemporary artists and performers gain international recognition. "
    culture += "Educational and cultural exchanges strengthen ties with other nations."
    
    # Government & Politics
    government = f"The government of {name} operates under a specific constitutional framework. "
    government += "Political institutions ensure representation and democratic participation. "
    government += "Diplomatic relations extend to countries across multiple continents. "
    government += "Legal systems provide frameworks for justice and conflict resolution. "
    government += "Public administration delivers essential services to citizens nationwide."
    
    # Unique fact
    fact_statement = f"A remarkable characteristic that distinguishes {name}: {unique_fact}. "
    fact_statement += "This fascinating aspect highlights the country's unique position in the world community."
    
    # Combine all sections
    document = intro + " " + geography + " " + demographics + " " + economy + " " + culture + " " + government + " " + fact_statement
    
    # Add filler to reach word target
    current_words = len(document.split())
    words_needed = word_target - current_words
    
    if words_needed > 0:
        filler_sentences = [
            f"The nation of {name} continues to evolve in response to global challenges and opportunities. ",
            "Sustainable development goals guide policy planning and implementation across sectors. ",
            "Innovation and entrepreneurship receive government support through various programs. ",
            "Infrastructure improvements enhance connectivity and quality of life for residents. ",
            "Regional cooperation initiatives promote stability and mutual prosperity. ",
            f"Citizens of {name} contribute to global culture science and humanitarian efforts. ",
            "Environmental challenges require coordinated responses from government and society. ",
            "Digital transformation affects governance education healthcare and commerce. ",
            "Youth populations represent both opportunities and challenges for future development. ",
            f"International partnerships help {name} address complex transnational issues. ",
            "Agricultural modernization balances productivity with environmental sustainability. ",
            "Urban planning addresses population growth and infrastructure demands. ",
            "Energy security and renewable resources receive increasing policy attention. ",
            "Educational reforms aim to develop skills for 21st century economies. ",
            "Healthcare systems adapt to demographic changes and emerging diseases. ",
            "Transportation modernization reduces travel times and improves logistics. ",
            "Financial sector development supports economic growth and stability. ",
            "Tourism infrastructure expands to accommodate growing visitor numbers. ",
            "Cultural heritage preservation balances modernization with tradition. ",
            "Scientific research institutions contribute to global knowledge advancement. ",
        ]
        
        filler = ""
        while len(filler.split()) < words_needed:
            filler += random.choice(filler_sentences)
        
        # Trim to exact word count
        filler_words = filler.split()[:words_needed]
        filler = " ".join(filler_words)
        
        document += " " + filler
    
    return document.strip()


def generate_documents_set(num_documents: int, words_per_doc: int = 300) -> List[Dict[str, str]]:
    """
    Generate a set of country documents.
    Uses shuffle-and-cycle approach to ensure variety across different set sizes.
    """
    # Shuffle countries for randomness
    shuffled_countries = COUNTRIES.copy()
    random.seed(42)  # Fixed seed for reproducibility
    random.shuffle(shuffled_countries)
    
    documents = []
    
    for i in range(num_documents):
        # Cycle through countries if we need more than 50
        country = shuffled_countries[i % len(shuffled_countries)]
        
        # Generate document
        content = generate_country_document(country, word_target=words_per_doc)
        word_count = len(content.split())
        
        documents.append({
            "id": i + 1,
            "country": country["name"],
            "capital": country["capital"],
            "unique_fact": country["fact"],
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


if __name__ == "__main__":
    """Generate country documents for Phi-4-mini EXTREME context window testing."""
    
    print("=" * 80)
    print("LAB 2: CONTEXT WINDOW SIZE IMPACT - COUNTRIES DATASET (TRIAL 3)")
    print("EXTREME TEST: Will 300 words/doc finally break Phi-4-mini?")
    print("=" * 80)
    
    # Generate document sets for different context sizes: 2, 5, 10, 20, 50 documents
    context_sizes = [2, 5, 10, 20, 50]
    
    # ============================================================================
    # COUNTRIES DOCUMENTS (300 words each - 3.3x animals, 1.67x cities)
    # ============================================================================
    print("\n" + "🌍 " * 20)
    print("GENERATING COUNTRY DOCUMENTS FOR PHI-4-MINI-INSTRUCT")
    print("🌍 " * 20)
    print("\n📊 Previous tests:")
    print("   ✅ Animals (90w/doc):  6,636 tokens  → 100% accurate")
    print("   ✅ Cities (180w/doc):  14,328 tokens → 100% accurate")
    
    phi_words_per_doc = 300  # 3.3x the animal documents!
    print(f"\n📝 Using {phi_words_per_doc} words per document for Countries (3.3x Animals)")
    print(f"   This creates a progression from {context_sizes[0]*phi_words_per_doc:,} to {context_sizes[-1]*phi_words_per_doc:,} words")
    print(f"   Target: 50 docs (~15,000w / ~23K tokens) - EXTREME STRESS TEST!\n")
    
    print("❓ HYPOTHESIS: Will 3.3x larger docs FINALLY push Phi-4-mini past breaking point?")
    print("   - Same number of documents (2, 5, 10, 20, 50)")
    print("   - But 3.3x word count vs animals (300 vs 90 words)")
    print("   - Testing up to ~23,000 tokens - nearly 4x animals test!")
    print("   - This should reveal the TRUE limit...\n")
    
    for num_docs in context_sizes:
        print(f"\nGenerating {num_docs} country documents...")
        documents = generate_documents_set(num_docs, words_per_doc=phi_words_per_doc)
        
        total_words = sum(doc['word_count'] for doc in documents)
        avg_words = total_words / num_docs
        approx_tokens = int(total_words * 1.3)
        
        # Status indicator
        if total_words <= 6636:
            status = "✅ BELOW ANIMALS MAX"
        elif total_words <= 14328:
            status = "⚠️  BEYOND ANIMALS, BELOW CITIES"
        else:
            status = "❌ EXTREME - BEYOND ALL PREVIOUS TESTS"
        
        print(f"  Total words: {total_words:,} {status}")
        print(f"  Average words per doc: {avg_words:.1f}")
        print(f"  Estimated tokens: ~{approx_tokens:,}")
        
        save_documents(documents, f"documents_{num_docs}_countries.json")
    
    # ============================================================================
    # SUMMARY
    # ============================================================================
    print("\n" + "=" * 80)
    print("✓ Country document sets generated successfully!")
    print("=" * 80)
    
    print("\n📊 COUNTRIES CONTEXT SIZES (300 words/doc - TRIAL 3):")
    for n in context_sizes:
        total = n * phi_words_per_doc
        tokens = int(total * 1.3)
        if total <= 6636:
            status = "✅"
        elif total <= 14328:
            status = "⚠️ "
        else:
            status = "❌"
        print(f"   {status} {n:2d} docs: {total:6,} words (~{tokens:7,} tokens)")
    
    print("\n💡 PROGRESSION TEST:")
    print("   Trial 1 - Animals (90w):   6,636 tokens  ✅ 100%")
    print("   Trial 2 - Cities (180w):   14,328 tokens ✅ 100%")
    print("   Trial 3 - Countries (300w): ~23,000 tokens ❓ ???")
    print("\n🎯 This is the ULTIMATE test - will Phi-4-mini finally break?")
    print("=" * 80)

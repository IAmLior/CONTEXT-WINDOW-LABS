"""
Lab 2: Context Window Size Impact - Document Generator

This module generates synthetic documents about animals for testing how 
context window size affects LLM performance (latency and accuracy).
"""

import json
import random
from pathlib import Path
from typing import List, Dict


# Animal database with facts
ANIMALS = [
    {
        "name": "African Elephant",
        "scientific": "Loxodonta africana",
        "habitat": "African savannas and forests",
        "weight": "6000 kg",
        "lifespan": "60-70 years",
        "diet": "Herbivore",
        "fact": "African elephants have the longest gestation period of any mammal at 22 months"
    },
    {
        "name": "Blue Whale",
        "scientific": "Balaenoptera musculus",
        "habitat": "All major oceans",
        "weight": "150000 kg",
        "lifespan": "80-90 years",
        "diet": "Carnivore (krill)",
        "fact": "Blue whales are the largest animals ever known to have lived on Earth"
    },
    {
        "name": "Cheetah",
        "scientific": "Acinonyx jubatus",
        "habitat": "African grasslands",
        "weight": "72 kg",
        "lifespan": "10-12 years",
        "diet": "Carnivore",
        "fact": "Cheetahs can reach speeds of 120 km/h making them the fastest land animal"
    },
    {
        "name": "Giant Panda",
        "scientific": "Ailuropoda melanoleuca",
        "habitat": "Chinese mountain forests",
        "weight": "135 kg",
        "lifespan": "20 years",
        "diet": "Herbivore (bamboo)",
        "fact": "Giant pandas spend 12-16 hours a day eating bamboo"
    },
    {
        "name": "Siberian Tiger",
        "scientific": "Panthera tigris altaica",
        "habitat": "Russian far east forests",
        "weight": "320 kg",
        "lifespan": "15-18 years",
        "diet": "Carnivore",
        "fact": "Siberian tigers are the largest cats in the world"
    },
    {
        "name": "Emperor Penguin",
        "scientific": "Aptenodytes forsteri",
        "habitat": "Antarctic ice shelves",
        "weight": "40 kg",
        "lifespan": "20 years",
        "diet": "Carnivore (fish)",
        "fact": "Emperor penguins can dive to depths of 500 meters"
    },
    {
        "name": "Polar Bear",
        "scientific": "Ursus maritimus",
        "habitat": "Arctic ice",
        "weight": "450 kg",
        "lifespan": "25-30 years",
        "diet": "Carnivore",
        "fact": "Polar bears can swim continuously for days covering distances over 600 km"
    },
    {
        "name": "Mountain Gorilla",
        "scientific": "Gorilla beringei beringei",
        "habitat": "Central African mountains",
        "weight": "220 kg",
        "lifespan": "35-40 years",
        "diet": "Herbivore",
        "fact": "Mountain gorillas share 98.3% of their DNA with humans"
    },
    {
        "name": "Great White Shark",
        "scientific": "Carcharodon carcharias",
        "habitat": "Coastal ocean waters",
        "weight": "2000 kg",
        "lifespan": "70 years",
        "diet": "Carnivore",
        "fact": "Great white sharks can detect one drop of blood in 100 liters of water"
    },
    {
        "name": "Red Kangaroo",
        "scientific": "Macropus rufus",
        "habitat": "Australian deserts",
        "weight": "90 kg",
        "lifespan": "23 years",
        "diet": "Herbivore",
        "fact": "Red kangaroos can jump up to 9 meters in a single leap"
    },
    {
        "name": "Bald Eagle",
        "scientific": "Haliaeetus leucocephalus",
        "habitat": "North American forests near water",
        "weight": "6.3 kg",
        "lifespan": "20 years",
        "diet": "Carnivore (fish and small mammals)",
        "fact": "Bald eagles build the largest nests of any North American bird"
    },
    {
        "name": "Gray Wolf",
        "scientific": "Canis lupus",
        "habitat": "Northern forests and tundra",
        "weight": "80 kg",
        "lifespan": "6-8 years",
        "diet": "Carnivore",
        "fact": "Gray wolves can travel up to 50 km in a single day"
    },
    {
        "name": "Orangutan",
        "scientific": "Pongo pygmaeus",
        "habitat": "Borneo and Sumatra rainforests",
        "weight": "75 kg",
        "lifespan": "35-45 years",
        "diet": "Omnivore",
        "fact": "Orangutans share 97% of their DNA with humans"
    },
    {
        "name": "Komodo Dragon",
        "scientific": "Varanus komodoensis",
        "habitat": "Indonesian islands",
        "weight": "90 kg",
        "lifespan": "30 years",
        "diet": "Carnivore",
        "fact": "Komodo dragons are the largest living lizards in the world"
    },
    {
        "name": "California Condor",
        "scientific": "Gymnogyps californianus",
        "habitat": "Western North American mountains",
        "weight": "12 kg",
        "lifespan": "60 years",
        "diet": "Scavenger",
        "fact": "California condors have a wingspan of 3 meters"
    },
    {
        "name": "Snow Leopard",
        "scientific": "Panthera uncia",
        "habitat": "Central Asian mountains",
        "weight": "55 kg",
        "lifespan": "15-18 years",
        "diet": "Carnivore",
        "fact": "Snow leopards can leap 15 meters in distance"
    },
    {
        "name": "Hippopotamus",
        "scientific": "Hippopotamus amphibius",
        "habitat": "Sub-Saharan African rivers",
        "weight": "1500 kg",
        "lifespan": "40-50 years",
        "diet": "Herbivore",
        "fact": "Hippos can hold their breath underwater for up to 5 minutes"
    },
    {
        "name": "Giraffe",
        "scientific": "Giraffa camelopardalis",
        "habitat": "African savannas",
        "weight": "1200 kg",
        "lifespan": "25 years",
        "diet": "Herbivore",
        "fact": "Giraffes have the same number of neck vertebrae as humans: seven"
    },
    {
        "name": "Bengal Tiger",
        "scientific": "Panthera tigris tigris",
        "habitat": "Indian subcontinent forests",
        "weight": "260 kg",
        "lifespan": "15 years",
        "diet": "Carnivore",
        "fact": "Bengal tigers can eat up to 40 kg of meat in a single meal"
    },
    {
        "name": "Humpback Whale",
        "scientific": "Megaptera novaeangliae",
        "habitat": "All major oceans",
        "weight": "36000 kg",
        "lifespan": "45-50 years",
        "diet": "Carnivore (krill and small fish)",
        "fact": "Humpback whales sing complex songs that can last for 20 minutes"
    },
    {
        "name": "African Lion",
        "scientific": "Panthera leo",
        "habitat": "African grasslands and savannas",
        "weight": "190 kg",
        "lifespan": "10-14 years",
        "diet": "Carnivore",
        "fact": "African lions can roar so loud they can be heard up to 8 km away"
    },
    {
        "name": "Arctic Fox",
        "scientific": "Vulpes lagopus",
        "habitat": "Arctic tundra",
        "weight": "7 kg",
        "lifespan": "3-6 years",
        "diet": "Omnivore",
        "fact": "Arctic foxes can survive temperatures as low as -70°C"
    },
    {
        "name": "Spotted Hyena",
        "scientific": "Crocuta crocuta",
        "habitat": "Sub-Saharan Africa",
        "weight": "70 kg",
        "lifespan": "25 years",
        "diet": "Carnivore",
        "fact": "Spotted hyenas have one of the strongest bites among mammals"
    },
    {
        "name": "American Bison",
        "scientific": "Bison bison",
        "habitat": "North American grasslands",
        "weight": "900 kg",
        "lifespan": "15-20 years",
        "diet": "Herbivore",
        "fact": "American bison can run at speeds up to 55 km/h despite their massive size"
    },
    {
        "name": "Saltwater Crocodile",
        "scientific": "Crocodylus porosus",
        "habitat": "Southeast Asian coastal waters",
        "weight": "1000 kg",
        "lifespan": "70 years",
        "diet": "Carnivore",
        "fact": "Saltwater crocodiles are the largest living reptiles"
    },
    {
        "name": "Gray Whale",
        "scientific": "Eschrichtius robustus",
        "habitat": "North Pacific Ocean",
        "weight": "36000 kg",
        "lifespan": "55-70 years",
        "diet": "Carnivore (amphipods)",
        "fact": "Gray whales migrate 20,000 km annually, the longest migration of any mammal"
    },
    {
        "name": "Grizzly Bear",
        "scientific": "Ursus arctos horribilis",
        "habitat": "North American forests and mountains",
        "weight": "360 kg",
        "lifespan": "25 years",
        "diet": "Omnivore",
        "fact": "Grizzly bears can run at speeds up to 48 km/h"
    },
    {
        "name": "King Cobra",
        "scientific": "Ophiophagus hannah",
        "habitat": "South and Southeast Asian forests",
        "weight": "6 kg",
        "lifespan": "20 years",
        "diet": "Carnivore (other snakes)",
        "fact": "King cobras can grow up to 5.5 meters making them the longest venomous snakes"
    },
    {
        "name": "Manta Ray",
        "scientific": "Mobula birostris",
        "habitat": "Tropical and subtropical oceans",
        "weight": "1350 kg",
        "lifespan": "20 years",
        "diet": "Carnivore (plankton)",
        "fact": "Manta rays have the largest brain-to-body ratio of all fish"
    },
    {
        "name": "Peregrine Falcon",
        "scientific": "Falco peregrinus",
        "habitat": "Worldwide, various habitats",
        "weight": "1.5 kg",
        "lifespan": "15-20 years",
        "diet": "Carnivore (birds)",
        "fact": "Peregrine falcons can reach speeds over 320 km/h during hunting dives"
    },
    {
        "name": "Giant Tortoise",
        "scientific": "Chelonoidis niger",
        "habitat": "Galapagos Islands",
        "weight": "250 kg",
        "lifespan": "100-150 years",
        "diet": "Herbivore",
        "fact": "Giant tortoises can live for over 150 years making them one of the longest-lived animals"
    },
    {
        "name": "Black Rhinoceros",
        "scientific": "Diceros bicornis",
        "habitat": "Eastern and Southern Africa",
        "weight": "1400 kg",
        "lifespan": "35-50 years",
        "diet": "Herbivore",
        "fact": "Black rhinos can charge at speeds up to 55 km/h despite weighing over a ton"
    },
    {
        "name": "Capybara",
        "scientific": "Hydrochoerus hydrochaeris",
        "habitat": "South American wetlands",
        "weight": "65 kg",
        "lifespan": "8-10 years",
        "diet": "Herbivore",
        "fact": "Capybaras are the largest rodents in the world"
    },
    {
        "name": "Howler Monkey",
        "scientific": "Alouatta",
        "habitat": "Central and South American forests",
        "weight": "10 kg",
        "lifespan": "15-20 years",
        "diet": "Herbivore",
        "fact": "Howler monkeys produce the loudest call of any land animal"
    },
    {
        "name": "Secretary Bird",
        "scientific": "Sagittarius serpentarius",
        "habitat": "African grasslands",
        "weight": "4 kg",
        "lifespan": "12-15 years",
        "diet": "Carnivore",
        "fact": "Secretary birds kill snakes by stamping on them with powerful kicks"
    },
    {
        "name": "Narwhal",
        "scientific": "Monodon monoceros",
        "habitat": "Arctic waters",
        "weight": "1600 kg",
        "lifespan": "50 years",
        "diet": "Carnivore (fish and squid)",
        "fact": "Narwhals have a spiral tusk that can grow up to 3 meters long"
    },
    {
        "name": "Moose",
        "scientific": "Alces alces",
        "habitat": "Northern forests",
        "weight": "700 kg",
        "lifespan": "15-25 years",
        "diet": "Herbivore",
        "fact": "Moose are the largest members of the deer family"
    },
    {
        "name": "Orca",
        "scientific": "Orcinus orca",
        "habitat": "All oceans",
        "weight": "5500 kg",
        "lifespan": "50-90 years",
        "diet": "Carnivore",
        "fact": "Orcas are the largest members of the dolphin family"
    },
    {
        "name": "Platypus",
        "scientific": "Ornithorhynchus anatinus",
        "habitat": "Eastern Australian waterways",
        "weight": "1.5 kg",
        "lifespan": "17 years",
        "diet": "Carnivore (invertebrates)",
        "fact": "Platypuses are one of only five species of egg-laying mammals"
    },
    {
        "name": "Sloth",
        "scientific": "Bradypus",
        "habitat": "Central and South American rainforests",
        "weight": "5 kg",
        "lifespan": "20-30 years",
        "diet": "Herbivore",
        "fact": "Sloths sleep up to 20 hours a day"
    },
    {
        "name": "Tasmanian Devil",
        "scientific": "Sarcophilus harrisii",
        "habitat": "Tasmania",
        "weight": "12 kg",
        "lifespan": "5 years",
        "diet": "Carnivore",
        "fact": "Tasmanian devils have the strongest bite force relative to body size of any mammal"
    },
    {
        "name": "Walrus",
        "scientific": "Odobenus rosmarus",
        "habitat": "Arctic waters",
        "weight": "1700 kg",
        "lifespan": "40 years",
        "diet": "Carnivore (mollusks)",
        "fact": "Walrus tusks can grow up to 1 meter long"
    },
    {
        "name": "Wolverine",
        "scientific": "Gulo gulo",
        "habitat": "Northern forests and tundra",
        "weight": "20 kg",
        "lifespan": "5-13 years",
        "diet": "Carnivore",
        "fact": "Wolverines can take down prey much larger than themselves"
    },
    {
        "name": "Bongo",
        "scientific": "Tragelaphus eurycerus",
        "habitat": "Central African forests",
        "weight": "250 kg",
        "lifespan": "19 years",
        "diet": "Herbivore",
        "fact": "Bongos are the largest forest antelope species"
    },
    {
        "name": "Galapagos Penguin",
        "scientific": "Spheniscus mendiculus",
        "habitat": "Galapagos Islands",
        "weight": "2.5 kg",
        "lifespan": "15-20 years",
        "diet": "Carnivore (fish)",
        "fact": "Galapagos penguins are the only penguin species found north of the equator"
    },
    {
        "name": "Mandrill",
        "scientific": "Mandrillus sphinx",
        "habitat": "Central African rainforests",
        "weight": "35 kg",
        "lifespan": "20 years",
        "diet": "Omnivore",
        "fact": "Mandrills have the most colorful face of any mammal"
    },
    {
        "name": "Reticulated Python",
        "scientific": "Malayopython reticulatus",
        "habitat": "Southeast Asian forests",
        "weight": "75 kg",
        "lifespan": "20-25 years",
        "diet": "Carnivore",
        "fact": "Reticulated pythons are the longest snakes in the world reaching up to 7 meters"
    },
    {
        "name": "Snow Goose",
        "scientific": "Anser caerulescens",
        "habitat": "North American tundra and marshes",
        "weight": "3 kg",
        "lifespan": "15 years",
        "diet": "Herbivore",
        "fact": "Snow geese migrate over 5000 km between breeding and wintering grounds"
    },
    {
        "name": "Sun Bear",
        "scientific": "Helarctos malayanus",
        "habitat": "Southeast Asian rainforests",
        "weight": "65 kg",
        "lifespan": "25 years",
        "diet": "Omnivore",
        "fact": "Sun bears have the longest tongues of any bear species at 25 cm"
    },
    {
        "name": "Spectacled Bear",
        "scientific": "Tremarctos ornatus",
        "habitat": "South American Andes",
        "weight": "140 kg",
        "lifespan": "20 years",
        "diet": "Omnivore",
        "fact": "Spectacled bears are the only bear species native to South America"
    }
]


# Filler sentences to add context and increase document length
FILLER_SENTENCES = [
    "Conservation efforts are crucial for protecting endangered species.",
    "Climate change affects wildlife habitats across the globe.",
    "Biodiversity is essential for ecosystem health and stability.",
    "Wildlife researchers use various tracking technologies to study animal behavior.",
    "Protected areas and national parks play a vital role in species preservation.",
    "Human activities have significant impacts on natural habitats.",
    "Ecosystem restoration projects help rebuild damaged environments.",
    "Genetic diversity within populations is critical for species survival.",
    "Migration patterns are influenced by seasonal changes and food availability.",
    "Predator-prey relationships maintain ecological balance in ecosystems.",
    "Endangered species programs work to prevent extinction.",
    "Habitat fragmentation is a major threat to wildlife populations.",
    "Captive breeding programs contribute to species recovery efforts.",
    "Wildlife corridors enable animals to move between protected areas.",
    "Citizen science projects engage the public in conservation research.",
    "Invasive species can disrupt native ecosystems dramatically.",
    "Sustainable practices help minimize human impact on nature.",
    "Environmental education raises awareness about conservation issues.",
    "International cooperation is necessary for global conservation success.",
    "Technology advances improve our ability to monitor wildlife populations.",
]


def generate_animal_document(animal: Dict[str, str], word_target: int = 300) -> str:
    """
    Generate a descriptive document about a specific animal.
    
    Args:
        animal: Dictionary containing animal information
        word_target: Target word count for the document
        
    Returns:
        Formatted document text about the animal
    """
    # Start with basic introduction
    doc_parts = []
    
    # Title and intro
    doc_parts.append(f"# {animal['name']}\n")
    doc_parts.append(f"Scientific name: {animal['scientific']}\n")
    
    # Basic facts paragraph
    doc_parts.append(
        f"The {animal['name']} ({animal['scientific']}) is a fascinating {animal['diet'].lower()} "
        f"found primarily in {animal['habitat']}. "
        f"These remarkable creatures typically weigh around {animal['weight']} "
        f"and can live up to {animal['lifespan']} in the wild. "
    )
    
    # Add the unique fact
    doc_parts.append(f"{animal['fact']}. ")
    
    # Add filler content to reach target word count
    current_text = ''.join(doc_parts)
    current_words = len(current_text.split())
    
    # Shuffle filler sentences for variety
    filler_pool = FILLER_SENTENCES.copy()
    random.shuffle(filler_pool)
    filler_index = 0
    
    while current_words < word_target:
        doc_parts.append(filler_pool[filler_index] + " ")
        current_words = len(''.join(doc_parts).split())
        filler_index += 1
        
        # Reshuffle when we run out of filler sentences
        if filler_index >= len(filler_pool):
            random.shuffle(filler_pool)
            filler_index = 0
    
    return ''.join(doc_parts).strip()


def generate_documents_set(num_documents: int, words_per_doc: int = 300) -> List[Dict[str, str]]:
    """
    Generate a set of animal documents.
    
    Args:
        num_documents: Number of documents to generate
        words_per_doc: Target word count per document
        
    Returns:
        List of document dictionaries with metadata
    """
    if num_documents > len(ANIMALS):
        raise ValueError(f"Cannot generate {num_documents} documents. Only {len(ANIMALS)} animals available.")
    
    # Select random animals
    selected_animals = random.sample(ANIMALS, num_documents)
    
    documents = []
    for i, animal in enumerate(selected_animals):
        doc_text = generate_animal_document(animal, words_per_doc)
        
        documents.append({
            "id": i + 1,
            "animal": animal["name"],
            "scientific_name": animal["scientific"],
            "text": doc_text,
            "word_count": len(doc_text.split()),
            "key_fact": animal["fact"]
        })
    
    return documents


def save_documents(documents: List[Dict[str, str]], filename: str):
    """
    Save generated documents to a JSON file.
    
    Args:
        documents: List of document dictionaries
        filename: Output filename (without path)
    """
    output_dir = Path(__file__).parent / "data"
    output_dir.mkdir(exist_ok=True)
    
    output_path = output_dir / filename
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(documents, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Saved {len(documents)} documents to {output_path}")


def load_documents(filename: str) -> List[Dict[str, str]]:
    """
    Load documents from a JSON file.
    
    Args:
        filename: Input filename (without path)
        
    Returns:
        List of document dictionaries
    """
    input_path = Path(__file__).parent / "data" / filename
    
    if not input_path.exists():
        raise FileNotFoundError(f"Document file not found: {input_path}")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        documents = json.load(f)
    
    print(f"✓ Loaded {len(documents)} documents from {input_path}")
    return documents


if __name__ == "__main__":
    """Generate documents for various context sizes."""
    
    print("=" * 80)
    print("LAB 2: CONTEXT WINDOW SIZE IMPACT")
    print("Generating Animal Documents for Two Models")
    print("=" * 80)
    
    # Generate document sets for different context sizes: 2, 5, 10, 20, 50 documents
    context_sizes = [2, 5, 10, 20, 50]
    
    # Generate TWO sets with different document sizes for each model
    
    # ============================================================================
    # PHI-4-MINI DOCUMENTS (400 words each)
    # ============================================================================
    print("\n" + "🤖 " * 20)
    print("GENERATING DOCUMENTS FOR PHI-4-MINI-INSTRUCT")
    print("🤖 " * 20)
    print("\n📊 From Lab 1 Trial 5, Phi-4-mini limits:")
    print("   ✅ 3,500 words: 100% accurate (safe)")
    print("   ⚠️  4,000 words: ~60% accurate (unstable)")
    print("   ❌ 5,000 words: 0% accurate (complete failure)")
    
    phi_words_per_doc = 90
    print(f"\n📝 Using {phi_words_per_doc} words per document for Phi-4-mini")
    print(f"   This creates a progression from {context_sizes[0]*phi_words_per_doc:,} to {context_sizes[-1]*phi_words_per_doc:,} words")
    print(f"   Target: 20 docs (~1,800w) should PASS ✅, 50 docs (~4,500w) should FAIL ❌\n")
    
    for num_docs in context_sizes:
        print(f"\nGenerating {num_docs} documents for Phi-4-mini...")
        documents = generate_documents_set(num_docs, words_per_doc=phi_words_per_doc)
        
        total_words = sum(doc['word_count'] for doc in documents)
        avg_words = total_words / num_docs
        approx_tokens = int(total_words * 1.3)
        
        # Status indicator based on Lab 1 findings
        if total_words <= 3500:
            status = "✅ SAFE"
        elif total_words <= 4500:
            status = "⚠️  UNSTABLE"
        else:
            status = "❌ EXPECT FAILURE"
        
        print(f"  Total words: {total_words:,} {status}")
        print(f"  Average words per doc: {avg_words:.1f}")
        print(f"  Estimated tokens: ~{approx_tokens:,}")
        
        save_documents(documents, f"documents_{num_docs}_phi4mini.json")
    
    # ============================================================================
    # SUMMARY
    # ============================================================================
    print("\n" + "=" * 80)
    print("✓ Phi-4-mini document sets generated successfully!")
    print("=" * 80)
    
    print("\n📊 PHI-4-MINI CONTEXT SIZES (90 words/doc):")
    for n in context_sizes:
        total = n * phi_words_per_doc
        tokens = int(total * 1.3)
        if total <= 3500:
            status = "✅"
        elif total <= 4500:
            status = "⚠️ "
        else:
            status = "❓"
        print(f"   {status} {n:2d} docs: {total:6,} words (~{tokens:6,} tokens)")
    
    print("\n💡 HYPOTHESIS:")
    print("   Lab 1 (complex task): Failed at 5,000 words")
    print("   Lab 2 (simple task): Will it succeed at 4,500+ words?")
    print("   Testing if context limits are TASK-DEPENDENT!")
    print("=" * 80)

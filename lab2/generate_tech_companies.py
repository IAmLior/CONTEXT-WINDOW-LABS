"""
Generate tech companies dataset for Lab 2 - Trial 4
Each company document is ~400 words (4.4x the animals baseline)
Testing extreme document size to find complete failure threshold
"""

import json
import random
import os

def generate_tech_company_document(company_name, industry, founded_year, headquarters, key_fact):
    """
    Generate a ~400-word document about a tech company.
    Much larger than countries (300w) to test beyond the instability threshold.
    """
    
    # Base content (~100 words)
    base_info = f"""{company_name} is a prominent technology company in the {industry} industry. 
Founded in {founded_year}, the company has established itself as a major player in the global tech ecosystem. 
Headquartered in {headquarters}, {company_name} has grown to become one of the most recognized names in technology. 
The company's innovative approach and commitment to excellence have earned it numerous accolades and industry recognition. 
With operations spanning multiple continents, {company_name} continues to push the boundaries of what's possible in {industry}."""

    # Business operations (~100 words)
    operations = f"""The company operates through multiple business divisions, each focused on different aspects of {industry}. 
{company_name}'s revenue streams are diversified across various product lines and service offerings, ensuring stable growth and market resilience. 
The organization employs thousands of skilled professionals, including engineers, designers, product managers, and business strategists. 
Their corporate culture emphasizes innovation, collaboration, and continuous learning. The company invests heavily in research and development, 
allocating a significant portion of annual revenue to exploring emerging technologies and developing next-generation solutions that meet evolving market demands."""

    # Market presence (~100 words)  
    market_presence = f"""In the competitive landscape of {industry}, {company_name} has carved out a distinctive market position through strategic partnerships, 
acquisitions, and organic growth initiatives. The company's brand value has consistently ranked among the top in the technology sector. 
Customer satisfaction ratings remain high, reflecting the quality and reliability of their products and services. 
{company_name} maintains strong relationships with enterprise clients, government agencies, and individual consumers worldwide. 
Their go-to-market strategy combines direct sales, channel partnerships, and digital distribution platforms to reach diverse customer segments effectively."""

    # Key fact and future (~100 words)
    future_outlook = f"""Looking ahead, {company_name} continues to invest in emerging technologies such as artificial intelligence, cloud computing, 
cybersecurity, and sustainable technology solutions. The company's leadership team has outlined ambitious growth targets for the coming years. 
Environmental, social, and governance (ESG) initiatives have become central to the company's strategic planning and operational execution. 
A notable characteristic of {company_name} is that {key_fact}. This unique aspect sets the company apart from competitors and contributes 
to its sustained success in the marketplace. Analysts predict continued growth and market expansion as the company leverages its technological 
capabilities and market expertise to capitalize on new opportunities in the evolving digital economy."""

    full_document = f"{base_info}\n\n{operations}\n\n{market_presence}\n\n{future_outlook}"
    
    word_count = len(full_document.split())
    
    return {
        "company": company_name,
        "industry": industry,
        "founded": founded_year,
        "headquarters": headquarters,
        "key_fact": key_fact,
        "content": full_document,
        "word_count": word_count
    }

def generate_all_companies():
    """Generate 50 unique tech companies with diverse characteristics."""
    
    companies_data = [
        ("Apple Inc.", "Consumer Electronics", 1976, "Cupertino, California", 
         "it was the first company to reach a market capitalization of three trillion dollars"),
        
        ("Microsoft Corporation", "Software and Cloud Services", 1975, "Redmond, Washington",
         "it generates over two hundred billion dollars in annual revenue from cloud services alone"),
        
        ("Alphabet Inc.", "Internet Services", 1998, "Mountain View, California",
         "it processes over eight billion search queries every single day across the globe"),
        
        ("Amazon.com", "E-commerce and Cloud", 1994, "Seattle, Washington",
         "it delivers over ten million packages daily and employs more than one and a half million people worldwide"),
        
        ("Meta Platforms", "Social Media", 2004, "Menlo Park, California",
         "it connects over three billion monthly active users across its family of applications"),
        
        ("Tesla Inc.", "Electric Vehicles", 2003, "Austin, Texas",
         "it produces more than one and a half million electric vehicles annually with fully integrated battery production"),
        
        ("NVIDIA Corporation", "Semiconductors and AI", 1993, "Santa Clara, California",
         "it controls over eighty percent of the discrete graphics processing unit market worldwide"),
        
        ("Samsung Electronics", "Consumer Electronics", 1969, "Suwon, South Korea",
         "it manufactures over three hundred million smartphones annually and leads the global memory chip market"),
        
        ("Intel Corporation", "Semiconductors", 1968, "Santa Clara, California",
         "it invests over fifteen billion dollars annually in semiconductor research and manufacturing capabilities"),
        
        ("IBM", "Enterprise Technology", 1911, "Armonk, New York",
         "it holds more patents than any other technology company with over one hundred thousand active patents"),
        
        ("Oracle Corporation", "Database Software", 1977, "Austin, Texas",
         "it manages database systems for ninety percent of Fortune 100 companies worldwide"),
        
        ("Salesforce", "Cloud CRM", 1999, "San Francisco, California",
         "it pioneered the Software-as-a-Service model and serves over one hundred fifty thousand customers globally"),
        
        ("Adobe Inc.", "Creative Software", 1982, "San Jose, California",
         "it created the PDF format and its Creative Cloud serves over thirty million subscribers"),
        
        ("Netflix", "Streaming Entertainment", 1997, "Los Gatos, California",
         "it streams over one billion hours of content every week to subscribers in over one hundred ninety countries"),
        
        ("Spotify", "Music Streaming", 2006, "Stockholm, Sweden",
         "it offers access to over one hundred million songs and podcasts to more than six hundred million users"),
        
        ("Uber Technologies", "Ride Sharing", 2009, "San Francisco, California",
         "it completes over twenty million trips per day across seventy countries on six continents"),
        
        ("Airbnb", "Hospitality Platform", 2008, "San Francisco, California",
         "it lists over seven million properties worldwide and has facilitated over one billion guest arrivals"),
        
        ("PayPal", "Digital Payments", 1998, "San Jose, California",
         "it processes over twenty billion dollars in payment volume every single day across two hundred markets"),
        
        ("Square (Block)", "Financial Services", 2009, "San Francisco, California",
         "it serves over four million merchant locations and processes hundreds of billions in annual payment volume"),
        
        ("Shopify", "E-commerce Platform", 2006, "Ottawa, Canada",
         "it powers over two million online stores that collectively generate over five hundred billion in sales"),
        
        ("Zoom Video", "Video Communications", 2011, "San Jose, California",
         "it hosts over three billion meeting minutes daily and became essential infrastructure during global remote work transition"),
        
        ("Slack Technologies", "Business Communication", 2013, "San Francisco, California",
         "it facilitates over nine million messages per minute for teams across more than one hundred fifty countries"),
        
        ("Twilio", "Cloud Communications", 2008, "San Francisco, California",
         "it powers communications for over three hundred thousand businesses processing trillions of interactions annually"),
        
        ("Atlassian", "Collaboration Software", 2002, "Sydney, Australia",
         "it serves over three hundred thousand customers with no direct sales force using a product-led growth strategy"),
        
        ("ServiceNow", "Workflow Automation", 2004, "Santa Clara, California",
         "it manages digital workflows for over eighty-five percent of Fortune 500 companies globally"),
        
        ("Workday", "Enterprise Cloud", 2005, "Pleasanton, California",
         "it processes payroll for over fifty million workers across ten thousand organizations worldwide"),
        
        ("Snowflake", "Cloud Data Platform", 2012, "Bozeman, Montana",
         "it enables organizations to analyze exabytes of data with near-infinite scalability across multiple clouds"),
        
        ("Databricks", "Data Analytics", 2013, "San Francisco, California",
         "it processes over one exabyte of data daily for thousands of enterprises using unified analytics"),
        
        ("Palantir Technologies", "Data Analytics", 2003, "Denver, Colorado",
         "it provides data analysis platforms for intelligence agencies and serves over three hundred commercial customers"),
        
        ("CrowdStrike", "Cybersecurity", 2011, "Austin, Texas",
         "it protects over twenty-four thousand customers by analyzing six trillion security events weekly"),
        
        ("Cloudflare", "Internet Infrastructure", 2009, "San Francisco, California",
         "it handles over forty-six million HTTP requests per second protecting millions of websites globally"),
        
        ("Datadog", "Monitoring Platform", 2010, "New York, New York",
         "it monitors over twenty-five thousand customers infrastructure processing trillions of data points daily"),
        
        ("HashiCorp", "Cloud Infrastructure", 2012, "San Francisco, California",
         "it enables multi-cloud infrastructure automation for over two thousand enterprise customers worldwide"),
        
        ("GitLab", "DevOps Platform", 2011, "San Francisco, California",
         "it serves over thirty million developers with an all-remote company structure of over two thousand employees"),
        
        ("MongoDB", "Database Technology", 2007, "New York, New York",
         "it powers over forty-three thousand customers applications with its document-oriented database platform"),
        
        ("Elastic", "Search and Analytics", 2012, "Mountain View, California",
         "it processes over one trillion searches annually for thousands of enterprises across multiple industries"),
        
        ("Splunk", "Data Platform", 2003, "San Francisco, California",
         "it analyzes machine data from millions of sources helping organizations gain operational intelligence"),
        
        ("HubSpot", "Marketing Platform", 2006, "Cambridge, Massachusetts",
         "it serves over two hundred thousand customers across more than one hundred twenty countries worldwide"),
        
        ("Zendesk", "Customer Service", 2007, "San Francisco, California",
         "it powers customer service for over one hundred sixty thousand businesses processing billions of support interactions"),
        
        ("DocuSign", "Digital Agreement", 2003, "San Francisco, California",
         "it has facilitated over two billion electronic signatures across one hundred eighty countries globally"),
        
        ("RingCentral", "Cloud Communications", 2003, "Belmont, California",
         "it delivers communications services to over four hundred thousand businesses with billions of connection minutes"),
        
        ("Okta", "Identity Management", 2009, "San Francisco, California",
         "it secures identities for over eighteen thousand organizations with billions of authentication transactions monthly"),
        
        ("Zscaler", "Cloud Security", 2008, "San Jose, California",
         "it processes over three hundred billion transactions daily protecting users across one hundred fifty countries"),
        
        ("Palo Alto Networks", "Cybersecurity", 2005, "Santa Clara, California",
         "it protects over eighty-five thousand customers with next-generation firewalls and cloud security platforms"),
        
        ("Fortinet", "Network Security", 2000, "Sunnyvale, California",
         "it secures over seven hundred thousand customers worldwide with integrated security fabric architecture"),
        
        ("Autodesk", "Design Software", 1982, "San Francisco, California",
         "it enables design of ninety-five percent of automotive designs globally with software used by millions"),
        
        ("Intuit", "Financial Software", 1983, "Mountain View, California",
         "it serves over one hundred million customers with TurboTax QuickBooks and other financial management tools"),
        
        ("VMware", "Cloud Infrastructure", 1998, "Palo Alto, California",
         "it virtualizes infrastructure for over five hundred thousand customers running millions of workloads"),
        
        ("Red Hat", "Open Source Software", 1993, "Raleigh, North Carolina",
         "it delivers enterprise Linux and open-source solutions to ninety percent of Fortune 500 companies"),
        
        ("SAP SE", "Enterprise Software", 1972, "Walldorf, Germany",
         "it runs business operations for over four hundred forty thousand customers including ninety-two percent of Forbes Global 2000 companies")
    ]
    
    return companies_data

def main():
    print("🏢 GENERATING TECH COMPANIES DATASET - TRIAL 4")
    print("=" * 70)
    print("Target: 400 words per document (4.4x animals, 1.33x countries)")
    print("Testing: Extreme document size to find complete failure threshold")
    print("=" * 70)
    print()
    
    companies = generate_all_companies()
    
    # Create data directory if it doesn't exist
    data_dir = os.path.join("lab2", "data")
    os.makedirs(data_dir, exist_ok=True)
    
    # Document counts to test
    test_sizes = [2, 5, 10, 20, 50]
    
    total_words = 0
    total_docs = 0
    
    for size in test_sizes:
        # Select random companies for this test size
        selected = random.sample(companies, size)
        
        documents = []
        test_words = 0
        
        for company_data in selected:
            doc = generate_tech_company_document(*company_data)
            documents.append(doc)
            test_words += doc["word_count"]
            total_words += doc["word_count"]
            total_docs += 1
        
        # Save to JSON
        filename = os.path.join(data_dir, f"documents_{size}_tech_companies.json")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(documents, f, indent=2, ensure_ascii=False)
        
        avg_words = test_words / size
        estimated_tokens = int(test_words * 1.3)  # Rough token estimate
        
        print(f"✓ Generated {size} documents: {test_words:,} words (~{estimated_tokens:,} tokens)")
        print(f"  Average: {avg_words:.0f} words/doc")
        print(f"  Saved to: {filename}")
        print()
    
    avg_doc_size = total_words / total_docs
    print("=" * 70)
    print(f"✅ DATASET COMPLETE")
    print(f"📊 Total: {total_docs} documents, {total_words:,} words")
    print(f"📏 Average document size: {avg_doc_size:.0f} words")
    print()
    print("Expected context sizes:")
    print("  2 docs  = ~800 words     (~1,040 tokens)")
    print("  5 docs  = ~2,000 words   (~2,600 tokens)")
    print("  10 docs = ~4,000 words   (~5,200 tokens)")
    print("  20 docs = ~8,000 words   (~10,400 tokens)")
    print("  50 docs = ~20,000 words  (~26,000 tokens)")
    print()
    print("⚠️  PREDICTION: Expect high failure rate (300w/doc showed 60-80% accuracy)")
    print("❓ QUESTION: Will 400w/doc cause complete failure or just more instability?")
    print("=" * 70)

if __name__ == "__main__":
    main()

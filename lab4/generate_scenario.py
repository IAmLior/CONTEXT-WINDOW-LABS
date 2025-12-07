"""
Generate a multi-step scenario that simulates an agent performing actions.
Each step produces state updates and facts that grow the history.
"""
import json
import os

def generate_detective_scenario(num_steps=10):
    """
    Generate a detective investigation scenario where an agent discovers clues over time.
    Each step reveals new information about a mystery.
    
    Args:
        num_steps: Number of investigation steps
        
    Returns:
        dict with:
        - steps: list of step descriptions
        - ground_truth: correct answers to evaluation questions
        - questions: questions to ask at each step
    """
    
    # Define a coherent story that unfolds over steps
    story_steps = [
        {
            "step": 1,
            "action": "Arrive at crime scene",
            "observations": "The office window is broken from the outside. Glass shards are scattered on the floor inside. A laptop is missing from the desk. The safe is closed but shows scratches around the lock.",
            "time": "Monday 9:00 AM"
        },
        {
            "step": 2,
            "action": "Interview witness",
            "observations": "Security guard Tom reports seeing a person in a red jacket near the building at 7:30 AM. The person was carrying a large backpack. Tom didn't get a clear view of their face.",
            "time": "Monday 9:30 AM"
        },
        {
            "step": 3,
            "action": "Examine security footage",
            "observations": "Camera footage shows the person in red jacket has long dark hair. They used a crowbar to break the window. The footage timestamp is 7:45 AM. The person spent exactly 12 minutes inside.",
            "time": "Monday 10:00 AM"
        },
        {
            "step": 4,
            "action": "Forensic analysis",
            "observations": "Fingerprints on the window frame match Sarah Chen, a former employee who was fired three months ago. Hair samples found match the description from footage. Crowbar was left at the scene with serial number traced to hardware store on Elm Street.",
            "time": "Monday 11:30 AM"
        },
        {
            "step": 5,
            "action": "Check employee records",
            "observations": "Sarah Chen worked as an accountant for 5 years. She had access to the office and knew the layout. Her termination was due to a dispute over expense reports. Her last known address is 742 Oak Avenue.",
            "time": "Monday 1:00 PM"
        },
        {
            "step": 6,
            "action": "Visit hardware store",
            "observations": "Store clerk at Elm Street confirms selling a crowbar to a woman matching Sarah's description on Friday afternoon. She paid cash. The clerk remembers she asked about lock-picking tools but he refused to sell them.",
            "time": "Monday 2:30 PM"
        },
        {
            "step": 7,
            "action": "Investigate suspect's home",
            "observations": "At 742 Oak Avenue, neighbors report Sarah moved out two weeks ago. She mentioned relocating to Seattle. Landlord says she paid rent until end of month but left suddenly. No forwarding address provided.",
            "time": "Monday 4:00 PM"
        },
        {
            "step": 8,
            "action": "Check financial records",
            "observations": "Sarah's bank account shows large withdrawals totaling $15,000 in the past month. Credit card activity shows purchases of camping gear and a one-way bus ticket to Seattle dated for Tuesday morning. Last transaction was at a coffee shop near the crime scene on Monday at 8:30 AM.",
            "time": "Monday 5:30 PM"
        },
        {
            "step": 9,
            "action": "Analyze stolen laptop",
            "observations": "IT department confirms the stolen laptop contained sensitive financial documents. These documents allegedly show evidence of company fraud that Sarah had discovered before her termination. The safe contained backup drives with the same information - it was not opened.",
            "time": "Tuesday 9:00 AM"
        },
        {
            "step": 10,
            "action": "Locate suspect",
            "observations": "Sarah Chen was apprehended at the Seattle bus station. She confessed to the break-in, stating she needed evidence of the fraud to clear her name. The laptop was recovered intact. She claims her termination was retaliation for reporting suspicious accounting practices.",
            "time": "Tuesday 2:00 PM"
        }
    ]
    
    # Questions that require understanding the cumulative history
    questions_per_step = [
        "What crime was committed?",  # Step 1
        "Who is the suspect based on witness description?",  # Step 2
        "What time did the break-in occur?",  # Step 3
        "What is the name of the identified suspect?",  # Step 4
        "What was Sarah Chen's previous job at the company?",  # Step 5
        "Where did Sarah buy the crowbar?",  # Step 6
        "Where did Sarah Chen move to?",  # Step 7
        "How much money did Sarah withdraw recently?",  # Step 8
        "What information was on the stolen laptop?",  # Step 9
        "Why did Sarah Chen commit the break-in?"  # Step 10
    ]
    
    # Ground truth answers (what a perfect system should answer)
    ground_truth_answers = [
        "A break-in and theft of a laptop from an office",
        "A person wearing a red jacket with a backpack",
        "7:45 AM on Monday",
        "Sarah Chen",
        "Accountant",
        "Hardware store on Elm Street",
        "Seattle",
        "$15,000",
        "Sensitive financial documents showing evidence of company fraud",
        "To obtain evidence of fraud to clear her name after being wrongfully terminated"
    ]
    
    scenario = {
        "scenario_type": "detective_investigation",
        "num_steps": num_steps,
        "steps": story_steps[:num_steps],
        "questions": questions_per_step[:num_steps],
        "ground_truth": ground_truth_answers[:num_steps],
        "description": "A detective investigates a break-in where a former employee stole a laptop containing evidence of corporate fraud."
    }
    
    return scenario


def save_scenario(scenario, output_dir="data"):
    """Save scenario to JSON file."""
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"scenario_{scenario['scenario_type']}_{scenario['num_steps']}steps.json"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(scenario, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Saved scenario to {filepath}")
    print(f"  - {scenario['num_steps']} steps")
    print(f"  - {len(scenario['questions'])} evaluation questions")
    
    return filepath


if __name__ == "__main__":
    # Generate the detective scenario
    scenario = generate_detective_scenario(num_steps=10)
    
    # Save to file
    save_scenario(scenario, output_dir="lab4/data")
    
    print("\n" + "="*60)
    print("Scenario Overview:")
    print("="*60)
    print(f"\nType: {scenario['scenario_type']}")
    print(f"Steps: {scenario['num_steps']}")
    print(f"\nDescription: {scenario['description']}")
    print(f"\nFirst step: {scenario['steps'][0]['action']}")
    print(f"Last step: {scenario['steps'][-1]['action']}")
    print(f"\nFirst question: {scenario['questions'][0]}")
    print(f"Last question: {scenario['questions'][-1]}")

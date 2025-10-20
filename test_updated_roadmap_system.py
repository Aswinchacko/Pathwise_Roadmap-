"""
Test script for the updated roadmap system
Tests various queries to verify the improved matching algorithm
"""
import requests
import json

API_URL = "http://localhost:8003/api/roadmap/generate-roadmap"

def test_roadmap(goal, domain=None):
    """Test roadmap generation for a given goal"""
    print("\n" + "=" * 80)
    print(f"Testing: {goal}")
    if domain:
        print(f"Domain: {domain}")
    print("=" * 80)
    
    payload = {
        "goal": goal,
        "domain": domain,
        "user_id": "test_user"
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"\n✓ Match Found!")
            print(f"  Title: {data['title']}")
            print(f"  Domain: {data['domain']}")
            print(f"  Difficulty: {data.get('difficulty', 'N/A')}")
            print(f"  Estimated Hours: {data.get('estimated_hours', 'N/A')}")
            print(f"  Match Score: {data.get('match_score', 'N/A')}")
            print(f"\n  Steps: {len(data.get('steps', []))} categories")
            for i, step in enumerate(data.get('steps', [])[:3], 1):  # Show first 3
                print(f"    {i}. {step['category']} ({len(step['skills'])} skills)")
            if len(data.get('steps', [])) > 3:
                print(f"    ... and {len(data.get('steps', [])) - 3} more categories")
            
            print(f"\n  Prerequisites: {data.get('prerequisites', 'N/A')[:100]}...")
            print(f"  Learning Outcomes: {data.get('learning_outcomes', 'N/A')[:100]}...")
        else:
            print(f"✗ Error: {response.status_code}")
            print(response.text)
    except requests.exceptions.ConnectionError:
        print("✗ Error: Could not connect to roadmap API. Make sure it's running on http://localhost:8003")
    except Exception as e:
        print(f"✗ Error: {e}")

def main():
    print("\n" + "🚀" * 40)
    print("Testing Updated Roadmap System")
    print("🚀" * 40)
    
    # Test cases for the new comprehensive dataset
    test_cases = [
        ("Full Stack Web Developer", "Full Stack Development"),
        ("AI Engineer", "Machine Learning"),
        ("React Native Developer", "Mobile Development"),
        ("DevOps Engineer", "DevOps"),
        ("Cybersecurity Specialist", "Cybersecurity"),
        ("Data Engineer", "Data Engineering"),
        ("UI/UX Designer", "Design"),
        ("Backend Python Developer", "Backend Development"),
        ("Blockchain Developer", "Blockchain"),
        ("Cloud Architect", "Cloud Computing"),
        ("Unity Game Developer", "Game Development"),
        ("iOS Developer", "Mobile Development"),
        ("Android Developer", "Mobile Development"),
        ("Product Manager", "Product Management"),
        ("Site Reliability Engineer", "DevOps"),
        ("QA Automation Engineer", "Quality Assurance"),
        ("Technical Writer", "Technical Writing"),
        ("Data Analyst", "Data Analytics"),
        ("Digital Marketing", "Digital Marketing"),
        ("Graphic Designer", "Design"),
        # Test generic queries
        ("I want to become a full stack developer", None),
        ("machine learning and AI", None),
        ("mobile app development", None),
        ("cybersecurity and ethical hacking", None),
        ("cloud computing AWS", None),
    ]
    
    for goal, domain in test_cases:
        test_roadmap(goal, domain)
    
    print("\n" + "=" * 80)
    print("✓ Testing complete!")
    print("=" * 80)

if __name__ == "__main__":
    main()


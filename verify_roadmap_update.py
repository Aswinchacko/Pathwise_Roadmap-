"""
Quick verification script for the updated roadmap system
Checks database and shows sample roadmaps
"""
import os
from pymongo import MongoClient
from datetime import datetime

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "pathwise")

# Initialize MongoDB client
client = MongoClient(MONGODB_URL)
db = client[DATABASE_NAME]
roadmap_collection = db["roadmap"]

def main():
    print("\n" + "=" * 80)
    print("ROADMAP SYSTEM VERIFICATION")
    print("=" * 80)
    
    # Check connection
    try:
        client.admin.command('ping')
        print("[OK] Connected to MongoDB")
    except Exception as e:
        print(f"[ERROR] MongoDB connection failed: {e}")
        return
    
    # Count roadmaps
    total_count = roadmap_collection.count_documents({"source": "csv_import"})
    print(f"\n[OK] Total roadmaps in database: {total_count}")
    
    # Count by dataset
    print("\n" + "-" * 80)
    print("ROADMAPS BY DATASET:")
    print("-" * 80)
    
    datasets = [
        "comprehensive_roadmap_dataset.csv",
        "enhanced_roadmap_datasets.csv", 
        "cross_domain_roadmaps_520.csv"
    ]
    
    for dataset in datasets:
        count = roadmap_collection.count_documents({"dataset_source": dataset})
        print(f"  {dataset}: {count} roadmaps")
    
    # Show comprehensive dataset roadmaps
    print("\n" + "-" * 80)
    print("COMPREHENSIVE DATASET ROADMAPS (Sample):")
    print("-" * 80)
    
    comprehensive_roadmaps = list(roadmap_collection.find(
        {"dataset_source": "comprehensive_roadmap_dataset.csv"}
    ).limit(20))
    
    for i, roadmap in enumerate(comprehensive_roadmaps, 1):
        print(f"\n{i}. {roadmap['goal']}")
        print(f"   Domain: {roadmap['domain']}")
        print(f"   Difficulty: {roadmap.get('difficulty', 'N/A')}")
        print(f"   Estimated Hours: {roadmap.get('estimated_hours', 'N/A')}")
        print(f"   Categories: {len(roadmap.get('steps', []))}")
        total_skills = sum(len(step['skills']) for step in roadmap.get('steps', []))
        print(f"   Total Skills: {total_skills}")
        
        # Show first 2 categories as sample
        if roadmap.get('steps'):
            print(f"   Sample Categories:")
            for step in roadmap['steps'][:2]:
                print(f"     - {step['category']} ({len(step['skills'])} skills)")
    
    # Show domains
    print("\n" + "-" * 80)
    print("ALL DOMAINS COVERED:")
    print("-" * 80)
    
    domains = sorted(roadmap_collection.distinct("domain", {"source": "csv_import"}))
    for i, domain in enumerate(domains, 1):
        count = roadmap_collection.count_documents({"domain": domain, "source": "csv_import"})
        print(f"  {i}. {domain} ({count} roadmaps)")
    
    # Show difficulty distribution
    print("\n" + "-" * 80)
    print("DIFFICULTY DISTRIBUTION:")
    print("-" * 80)
    
    difficulties = roadmap_collection.distinct("difficulty", {"source": "csv_import"})
    for difficulty in sorted(difficulties):
        count = roadmap_collection.count_documents({"difficulty": difficulty, "source": "csv_import"})
        print(f"  {difficulty}: {count} roadmaps")
    
    # Test matching algorithm
    print("\n" + "-" * 80)
    print("MATCHING ALGORITHM TEST:")
    print("-" * 80)
    
    test_queries = [
        "Full Stack Web Developer",
        "AI Engineer",
        "Mobile Developer React Native",
        "DevOps Engineer",
        "Blockchain Developer"
    ]
    
    for query in test_queries:
        # Simple search
        results = list(roadmap_collection.find(
            {"goal": {"$regex": query, "$options": "i"}},
            {"goal": 1, "domain": 1, "difficulty": 1}
        ).limit(1))
        
        if results:
            print(f"\n  Query: '{query}'")
            print(f"  Match: {results[0]['goal']}")
            print(f"  Domain: {results[0]['domain']}")
        else:
            print(f"\n  Query: '{query}' - No exact match (will use semantic matching)")
    
    print("\n" + "=" * 80)
    print("[SUCCESS] Roadmap system verification complete!")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Start the roadmap API: cd roadmap_api && python main.py")
    print("2. Test with: python test_updated_roadmap_system.py")
    print("3. Use in your application!")
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()


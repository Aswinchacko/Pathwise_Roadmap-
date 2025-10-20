"""
Script to reload roadmap data into MongoDB
This will clear existing CSV imports and reload fresh data from all datasets
"""
import os
from pymongo import MongoClient
from datetime import datetime
import pandas as pd

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "pathwise")

# Initialize MongoDB client
client = MongoClient(MONGODB_URL)
db = client[DATABASE_NAME]
roadmap_collection = db["roadmap"]

def parse_roadmap_steps(roadmap_text: str):
    """Parse roadmap text into structured steps"""
    steps = []
    
    # Split by | to get main categories
    categories = roadmap_text.split(' | ')
    
    for category in categories:
        if ':' in category:
            category_name, skills_text = category.split(':', 1)
            category_name = category_name.strip()
            # Split skills by semicolon and clean them up
            skills = [skill.strip() for skill in skills_text.split(';') if skill.strip()]
            
            steps.append({
                "category": category_name,
                "skills": skills
            })
    
    return steps

def load_roadmap_datasets():
    """Load roadmap data from multiple CSV sources"""
    datasets = [
        "comprehensive_roadmap_dataset.csv",
        "enhanced_roadmap_datasets.csv",
        "cross_domain_roadmaps_520.csv"
    ]
    
    all_roadmaps = []
    
    for dataset_path in datasets:
        try:
            df = pd.read_csv(dataset_path)
            print(f"[OK] Loaded {len(df)} roadmaps from {dataset_path}")
            
            for _, row in df.iterrows():
                roadmap_doc = {
                    "csv_id": int(row['id']),
                    "title": row['goal'],
                    "goal": row['goal'],
                    "domain": row['domain'],
                    "roadmap_text": row['roadmap'],
                    "steps": parse_roadmap_steps(row['roadmap']),
                    "created_at": datetime.now(),
                    "source": "csv_import",
                    # Enhanced metadata
                    "difficulty": row.get('difficulty', 'Intermediate'),
                    "estimated_hours": int(row.get('estimated_hours', 300)),
                    "prerequisites": row.get('prerequisites', ''),
                    "learning_outcomes": row.get('learning_outcomes', ''),
                    "dataset_source": dataset_path
                }
                all_roadmaps.append(roadmap_doc)
                
        except FileNotFoundError:
            print(f"[ERROR] Dataset not found: {dataset_path}")
        except Exception as e:
            print(f"[ERROR] Error loading {dataset_path}: {e}")
    
    return all_roadmaps

def main():
    print("=" * 60)
    print("Roadmap Data Reload Script")
    print("=" * 60)
    
    # Check connection
    try:
        client.admin.command('ping')
        print("[OK] Connected to MongoDB successfully")
    except Exception as e:
        print(f"[ERROR] Failed to connect to MongoDB: {e}")
        return
    
    # Count existing roadmaps
    existing_count = roadmap_collection.count_documents({"source": "csv_import"})
    print(f"\nExisting CSV roadmaps in database: {existing_count}")
    
    # Ask for confirmation
    if existing_count > 0:
        response = input(f"\nThis will delete {existing_count} existing CSV roadmaps and reload. Continue? (yes/no): ")
        if response.lower() != 'yes':
            print("Operation cancelled.")
            return
    
    # Delete existing CSV imports
    if existing_count > 0:
        result = roadmap_collection.delete_many({"source": "csv_import"})
        print(f"[OK] Deleted {result.deleted_count} existing CSV roadmaps")
    
    # Load new data
    print("\nLoading roadmap datasets...")
    all_roadmaps = load_roadmap_datasets()
    
    if not all_roadmaps:
        print("[ERROR] No roadmap data loaded")
        return
    
    # Insert new data
    print(f"\nInserting {len(all_roadmaps)} roadmaps into MongoDB...")
    result = roadmap_collection.insert_many(all_roadmaps)
    print(f"[OK] Successfully inserted {len(result.inserted_ids)} roadmaps")
    
    # Show summary by dataset
    print("\n" + "=" * 60)
    print("Summary by Dataset:")
    print("=" * 60)
    for dataset in ["comprehensive_roadmap_dataset.csv", "enhanced_roadmap_datasets.csv", "cross_domain_roadmaps_520.csv"]:
        count = roadmap_collection.count_documents({"dataset_source": dataset})
        print(f"{dataset}: {count} roadmaps")
    
    # Show summary by domain
    print("\n" + "=" * 60)
    print("Summary by Domain:")
    print("=" * 60)
    domains = roadmap_collection.distinct("domain", {"source": "csv_import"})
    for domain in sorted(domains):
        count = roadmap_collection.count_documents({"domain": domain, "source": "csv_import"})
        print(f"{domain}: {count} roadmaps")
    
    print("\n" + "=" * 60)
    print("[OK] Reload complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()


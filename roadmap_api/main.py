from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import random
import re
from datetime import datetime
import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import os

app = FastAPI(title="Roadmap Generator API", version="1.0.0")

# Health check endpoint
@app.get("/health")
async def health_check():
    try:
        # Test MongoDB connection
        db.admin.command('ping')
        return {"status": "healthy", "service": "roadmap-api", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "service": "roadmap-api", "database": "disconnected", "error": str(e)}

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Add your frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "pathwise")

# Initialize MongoDB client
client = MongoClient(MONGODB_URL)
db = client[DATABASE_NAME]
roadmap_collection = db["roadmap"]

# Load CSV data from multiple sources
def load_roadmap_datasets():
    """Load roadmap data from multiple CSV sources"""
    datasets = [
        "../comprehensive_roadmap_dataset.csv",
        "../enhanced_roadmap_datasets.csv",
        "cross_domain_roadmaps_520.csv"
    ]
    
    all_roadmaps = []
    
    for dataset_path in datasets:
        try:
            df = pd.read_csv(dataset_path)
            print(f"Loaded {len(df)} roadmaps from {dataset_path}")
            
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
                    "estimated_hours": row.get('estimated_hours', 300),
                    "prerequisites": row.get('prerequisites', ''),
                    "learning_outcomes": row.get('learning_outcomes', ''),
                    "dataset_source": dataset_path
                }
                all_roadmaps.append(roadmap_doc)
                
        except FileNotFoundError:
            print(f"Dataset not found: {dataset_path}")
        except Exception as e:
            print(f"Error loading {dataset_path}: {e}")
    
    return all_roadmaps

# Load and store roadmap data
try:
    # Check if we need to load data
    existing_count = roadmap_collection.count_documents({"source": "csv_import"})
    
    if existing_count == 0:
        print("Loading roadmap datasets...")
        all_roadmaps = load_roadmap_datasets()
        
        if all_roadmaps:
            roadmap_collection.insert_many(all_roadmaps)
            print(f"Stored {len(all_roadmaps)} roadmaps in MongoDB from all datasets")
        else:
            print("No roadmap data loaded")
    else:
        print(f"MongoDB already contains {existing_count} roadmaps from datasets")
        
except Exception as e:
    print(f"Error loading roadmap datasets: {e}")

# Pydantic models
class RoadmapRequest(BaseModel):
    goal: str
    domain: Optional[str] = None
    user_id: Optional[str] = None

class RoadmapResponse(BaseModel):
    id: str
    title: str
    goal: str
    domain: str
    steps: List[dict]
    created_at: str
    difficulty: Optional[str] = "Intermediate"
    estimated_hours: Optional[int] = 300
    prerequisites: Optional[str] = ""
    learning_outcomes: Optional[str] = ""
    match_score: Optional[float] = 0.0

class DomainResponse(BaseModel):
    domains: List[str]

class UserRoadmapsResponse(BaseModel):
    roadmaps: List[dict]

# MongoDB is used for storage instead of in-memory

def parse_roadmap_steps(roadmap_text: str) -> List[dict]:
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

def calculate_semantic_similarity(text1: str, text2: str) -> float:
    """Calculate semantic similarity between two texts using simple word overlap"""
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    if not words1 or not words2:
        return 0.0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union) if union else 0.0

def find_best_roadmap(goal: str, domain: Optional[str] = None) -> dict:
    """Enhanced roadmap matching with semantic analysis and comprehensive scoring"""
    try:
        # Build MongoDB query with source prioritization
        query = {"source": "csv_import"}
        if domain:
            query["domain"] = {"$regex": domain, "$options": "i"}
        
        # Get all roadmaps from MongoDB
        roadmaps = list(roadmap_collection.find(query))
        
        if not roadmaps:
            # Fallback to all roadmaps if domain filter returns nothing
            roadmaps = list(roadmap_collection.find({"source": "csv_import"}))
        
        if not roadmaps:
            raise HTTPException(status_code=500, detail="No roadmaps available in database")
        
        # Enhanced keyword mappings with synonyms and related terms
        goal_lower = goal.lower()
        best_match = None
        best_score = 0
        
        # Comprehensive keyword mappings
        keyword_mappings = {
            'frontend': ['frontend', 'front-end', 'ui', 'ux', 'react', 'vue', 'angular', 'javascript', 'css', 'html', 'web design', 'client-side', 'browser', 'svelte', 'next.js'],
            'backend': ['backend', 'back-end', 'server', 'api', 'node', 'python', 'java', 'php', 'ruby', 'go', 'server-side', 'database', 'express', 'fastapi', 'django', 'flask'],
            'fullstack': ['fullstack', 'full-stack', 'full stack', 'mern', 'mean', 'lamp', 'end-to-end', 'complete', 'full', 'stack'],
            'data': ['data', 'analytics', 'science', 'scientist', 'analysis', 'machine learning', 'ai', 'ml', 'statistics', 'big data', 'visualization', 'analyst', 'engineer'],
            'devops': ['devops', 'dev ops', 'deployment', 'ci/cd', 'docker', 'kubernetes', 'aws', 'cloud', 'infrastructure', 'automation', 'sre', 'reliability', 'terraform', 'ansible'],
            'mobile': ['mobile', 'ios', 'android', 'react native', 'flutter', 'swift', 'kotlin', 'app development', 'smartphone', 'app', 'native'],
            'python': ['python', 'django', 'flask', 'fastapi', 'pandas', 'numpy', 'data science', 'automation', 'scripting', 'py'],
            'javascript': ['javascript', 'js', 'node', 'react', 'vue', 'angular', 'typescript', 'es6', 'web development', 'nodejs', 'ts'],
            'java': ['java', 'spring', 'hibernate', 'maven', 'gradle', 'enterprise', 'jvm', 'android'],
            'web': ['web', 'website', 'web development', 'html', 'css', 'javascript', 'responsive', 'progressive', 'internet'],
            'cybersecurity': ['security', 'cybersecurity', 'ethical hacking', 'penetration testing', 'vulnerability', 'encryption', 'infosec', 'cyber', 'hacking', 'pentesting'],
            'blockchain': ['blockchain', 'cryptocurrency', 'bitcoin', 'ethereum', 'smart contracts', 'defi', 'web3', 'crypto', 'solidity', 'nft'],
            'game': ['game', 'gaming', 'unity', 'unreal', 'gamedev', 'interactive', 'entertainment', '3d', '2d'],
            'cloud': ['cloud', 'aws', 'azure', 'gcp', 'serverless', 'microservices', 'scalability', 'google cloud', 'amazon web services'],
            'design': ['design', 'ui', 'ux', 'user experience', 'user interface', 'visual', 'graphic', 'prototype', 'figma', 'sketch', 'designer'],
            'qa': ['qa', 'quality assurance', 'testing', 'test automation', 'selenium', 'cypress', 'tester', 'quality'],
            'ai': ['ai', 'artificial intelligence', 'machine learning', 'deep learning', 'ml', 'neural network', 'nlp', 'computer vision'],
            'database': ['database', 'sql', 'mysql', 'postgresql', 'mongodb', 'nosql', 'db', 'data storage'],
            'product': ['product', 'product manager', 'pm', 'product management', 'product owner'],
            'marketing': ['marketing', 'digital marketing', 'seo', 'sem', 'social media', 'content marketing', 'email marketing'],
            'ios': ['ios', 'swift', 'swiftui', 'xcode', 'iphone', 'ipad', 'apple'],
            'android': ['android', 'kotlin', 'java', 'android studio', 'google play']
        }
        
        # Experience level mappings
        experience_keywords = {
            'beginner': ['beginner', 'start', 'learn', 'basic', 'introduction', 'fundamentals'],
            'intermediate': ['intermediate', 'advance', 'improve', 'enhance', 'develop'],
            'advanced': ['advanced', 'expert', 'master', 'professional', 'senior', 'architect']
        }
        
        for roadmap in roadmaps:
            score = 0
            roadmap_goal = roadmap['goal'].lower()
            roadmap_domain = roadmap['domain'].lower()
            roadmap_text = roadmap.get('roadmap_text', '').lower()
            
            # 1. Exact goal match (highest priority)
            if goal_lower == roadmap_goal:
                score += 100  # Perfect match
            elif goal_lower in roadmap_goal:
                score += 50
            elif roadmap_goal in goal_lower:
                score += 40
            
            # 2. Semantic similarity (word overlap)
            semantic_score = calculate_semantic_similarity(goal_lower, roadmap_goal)
            score += semantic_score * 30
            
            # 3. Domain matching (very important)
            if domain:
                domain_lower = domain.lower()
                if domain_lower == roadmap_domain:
                    score += 35
                elif domain_lower in roadmap_domain:
                    score += 20
                elif roadmap_domain in domain_lower:
                    score += 15
            
            # 4. Enhanced keyword category matching
            goal_words = set(goal_lower.split())
            roadmap_goal_words = set(roadmap_goal.split())
            
            # Direct word overlap bonus
            word_overlap = goal_words.intersection(roadmap_goal_words)
            score += len(word_overlap) * 8
            
            for word in goal_words:
                # Category keyword matching with stronger weights
                for category, keywords in keyword_mappings.items():
                    if word in keywords:
                        # Check if category appears in roadmap
                        if category in roadmap_goal:
                            score += 12
                        elif category in roadmap_domain:
                            score += 10
                        elif category in roadmap_text:
                            score += 5
                        
                        # Check for exact keyword match
                        for keyword in keywords:
                            if keyword in roadmap_goal and len(keyword) > 3:
                                score += 6
            
            # 5. Experience level matching
            for level, level_keywords in experience_keywords.items():
                goal_has_level = any(kw in goal_lower for kw in level_keywords)
                roadmap_level = roadmap.get('difficulty', 'Intermediate').lower()
                
                if goal_has_level and level in roadmap_level:
                    score += 15
            
            # 6. Role/title matching
            role_terms = ['developer', 'engineer', 'programmer', 'coder', 'architect', 'specialist', 'designer', 'manager', 'analyst', 'scientist']
            for term in role_terms:
                if term in goal_lower and term in roadmap_goal:
                    score += 8
            
            # 7. Technology/framework specific matching
            goal_technologies = []
            for category, keywords in keyword_mappings.items():
                for keyword in keywords:
                    if keyword in goal_lower and len(keyword) > 3:
                        goal_technologies.append(keyword)
            
            for tech in goal_technologies:
                if tech in roadmap_goal or tech in roadmap_domain:
                    score += 10
                elif tech in roadmap_text:
                    score += 3
            
            # 8. Penalize poor matches and boost good ones
            if score < 5:
                score = score * 0.3  # Heavily penalize very poor matches
            elif score > 50:
                score = score * 1.2  # Boost good matches
            
            # Track best match
            if score > best_score:
                best_score = score
                best_match = roadmap
        
        # Enhanced fallback strategy
        if best_match is None or best_score < 10:
            # Try to find a general match by domain
            if domain:
                domain_matches = [r for r in roadmaps if domain.lower() in r['domain'].lower()]
                if domain_matches:
                    best_match = domain_matches[0]
                else:
                    best_match = roadmaps[0]
            else:
                best_match = roadmaps[0]
        
        print(f"Best match for '{goal}': {best_match['goal']} (score: {best_score})")
        return best_match
        
    except Exception as e:
        print(f"Error finding roadmap in MongoDB: {e}")
        raise HTTPException(status_code=500, detail=f"Error finding roadmap: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Roadmap Generator API is running"}

@app.post("/api/roadmap/generate-roadmap", response_model=RoadmapResponse)
async def generate_roadmap(request: RoadmapRequest):
    """Generate a roadmap based on goal and domain and store/update in MongoDB"""
    try:
        # Find best matching roadmap from MongoDB with scoring
        best_match = find_best_roadmap(request.goal, request.domain)
        
        # Use pre-parsed steps from MongoDB
        steps = best_match.get('steps', [])
        
        # Calculate match score for transparency
        match_score = calculate_semantic_similarity(request.goal.lower(), best_match['goal'].lower())
        
        # Debug logging
        print(f"Generated roadmap for goal: '{request.goal}'")
        print(f"Matched domain: {best_match['domain']}")
        print(f"Match score: {match_score:.2f}")
        print(f"Number of steps: {len(steps)}")
        for i, step in enumerate(steps):
            print(f"Step {i+1}: {step['category']} - {len(step['skills'])} skills")
        
        # Create response with enhanced metadata
        roadmap_id = f"roadmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}"
        
        response = RoadmapResponse(
            id=roadmap_id,
            title=request.goal,
            goal=request.goal,
            domain=best_match['domain'],
            steps=steps,
            created_at=datetime.now().isoformat(),
            difficulty=best_match.get('difficulty', 'Intermediate'),
            estimated_hours=best_match.get('estimated_hours', 300),
            prerequisites=best_match.get('prerequisites', ''),
            learning_outcomes=best_match.get('learning_outcomes', ''),
            match_score=round(match_score, 2)
        )
        
        # Store/Update roadmap in MongoDB
        roadmap_doc = {
            "roadmap_id": roadmap_id,
            "title": request.goal,  # Add explicit title field
            "goal": request.goal,
            "domain": best_match['domain'],
            "steps": steps,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "source": "user_generated",
            "user_id": request.user_id,
            "base_roadmap_id": best_match.get('_id'),  # Reference to original roadmap
            "generation_count": 1
        }
        
        # Check if user already has a roadmap for this goal
        if request.user_id:
            existing_roadmap = roadmap_collection.find_one({
                "user_id": request.user_id,
                "goal": request.goal,
                "source": "user_generated"
            })
            
            if existing_roadmap:
                # Update existing roadmap
                roadmap_doc["generation_count"] = existing_roadmap.get("generation_count", 1) + 1
                roadmap_doc["roadmap_id"] = existing_roadmap["roadmap_id"]  # Keep same ID
                roadmap_doc["created_at"] = existing_roadmap["created_at"]  # Keep original creation date
                
                result = roadmap_collection.update_one(
                    {
                        "user_id": request.user_id,
                        "goal": request.goal,
                        "source": "user_generated"
                    },
                    {
                        "$set": {
                            "title": request.goal,  # Update title field
                            "domain": best_match['domain'],
                            "steps": steps,
                            "updated_at": datetime.now(),
                            "generation_count": roadmap_doc["generation_count"],
                            "base_roadmap_id": best_match.get('_id')
                        }
                    }
                )
                
                if result.modified_count > 0:
                    print(f"Updated existing roadmap for user {request.user_id} (generation #{roadmap_doc['generation_count']})")
                else:
                    print(f"No changes made to roadmap for user {request.user_id}")
                
                # Update response with existing roadmap ID
                response.id = existing_roadmap["roadmap_id"]
            else:
                # Insert new roadmap
                roadmap_collection.insert_one(roadmap_doc)
                print(f"Created new roadmap for user {request.user_id}")
        else:
            # Insert new roadmap without user_id
            roadmap_collection.insert_one(roadmap_doc)
            print(f"Created new roadmap (no user)")
        
        return response
        
    except Exception as e:
        print(f"Error generating roadmap: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating roadmap: {str(e)}")

@app.get("/api/roadmap/roadmaps/domains", response_model=DomainResponse)
async def get_available_domains():
    """Get list of available domains from MongoDB"""
    try:
        # Get unique domains from MongoDB
        domains = roadmap_collection.distinct("domain")
        return DomainResponse(domains=domains)
    except Exception as e:
        print(f"Error getting domains: {e}")
        return DomainResponse(domains=[])

@app.get("/api/roadmap/roadmaps/similar")
async def get_similar_roadmaps(goal: str, domain: Optional[str] = None, limit: int = 5):
    """Get similar roadmaps based on goal from MongoDB"""
    try:
        # Build MongoDB query
        query = {}
        if domain:
            query["domain"] = {"$regex": domain, "$options": "i"}
        
        # Get roadmaps from MongoDB
        roadmaps = list(roadmap_collection.find(query).limit(limit * 2))  # Get more to filter
        
        if not roadmaps:
            return {"roadmaps": []}
        
        # Simple similarity scoring
        goal_lower = goal.lower()
        scored_roadmaps = []
        
        for roadmap in roadmaps:
            score = 0
            roadmap_goal = roadmap['goal'].lower()
            
            # Check for keyword matches
            goal_words = goal_lower.split()
            for word in goal_words:
                if word in roadmap_goal:
                    score += 1
            
            if score > 0:
                # Convert MongoDB document to dict and remove _id
                roadmap_dict = {k: v for k, v in roadmap.items() if k != '_id'}
                scored_roadmaps.append((score, roadmap_dict))
        
        # Sort by score and return top results
        scored_roadmaps.sort(key=lambda x: x[0], reverse=True)
        similar_roadmaps = [roadmap for _, roadmap in scored_roadmaps[:limit]]
        
        return {"roadmaps": similar_roadmaps}
        
    except Exception as e:
        print(f"Error finding similar roadmaps: {e}")
        raise HTTPException(status_code=500, detail=f"Error finding similar roadmaps: {str(e)}")

@app.get("/api/roadmap/roadmaps/recommendations")
async def get_roadmap_recommendations(
    interests: str = "",
    experience_level: str = "intermediate",
    time_commitment: int = 300,
    limit: int = 5
):
    """Get personalized roadmap recommendations based on user preferences"""
    try:
        # Build query based on preferences
        query = {"source": "csv_import"}
        
        # Filter by difficulty if specified
        if experience_level.lower() in ['beginner', 'intermediate', 'advanced']:
            query["difficulty"] = {"$regex": experience_level, "$options": "i"}
        
        # Get roadmaps from MongoDB
        roadmaps = list(roadmap_collection.find(query))
        
        if not roadmaps:
            return {"recommendations": []}
        
        # Score roadmaps based on preferences
        scored_roadmaps = []
        interests_lower = interests.lower()
        
        for roadmap in roadmaps:
            score = 0
            roadmap_goal = roadmap['goal'].lower()
            roadmap_domain = roadmap['domain'].lower()
            roadmap_text = roadmap.get('roadmap_text', '').lower()
            
            # Interest matching
            if interests:
                interest_words = interests_lower.split()
                for word in interest_words:
                    if word in roadmap_goal:
                        score += 10
                    elif word in roadmap_domain:
                        score += 8
                    elif word in roadmap_text:
                        score += 5
            
            # Time commitment matching
            estimated_hours = roadmap.get('estimated_hours', 300)
            if estimated_hours:
                time_diff = abs(estimated_hours - time_commitment)
                time_score = max(0, 10 - (time_diff / 50))  # Closer to preferred time = higher score
                score += time_score
            
            # Add some randomness for diversity
            score += random.uniform(0, 5)
            
            if score > 0:
                roadmap_dict = {k: v for k, v in roadmap.items() if k != '_id'}
                roadmap_dict['recommendation_score'] = round(score, 2)
                scored_roadmaps.append((score, roadmap_dict))
        
        # Sort by score and return top results
        scored_roadmaps.sort(key=lambda x: x[0], reverse=True)
        recommendations = [roadmap for _, roadmap in scored_roadmaps[:limit]]
        
        return {"recommendations": recommendations}
        
    except Exception as e:
        print(f"Error getting roadmap recommendations: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting recommendations: {str(e)}")

@app.get("/api/roadmap/roadmaps/user/{user_id}", response_model=UserRoadmapsResponse)
async def get_user_roadmaps(user_id: str):
    """Get saved roadmaps for a user from MongoDB"""
    try:
        # Get user roadmaps from MongoDB
        user_roadmaps = list(roadmap_collection.find(
            {"user_id": user_id, "source": "user_generated"}
        ).sort("updated_at", -1))  # Sort by updated_at to show most recently modified first
        
        # Convert MongoDB documents to dict format
        roadmaps = []
        for roadmap in user_roadmaps:
            roadmap_dict = {
                "_id": str(roadmap["_id"]),
                "id": roadmap["roadmap_id"],
                "title": roadmap.get("title", roadmap["goal"]),  # Use title field, fallback to goal
                "goal": roadmap["goal"],
                "domain": roadmap["domain"],
                "steps": roadmap["steps"],
                "created_at": roadmap["created_at"].isoformat(),
                "updated_at": roadmap.get("updated_at", roadmap["created_at"]).isoformat(),
                "generation_count": roadmap.get("generation_count", 1)
            }
            roadmaps.append(roadmap_dict)
        
        return UserRoadmapsResponse(roadmaps=roadmaps)
        
    except Exception as e:
        print(f"Error getting user roadmaps: {e}")
        return UserRoadmapsResponse(roadmaps=[])

@app.get("/api/roadmap/roadmaps/all")
async def get_all_generated_roadmaps(limit: int = 50, skip: int = 0):
    """Get all generated roadmaps from MongoDB"""
    try:
        # Get all user-generated roadmaps
        roadmaps = list(roadmap_collection.find(
            {"source": "user_generated"}
        ).sort("updated_at", -1).skip(skip).limit(limit))
        
        # Convert MongoDB documents to dict format
        roadmap_list = []
        for roadmap in roadmaps:
            roadmap_dict = {
                "_id": str(roadmap["_id"]),
                "id": roadmap["roadmap_id"],
                "title": roadmap.get("title", roadmap["goal"]),  # Use title field, fallback to goal
                "goal": roadmap["goal"],
                "domain": roadmap["domain"],
                "steps": roadmap["steps"],
                "created_at": roadmap["created_at"].isoformat(),
                "updated_at": roadmap.get("updated_at", roadmap["created_at"]).isoformat(),
                "generation_count": roadmap.get("generation_count", 1),
                "user_id": roadmap.get("user_id")
            }
            roadmap_list.append(roadmap_dict)
        
        # Get total count
        total_count = roadmap_collection.count_documents({"source": "user_generated"})
        
        return {
            "roadmaps": roadmap_list,
            "total": total_count,
            "limit": limit,
            "skip": skip
        }
        
    except Exception as e:
        print(f"Error getting all roadmaps: {e}")
        return {"roadmaps": [], "total": 0, "limit": limit, "skip": skip}

@app.get("/api/roadmap/resources/domain/{domain}")
async def get_resources_by_domain(domain: str):
    """Get learning resources for a specific domain"""
    try:
        # Get roadmaps for the domain
        roadmaps = list(roadmap_collection.find({
            "domain": {"$regex": domain, "$options": "i"}
        }).limit(10))
        
        if not roadmaps:
            return {"resources": [], "skills": []}
        
        # Extract all skills from roadmaps
        all_skills = set()
        for roadmap in roadmaps:
            if roadmap.get('steps'):
                for step in roadmap['steps']:
                    if step.get('skills'):
                        all_skills.update(step['skills'])
        
        # Convert to list and return
        skills_list = list(all_skills)
        
        return {
            "domain": domain,
            "skills": skills_list,
            "roadmap_count": len(roadmaps),
            "message": f"Found {len(skills_list)} skills for {domain} domain"
        }
        
    except Exception as e:
        print(f"Error getting domain resources: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting domain resources: {str(e)}")

@app.get("/api/roadmap/resources/skills")
async def get_all_skills():
    """Get all unique skills from all roadmaps"""
    try:
        # Get all roadmaps
        roadmaps = list(roadmap_collection.find({}))
        
        # Extract all skills
        all_skills = set()
        for roadmap in roadmaps:
            if roadmap.get('steps'):
                for step in roadmap['steps']:
                    if step.get('skills'):
                        all_skills.update(step['skills'])
        
        # Convert to list and return
        skills_list = list(all_skills)
        
        return {
            "skills": skills_list,
            "total_skills": len(skills_list),
            "total_roadmaps": len(roadmaps)
        }
        
    except Exception as e:
        print(f"Error getting all skills: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting all skills: {str(e)}")

@app.delete("/api/roadmap/roadmaps/{roadmap_id}")
async def delete_roadmap(roadmap_id: str, user_id: str):
    """Delete a saved roadmap from MongoDB"""
    try:
        # Delete roadmap from MongoDB
        result = roadmap_collection.delete_one({
            "roadmap_id": roadmap_id,
            "user_id": user_id,
            "source": "user_generated"
        })
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Roadmap not found")
        
        return {"message": "Roadmap deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error deleting roadmap: {e}")
        raise HTTPException(status_code=500, detail=f"Error deleting roadmap: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

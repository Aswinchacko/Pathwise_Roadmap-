"""
Simple JSON database for storing AI-generated projects
"""
import json
import os
from datetime import datetime
from typing import List, Dict

DATABASE_FILE = "ai_projects.json"

def load_projects() -> List[Dict]:
    """Load projects from JSON file"""
    if not os.path.exists(DATABASE_FILE):
        return []
    
    try:
        with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_projects(projects: List[Dict]) -> None:
    """Save projects to JSON file"""
    with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
        json.dump(projects, f, indent=2, ensure_ascii=False)

def add_project(project: Dict) -> Dict:
    """Add a new project to the database"""
    projects = load_projects()
    
    # Generate unique ID
    max_id = max([p.get('id', 0) for p in projects], default=0)
    project['id'] = max_id + 1
    
    # Add metadata
    project['created_at'] = datetime.now().isoformat()
    project['source'] = 'ai-generated'
    
    projects.append(project)
    save_projects(projects)
    
    return project

def get_all_projects() -> List[Dict]:
    """Get all projects from database"""
    return load_projects()

def get_project_by_id(project_id: int) -> Dict:
    """Get a specific project by ID"""
    projects = load_projects()
    return next((p for p in projects if p['id'] == project_id), None)

def search_projects(query: str = None, category: str = None, difficulty: str = None) -> List[Dict]:
    """Search projects with filters"""
    projects = load_projects()
    
    if query:
        query_lower = query.lower()
        projects = [p for p in projects if 
                   query_lower in p.get('title', '').lower() or
                   query_lower in p.get('description', '').lower() or
                   any(query_lower in skill.lower() for skill in p.get('skills', []))]
    
    if category:
        projects = [p for p in projects if p.get('category') == category]
    
    if difficulty:
        projects = [p for p in projects if p.get('difficulty', '').lower() == difficulty.lower()]
    
    return projects

def delete_project(project_id: int) -> bool:
    """Delete a project by ID"""
    projects = load_projects()
    original_count = len(projects)
    projects = [p for p in projects if p['id'] != project_id]
    
    if len(projects) < original_count:
        save_projects(projects)
        return True
    return False

def get_stats() -> Dict:
    """Get database statistics"""
    projects = load_projects()
    
    if not projects:
        return {
            "total_projects": 0,
            "by_category": {},
            "by_difficulty": {},
            "recent_projects": 0
        }
    
    # Count by category
    by_category = {}
    by_difficulty = {}
    recent_count = 0
    
    for project in projects:
        category = project.get('category', 'unknown')
        difficulty = project.get('difficulty', 'unknown')
        
        by_category[category] = by_category.get(category, 0) + 1
        by_difficulty[difficulty] = by_difficulty.get(difficulty, 0) + 1
        
        # Count recent projects (last 7 days)
        created_at = project.get('created_at', '')
        if created_at:
            try:
                created_date = datetime.fromisoformat(created_at)
                days_ago = (datetime.now() - created_date).days
                if days_ago <= 7:
                    recent_count += 1
            except:
                pass
    
    return {
        "total_projects": len(projects),
        "by_category": by_category,
        "by_difficulty": by_difficulty,
        "recent_projects": recent_count
    }

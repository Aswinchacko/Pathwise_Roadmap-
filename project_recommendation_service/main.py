from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import requests
import re
from typing import List, Dict
import json
from database import add_project, get_all_projects, get_project_by_id, search_projects, get_stats

load_dotenv()

app = Flask(__name__)
CORS(app)

# Groq API (free and fast) - get key from https://console.groq.com
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


def recommend_with_groq(user_aim: str, num_recommendations: int = 5) -> List[Dict]:
    """Use Groq AI to GENERATE custom project recommendations"""
    if not GROQ_API_KEY:
        print("⚠️  No Groq API key - using rule-based fallback")
        return None
    
    try:
        prompt = f"""You are an expert career advisor. Based on the user's career goal, suggest {num_recommendations} practical project ideas they should build.

User's Goal: {user_aim}

Generate {num_recommendations} project ideas as a JSON array. Each project should have:
- title: Short project name
- description: 1-2 sentences about what to build
- difficulty: "Beginner", "Intermediate", or "Advanced"
- skills: Array of 4-6 relevant skills/technologies
- duration: Estimated time (e.g., "2 weeks", "1 month")
- category: "web-dev", "ai-ml", "data-science", or "mobile-dev"

Example format:
[
  {{
    "title": "Personal Portfolio Website",
    "description": "Build a responsive portfolio website to showcase your work",
    "difficulty": "Beginner",
    "skills": ["HTML", "CSS", "JavaScript", "Responsive Design"],
    "duration": "1 week",
    "category": "web-dev"
  }}
]

Generate projects that are:
- Relevant to their goal
- Progressively challenging
- Practical and portfolio-worthy
- Use modern technologies

Response (JSON array only, no markdown):"""

        print(f"🤖 Calling Groq AI to GENERATE projects for: '{user_aim[:50]}...'")
        
        response = requests.post(
            GROQ_API_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,  # Higher for more creativity
                "max_tokens": 1500   # More tokens for full project descriptions
            },
            timeout=20
        )
        
        print(f"📡 Groq API response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content'].strip()
            print(f"💬 AI Response received ({len(content)} chars)")
            
            # Remove markdown code blocks if present
            content = re.sub(r'```json\s*', '', content)
            content = re.sub(r'```\s*', '', content)
            content = content.strip()
            
            # Try to parse JSON
            try:
                projects = json.loads(content)
                
                if isinstance(projects, list) and len(projects) > 0:
                    # Add default values and save to database
                    saved_projects = []
                    for proj in projects:
                        proj['rating'] = 4.5  # Default rating
                        proj['students'] = 0   # New project
                        proj['topics'] = proj.get('skills', [])[:3]  # Use first 3 skills as topics
                        
                        # Save to database
                        saved_proj = add_project(proj)
                        saved_projects.append(saved_proj)
                    
                    print(f"✅ AI generated {len(saved_projects)} custom projects and saved to database!")
                    for i, p in enumerate(saved_projects, 1):
                        print(f"  {i}. {p['title']} ({p['difficulty']}) [ID: {p['id']}]")
                    
                    return saved_projects[:num_recommendations]
                else:
                    print(f"⚠️  AI response not in expected format")
                    return None
                    
            except json.JSONDecodeError as e:
                print(f"⚠️  Could not parse AI JSON response: {e}")
                print(f"Raw response: {content[:200]}...")
                return None
                
        elif response.status_code == 401:
            print(f"❌ Groq API authentication failed - check your API key")
            return None
        elif response.status_code == 429:
            print(f"⚠️  Groq API rate limit exceeded - using rule-based fallback")
            return None
        else:
            print(f"❌ Groq API error: {response.status_code} - {response.text[:200]}")
            return None
        
    except requests.exceptions.Timeout:
        print(f"⏱️  Groq API timeout - using rule-based fallback")
        return None
    except requests.exceptions.ConnectionError:
        print(f"🔌 Cannot connect to Groq API - using rule-based fallback")
        return None
    except Exception as e:
        print(f"❌ Groq API error: {type(e).__name__} - {str(e)}")
        return None


def recommend_with_rules(user_aim: str, num_recommendations: int = 5) -> List[Dict]:
    """Fallback rule-based recommendation system using database"""
    aim_lower = user_aim.lower()
    
    print(f"🎯 Rule-based engine analyzing: '{aim_lower}'")
    
    # Search existing projects in database
    projects = search_projects(query=aim_lower)
    
    if not projects:
        print("📭 No projects found in database. Please generate some AI projects first!")
        return []
    
    # Simple scoring based on keyword matches
    scores = []
    for project in projects:
        score = 0
        
        # Check title and description
        title_words = project.get('title', '').lower().split()
        desc_words = project.get('description', '').lower().split()
        aim_words = aim_lower.split()
        
        for aim_word in aim_words:
            if len(aim_word) > 3:  # Skip short words
                if any(aim_word in word for word in title_words):
                    score += 5
                if any(aim_word in word for word in desc_words):
                    score += 3
        
        # Check skills
        for skill in project.get('skills', []):
            if skill.lower() in aim_lower or any(s in skill.lower() for s in aim_words if len(s) > 2):
                score += 10
        
        # Check category match
        category_keywords = {
            'web-dev': ['web', 'html', 'css', 'javascript', 'frontend', 'backend', 'fullstack', 'full-stack', 'website', 'react', 'node', 'django', 'flask'],
            'ai-ml': ['ai', 'ml', 'machine learning', 'neural', 'deep learning', 'model', 'tensorflow', 'pytorch', 'data science'],
            'data-science': ['data', 'analytics', 'visualization', 'dashboard', 'pandas', 'numpy', 'analysis'],
            'mobile-dev': ['mobile', 'app', 'android', 'ios', 'react native', 'flutter']
        }
        
        for cat, keywords in category_keywords.items():
            if project.get('category') == cat:
                if any(keyword in aim_lower for keyword in keywords):
                    score += 15  # Big boost for category match
        
        scores.append((project, score))
        print(f"  Project: {project.get('title', 'Unknown')[:30]:30} | Score: {score}")
    
    # Sort by score and return top N
    scores.sort(key=lambda x: x[1], reverse=True)
    top_projects = [project for project, score in scores[:num_recommendations]]
    
    print(f"🏆 Top {len(top_projects)} projects selected from database:")
    for i, p in enumerate(top_projects, 1):
        print(f"  {i}. {p.get('title', 'Unknown')}")
    
    return top_projects


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "project_recommendation",
        "ai_enabled": bool(GROQ_API_KEY)
    })


@app.route('/api/recommend', methods=['POST'])
def recommend_projects():
    """Main endpoint to get project recommendations"""
    try:
        data = request.get_json()
        user_aim = data.get('aim', '').strip()
        num_recommendations = data.get('limit', 5)
        
        if not user_aim:
            return jsonify({"error": "Please provide your aim"}), 400
        
        print(f"\n{'='*60}")
        print(f"📥 Recommendation Request")
        print(f"{'='*60}")
        print(f"Aim: {user_aim}")
        print(f"Limit: {num_recommendations}")
        
        # Try AI to GENERATE custom projects first, fall back to database search
        recommendations = recommend_with_groq(user_aim, num_recommendations)
        
        if recommendations is None:
            print(f"🎯 Using rule-based fallback (database search)")
            recommendations = recommend_with_rules(user_aim, num_recommendations)
            method = "rule-based"
        else:
            method = "ai-powered"
        
        print(f"✅ Returning {len(recommendations)} projects using {method} method")
        print(f"{'='*60}\n")
        
        return jsonify({
            "success": True,
            "aim": user_aim,
            "method": method,
            "recommendations": recommendations,
            "total": len(recommendations)
        })
    
    except Exception as e:
        print(f"❌ Error in recommend endpoint: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/projects', methods=['GET'])
def get_all_projects():
    """Get all available projects from database"""
    category = request.args.get('category')
    difficulty = request.args.get('difficulty')
    search = request.args.get('search')
    
    projects = search_projects(query=search, category=category, difficulty=difficulty)
    
    return jsonify({
        "success": True,
        "projects": projects,
        "total": len(projects)
    })


@app.route('/api/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """Get a specific project by ID"""
    project = get_project_by_id(project_id)
    
    if project:
        return jsonify({"success": True, "project": project})
    return jsonify({"error": "Project not found"}), 404


@app.route('/api/projects/stats', methods=['GET'])
def get_project_stats():
    """Get project database statistics"""
    stats = get_stats()
    return jsonify({
        "success": True,
        "stats": stats
    })


@app.route('/api/recommend/phase', methods=['POST'])
def recommend_projects_for_phase():
    """Recommend projects based on a completed phase"""
    try:
        data = request.get_json()
        if not data or 'phase' not in data:
            return jsonify({
                'success': False,
                'error': 'Phase information is required'
            }), 400
        
        phase = data['phase']
        limit = data.get('limit', 3)
        
        print(f"\n{'='*60}")
        print(f"📚 Phase-based Recommendation Request")
        print(f"{'='*60}")
        print(f"Phase: {phase}")
        print(f"Limit: {limit}")
        
        # Generate projects based on completed phase using Groq
        recommendations = recommend_projects_for_phase_groq(phase, limit)
        
        if recommendations:
            print(f"✅ Generated {len(recommendations)} phase-based recommendations using AI")
            method = "phase-based-ai"
        else:
            # Fallback to rule-based phase recommendations
            recommendations = recommend_projects_for_phase_rules(phase, limit)
            print(f"🎯 Using fallback rule-based recommendations for phase: {phase}")
            method = "phase-based-rules"
        
        print(f"✅ Returning {len(recommendations)} projects using {method} method")
        print(f"{'='*60}\n")
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'method': method,
            'phase': phase,
            'total': len(recommendations)
        })
            
    except Exception as e:
        print(f"❌ Error in phase-based recommendation: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to generate phase-based recommendations'
        }), 500


def recommend_projects_for_phase_groq(phase: str, limit: int = 3):
    """Generate project recommendations based on completed phase using Groq AI"""
    if not GROQ_API_KEY:
        print("⚠️  No Groq API key - using rule-based fallback for phase")
        return None
    
    try:
        # Create a detailed prompt for phase-based project generation
        prompt = f"""Based on the completed phase "{phase}", recommend {limit} practical projects that would help reinforce and apply the skills learned in this phase.

The projects should be:
- Directly related to the completed phase
- Practical and hands-on
- Progressive in difficulty
- Include specific skills and technologies

Return ONLY a JSON array of project objects with this exact structure:
[
  {{
    "title": "Project Title",
    "description": "Detailed project description explaining what to build and why it's relevant to the phase",
    "difficulty": "beginner|intermediate|advanced",
    "skills": ["skill1", "skill2", "skill3"],
    "duration": "1-2 weeks|2-4 weeks|1-2 months",
    "category": "web-dev|ai-ml|data-science|mobile-dev|design|other"
  }}
]

Phase: {phase}"""

        print(f"🤖 Calling Groq AI for phase-based projects: '{phase}'")
        
        response = requests.post(
            GROQ_API_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 1500
            },
            timeout=20
        )
        
        print(f"📡 Groq API response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content'].strip()
            print(f"💬 AI Phase Response received ({len(content)} chars)")
            
            # Remove markdown code blocks if present
            content = re.sub(r'```json\s*', '', content)
            content = re.sub(r'```\s*', '', content)
            content = content.strip()
            
            # Try to parse JSON
            try:
                projects = json.loads(content)
                
                if isinstance(projects, list) and len(projects) > 0:
                    # Add metadata to each project
                    saved_projects = []
                    for i, project in enumerate(projects):
                        project['id'] = 200 + i  # Start from 200 for phase-based projects
                        project['rating'] = 4.5
                        project['students'] = 0
                        project['topics'] = [phase.lower().replace(' ', '-')]
                        project['unlocked'] = True  # Phase-based projects are unlocked
                        project['saved'] = False  # Not saved yet
                        project['phase'] = phase  # Add phase information
                        
                        # Save to database
                        saved_proj = add_project(project)
                        saved_projects.append(saved_proj)
                    
                    print(f"✅ AI generated {len(saved_projects)} phase-based projects and saved to database!")
                    for i, p in enumerate(saved_projects, 1):
                        print(f"  {i}. {p['title']} ({p['difficulty']}) [ID: {p['id']}]")
                    
                    return saved_projects[:limit]
                else:
                    print(f"⚠️  AI phase response not in expected format")
                    return None
                    
            except json.JSONDecodeError as e:
                print(f"⚠️  Could not parse AI phase JSON response: {e}")
                print(f"Raw response: {content[:200]}...")
                return None
                
        elif response.status_code == 401:
            print(f"❌ Groq API authentication failed for phase recommendation")
            return None
        elif response.status_code == 429:
            print(f"⚠️  Groq API rate limit exceeded for phase recommendation")
            return None
        else:
            print(f"❌ Groq API error for phase: {response.status_code} - {response.text[:200]}")
            return None
        
    except requests.exceptions.Timeout:
        print(f"⏱️  Groq API timeout for phase recommendation")
        return None
    except requests.exceptions.ConnectionError:
        print(f"🔌 Cannot connect to Groq API for phase recommendation")
        return None
    except Exception as e:
        print(f"❌ Groq API error for phase: {type(e).__name__} - {str(e)}")
        return None


def recommend_projects_for_phase_rules(phase: str, limit: int = 3):
    """Fallback rule-based recommendations for completed phases"""
    phase_lower = phase.lower()
    
    print(f"🎯 Rule-based phase engine analyzing: '{phase_lower}'")
    
    # Phase-based project mappings
    phase_projects = {
        'design fundamentals': [
            {
                "title": "Personal Brand Identity Design",
                "description": "Create a complete brand identity including logo, color palette, typography, and business cards",
                "difficulty": "intermediate",
                "skills": ["Design Principles", "Color Theory", "Typography", "Branding"],
                "duration": "2-3 weeks",
                "category": "design"
            },
            {
                "title": "UI/UX Design System",
                "description": "Design a comprehensive design system with components, patterns, and guidelines",
                "difficulty": "advanced",
                "skills": ["Design Systems", "UI/UX", "Component Design", "Documentation"],
                "duration": "3-4 weeks",
                "category": "design"
            },
            {
                "title": "Portfolio Website Design",
                "description": "Design and build a personal portfolio website showcasing your design skills",
                "difficulty": "intermediate",
                "skills": ["Web Design", "Portfolio", "Responsive Design", "UI/UX"],
                "duration": "2-3 weeks",
                "category": "design"
            }
        ],
        'adobe creative suite': [
            {
                "title": "Digital Magazine Layout",
                "description": "Create a professional magazine layout using InDesign with master pages and typography",
                "difficulty": "intermediate",
                "skills": ["InDesign", "Layout Design", "Typography", "Print Design"],
                "duration": "2-3 weeks",
                "category": "design"
            },
            {
                "title": "Interactive Prototype",
                "description": "Build an interactive mobile app prototype using Adobe XD with animations and transitions",
                "difficulty": "advanced",
                "skills": ["Adobe XD", "Prototyping", "User Experience", "Animation"],
                "duration": "3-4 weeks",
                "category": "design"
            },
            {
                "title": "Photo Manipulation Project",
                "description": "Create a creative photo manipulation using Photoshop with advanced techniques",
                "difficulty": "intermediate",
                "skills": ["Photoshop", "Photo Manipulation", "Creative Design", "Image Editing"],
                "duration": "1-2 weeks",
                "category": "design"
            }
        ]
    }
    
    # Find matching phase projects
    recommendations = []
    for phase_key, projects in phase_projects.items():
        if phase_key in phase_lower:
            for project in projects:
                project['id'] = 200 + len(recommendations)
                project['rating'] = 4.5
                project['students'] = 0
                project['topics'] = [phase.lower().replace(' ', '-')]
                project['unlocked'] = True
                project['saved'] = False
                project['phase'] = phase
                recommendations.append(project)
            break
    
    # If no specific phase match, return general design projects
    if not recommendations:
        general_projects = [
            {
                "title": "Portfolio Website Design",
                "description": "Design and build a personal portfolio website showcasing your design skills",
                "difficulty": "intermediate",
                "skills": ["Web Design", "Portfolio", "Responsive Design", "UI/UX"],
                "duration": "2-3 weeks",
                "category": "design"
            }
        ]
        
        for project in general_projects:
            project['id'] = 200 + len(recommendations)
            project['rating'] = 4.5
            project['students'] = 0
            project['topics'] = ["general-design"]
            project['unlocked'] = True
            project['saved'] = False
            project['phase'] = phase
            recommendations.append(project)
    
    print(f"🏆 Selected {len(recommendations)} phase-based projects:")
    for i, p in enumerate(recommendations, 1):
        print(f"  {i}. {p.get('title', 'Unknown')}")
    
    return recommendations[:limit]


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5003))
    print(f"🚀 Project Recommendation Service starting on port {port}")
    print(f"🤖 AI Mode: {'Enabled (Groq)' if GROQ_API_KEY else 'Disabled (Database search only)'}")
    print(f"💾 Database: JSON file (ai_projects.json)")
    app.run(host='0.0.0.0', port=port, debug=True)
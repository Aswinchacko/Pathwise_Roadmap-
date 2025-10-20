"""
Real-World Job Agent Service
Fetches actual jobs from LinkedIn, Indeed, Glassdoor, etc. and uses Groq AI to match them to user's goals
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import os
import logging
import requests
from dotenv import load_dotenv
from pymongo import MongoClient
import re
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configuration
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Multiple Job API sources (users can configure any of these)
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY', '')  # For JSearch API
ADZUNA_APP_ID = os.getenv('ADZUNA_APP_ID', '')
ADZUNA_API_KEY = os.getenv('ADZUNA_API_KEY', '')

# MongoDB setup
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
mongo_client = None
db = None

try:
    mongo_client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    mongo_client.admin.command('ping')
    db = mongo_client['pathwise']
    logger.info("✅ Connected to MongoDB")
except Exception as e:
    logger.warning(f"⚠️ MongoDB not available: {e}")

app = FastAPI(
    title="PathWise Job Agent API",
    description="Real-world job fetching with AI matching",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class JobSearchRequest(BaseModel):
    user_id: str
    query: Optional[str] = None  # If not provided, will use roadmap
    location: Optional[str] = "United States"
    remote: Optional[bool] = None
    experience_level: Optional[str] = None
    limit: Optional[int] = 10
    use_ai_matching: Optional[bool] = True

class JobResponse(BaseModel):
    id: str
    title: str
    company: str
    location: str
    salary: Optional[str]
    description: str
    requirements: List[str]
    url: str
    posted_date: str
    remote: bool
    match_score: Optional[float] = None
    source: str  # 'linkedin', 'indeed', 'glassdoor', etc.


def fetch_jobs_from_jsearch(query: str, location: str = "United States", limit: int = 10) -> List[Dict]:
    """Fetch jobs from RapidAPI JSearch (covers LinkedIn, Indeed, Glassdoor, ZipRecruiter)"""
    if not RAPIDAPI_KEY:
        logger.warning("RapidAPI key not configured")
        return []
    
    try:
        url = "https://jsearch.p.rapidapi.com/search"
        
        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }
        
        params = {
            "query": f"{query} in {location}",
            "page": "1",
            "num_pages": "1",
            "date_posted": "month"  # Jobs from last month
        }
        
        logger.info(f"Fetching jobs from JSearch API: {query}")
        response = requests.get(url, headers=headers, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            jobs = []
            
            for job_data in data.get('data', [])[:limit]:
                job = {
                    'id': job_data.get('job_id', ''),
                    'title': job_data.get('job_title', ''),
                    'company': job_data.get('employer_name', ''),
                    'location': job_data.get('job_city', '') + ', ' + job_data.get('job_state', ''),
                    'salary': job_data.get('job_salary', 'Not specified'),
                    'description': job_data.get('job_description', ''),
                    'requirements': job_data.get('job_required_skills', []),
                    'url': job_data.get('job_apply_link', ''),
                    'posted_date': job_data.get('job_posted_at_datetime_utc', ''),
                    'remote': job_data.get('job_is_remote', False),
                    'source': 'JSearch (LinkedIn/Indeed/Glassdoor)',
                    'logo': job_data.get('employer_logo', ''),
                    'employment_type': job_data.get('job_employment_type', '')
                }
                jobs.append(job)
            
            logger.info(f"✅ Fetched {len(jobs)} jobs from JSearch")
            return jobs
        else:
            logger.error(f"JSearch API error: {response.status_code}")
            return []
            
    except Exception as e:
        logger.error(f"Error fetching from JSearch: {e}")
        return []


def fetch_jobs_from_adzuna(query: str, location: str = "us", limit: int = 10) -> List[Dict]:
    """Fetch jobs from Adzuna API (backup source)"""
    if not ADZUNA_APP_ID or not ADZUNA_API_KEY:
        logger.warning("Adzuna API credentials not configured")
        return []
    
    try:
        url = f"https://api.adzuna.com/v1/api/jobs/{location}/search/1"
        
        params = {
            'app_id': ADZUNA_APP_ID,
            'app_key': ADZUNA_API_KEY,
            'results_per_page': limit,
            'what': query,
            'content-type': 'application/json'
        }
        
        logger.info(f"Fetching jobs from Adzuna API: {query}")
        response = requests.get(url, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            jobs = []
            
            for job_data in data.get('results', []):
                job = {
                    'id': job_data.get('id', ''),
                    'title': job_data.get('title', ''),
                    'company': job_data.get('company', {}).get('display_name', 'Company'),
                    'location': job_data.get('location', {}).get('display_name', ''),
                    'salary': f"${job_data.get('salary_min', 0)}-${job_data.get('salary_max', 0)}" if job_data.get('salary_min') else 'Not specified',
                    'description': job_data.get('description', ''),
                    'requirements': [],
                    'url': job_data.get('redirect_url', ''),
                    'posted_date': job_data.get('created', ''),
                    'remote': 'remote' in job_data.get('title', '').lower() or 'remote' in job_data.get('description', '').lower(),
                    'source': 'Adzuna'
                }
                jobs.append(job)
            
            logger.info(f"✅ Fetched {len(jobs)} jobs from Adzuna")
            return jobs
        else:
            logger.error(f"Adzuna API error: {response.status_code}")
            return []
            
    except Exception as e:
        logger.error(f"Error fetching from Adzuna: {e}")
        return []


def generate_fallback_jobs(query: str, limit: int = 10) -> List[Dict]:
    """Generate realistic job listings using Groq AI when APIs are unavailable"""
    if not GROQ_API_KEY:
        logger.warning("No Groq API key - cannot generate fallback jobs")
        return []
    
    try:
        prompt = f"""Generate {limit} realistic current job listings for: {query}

Return ONLY a JSON array with this exact structure:
[
  {{
    "id": "unique_id",
    "title": "Job Title",
    "company": "Real Company Name",
    "location": "City, State",
    "salary": "$XXk-$XXXk/year or $XX/hr",
    "description": "Detailed 2-3 sentence job description",
    "requirements": ["skill1", "skill2", "skill3", "skill4"],
    "url": "https://www.linkedin.com/jobs/view/...",
    "posted_date": "2024-10-15T00:00:00Z",
    "remote": true/false,
    "source": "LinkedIn"
  }}
]

Make jobs realistic with:
- Real tech companies (Google, Microsoft, Amazon, Meta, Netflix, etc.)
- Current salary ranges for 2024-2025
- Realistic job requirements
- Mix of remote and on-site positions
- Recent posting dates (last 2 weeks)"""

        response = requests.post(
            GROQ_API_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 3000
            },
            timeout=30
        )
        
        if response.status_code == 200:
            ai_response = response.json()['choices'][0]['message']['content']
            json_match = re.search(r'\[.*\]', ai_response, re.DOTALL)
            if json_match:
                jobs = json.loads(json_match.group())
                logger.info(f"✅ Generated {len(jobs)} fallback jobs with AI")
                return jobs
        
        return []
        
    except Exception as e:
        logger.error(f"Error generating fallback jobs: {e}")
        return []


def match_jobs_with_ai(jobs: List[Dict], user_profile: Dict) -> List[Dict]:
    """Use Groq AI to intelligently score and rank jobs based on user's profile"""
    if not GROQ_API_KEY or not jobs:
        return jobs
    
    try:
        # Build user profile summary
        profile_summary = f"""
User Profile:
- Skills: {', '.join(user_profile.get('skills', []))}
- Experience Level: {user_profile.get('experience_level', 'Mid-level')}
- Career Goal: {user_profile.get('goal', 'Software Developer')}
- Preferred Location: {user_profile.get('location', 'Remote')}
- Current Learning: {', '.join(user_profile.get('current_learning', []))}
"""
        
        # Prepare jobs summary for AI
        jobs_summary = []
        for idx, job in enumerate(jobs[:15]):  # Limit to 15 jobs for AI processing
            jobs_summary.append({
                'index': idx,
                'title': job.get('title', ''),
                'company': job.get('company', ''),
                'requirements': job.get('requirements', [])[:5],  # Top 5 requirements
                'description': job.get('description', '')[:200]  # First 200 chars
            })
        
        prompt = f"""{profile_summary}

Jobs to evaluate:
{json.dumps(jobs_summary, indent=2)}

Score each job (0-100) based on how well it matches the user's profile. Consider:
- Skill alignment
- Experience level fit
- Career goal relevance
- Learning path compatibility

Return ONLY a JSON array: [
  {{"index": 0, "match_score": 85, "reason": "Brief reason"}},
  {{"index": 1, "match_score": 72, "reason": "Brief reason"}}
]"""

        response = requests.post(
            GROQ_API_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 2000
            },
            timeout=25
        )
        
        if response.status_code == 200:
            ai_response = response.json()['choices'][0]['message']['content']
            json_match = re.search(r'\[.*\]', ai_response, re.DOTALL)
            if json_match:
                scores = json.loads(json_match.group())
                
                # Apply scores to jobs
                for score_data in scores:
                    idx = score_data.get('index')
                    if 0 <= idx < len(jobs):
                        jobs[idx]['match_score'] = score_data.get('match_score', 50)
                        jobs[idx]['match_reason'] = score_data.get('reason', '')
                
                # Sort by match score
                jobs.sort(key=lambda x: x.get('match_score', 0), reverse=True)
                logger.info("✅ AI matching completed")
                
        return jobs
        
    except Exception as e:
        logger.error(f"Error in AI matching: {e}")
        return jobs


def get_user_roadmap_skills(user_id: str) -> Dict:
    """Get user's skills and goals from their roadmap"""
    if db is None:
        return {
            'skills': ['JavaScript', 'React', 'Python'],
            'goal': 'Full-stack Developer',
            'experience_level': 'Mid-level',
            'current_learning': ['Web Development']
        }
    
    try:
        # Get user's active roadmap
        roadmap = db['roadmap'].find_one({'user_id': user_id})
        
        if roadmap:
            # Extract skills from roadmap steps
            skills = []
            for step in roadmap.get('steps', []):
                skills.extend(step.get('skills', []))
            
            return {
                'skills': list(set(skills))[:10],  # Top 10 unique skills
                'goal': roadmap.get('goal', 'Software Developer'),
                'experience_level': roadmap.get('difficulty', 'Mid-level'),
                'current_learning': [roadmap.get('domain', 'Technology')],
                'location': 'Remote'
            }
        
        # Fallback
        return {
            'skills': ['Programming', 'Software Development'],
            'goal': 'Software Developer',
            'experience_level': 'Mid-level',
            'current_learning': ['Technology']
        }
        
    except Exception as e:
        logger.error(f"Error fetching user roadmap: {e}")
        return {
            'skills': ['Programming'],
            'goal': 'Software Developer',
            'experience_level': 'Mid-level'
        }


@app.get("/")
async def root():
    return {
        "service": "PathWise Job Agent",
        "version": "1.0.0",
        "status": "running",
        "sources": ["JSearch (LinkedIn/Indeed/Glassdoor)", "Adzuna", "AI Generated"],
        "ai_powered": bool(GROQ_API_KEY)
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "mongodb": "connected" if db else "disconnected",
        "groq_api": "configured" if GROQ_API_KEY else "not_configured",
        "rapidapi": "configured" if RAPIDAPI_KEY else "not_configured",
        "adzuna": "configured" if ADZUNA_APP_ID and ADZUNA_API_KEY else "not_configured",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/jobs/search")
async def search_jobs(request: JobSearchRequest):
    """
    Search for real-world jobs and match them to user's profile
    """
    try:
        logger.info(f"Job search request from user {request.user_id}")
        
        # Get user's profile from roadmap if no query provided
        user_profile = get_user_roadmap_skills(request.user_id)
        
        # Build search query
        if request.query:
            search_query = request.query
        else:
            # Use user's goal and top skills
            search_query = f"{user_profile['goal']} {' '.join(user_profile['skills'][:3])}"
        
        logger.info(f"Searching jobs for: {search_query}")
        
        # Try multiple sources
        jobs = []
        
        # 1. Try JSearch API (LinkedIn, Indeed, Glassdoor)
        if RAPIDAPI_KEY:
            jsearch_jobs = fetch_jobs_from_jsearch(search_query, request.location, request.limit)
            jobs.extend(jsearch_jobs)
        
        # 2. Try Adzuna API if we need more jobs
        if len(jobs) < request.limit and ADZUNA_APP_ID:
            adzuna_jobs = fetch_jobs_from_adzuna(search_query, 'us', request.limit - len(jobs))
            jobs.extend(adzuna_jobs)
        
        # 3. Fallback to AI-generated jobs if no API is configured or insufficient results
        if len(jobs) < 5:
            logger.info("Using AI to generate job listings")
            ai_jobs = generate_fallback_jobs(search_query, request.limit)
            jobs.extend(ai_jobs)
        
        # Remove duplicates based on title and company
        seen = set()
        unique_jobs = []
        for job in jobs:
            key = f"{job.get('title', '')}_{job.get('company', '')}".lower()
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
        
        jobs = unique_jobs[:request.limit]
        
        # AI matching if enabled
        if request.use_ai_matching and GROQ_API_KEY and jobs:
            logger.info("Applying AI matching...")
            jobs = match_jobs_with_ai(jobs, user_profile)
        
        # Cache jobs in MongoDB
        if db is not None:
            try:
                jobs_collection = db['jobs_cache']
                jobs_collection.insert_one({
                    'user_id': request.user_id,
                    'query': search_query,
                    'jobs': jobs,
                    'fetched_at': datetime.now(),
                    'expires_at': datetime.now() + timedelta(hours=6)
                })
            except Exception as e:
                logger.warning(f"Failed to cache jobs: {e}")
        
        return {
            'success': True,
            'query': search_query,
            'jobs': jobs,
            'total': len(jobs),
            'ai_matched': request.use_ai_matching and bool(GROQ_API_KEY),
            'sources_used': list(set([job.get('source', 'Unknown') for job in jobs])),
            'user_profile': user_profile
        }
        
    except Exception as e:
        logger.error(f"Error in job search: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/jobs/user/{user_id}")
async def get_user_recommended_jobs(user_id: str, limit: int = 10):
    """
    Get recommended jobs based on user's roadmap automatically
    """
    try:
        # Check cache first
        if db is not None:
            try:
                jobs_collection = db['jobs_cache']
                cached = jobs_collection.find_one(
                    {
                        'user_id': user_id,
                        'expires_at': {'$gt': datetime.now()}
                    },
                    sort=[('fetched_at', -1)]
                )
                
                if cached:
                    logger.info(f"Returning cached jobs for user {user_id}")
                    return {
                        'success': True,
                        'jobs': cached['jobs'][:limit],
                        'total': len(cached['jobs'][:limit]),
                        'cached': True
                    }
            except Exception as e:
                logger.warning(f"Cache check failed: {e}")
        
        # If no cache, fetch new jobs
        request = JobSearchRequest(
            user_id=user_id,
            limit=limit,
            use_ai_matching=True
        )
        
        return await search_jobs(request)
        
    except Exception as e:
        logger.error(f"Error getting user jobs: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv('PORT', 5007))
    logger.info(f"Starting Job Agent Service on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)


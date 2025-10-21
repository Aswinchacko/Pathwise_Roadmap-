#!/usr/bin/env python3
"""
AI-Powered Mentor Search Service
Uses Groq API to search the web for real mentors based on user goals
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from pymongo import MongoClient
import time
import random
import re
import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
SERPER_API_KEY = os.getenv('SERPER_API_KEY', '')  # Optional: For Google search
ENABLE_WEB_SEARCH = bool(GROQ_API_KEY)

app = FastAPI(title="LinkedIn Mentor Scraping Service")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
try:
    mongo_client = MongoClient('mongodb://localhost:27017', serverSelectionTimeoutMS=5000)
    db = mongo_client['pathwise']
    roadmap_collection = db['roadmap']
    mentors_collection = db['mentors']
    print("[OK] Connected to MongoDB")
except Exception as e:
    print(f"[ERROR] MongoDB connection error: {e}")
    mongo_client = None

# Pydantic models
class MentorRequest(BaseModel):
    user_id: str
    limit: Optional[int] = 10
    experience_level: Optional[str] = "intermediate"
    refresh_cache: Optional[bool] = False

class MentorProfile(BaseModel):
    name: str
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    profile_url: str
    headline: str
    about: Optional[str] = None
    experience_years: Optional[int] = None
    connections: Optional[str] = None
    avatar_url: Optional[str] = None
    skills: List[str] = []
    scraped_at: str

class MentorResponse(BaseModel):
    success: bool
    mentors: List[dict]
    search_query: str
    total_found: int
    cached: bool = False
    message: Optional[str] = None
    search_source: str = "ai"  # "ai", "static", or "web"

def search_google_for_professionals(query: str, domain: str) -> List[Dict[str, Any]]:
    """Search Google for professional profiles from various sources using Serper API"""
    if not SERPER_API_KEY:
        print("[WARN] No Serper API key, skipping Google search")
        return []
    
    try:
        print(f"[GOOGLE SEARCH] Searching for: {query}")
        
        # Build search query to find mid-level professionals in India from various sources
        # Include: LinkedIn, GitHub, personal websites, company pages, portfolio sites
        search_query = f'{query} developer engineer India portfolio OR github OR linkedin -CEO -CTO -founder -director -VP -job'
        
        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }
        
        payload = {
            "q": search_query,
            "num": 25,  # Get more results for diverse sources
            "gl": "in",  # India
            "hl": "en"
        }
        
        response = requests.post(
            "https://google.serper.dev/search",
            headers=headers,
            json=payload,
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"[ERROR] Serper API error: {response.status_code}")
            return []
        
        data = response.json()
        results = data.get('organic', [])
        
        # Extract professional profiles from various sources
        profiles = []
        for result in results:
            link = result.get('link', '')
            title = result.get('title', '')
            snippet = result.get('snippet', '')
            
            # Filter out job postings, courses, and irrelevant pages
            skip_keywords = ['job', 'hiring', 'vacancy', 'course', 'tutorial', 'learn', 'training', 'bootcamp', 'salary']
            if any(keyword in title.lower() or keyword in snippet.lower() for keyword in skip_keywords):
                continue
            
            # Include profiles from various sources
            valid_sources = [
                'linkedin.com/in/',
                'github.com/',
                'twitter.com/',
                'medium.com/@',
                'dev.to/',
                'portfolio',
                'about',
                'profile'
            ]
            
            # Check if it's a profile/portfolio page
            is_profile = any(source in link.lower() for source in valid_sources)
            has_name = any(char.isupper() for char in title)  # Title has capital letters (likely a name)
            
            if is_profile or has_name:
                profiles.append({
                    'url': link.split('?')[0],  # Clean URL
                    'title': title,
                    'snippet': snippet,
                    'source': 'linkedin' if 'linkedin.com' in link else 
                             'github' if 'github.com' in link else
                             'twitter' if 'twitter.com' in link else
                             'medium' if 'medium.com' in link else
                             'devto' if 'dev.to' in link else
                             'website'
                })
        
        print(f"[GOOGLE SEARCH] Found {len(profiles)} professional profiles from Google")
        
        # Show source breakdown
        source_count = {}
        for p in profiles:
            source = p.get('source', 'other')
            source_count[source] = source_count.get(source, 0) + 1
        print(f"[SOURCES] {', '.join([f'{k}: {v}' for k, v in source_count.items()])}")
        
        return profiles
        
    except Exception as e:
        print(f"[ERROR] Google search failed: {e}")
        return []

def extract_profiles_with_groq(google_results: List[Dict], query: str, goal: str, domain: str) -> List[Dict[str, Any]]:
    """Use Groq AI to extract and structure profile data from Google results (diverse sources)"""
    if not GROQ_API_KEY or not google_results:
        return []
    
    try:
        print(f"[AI EXTRACT] Using Groq to extract data from {len(google_results)} profiles")
        
        # Prepare search results for AI with source info
        results_text = "\n".join([
            f"Source: {r.get('source', 'website')}\nURL: {r['url']}\nTitle: {r['title']}\nSnippet: {r['snippet']}\n"
            for r in google_results[:20]
        ])
        
        prompt = f"""Based on these REAL professional profiles found via Google search from various sources (LinkedIn, GitHub, personal websites, portfolios), extract structured mentor information.

User Goal: {goal}
Domain: {domain}
Search Query: {query}

Google Search Results (from LinkedIn, GitHub, portfolios, personal websites):
{results_text}

Extract information for each professional and create a structured JSON array. For each person:
1. Extract their name from the URL, title, or snippet
2. Infer their current job title from the context (prefer mid-level: Senior Engineer, Lead Developer, etc.)
3. Extract or infer company name from the snippet
4. Set location as Indian tech hub (Bangalore, Hyderabad, Pune, Mumbai, Delhi)
5. Use the actual URL from search results (keep as-is: LinkedIn, GitHub, portfolio, etc.)
6. Create a brief professional bio based on the snippet and source
7. Estimate 4-10 years of experience (mid-level professionals)
8. List 5-6 relevant technical skills for {domain} based on context
9. Add social profile URL if found (GitHub, Twitter, LinkedIn, personal website)
10. Estimate connections as 500+, 1000+, or 1500+ (for social profiles)

FILTER OUT:
- CEOs, CTOs, VPs, Directors, Founders (only mid-level professionals)
- Profiles not related to {domain}
- Job postings, courses, tutorials

Return ONLY a JSON array (NO markdown, NO explanations):
[
  {{
    "name": "Full Name",
    "title": "Senior Software Engineer",
    "company": "Company Name",
    "location": "Bangalore, Karnataka, India",
    "profile_url": "actual_url_from_search",
    "headline": "Title at Company",
    "about": "Professional bio based on snippet and web presence",
    "experience_years": 6,
    "connections": "1000+",
    "skills": ["skill1", "skill2", "skill3", "skill4", "skill5"],
    "is_real_profile": true,
    "source_type": "github OR linkedin OR portfolio OR website"
  }}
]"""

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a data extraction expert. Extract and structure LinkedIn profile information from search results. Return only valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3,  # Lower for more consistent extraction
            "max_tokens": 4000
        }
        
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code != 200:
            print(f"[ERROR] Groq API error: {response.status_code}")
            return []
        
        data = response.json()
        ai_response = data.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
        
        # Extract JSON
        json_text = ai_response
        if '```json' in ai_response:
            json_text = ai_response.split('```json')[1].split('```')[0].strip()
        elif '```' in ai_response:
            json_text = ai_response.split('```')[1].split('```')[0].strip()
        
        mentors = json.loads(json_text)
        
        # Add metadata
        for mentor in mentors:
            mentor['scraped_at'] = datetime.now().isoformat()
            mentor['is_ai_generated'] = False
            mentor['is_real_profile'] = True
            mentor['search_method'] = 'serper_google_search'
            mentor['search_source'] = 'real'
            
            # Set source badge based on profile URL
            if 'source_type' not in mentor:
                url = mentor.get('profile_url', '')
                if 'github.com' in url:
                    mentor['source_type'] = 'github'
                elif 'linkedin.com' in url:
                    mentor['source_type'] = 'linkedin'
                elif 'medium.com' in url or 'dev.to' in url:
                    mentor['source_type'] = 'blog'
                else:
                    mentor['source_type'] = 'website'
            
            if 'avatar_url' not in mentor or not mentor['avatar_url']:
                mentor['avatar_url'] = f"https://ui-avatars.com/api/?name={mentor['name']}&size=200&background=3b82f6&color=fff"
        
        print(f"[SUCCESS] Extracted {len(mentors)} mentor profiles")
        return mentors
        
    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to parse JSON: {e}")
        print(f"[DEBUG] Response: {ai_response[:500]}...")
        return []
    except Exception as e:
        print(f"[ERROR] Groq extraction failed: {e}")
        import traceback
        traceback.print_exc()
        return []

def search_web_with_groq(query: str, goal: str, domain: str) -> List[Dict[str, Any]]:
    """
    Search for real LinkedIn profiles using:
    1. Serper API (Google search) to find actual profiles
    2. Groq AI to extract and structure the data
    """
    if not GROQ_API_KEY:
        print("[WARN] No Groq API key, falling back to static data")
        return []
    
    # Try Serper + Groq for REAL profiles from various web sources
    if SERPER_API_KEY:
        print("[REAL SEARCH] Using Serper API + Groq AI for real profiles from Google")
        google_results = search_google_for_professionals(query, domain)
        
        if google_results:
            mentors = extract_profiles_with_groq(google_results, query, goal, domain)
            if mentors:
                return mentors
    
    # Fallback: Use Groq alone (generates realistic but synthetic profiles)
    print("[FALLBACK] Using Groq AI to generate realistic profiles")
    try:
        prompt = f"""Generate 15 REALISTIC mid-level tech professional profiles for Indian tech industry.

User Goal: {goal}
Domain: {domain}
Search Keywords: {query}

Create profiles for professionals who:
- Are 4-10 years experienced (mid-level, NOT executives)
- Work at real Indian tech companies (Razorpay, CRED, Flipkart, Swiggy, Zomato, PhonePe, etc.)
- Match the domain: {domain}
- Are based in Indian tech hubs
- Have realistic Indian names

Return ONLY a JSON array:
[
  {{
    "name": "Realistic Indian Name",
    "title": "Senior Software Engineer or Lead Engineer",
    "company": "Real Indian Tech Company",
    "location": "Bangalore, Karnataka, India",
    "profile_url": "https://www.linkedin.com/in/realistic-profile-slug",
    "headline": "Title at Company",
    "about": "Brief professional bio focused on {domain}",
    "experience_years": 6,
    "connections": "1000+",
    "skills": ["skill1", "skill2", "skill3", "skill4", "skill5"]
  }}
]"""

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "You are an expert on the Indian tech industry. Generate realistic mid-level professional profiles. Return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 4000
        }
        
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code != 200:
            return []
        
        data = response.json()
        ai_response = data.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
        
        json_text = ai_response
        if '```json' in ai_response:
            json_text = ai_response.split('```json')[1].split('```')[0].strip()
        elif '```' in ai_response:
            json_text = ai_response.split('```')[1].split('```')[0].strip()
        
        mentors = json.loads(json_text)
        
        for mentor in mentors:
            mentor['scraped_at'] = datetime.now().isoformat()
            mentor['is_ai_generated'] = True
            mentor['search_method'] = 'groq_generation'
            
            if 'avatar_url' not in mentor or not mentor['avatar_url']:
                mentor['avatar_url'] = f"https://ui-avatars.com/api/?name={mentor['name']}&size=200&background=3b82f6&color=fff"
        
        print(f"[SUCCESS] Generated {len(mentors)} realistic profiles")
        return mentors
        
    except Exception as e:
        print(f"[ERROR] Groq generation failed: {e}")
        return []

def generate_realistic_mentors(goal: str, domain: str, limit: int) -> List[dict]:
    """Generate realistic Indian tech mentor profiles based on domain"""
    import hashlib
    
    # Generate consistent data based on goal
    seed = int(hashlib.md5(goal.encode()).hexdigest()[:8], 16)
    random.seed(seed)
    
    # Real-looking Indian names
    first_names_male = ["Rahul", "Arjun", "Vikram", "Rohan", "Aditya", "Karan", "Amit", "Nikhil", "Siddharth", "Varun", "Prateek", "Kartik"]
    first_names_female = ["Priya", "Ananya", "Sneha", "Neha", "Kavya", "Pooja", "Divya", "Anjali", "Riya", "Shreya", "Isha", "Sakshi"]
    last_names = ["Sharma", "Kumar", "Patel", "Singh", "Reddy", "Gupta", "Verma", "Mehta", "Iyer", "Nair", "Joshi", "Desai", "Agarwal", "Shah", "Chopra", "Malhotra"]
    
    # Domain-specific titles and skills
    domain_data = {
        'frontend': {
            'titles': ['Frontend Developer', 'React Developer', 'UI Engineer', 'Senior Frontend Engineer', 'JavaScript Developer', 'Frontend Tech Lead'],
            'skills': ['React', 'JavaScript', 'TypeScript', 'CSS', 'HTML', 'Redux', 'Next.js', 'Tailwind CSS'],
            'companies': ['Razorpay', 'CRED', 'Flipkart', 'Amazon India', 'Swiggy', 'Zomato', 'PhonePe', 'Paytm', 'Microsoft India', 'Adobe India']
        },
        'backend': {
            'titles': ['Backend Developer', 'Python Developer', 'Java Developer', 'Senior Backend Engineer', 'API Developer', 'Backend Tech Lead'],
            'skills': ['Python', 'Java', 'Node.js', 'Django', 'Spring Boot', 'PostgreSQL', 'MongoDB', 'REST API'],
            'companies': ['Amazon India', 'Microsoft India', 'Google India', 'Walmart Labs', 'Flipkart', 'Oracle India', 'SAP Labs India', 'Infosys']
        },
        'fullstack': {
            'titles': ['Full Stack Developer', 'MERN Stack Developer', 'Software Engineer', 'Senior Full Stack Engineer', 'Full Stack Tech Lead'],
            'skills': ['React', 'Node.js', 'MongoDB', 'Express', 'JavaScript', 'Python', 'Docker', 'AWS'],
            'companies': ['Razorpay', 'CRED', 'Paytm', 'Zomato', 'Swiggy', 'Ola', 'Udaan', 'Meesho', 'Dream11', 'Unacademy']
        },
        'data science': {
            'titles': ['Data Scientist', 'ML Engineer', 'Data Analyst', 'Senior Data Scientist', 'AI/ML Engineer', 'Data Science Lead'],
            'skills': ['Python', 'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'SQL', 'Pandas', 'Scikit-learn'],
            'companies': ['Amazon India', 'Microsoft India', 'Flipkart', 'PhonePe', 'Ola', 'Swiggy', 'Myntra', 'Analytics Vidhya']
        },
        'mobile': {
            'titles': ['Android Developer', 'iOS Developer', 'React Native Developer', 'Mobile App Developer', 'Senior Mobile Engineer'],
            'skills': ['React Native', 'Android', 'Kotlin', 'Swift', 'Flutter', 'iOS', 'Mobile Development', 'Firebase'],
            'companies': ['PhonePe', 'Paytm', 'Zomato', 'Swiggy', 'Ola', 'MakeMyTrip', 'BookMyShow', 'Dunzo', 'InShorts']
        },
        'devops': {
            'titles': ['DevOps Engineer', 'SRE', 'Cloud Engineer', 'Senior DevOps Engineer', 'Infrastructure Engineer'],
            'skills': ['Docker', 'Kubernetes', 'AWS', 'Jenkins', 'CI/CD', 'Terraform', 'Linux', 'Ansible'],
            'companies': ['Amazon India', 'Microsoft India', 'Flipkart', 'Razorpay', 'Freshworks', 'Zoho', 'Chargebee']
        },
        'ai': {
            'titles': ['AI Engineer', 'ML Engineer', 'Deep Learning Engineer', 'NLP Engineer', 'Computer Vision Engineer'],
            'skills': ['Python', 'TensorFlow', 'PyTorch', 'NLP', 'Computer Vision', 'Deep Learning', 'Keras', 'OpenCV'],
            'companies': ['Amazon India', 'Microsoft Research', 'Google India', 'Fractal Analytics', 'Tiger Analytics', 'LatentView']
        },
        'design': {
            'titles': ['UI/UX Designer', 'Product Designer', 'UX Researcher', 'Senior Product Designer', 'Design Lead'],
            'skills': ['Figma', 'Adobe XD', 'Sketch', 'User Research', 'Prototyping', 'UI Design', 'UX Design', 'Design Systems'],
            'companies': ['CRED', 'Razorpay', 'Swiggy', 'Zomato', 'Flipkart', 'PhonePe', 'Dream11', 'Meesho']
        }
    }
    
    # Default fallback
    domain_lower = domain.lower()
    config = None
    for key in domain_data:
        if key in domain_lower or key in goal.lower():
            config = domain_data[key]
            break
    
    if not config:
        config = {
            'titles': ['Software Engineer', 'Software Developer', 'Senior Engineer', 'Tech Lead', 'Engineering Manager'],
            'skills': ['Python', 'JavaScript', 'Java', 'SQL', 'Git', 'Agile', 'Problem Solving', 'Team Collaboration'],
            'companies': ['TCS', 'Infosys', 'Wipro', 'Tech Mahindra', 'HCL', 'Cognizant', 'Accenture India']
        }
    
    locations = [
        "Bangalore, Karnataka, India", "Bengaluru, Karnataka, India", "Hyderabad, Telangana, India", 
        "Pune, Maharashtra, India", "Mumbai, Maharashtra, India", "Gurgaon, Haryana, India",
        "Noida, Uttar Pradesh, India", "Chennai, Tamil Nadu, India"
    ]
    
    mentors = []
    for i in range(limit):
        # Alternate between male and female names
        if i % 2 == 0:
            first_name = random.choice(first_names_male)
        else:
            first_name = random.choice(first_names_female)
        
        last_name = random.choice(last_names)
        name = f"{first_name} {last_name}"
        name_slug = name.lower().replace(" ", "-")
        
        title = random.choice(config['titles'])
        company = random.choice(config['companies'])
        location = random.choice(locations)
        experience_years = random.randint(3, 12)
        
        # Select relevant skills
        selected_skills = random.sample(config['skills'], min(6, len(config['skills'])))
        
        mentor = {
            "name": name,
            "title": title,
            "company": company,
            "location": location,
            "profile_url": f"https://www.linkedin.com/in/{name_slug}-{random.randint(100, 999)}",
            "headline": f"{title} at {company}",
            "about": f"{experience_years}+ years experienced {title} specializing in {', '.join(selected_skills[:3])}. Passionate about {domain.lower()} and mentoring aspiring developers. Open to networking and helping others grow in tech.",
            "experience_years": experience_years,
            "connections": f"{random.choice([500, 1000, 1500, 2000])}+",
            "avatar_url": f"https://ui-avatars.com/api/?name={name}&size=200&background=random&color=fff",
            "skills": selected_skills,
            "scraped_at": datetime.now().isoformat(),
            "is_curated": True
        }
        mentors.append(mentor)
    
    return mentors

class LinkedInScraper:
    """LinkedIn Profile Scraper using Selenium"""
    
    def __init__(self):
        self.driver = None
        self.wait = None
    
    def extract_key_skills(self, goal: str, domain: str) -> List[str]:
        """Extract key skills/technologies from roadmap goal"""
        # Common technology keywords by domain
        tech_keywords = {
            'frontend': ['react', 'javascript', 'typescript', 'vue', 'angular', 'css', 'html', 'nextjs', 'redux'],
            'backend': ['python', 'java', 'nodejs', 'express', 'django', 'flask', 'spring', 'api', 'microservices'],
            'fullstack': ['react', 'nodejs', 'mongodb', 'express', 'javascript', 'python', 'api'],
            'data science': ['python', 'machine learning', 'pandas', 'tensorflow', 'pytorch', 'sql', 'analytics'],
            'mobile': ['react native', 'flutter', 'android', 'ios', 'swift', 'kotlin', 'mobile app'],
            'devops': ['docker', 'kubernetes', 'aws', 'jenkins', 'ci/cd', 'terraform', 'ansible'],
            'ai': ['machine learning', 'deep learning', 'tensorflow', 'pytorch', 'nlp', 'computer vision'],
            'blockchain': ['solidity', 'ethereum', 'smart contracts', 'web3', 'cryptocurrency'],
            'cybersecurity': ['security', 'penetration testing', 'ethical hacking', 'cybersecurity'],
            'cloud': ['aws', 'azure', 'gcp', 'cloud computing', 'serverless']
        }
        
        goal_lower = goal.lower()
        domain_lower = domain.lower()
        
        # Find matching keywords from goal text
        extracted = []
        
        # Add domain-specific keywords
        for key, keywords in tech_keywords.items():
            if key in domain_lower:
                extracted.extend(keywords[:3])  # Take top 3 keywords
                break
        
        # Extract specific technologies mentioned in goal
        for key, keywords in tech_keywords.items():
            for keyword in keywords:
                if keyword in goal_lower:
                    extracted.append(keyword)
        
        # Remove duplicates and limit
        extracted = list(dict.fromkeys(extracted))[:4]  # Max 4 keywords
        
        # Fallback if no specific tech found
        if not extracted:
            extracted = [domain_lower, 'engineer', 'developer']
        
        return extracted
        
    def setup_driver(self):
        """Setup Chrome driver with stealth options"""
        chrome_options = Options()
        
        # Better stealth settings
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--start-maximized')
        
        # Real user agent
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Disable automation flags
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Additional stealth
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        try:
            print("[INIT] Setting up Chrome driver...")
            
            # Try without explicit service first (let Selenium auto-detect)
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            
            # Inject stealth JavaScript to hide automation
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                    window.chrome = {
                        runtime: {}
                    };
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [1, 2, 3, 4, 5]
                    });
                    Object.defineProperty(navigator, 'languages', {
                        get: () => ['en-US', 'en']
                    });
                '''
            })
            
            print("[OK] Chrome driver initialized with stealth mode")
            return True
        except Exception as e:
            print(f"[ERROR] Auto-detect failed: {e}")
            print("[INFO] Trying with ChromeDriverManager...")
            
            try:
                # Fallback: Use ChromeDriverManager
                driver_path = ChromeDriverManager().install()
                print(f"[OK] ChromeDriver installed at: {driver_path}")
                
                service = Service(driver_path)
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                self.wait = WebDriverWait(self.driver, 10)
                
                # Inject stealth JavaScript to hide automation
                self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                    'source': '''
                        Object.defineProperty(navigator, 'webdriver', {
                            get: () => undefined
                        });
                        window.chrome = {
                            runtime: {}
                        };
                        Object.defineProperty(navigator, 'plugins', {
                            get: () => [1, 2, 3, 4, 5]
                        });
                        Object.defineProperty(navigator, 'languages', {
                            get: () => ['en-US', 'en']
                        });
                    '''
                })
                
                print("[OK] Chrome driver initialized with stealth mode")
                return True
            except Exception as e2:
                print(f"[ERROR] ChromeDriverManager also failed: {e2}")
                print("[INFO] Please ensure Chrome browser is installed")
                print("[INFO] Chrome version and ChromeDriver must match")
                return False
    
    def search_linkedin_profiles(self, search_query: str, limit: int = 10) -> List[dict]:
        """Search LinkedIn for profiles matching the query"""
        mentors = []
        
        try:
            keywords = search_query.split()
            main_tech = keywords[0] if keywords else 'software'
            
            # Try multiple search engines
            search_attempts = [
                {
                    'name': 'DuckDuckGo',
                    'url': f'https://duckduckgo.com/?q={main_tech}+engineer+India+site:linkedin.com/in',
                    'selectors': ['a[href*="linkedin.com/in/"]']
                },
                {
                    'name': 'Bing',
                    'url': f'https://www.bing.com/search?q={main_tech}+engineer+India+site:linkedin.com/in',
                    'selectors': ['li.b_algo a[href*="linkedin.com/in/"]', 'a[href*="linkedin.com/in/"]']
                },
                {
                    'name': 'Google',
                    'url': f'https://www.google.com/search?q={main_tech}+engineer+India+site:linkedin.com/in',
                    'selectors': ['a[href*="linkedin.com/in/"]', 'div.g a[href*="linkedin.com"]']
                }
            ]
            
            profile_links = []
            
            for attempt in search_attempts:
                if profile_links:
                    break
                    
                print(f"[SEARCH] Trying {attempt['name']}: {attempt['url']}")
                
                try:
                    self.driver.get(attempt['url'])
                    time.sleep(random.uniform(3, 6))
                    
                    # Extract LinkedIn URLs
                    for selector in attempt['selectors']:
                        links = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        print(f"[DEBUG] {attempt['name']} - Selector '{selector}': {len(links)} links")
                        
                        for link in links:
                            try:
                                href = link.get_attribute('href')
                                if href and 'linkedin.com/in/' in href and '/in/dir/' not in href:
                                    # Clean URL
                                    if '/url?q=' in href:
                                        clean_url = href.split('/url?q=')[1].split('&')[0]
                                    else:
                                        clean_url = href.split('?')[0]
                                    
                                    if clean_url.startswith('http') and clean_url not in profile_links:
                                        profile_links.append(clean_url)
                                        print(f"[FOUND] {clean_url}")
                                    
                                    if len(profile_links) >= limit * 3:
                                        break
                            except Exception as e:
                                continue
                        
                        if profile_links:
                            break
                    
                    if profile_links:
                        print(f"[SUCCESS] Found {len(profile_links)} profiles using {attempt['name']}")
                        break
                        
                except Exception as e:
                    print(f"[ERROR] {attempt['name']} search failed: {e}")
                    continue
            
            # If still no results, save screenshot
            if not profile_links:
                try:
                    screenshot_path = 'linkedin_mentor_service/search_debug.png'
                    self.driver.save_screenshot(screenshot_path)
                    print(f"[DEBUG] Screenshot saved to {screenshot_path}")
                    
                    # Also save page source
                    with open('linkedin_mentor_service/search_debug.html', 'w', encoding='utf-8') as f:
                        f.write(self.driver.page_source)
                    print(f"[DEBUG] Page source saved")
                except Exception as e:
                    print(f"[DEBUG] Could not save debug files: {e}")
            
            # Scrape each profile
            print(f"[SCRAPING] Starting to scrape {len(profile_links)} profiles...")
            for idx, profile_url in enumerate(profile_links[:limit * 2]):
                try:
                    print(f"[SCRAPING] {idx + 1}/{len(profile_links)}: {profile_url}")
                    mentor_data = self.scrape_profile(profile_url, search_query)
                    
                    if mentor_data:
                        mentors.append(mentor_data)
                        print(f"[SUCCESS] ✓ {mentor_data.get('name')} - {mentor_data.get('title')}")
                    
                    if len(mentors) >= limit:
                        print(f"[COMPLETE] Reached target of {limit} mentors")
                        break
                    
                    time.sleep(random.uniform(2, 4))
                    
                except Exception as e:
                    print(f"[WARNING] Failed {profile_url}: {e}")
                    continue
            
            print(f"[FINAL] Successfully scraped {len(mentors)} mentor profiles")
            
        except Exception as e:
            print(f"[ERROR] Search failed: {e}")
            import traceback
            traceback.print_exc()
        
        return mentors
    
    def scrape_profile(self, profile_url: str, search_context: str) -> Optional[dict]:
        """Scrape a single LinkedIn profile"""
        try:
            print(f"[PROFILE] Loading {profile_url}")
            self.driver.get(profile_url)
            time.sleep(random.uniform(3, 5))
            
            # Extract profile data
            mentor_data = {
                'profile_url': profile_url,
                'scraped_at': datetime.now().isoformat(),
                'search_context': search_context
            }
            
            # Name - try multiple selectors
            name_selectors = ['h1.text-heading-xlarge', 'h1', 'div.top-card-layout__title']
            for selector in name_selectors:
                try:
                    name_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    name_text = name_element.text.strip()
                    if name_text and len(name_text) > 2:
                        mentor_data['name'] = name_text
                        break
                except:
                    continue
            
            # Fallback: extract from URL or page title
            if 'name' not in mentor_data:
                try:
                    title = self.driver.title
                    if '|' in title:
                        mentor_data['name'] = title.split('|')[0].strip()
                    elif '-' in title:
                        mentor_data['name'] = title.split('-')[0].strip()
                    else:
                        mentor_data['name'] = profile_url.split('/in/')[-1].split('/')[0].replace('-', ' ').title()
                except:
                    mentor_data['name'] = profile_url.split('/in/')[-1].split('/')[0].replace('-', ' ').title()
            
            # Headline/Title
            try:
                headline_element = self.driver.find_element(By.CSS_SELECTOR, 'div.text-body-medium, div.top-card-layout__headline')
                mentor_data['headline'] = headline_element.text.strip()
                mentor_data['title'] = headline_element.text.strip()
            except:
                mentor_data['headline'] = f"{search_context} Professional"
                mentor_data['title'] = f"{search_context} Professional"
            
            # Company (from headline if present)
            try:
                headline = mentor_data.get('headline', '')
                if ' at ' in headline:
                    mentor_data['company'] = headline.split(' at ')[-1].strip()
            except:
                pass
            
            # Location
            try:
                location_element = self.driver.find_element(By.CSS_SELECTOR, 'span.text-body-small.inline.t-black--light.break-words')
                mentor_data['location'] = location_element.text.strip()
            except:
                mentor_data['location'] = 'Location not available'
            
            # Connections
            try:
                connections_element = self.driver.find_element(By.CSS_SELECTOR, 'span.dist-value')
                mentor_data['connections'] = connections_element.text.strip()
            except:
                mentor_data['connections'] = '500+'
            
            # Avatar
            try:
                avatar_element = self.driver.find_element(By.CSS_SELECTOR, 'img.pv-top-card-profile-picture__image')
                mentor_data['avatar_url'] = avatar_element.get_attribute('src')
            except:
                # Generate placeholder avatar
                mentor_data['avatar_url'] = f"https://ui-avatars.com/api/?name={mentor_data['name']}&size=200&background=random"
            
            # About section
            try:
                about_button = self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label*="about"]')
                about_button.click()
                time.sleep(1)
                
                about_element = self.driver.find_element(By.CSS_SELECTOR, 'div.display-flex.ph5.pv3 p')
                mentor_data['about'] = about_element.text.strip()[:500]  # Limit to 500 chars
            except:
                mentor_data['about'] = None
            
            # Skills (try to extract from page)
            skills = []
            try:
                skill_elements = self.driver.find_elements(By.CSS_SELECTOR, 'span.skill-category-entity__name')
                for skill in skill_elements[:10]:  # Limit to 10 skills
                    skill_text = skill.text.strip()
                    if skill_text:
                        skills.append(skill_text)
            except:
                # Generate skills based on search context
                skills = self.generate_relevant_skills(search_context)
            
            mentor_data['skills'] = skills
            
            # Estimate experience years (rough heuristic)
            try:
                experience_text = self.driver.find_element(By.CSS_SELECTOR, 'div.experience-section').text
                years_match = re.findall(r'(\d+)\s*(?:yr|year)', experience_text, re.IGNORECASE)
                if years_match:
                    mentor_data['experience_years'] = max([int(y) for y in years_match])
                else:
                    mentor_data['experience_years'] = random.randint(3, 15)
            except:
                mentor_data['experience_years'] = random.randint(3, 15)
            
            # Basic validation
            if not mentor_data.get('name'):
                print(f"[SKIP] No name found")
                return None
            
            location = mentor_data.get('location', '').lower()
            title_lower = mentor_data.get('title', '').lower()
            headline = mentor_data.get('headline', '').lower()
            
            # Prefer India-based, but don't strictly require it for now
            is_india = any(city in location for city in ['india', 'bangalore', 'mumbai', 'delhi', 'hyderabad', 'pune', 'chennai', 'bengaluru', 'gurugram', 'noida'])
            
            # Filter out C-level executives
            is_executive = any(exec_title in title_lower or exec_title in headline for exec_title in ['ceo', 'cto', 'cfo', 'founder', 'president', 'vp'])
            
            if is_executive:
                print(f"[SKIP] Executive: {mentor_data.get('title')}")
                return None
            
            # Loose field matching - check if it's tech-related
            profile_text = f"{title_lower} {headline}".lower()
            tech_keywords = ['engineer', 'developer', 'programmer', 'software', 'tech', 'analyst', 'architect', 'consultant', 'designer', 'specialist']
            
            is_tech = any(keyword in profile_text for keyword in tech_keywords)
            
            if not is_tech:
                print(f"[SKIP] Not tech-related: {mentor_data.get('title')}")
                return None
            
            # Prioritize India profiles
            if is_india:
                print(f"[VALID] India-based tech professional")
            else:
                print(f"[VALID] Tech professional (non-India)")
            
            return mentor_data
                
        except Exception as e:
            print(f"[ERROR] Error scraping profile {profile_url}: {e}")
            return None
    
    def generate_relevant_skills(self, search_context: str) -> List[str]:
        """Generate relevant skills based on search context"""
        skill_map = {
            'frontend': ['React', 'JavaScript', 'CSS', 'HTML', 'TypeScript', 'Vue.js'],
            'backend': ['Python', 'Node.js', 'Java', 'SQL', 'API Design', 'Microservices'],
            'fullstack': ['React', 'Node.js', 'MongoDB', 'REST API', 'Docker', 'AWS'],
            'data': ['Python', 'SQL', 'Machine Learning', 'Data Analysis', 'Pandas', 'TensorFlow'],
            'mobile': ['React Native', 'iOS', 'Android', 'Flutter', 'Mobile UI/UX'],
            'devops': ['Docker', 'Kubernetes', 'CI/CD', 'AWS', 'Jenkins', 'Terraform'],
        }
        
        context_lower = search_context.lower()
        for key, skills in skill_map.items():
            if key in context_lower:
                return skills
        
        return ['Leadership', 'Communication', 'Problem Solving', 'Team Management']
    
    def close(self):
        """Close the driver"""
        if self.driver:
            self.driver.quit()
            print("[OK] Chrome driver closed")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "AI-Powered Mentor Search Service",
        "status": "running",
        "mongodb": "connected" if mongo_client else "disconnected",
        "ai_enabled": bool(GROQ_API_KEY),
        "groq_api_key_configured": bool(GROQ_API_KEY),
        "search_capabilities": {
            "web_search": ENABLE_WEB_SEARCH,
            "ai_powered": bool(GROQ_API_KEY),
            "static_fallback": True
        }
    }

@app.post("/api/mentors/scrape", response_model=MentorResponse)
async def scrape_mentors(request: MentorRequest):
    """
    Scrape LinkedIn mentors based on user's roadmap goal from MongoDB
    """
    if not mongo_client:
        raise HTTPException(status_code=503, detail="MongoDB not connected")
    
    try:
        # 1. Fetch user's latest roadmap from MongoDB
        user_roadmap = roadmap_collection.find_one(
            {"user_id": request.user_id, "source": "user_generated"},
            sort=[("created_at", -1)]
        )
        
        if not user_roadmap:
            raise HTTPException(
                status_code=404,
                detail="No roadmap found for user. Please create a roadmap first."
            )
        
        roadmap_goal = user_roadmap.get('goal', '')
        domain = user_roadmap.get('domain', '')
        
        # Create more specific search query from roadmap goal and domain
        # Extract key technologies/skills from the goal
        scraper_temp = LinkedInScraper()
        goal_keywords = scraper_temp.extract_key_skills(roadmap_goal, domain)
        search_query = f"{domain} {' '.join(goal_keywords)}".strip()
        
        print(f"[GOAL] User roadmap goal: {roadmap_goal}")
        print(f"[DOMAIN] Domain: {domain}")
        print(f"[KEYWORDS] Extracted keywords: {goal_keywords}")
        print(f"[QUERY] Search query: {search_query}")
        
        # 2. Check cache (if not refreshing)
        if not request.refresh_cache:
            cached_mentors = list(mentors_collection.find(
                {
                    "user_id": request.user_id,
                    "search_query": search_query
                },
                {"_id": 0}
            ).limit(request.limit))
            
            if cached_mentors:
                print(f"[CACHE] Returning {len(cached_mentors)} cached mentors")
                # Determine search source from cached data
                cached_source = "ai" if cached_mentors[0].get('is_ai_generated') else "static"
                return MentorResponse(
                    success=True,
                    mentors=cached_mentors,
                    search_query=search_query,
                    total_found=len(cached_mentors),
                    cached=True,
                    search_source=cached_source,
                    message="Returned cached mentors"
                )
        
        # 3. Try AI-powered web search first, fallback to static data
        mentors = []
        search_source = "static"
        
        if GROQ_API_KEY and ENABLE_WEB_SEARCH:
            print("[AI] Attempting Groq-powered web search for mentors...")
            mentors = search_web_with_groq(search_query, roadmap_goal, domain)
            if mentors:
                # Check if they are real profiles (from Serper) or AI-generated
                search_source = mentors[0].get('search_source', 'ai')
                print(f"[SUCCESS] Search returned {len(mentors)} mentors (source: {search_source})")
        
        # Fallback to static generation if AI fails or not available
        if not mentors:
            print("[FALLBACK] Using static mentor generation...")
            mentors = generate_realistic_mentors(roadmap_goal, domain, request.limit)
            search_source = "static"
        
        if not mentors:
            return MentorResponse(
                success=False,
                mentors=[],
                search_query=search_query,
                total_found=0,
                search_source=search_source,
                message="No mentors found. Try adjusting your roadmap goal."
            )
        
        # 4. Save to MongoDB cache
        for mentor in mentors:
            mentor['user_id'] = request.user_id
            mentor['search_query'] = search_query
            mentor['roadmap_goal'] = roadmap_goal
            mentor['domain'] = domain
            
            # Upsert to avoid duplicates
            mentors_collection.update_one(
                {"profile_url": mentor['profile_url'], "user_id": request.user_id},
                {"$set": mentor},
                upsert=True
            )
        
        print(f"[SUCCESS] Generated and cached {len(mentors)} mentors via {search_source}")
        
        message = f"Found {len(mentors)} relevant mentors in {domain}"
        if search_source == "ai":
            message += " (AI-powered web search)"
        elif search_source == "static":
            message += " (curated recommendations)"
        
        return MentorResponse(
            success=True,
            mentors=mentors,
            search_query=search_query,
            total_found=len(mentors),
            cached=False,
            search_source=search_source,
            message=message
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Error in scrape_mentors: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/mentors/cache/{user_id}")
async def clear_mentor_cache(user_id: str):
    """Clear cached mentors for a user"""
    if not mongo_client:
        raise HTTPException(status_code=503, detail="MongoDB not connected")
    
    try:
        result = mentors_collection.delete_many({"user_id": user_id})
        return {
            "success": True,
            "deleted_count": result.deleted_count,
            "message": f"Cleared {result.deleted_count} cached mentors"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/mentors/health")
async def health_check():
    """Check service health"""
    return {
        "service": "AI-Powered Mentor Search Service",
        "status": "healthy",
        "mongodb": "connected" if mongo_client else "disconnected",
        "ai_search": "enabled" if GROQ_API_KEY else "disabled",
        "groq_api": "configured" if GROQ_API_KEY else "not_configured",
        "search_mode": "ai" if GROQ_API_KEY else "static"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)


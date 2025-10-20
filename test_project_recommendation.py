"""
Test script for Project Recommendation Service
"""
import requests
import json

BASE_URL = "http://localhost:5003"

def test_health():
    """Test health check endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_get_all_projects():
    """Test getting all projects"""
    print("Testing get all projects...")
    response = requests.get(f"{BASE_URL}/api/projects")
    data = response.json()
    print(f"Status: {response.status_code}")
    print(f"Total projects: {data.get('total')}")
    print(f"First project: {data['projects'][0]['title']}\n")

def test_recommend_projects(aim):
    """Test project recommendation"""
    print(f"Testing recommendation for: '{aim}'...")
    response = requests.post(
        f"{BASE_URL}/api/recommend",
        json={"aim": aim, "limit": 5},
        headers={"Content-Type": "application/json"}
    )
    data = response.json()
    print(f"Status: {response.status_code}")
    print(f"Method: {data.get('method')}")
    print(f"Recommendations ({len(data.get('recommendations', []))}):")
    for i, project in enumerate(data.get('recommendations', []), 1):
        print(f"  {i}. {project['title']} - {project['difficulty']}")
        print(f"     Skills: {', '.join(project.get('skills', [])[:3])}")
    print()

def test_get_specific_project():
    """Test getting a specific project"""
    print("Testing get specific project (ID: 1)...")
    response = requests.get(f"{BASE_URL}/api/projects/1")
    data = response.json()
    print(f"Status: {response.status_code}")
    if data.get('success'):
        project = data['project']
        print(f"Project: {project['title']}")
        print(f"Description: {project['description']}")
        print(f"Skills: {', '.join(project['skills'])}\n")

def test_filter_by_category():
    """Test filtering projects by category"""
    print("Testing filter by category (ai-ml)...")
    response = requests.get(f"{BASE_URL}/api/projects?category=ai-ml")
    data = response.json()
    print(f"Status: {response.status_code}")
    print(f"AI/ML Projects: {data.get('total')}")
    for project in data.get('projects', []):
        print(f"  - {project['title']}")
    print()

def main():
    print("=" * 60)
    print("Project Recommendation Service Test")
    print("=" * 60)
    print()
    
    try:
        # Test health
        test_health()
        
        # Test all projects
        test_get_all_projects()
        
        # Test specific project
        test_get_specific_project()
        
        # Test filtering
        test_filter_by_category()
        
        # Test recommendations with different aims
        test_cases = [
            "I want to become a full-stack web developer",
            "I'm interested in machine learning and AI",
            "I want to learn data visualization and analytics",
            "I'm a beginner looking to learn Python",
            "I want to build mobile apps with React Native"
        ]
        
        for aim in test_cases:
            test_recommend_projects(aim)
        
        print("=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to service.")
        print("Make sure the service is running on http://localhost:5003")
        print("Run: python project_recommendation_service/main.py")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()


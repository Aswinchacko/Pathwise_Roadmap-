import requests
import json
import time

BASE_URL = "http://localhost:5003"

def test_phase_recommendation(phase: str, limit: int = 3):
    """Test phase-based project recommendations"""
    print(f"\n--- Testing Phase Recommendation for '{phase}' ---")
    try:
        response = requests.post(
            f"{BASE_URL}/api/recommend/phase",
            json={"phase": phase, "limit": limit},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        data = response.json()
        
        print(f"Phase Recommendation Response:")
        print(f"  Method: {data.get('method')}")
        print(f"  Phase: {data.get('phase')}")
        print(f"  Total: {data.get('total')}")
        print(f"  Success: {data.get('success')}")
        
        if data.get('recommendations'):
            print(f"\n  Projects:")
            for i, proj in enumerate(data.get('recommendations', []), 1):
                print(f"    {i}. {proj.get('title')}")
                print(f"       Difficulty: {proj.get('difficulty')}")
                print(f"       Category: {proj.get('category')}")
                print(f"       Duration: {proj.get('duration')}")
                print(f"       Skills: {', '.join(proj.get('skills', []))}")
                print(f"       Phase: {proj.get('phase')}")
                print(f"       Unlocked: {proj.get('unlocked')}")
                print()
        
        assert data['success'] == True
        assert len(data['recommendations']) <= limit
        assert data['method'] in ['phase-based-ai', 'phase-based-rules']
        print("✅ Phase recommendation test passed.")
        return data['recommendations']
        
    except requests.exceptions.ConnectionError:
        print("❌ Service is not running. Please start the backend service first.")
        return None
    except Exception as e:
        print(f"❌ Phase recommendation test failed: {e}")
        return None

def test_phase_save_project(project: dict):
    """Test saving a phase-based project"""
    print(f"\n--- Testing Save Phase Project: '{project.get('title')}' ---")
    try:
        response = requests.post(
            f"{BASE_URL}/api/projects/save",
            json=project,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        data = response.json()
        print(f"Save Phase Project Response: {data}")
        assert data['success'] == True
        assert 'id' in data
        print("✅ Save phase project test passed.")
        return data['id']
    except Exception as e:
        print(f"❌ Save phase project test failed: {e}")
        return None

def test_verify_phase_projects_in_db():
    """Verify phase-based projects are in the database"""
    print("\n--- Verifying Phase Projects in Database ---")
    try:
        response = requests.get(f"{BASE_URL}/api/projects")
        response.raise_for_status()
        data = response.json()
        
        phase_projects = [p for p in data.get('projects', []) if p.get('phase')]
        print(f"Total projects in DB: {len(data.get('projects', []))}")
        print(f"Phase-based projects: {len(phase_projects)}")
        
        if phase_projects:
            print("\nPhase-based projects found:")
            for proj in phase_projects:
                print(f"  - {proj.get('title')} (Phase: {proj.get('phase')})")
        
        assert data['success'] == True
        print("✅ Database verification passed.")
        return phase_projects
        
    except Exception as e:
        print(f"❌ Database verification failed: {e}")
        return None

if __name__ == "__main__":
    print("🧪 Testing Phase-Based Project Recommendations")
    print("=" * 60)
    
    # Test different phases
    test_phases = [
        "Design Fundamentals",
        "Adobe Creative Suite",
        "Web Development Basics",
        "Data Science Fundamentals"
    ]
    
    all_recommendations = []
    
    for phase in test_phases:
        recommendations = test_phase_recommendation(phase, limit=2)
        if recommendations:
            all_recommendations.extend(recommendations)
            
            # Save the first recommendation from each phase
            if recommendations:
                saved_id = test_phase_save_project(recommendations[0])
                if saved_id:
                    print(f"✅ Saved phase project with ID: {saved_id}")
        
        time.sleep(1)  # Small delay between requests
    
    # Verify all phase projects are in database
    phase_projects = test_verify_phase_projects_in_db()
    
    if phase_projects:
        print(f"\n🎉 Phase-Based Recommendation System Test Complete!")
        print(f"   Generated: {len(all_recommendations)} projects")
        print(f"   Saved to DB: {len(phase_projects)} projects")
        print(f"   Phases tested: {len(test_phases)}")
    else:
        print(f"\n❌ Phase-Based Recommendation System Test Failed!")

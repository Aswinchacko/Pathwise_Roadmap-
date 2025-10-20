import requests
import json
import time

BASE_URL = "http://localhost:5003"

def test_phase_projects_integration():
    """Test the complete phase-based projects integration"""
    print("🧪 Testing Phase-Based Projects Integration")
    print("=" * 60)
    
    # Test 1: Generate phase-based projects
    print("\n1. Generating phase-based projects...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/recommend/phase",
            json={
                "phase": "Design Fundamentals",
                "limit": 3
            },
            headers={"Content-Type": "application/json"}
        )
        
        if response.ok:
            data = response.json()
            print(f"✅ Generated {len(data['recommendations'])} phase-based projects")
            print(f"   Method: {data['method']}")
            print(f"   Phase: {data['phase']}")
            
            # Test 2: Save projects to database
            print("\n2. Saving projects to database...")
            saved_ids = []
            for i, project in enumerate(data['recommendations']):
                save_response = requests.post(
                    f"{BASE_URL}/api/projects/save",
                    json=project,
                    headers={"Content-Type": "application/json"}
                )
                
                if save_response.ok:
                    save_data = save_response.json()
                    saved_ids.append(save_data['id'])
                    print(f"   ✅ Project {i+1}: '{project['title']}' saved with ID {save_data['id']}")
                else:
                    print(f"   ❌ Failed to save project {i+1}: {save_response.status_text}")
            
            # Test 3: Verify projects in database
            print("\n3. Verifying projects in database...")
            verify_response = requests.get(f"{BASE_URL}/api/projects")
            
            if verify_response.ok:
                verify_data = verify_response.json()
                phase_projects = [p for p in verify_data['projects'] if p.get('phase')]
                print(f"   ✅ Found {len(phase_projects)} phase-based projects in database")
                
                for project in phase_projects:
                    print(f"      - {project['title']} (Phase: {project['phase']})")
                
                # Test 4: Test filtering
                print("\n4. Testing project filtering...")
                test_filters = ['all', 'phase-based', 'beginner', 'intermediate', 'advanced']
                
                for filter_type in test_filters:
                    filter_response = requests.get(
                        f"{BASE_URL}/api/projects",
                        params={'category': filter_type} if filter_type not in ['all', 'phase-based'] else {}
                    )
                    
                    if filter_response.ok:
                        filter_data = filter_response.json()
                        if filter_type == 'phase-based':
                            phase_count = len([p for p in filter_data['projects'] if p.get('phase')])
                            print(f"   ✅ Filter '{filter_type}': {phase_count} phase-based projects")
                        else:
                            print(f"   ✅ Filter '{filter_type}': {len(filter_data['projects'])} total projects")
                    else:
                        print(f"   ❌ Filter '{filter_type}' failed: {filter_response.status_text}")
                
                return True
            else:
                print(f"   ❌ Failed to verify projects: {verify_response.status_text}")
                return False
        else:
            print(f"❌ Failed to generate phase projects: {response.status_text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_multiple_phases():
    """Test multiple different phases"""
    print("\n" + "=" * 60)
    print("🔄 Testing Multiple Phases")
    print("=" * 60)
    
    phases = [
        "Design Fundamentals",
        "Adobe Creative Suite", 
        "Web Development Basics",
        "Data Science Fundamentals"
    ]
    
    all_saved = []
    
    for phase in phases:
        print(f"\n📚 Testing phase: {phase}")
        try:
            response = requests.post(
                f"{BASE_URL}/api/recommend/phase",
                json={"phase": phase, "limit": 2},
                headers={"Content-Type": "application/json"}
            )
            
            if response.ok:
                data = response.json()
                print(f"   ✅ Generated {len(data['recommendations'])} projects")
                
                # Save first project
                if data['recommendations']:
                    project = data['recommendations'][0]
                    save_response = requests.post(
                        f"{BASE_URL}/api/projects/save",
                        json=project,
                        headers={"Content-Type": "application/json"}
                    )
                    
                    if save_response.ok:
                        save_data = save_response.json()
                        all_saved.append(save_data['id'])
                        print(f"   ✅ Saved: '{project['title']}' (ID: {save_data['id']})")
                    else:
                        print(f"   ❌ Failed to save project")
            else:
                print(f"   ❌ Failed to generate projects for {phase}")
                
        except Exception as e:
            print(f"   ❌ Error with {phase}: {e}")
        
        time.sleep(1)  # Small delay between requests
    
    print(f"\n📊 Summary: {len(all_saved)} projects saved across {len(phases)} phases")
    return len(all_saved) > 0

def test_database_queries():
    """Test various database queries"""
    print("\n" + "=" * 60)
    print("🗄️ Testing Database Queries")
    print("=" * 60)
    
    try:
        # Get all projects
        response = requests.get(f"{BASE_URL}/api/projects")
        if response.ok:
            data = response.json()
            all_projects = data['projects']
            phase_projects = [p for p in all_projects if p.get('phase')]
            regular_projects = [p for p in all_projects if not p.get('phase')]
            
            print(f"📊 Database Statistics:")
            print(f"   Total projects: {len(all_projects)}")
            print(f"   Phase-based projects: {len(phase_projects)}")
            print(f"   Regular projects: {len(regular_projects)}")
            
            # Test by difficulty
            difficulties = {}
            for project in all_projects:
                diff = project.get('difficulty', 'unknown').lower()
                difficulties[diff] = difficulties.get(diff, 0) + 1
            
            print(f"\n📈 By Difficulty:")
            for diff, count in difficulties.items():
                print(f"   {diff.title()}: {count}")
            
            # Test by category
            categories = {}
            for project in all_projects:
                cat = project.get('category', 'unknown')
                categories[cat] = categories.get(cat, 0) + 1
            
            print(f"\n📂 By Category:")
            for cat, count in categories.items():
                print(f"   {cat}: {count}")
            
            return True
        else:
            print(f"❌ Failed to query database: {response.status_text}")
            return False
            
    except Exception as e:
        print(f"❌ Database query error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Phase-Based Projects Integration Test")
    print("=" * 60)
    
    # Test 1: Basic integration
    integration_success = test_phase_projects_integration()
    
    # Test 2: Multiple phases
    multiple_success = test_multiple_phases()
    
    # Test 3: Database queries
    database_success = test_database_queries()
    
    print("\n" + "=" * 60)
    print("📋 Test Results Summary")
    print("=" * 60)
    print(f"Integration Test: {'✅ PASS' if integration_success else '❌ FAIL'}")
    print(f"Multiple Phases: {'✅ PASS' if multiple_success else '❌ FAIL'}")
    print(f"Database Queries: {'✅ PASS' if database_success else '❌ FAIL'}")
    
    if integration_success and multiple_success and database_success:
        print(f"\n🎉 All tests passed! Phase-based projects integration is working perfectly!")
        print(f"\n📝 Next steps:")
        print(f"   1. Complete a phase in the roadmap")
        print(f"   2. Check the notification appears")
        print(f"   3. Click on project titles to save them")
        print(f"   4. Check the Projects page to see saved projects")
    else:
        print(f"\n⚠️ Some tests failed. Check the errors above.")

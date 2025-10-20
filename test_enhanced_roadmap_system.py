#!/usr/bin/env python3
"""
Comprehensive test suite for the enhanced roadmap system
Tests the improved matching algorithm, new datasets, and analytics features
"""

import requests
import json
import time
import random
from datetime import datetime

# Configuration
ROADMAP_API_URL = "http://localhost:8000"
TEST_USER_ID = "test_user_enhanced_" + str(int(time.time()))

def test_enhanced_roadmap_generation():
    """Test the enhanced roadmap generation with better matching"""
    print("🧪 Testing Enhanced Roadmap Generation...")
    
    test_cases = [
        {
            "goal": "Full Stack JavaScript Developer",
            "domain": "Full Stack Development",
            "expected_keywords": ["javascript", "react", "node", "mongodb"]
        },
        {
            "goal": "Python Data Scientist",
            "domain": "Data Science", 
            "expected_keywords": ["python", "pandas", "machine learning", "statistics"]
        },
        {
            "goal": "Mobile App Developer",
            "domain": "Mobile Development",
            "expected_keywords": ["mobile", "react native", "ios", "android"]
        },
        {
            "goal": "DevOps Engineer",
            "domain": "DevOps",
            "expected_keywords": ["docker", "kubernetes", "ci/cd", "aws"]
        },
        {
            "goal": "Cybersecurity Specialist",
            "domain": "Cybersecurity",
            "expected_keywords": ["security", "penetration testing", "encryption"]
        },
        {
            "goal": "Blockchain Developer",
            "domain": "Blockchain",
            "expected_keywords": ["blockchain", "smart contracts", "solidity"]
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases):
        print(f"  Test {i+1}: {test_case['goal']}")
        
        try:
            response = requests.post(f"{ROADMAP_API_URL}/api/roadmap/generate-roadmap", json={
                "goal": test_case["goal"],
                "domain": test_case["domain"],
                "user_id": TEST_USER_ID
            })
            
            if response.status_code == 200:
                data = response.json()
                
                # Check enhanced metadata
                assert "difficulty" in data, "Missing difficulty field"
                assert "estimated_hours" in data, "Missing estimated_hours field"
                assert "match_score" in data, "Missing match_score field"
                assert "prerequisites" in data, "Missing prerequisites field"
                assert "learning_outcomes" in data, "Missing learning_outcomes field"
                
                # Check match quality
                roadmap_text = json.dumps(data).lower()
                keyword_matches = sum(1 for keyword in test_case["expected_keywords"] 
                                    if keyword in roadmap_text)
                match_percentage = keyword_matches / len(test_case["expected_keywords"])
                
                results.append({
                    "goal": test_case["goal"],
                    "match_score": data.get("match_score", 0),
                    "keyword_match_percentage": match_percentage,
                    "difficulty": data.get("difficulty"),
                    "estimated_hours": data.get("estimated_hours"),
                    "steps_count": len(data.get("steps", [])),
                    "success": True
                })
                
                print(f"    ✅ Success - Match Score: {data.get('match_score', 0):.2f}, "
                      f"Keywords: {match_percentage:.1%}, "
                      f"Difficulty: {data.get('difficulty')}, "
                      f"Hours: {data.get('estimated_hours')}")
                
            else:
                print(f"    ❌ Failed - Status: {response.status_code}")
                results.append({
                    "goal": test_case["goal"],
                    "success": False,
                    "error": response.text
                })
                
        except Exception as e:
            print(f"    ❌ Error: {str(e)}")
            results.append({
                "goal": test_case["goal"],
                "success": False,
                "error": str(e)
            })
    
    # Summary
    successful_tests = sum(1 for r in results if r.get("success", False))
    print(f"\n📊 Enhanced Generation Results: {successful_tests}/{len(test_cases)} tests passed")
    
    if successful_tests > 0:
        avg_match_score = sum(r.get("match_score", 0) for r in results if r.get("success")) / successful_tests
        avg_keyword_match = sum(r.get("keyword_match_percentage", 0) for r in results if r.get("success")) / successful_tests
        print(f"   Average Match Score: {avg_match_score:.2f}")
        print(f"   Average Keyword Match: {avg_keyword_match:.1%}")
    
    return results

def test_roadmap_recommendations():
    """Test the new roadmap recommendations endpoint"""
    print("\n🎯 Testing Roadmap Recommendations...")
    
    test_cases = [
        {
            "interests": "web development javascript",
            "experience_level": "beginner",
            "time_commitment": 200
        },
        {
            "interests": "data science python machine learning",
            "experience_level": "intermediate", 
            "time_commitment": 400
        },
        {
            "interests": "mobile app development",
            "experience_level": "advanced",
            "time_commitment": 300
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"  Test {i+1}: {test_case['interests']} ({test_case['experience_level']})")
        
        try:
            response = requests.get(f"{ROADMAP_API_URL}/api/roadmap/roadmaps/recommendations", 
                                  params=test_case)
            
            if response.status_code == 200:
                data = response.json()
                recommendations = data.get("recommendations", [])
                
                print(f"    ✅ Got {len(recommendations)} recommendations")
                
                for j, rec in enumerate(recommendations[:3]):
                    score = rec.get("recommendation_score", 0)
                    goal = rec.get("goal", "Unknown")
                    difficulty = rec.get("difficulty", "Unknown")
                    print(f"      {j+1}. {goal} (Score: {score:.1f}, {difficulty})")
                    
            else:
                print(f"    ❌ Failed - Status: {response.status_code}")
                
        except Exception as e:
            print(f"    ❌ Error: {str(e)}")

def test_semantic_matching():
    """Test semantic matching improvements"""
    print("\n🧠 Testing Semantic Matching...")
    
    # Test similar goals that should match well
    similar_goals = [
        ("Frontend Developer", "Front-end Engineer"),
        ("Full Stack Developer", "Full-stack Engineer"),
        ("Data Scientist", "Data Analytics Specialist"),
        ("Mobile Developer", "App Developer"),
        ("DevOps Engineer", "Site Reliability Engineer")
    ]
    
    for goal1, goal2 in similar_goals:
        try:
            # Generate roadmap for first goal
            response1 = requests.post(f"{ROADMAP_API_URL}/api/roadmap/generate-roadmap", json={
                "goal": goal1,
                "user_id": TEST_USER_ID + "_semantic1"
            })
            
            # Generate roadmap for similar goal
            response2 = requests.post(f"{ROADMAP_API_URL}/api/roadmap/generate-roadmap", json={
                "goal": goal2,
                "user_id": TEST_USER_ID + "_semantic2"
            })
            
            if response1.status_code == 200 and response2.status_code == 200:
                data1 = response1.json()
                data2 = response2.json()
                
                # Check if they matched to similar roadmaps
                domain1 = data1.get("domain", "")
                domain2 = data2.get("domain", "")
                
                match_score1 = data1.get("match_score", 0)
                match_score2 = data2.get("match_score", 0)
                
                domain_match = domain1 == domain2
                good_scores = match_score1 > 0.3 and match_score2 > 0.3
                
                status = "✅" if domain_match and good_scores else "⚠️"
                print(f"  {status} {goal1} vs {goal2}")
                print(f"    Domains: {domain1} | {domain2} ({'Match' if domain_match else 'Different'})")
                print(f"    Scores: {match_score1:.2f} | {match_score2:.2f}")
                
        except Exception as e:
            print(f"  ❌ Error testing {goal1} vs {goal2}: {str(e)}")

def test_dataset_coverage():
    """Test coverage of the enhanced datasets"""
    print("\n📚 Testing Dataset Coverage...")
    
    try:
        # Get all available domains
        response = requests.get(f"{ROADMAP_API_URL}/api/roadmap/roadmaps/domains")
        
        if response.status_code == 200:
            data = response.json()
            domains = data.get("domains", [])
            
            print(f"  Available domains: {len(domains)}")
            for domain in sorted(domains):
                print(f"    - {domain}")
                
            # Test coverage for different domains
            expected_domains = [
                "Full Stack Development",
                "Data Science", 
                "Mobile Development",
                "DevOps",
                "Cybersecurity",
                "Blockchain",
                "Game Development",
                "Cloud Computing",
                "Machine Learning",
                "Design"
            ]
            
            coverage = sum(1 for domain in expected_domains if domain in domains)
            coverage_percentage = coverage / len(expected_domains)
            
            print(f"\n  Domain Coverage: {coverage}/{len(expected_domains)} ({coverage_percentage:.1%})")
            
            if coverage_percentage >= 0.7:
                print("  ✅ Good domain coverage")
            else:
                print("  ⚠️ Limited domain coverage")
                
        else:
            print(f"  ❌ Failed to get domains - Status: {response.status_code}")
            
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")

def test_performance():
    """Test API performance with enhanced features"""
    print("\n⚡ Testing Performance...")
    
    goals = [
        "Python Developer",
        "React Developer", 
        "Data Analyst",
        "DevOps Engineer",
        "Mobile Developer"
    ]
    
    times = []
    
    for goal in goals:
        start_time = time.time()
        
        try:
            response = requests.post(f"{ROADMAP_API_URL}/api/roadmap/generate-roadmap", json={
                "goal": goal,
                "user_id": TEST_USER_ID + "_perf"
            })
            
            end_time = time.time()
            response_time = end_time - start_time
            times.append(response_time)
            
            if response.status_code == 200:
                print(f"  ✅ {goal}: {response_time:.3f}s")
            else:
                print(f"  ❌ {goal}: Failed ({response.status_code})")
                
        except Exception as e:
            print(f"  ❌ {goal}: Error - {str(e)}")
    
    if times:
        avg_time = sum(times) / len(times)
        max_time = max(times)
        print(f"\n  Average Response Time: {avg_time:.3f}s")
        print(f"  Maximum Response Time: {max_time:.3f}s")
        
        if avg_time < 2.0:
            print("  ✅ Good performance")
        elif avg_time < 5.0:
            print("  ⚠️ Acceptable performance")
        else:
            print("  ❌ Slow performance")

def test_health_check():
    """Test API health"""
    print("\n🏥 Testing API Health...")
    
    try:
        response = requests.get(f"{ROADMAP_API_URL}/health")
        
        if response.status_code == 200:
            data = response.json()
            status = data.get("status", "unknown")
            database = data.get("database", "unknown")
            
            print(f"  Status: {status}")
            print(f"  Database: {database}")
            
            if status == "healthy" and database == "connected":
                print("  ✅ API is healthy")
                return True
            else:
                print("  ⚠️ API has issues")
                return False
                
        else:
            print(f"  ❌ Health check failed - Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ Health check error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Enhanced Roadmap System Test Suite")
    print("=" * 50)
    
    # Check if API is healthy first
    if not test_health_check():
        print("\n❌ API is not healthy. Please start the roadmap API service first.")
        print("Run: cd roadmap_api && python main.py")
        return
    
    # Run all tests
    test_enhanced_roadmap_generation()
    test_roadmap_recommendations()
    test_semantic_matching()
    test_dataset_coverage()
    test_performance()
    
    print("\n" + "=" * 50)
    print("🎉 Enhanced Roadmap System Test Complete!")
    print(f"Test User ID: {TEST_USER_ID}")
    print("\nNext steps:")
    print("1. Check the MongoDB database for stored roadmaps")
    print("2. Test the frontend with the enhanced features")
    print("3. Monitor performance in production")

if __name__ == "__main__":
    main()


"""Test if the service can start"""
import sys
import os

# Fix Windows console encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Add learning_path_service to path
sys.path.insert(0, 'learning_path_service')

try:
    print("Testing imports...")
    from knowledge_graph import SkillKnowledgeGraph
    from personalization_engine import PersonalizationEngine
    from visualization import LearningPathVisualizer
    from data_processor import RoadmapDataProcessor
    print("✅ All imports successful")
    
    print("\nTesting CSV file paths...")
    BASE_DIR = os.path.dirname(os.path.abspath('learning_path_service/main.py'))
    PARENT_DIR = os.path.dirname(BASE_DIR)
    CSV_PATH_1 = os.path.join(PARENT_DIR, "cross_domain_roadmaps_520.csv")
    CSV_PATH_2 = os.path.join(PARENT_DIR, "enhanced_roadmap_datasets.csv")
    
    print(f"CSV Path 1: {CSV_PATH_1}")
    print(f"Exists: {os.path.exists(CSV_PATH_1)}")
    print(f"CSV Path 2: {CSV_PATH_2}")
    print(f"Exists: {os.path.exists(CSV_PATH_2)}")
    
    print("\nTesting knowledge graph build...")
    graph = SkillKnowledgeGraph()
    graph.build_graph_from_roadmaps([CSV_PATH_1, CSV_PATH_2])
    print(f"✅ Graph built: {graph.graph.number_of_nodes()} nodes, {graph.graph.number_of_edges()} edges")
    
    print("\n✅ All tests passed! Service should work.")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()


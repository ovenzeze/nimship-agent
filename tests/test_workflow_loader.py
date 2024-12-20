import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflows.workflow_loader import WorkflowConfigLoader

def main():
    print("Testing WorkflowConfigLoader...")
    
    # Test case 1: Load existing workflow
    loader = WorkflowConfigLoader()
    try:
        config = loader.load_workflow("junior_developer")
        print("✓ Successfully loaded junior_developer workflow")
        print(f"✓ Workflow name: {config['name']}")
        print("✓ Config contains required fields:", 
              all(key in config for key in ['agents', 'state_data', 'transitions']))
    except Exception as e:
        print("✗ Failed to load workflow:", e)
    
    # Test case 2: Load non-existent workflow
    try:
        loader.load_workflow("nonexistent_workflow")
        print("✗ Should have failed for non-existent workflow")
    except FileNotFoundError:
        print("✓ Correctly handled non-existent workflow")

if __name__ == "__main__":
    main()
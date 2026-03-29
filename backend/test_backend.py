"""
Quick Test Script for FlowMind AI Backend
Tests basic functionality without frontend
"""

import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from services.workflow_service import WorkflowService


async def test_workflow():
    """Test workflow execution with sample task."""
    
    print("=" * 60)
    print("FlowMind AI - Backend Test")
    print("=" * 60)
    
    # Initialize workflow service
    print("\nInitializing workflow service...")
    try:
        service = WorkflowService(max_retries=2)
        print("✅ Workflow service initialized")
    except Exception as e:
        print(f"❌ Failed to initialize workflow service: {e}")
        print("\n⚠️  Make sure you have:")
        print("   1. Created .env file with OPENAI_API_KEY")
        print("   2. Installed all dependencies (pip install -r requirements.txt)")
        return False
    
    # Test task
    test_task = "Schedule a team meeting"
    print(f"\nTesting with task: '{test_task}'")
    print("-" * 60)
    
    try:
        # Run workflow
        print("Executing workflow...")
        result = await service.run_workflow(test_task)
        
        print("\n✅ Workflow completed successfully!")
        print(f"\n📊 Results Summary:")
        print(f"   - Plan steps: {len(result['plan'])}")
        print(f"   - Executed steps: {len(result['execution_results'])}")
        print(f"   - Validation: {'PASSED' if result['validation_result']['is_valid'] else 'FAILED'}")
        print(f"   - Issues detected: {len(result['monitoring_issues'])}")
        print(f"   - Total duration: {result['total_duration_seconds']:.2f}s")
        
        print("\n📋 Plan Steps:")
        for step in result['plan']:
            print(f"   {step.step_number}. {step.description}")
        
        print("\n⚙️ Execution Results:")
        success_count = sum(1 for r in result['execution_results'] if r.status == 'success')
        failed_count = sum(1 for r in result['execution_results'] if r.status == 'failed')
        print(f"   ✅ Successful: {success_count}")
        print(f"   ❌ Failed: {failed_count}")
        
        print("\n✓ Validation:")
        val = result['validation_result']
        print(f"   Status: {'PASSED' if val.is_valid else 'FAILED'}")
        print(f"   Confidence: {val.confidence_score * 100:.0f}%")
        print(f"   Reasoning: {val.reasoning[:100]}...")
        
        if result['monitoring_issues']:
            print("\n🔍 Monitoring Issues:")
            for issue in result['monitoring_issues'][:3]:  # Show first 3
                print(f"   [{issue.severity.upper()}] {issue.description}")
        
        print("\n" + "=" * 60)
        print("✅ All tests passed!")
        print("=" * 60)
        return True
        
    except ValueError as e:
        print(f"\n❌ Validation error: {e}")
        print("\n⚠️  This is likely an API key issue.")
        print("   Check your OPENAI_API_KEY in the .env file.")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_workflow())
    sys.exit(0 if success else 1)

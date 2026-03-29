"""
Workflow Service Module
Orchestrates all agents to execute complete workflows.
"""

import logging
import uuid
from datetime import datetime
from typing import Dict, Any, List
import sys
from pathlib import Path

# Add backend to path
backend_dir = str(Path(__file__).parent.parent)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Force demo mode - no API key required!
from services.demo_llm_service import DemoLLMService as LLMService
USE_DEMO_MODE = True

from agents.planner_agent import PlannerAgent
from agents.executor_agent import ExecutorAgent
from agents.validator_agent import ValidatorAgent
from agents.monitor_agent import MonitorAgent
from models.schemas import (
    PlanStep,
    ExecutionResult,
    ValidationResult,
    MonitoringIssue,
)

logger = logging.getLogger(__name__)


class WorkflowService:
    """Service for orchestrating end-to-end workflow execution."""

    def __init__(self, max_retries: int = 2):
        """
        Initialize workflow service.

        Args:
            max_retries: Maximum retries for failed steps
        """
        try:
            self.llm_service = LLMService()
            logger.info(f"WorkflowService initialized with LLM (demo_mode={USE_DEMO_MODE})")
        except Exception as e:
            logger.warning(f"LLM initialization failed: {e}")
            logger.info("Using demo mode without OpenAI")
            from services.demo_llm_service import DemoLLMService
            self.llm_service = DemoLLMService()
        
        self.planner = PlannerAgent(self.llm_service)
        self.executor = ExecutorAgent(max_retries=max_retries)
        self.validator = ValidatorAgent(self.llm_service)
        self.monitor = MonitorAgent()
        self.max_retries = max_retries

        logger.info(f"WorkflowService initialized with max_retries={max_retries}")

    async def run_workflow(self, task: str) -> Dict[str, Any]:
        """
        Execute a complete workflow from task to validation.

        Args:
            task: Task description to execute

        Returns:
            Complete workflow response with all results
        """
        execution_id = str(uuid.uuid4())
        started_at = datetime.now()

        logger.info(f"[Workflow] Starting execution {execution_id} for task: {task[:100]}...")

        try:
            # Step 1: Planning
            logger.info("[Workflow] Phase 1: Planning")
            plan_result = await self.planner.execute({"task": task})
            plan_steps = [PlanStep(**step) for step in plan_result["steps"]]
            logger.info(f"[Workflow] Generated {len(plan_steps)} plan steps")

            # Step 2: Execution
            logger.info("[Workflow] Phase 2: Execution")
            execution_data = {
                "steps": plan_result["steps"],
                "original_task": task,
            }
            execution_result = await self.executor.execute(execution_data)
            execution_results = [
                ExecutionResult(**result) for result in execution_result["execution_results"]
            ]
            logger.info(f"[Workflow] Completed {len(execution_results)} executions")

            # Step 3: Validation
            logger.info("[Workflow] Phase 3: Validation")
            validation_data = {
                "execution_results": [r.model_dump() for r in execution_results],
                "original_task": task,
            }
            validation_result_data = await self.validator.execute(validation_data)
            validation_result = ValidationResult(
                **validation_result_data["validation_result"]
            )
            logger.info(f"[Workflow] Validation result: {'PASSED' if validation_result.is_valid else 'FAILED'}")

            # Step 4: Monitoring
            logger.info("[Workflow] Phase 4: Monitoring")
            monitoring_data = {
                "execution_results": [r.model_dump() for r in execution_results],
                "plan": [p.model_dump() for p in plan_steps],
            }
            monitoring_result_data = await self.monitor.execute(monitoring_data)
            monitoring_issues = [
                MonitoringIssue(**issue) for issue in monitoring_result_data["monitoring_issues"]
            ]
            logger.info(f"[Workflow] Detected {len(monitoring_issues)} issues")

            completed_at = datetime.now()
            total_duration = (completed_at - started_at).total_seconds()

            # Build response
            response = {
                "task": task,
                "plan": plan_steps,
                "execution_results": execution_results,
                "validation_result": validation_result,
                "monitoring_issues": monitoring_issues,
                "execution_id": execution_id,
                "started_at": started_at,
                "completed_at": completed_at,
                "total_duration_seconds": total_duration,
            }

            logger.info(
                f"[Workflow] Execution {execution_id} completed in {total_duration:.2f}s"
            )

            return response

        except Exception as e:
            logger.error(f"[Workflow] Execution {execution_id} failed: {str(e)}")
            raise

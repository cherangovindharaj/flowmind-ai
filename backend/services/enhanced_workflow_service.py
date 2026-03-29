"""
Enhanced Workflow Service Module
Orchestrates advanced AI agents with comprehensive logging and demo mode support.
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

# Force demo mode for hackathon reliability
from services.demo_llm_service import DemoLLMService as LLMService
USE_DEMO_MODE = True

from agents.enhanced_planner_agent import EnhancedPlannerAgent
from agents.enhanced_executor_agent import EnhancedExecutorAgent
from agents.enhanced_validator_agent import EnhancedValidatorAgent
from agents.enhanced_monitor_agent import EnhancedMonitorAgent
from models.schemas import (
    PlanStep,
    ExecutionResult,
    ValidationResult,
    MonitoringIssue,
)

logger = logging.getLogger(__name__)


class EnhancedWorkflowService:
    """Advanced service for orchestrating enterprise-grade workflow execution."""

    def __init__(self, max_retries: int = 2, demo_mode: bool = True):
        """
        Initialize enhanced workflow service.

        Args:
            max_retries: Maximum retries for failed steps
            demo_mode: Enable realistic simulation mode
        """
        self.llm_service = LLMService()
        self.planner = EnhancedPlannerAgent(self.llm_service)
        self.executor = EnhancedExecutorAgent(max_retries=max_retries, demo_mode=demo_mode)
        self.validator = EnhancedValidatorAgent(self.llm_service)
        self.monitor = EnhancedMonitorAgent()
        self.max_retries = max_retries
        self.demo_mode = demo_mode

        logger.info(f"EnhancedWorkflowService initialized (demo_mode={demo_mode}, max_retries={max_retries})")

    async def run_workflow(self, task: str) -> Dict[str, Any]:
        """
        Execute a complete enhanced workflow from task to validation.

        Args:
            task: Task description to execute

        Returns:
            Complete workflow response with plan, execution, validation, monitoring, and logs
        """
        execution_id = str(uuid.uuid4())
        started_at = datetime.now()
        workflow_logs = []

        logger.info(f"[Workflow] Starting enhanced execution {execution_id} for task: {task[:100]}...")

        try:
            # Phase 1: Enhanced Planning
            logger.info("[Workflow] Phase 1: Enterprise Planning")
            workflow_logs.append({
                "timestamp": datetime.now().isoformat(),
                "phase": "PLANNING",
                "action": "PHASE_STARTED",
                "message": "Generating enterprise-grade workflow plan"
            })
            
            plan_result = await self.planner.execute({"task": task})
            plan_steps = plan_result["steps"]
            
            workflow_logs.append({
                "timestamp": datetime.now().isoformat(),
                "phase": "PLANNING",
                "action": "PLAN_GENERATED",
                "step_count": len(plan_steps),
                "metadata": plan_result.get("plan_metadata", {})
            })
            
            logger.info(f"[Workflow] Generated {len(plan_steps)} enterprise steps")

            # Phase 2: Enhanced Execution with Retry Logic
            logger.info("[Workflow] Phase 2: Intelligent Execution")
            workflow_logs.append({
                "timestamp": datetime.now().isoformat(),
                "phase": "EXECUTION",
                "action": "PHASE_STARTED",
                "message": f"Executing {len(plan_steps)} steps with automatic retry"
            })
            
            execution_data = {
                "steps": plan_steps,
                "original_task": task,
            }
            execution_result = await self.executor.execute(execution_data)
            execution_results = execution_result["execution_results"]
            execution_logs = execution_result.get("execution_logs", [])
            workflow_logs.extend(execution_logs)
            
            success_count = sum(1 for r in execution_results if r["status"] in ["SUCCESS", "RETRIED_SUCCESS"])
            workflow_logs.append({
                "timestamp": datetime.now().isoformat(),
                "phase": "EXECUTION",
                "action": "EXECUTION_COMPLETED",
                "successful_steps": success_count,
                "total_steps": len(execution_results)
            })
            
            logger.info(f"[Workflow] Completed {success_count}/{len(execution_results)} executions")

            # Phase 3: Enhanced Validation
            logger.info("[Workflow] Phase 3: Confidence Validation")
            workflow_logs.append({
                "timestamp": datetime.now().isoformat(),
                "phase": "VALIDATION",
                "action": "PHASE_STARTED",
                "message": "Analyzing execution results with confidence scoring"
            })
            
            validation_data = {
                "execution_results": execution_results,
                "original_task": task,
            }
            validation_result_data = await self.validator.execute(validation_data)
            validation_result = validation_result_data["validation_result"]
            
            workflow_logs.append({
                "timestamp": datetime.now().isoformat(),
                "phase": "VALIDATION",
                "action": "VALIDATION_COMPLETED",
                "status": validation_result["status"],
                "confidence_score": validation_result["confidence_score"]
            })
            
            logger.info(f"[Workflow] Validation result: {validation_result['status']} (Confidence: {validation_result['confidence_score']:.2f})")

            # Phase 4: Enhanced Monitoring
            logger.info("[Workflow] Phase 4: Comprehensive Monitoring")
            workflow_logs.append({
                "timestamp": datetime.now().isoformat(),
                "phase": "MONITORING",
                "action": "PHASE_STARTED",
                "message": "Detecting anomalies and generating insights"
            })
            
            monitoring_data = {
                "execution_results": execution_results,
                "steps": plan_steps,
            }
            monitoring_result_data = await self.monitor.execute(monitoring_data)
            monitoring_issues = monitoring_result_data["monitoring_issues"]
            monitoring_logs = monitoring_result_data.get("monitoring_logs", [])
            workflow_logs.extend(monitoring_logs)
            
            workflow_logs.append({
                "timestamp": datetime.now().isoformat(),
                "phase": "MONITORING",
                "action": "MONITORING_COMPLETED",
                "issues_detected": len(monitoring_issues)
            })
            
            logger.info(f"[Workflow] Detected {len(monitoring_issues)} monitoring issues")

            # Compile final results
            completed_at = datetime.now()
            total_duration = (completed_at - started_at).total_seconds()

            response = {
                "task": task,
                "plan": plan_steps,
                "execution": {
                    "results": execution_results,
                    "summary": {
                        "total_steps": len(execution_results),
                        "successful": success_count,
                        "failed": len(execution_results) - success_count,
                        "retried": sum(1 for r in execution_results if r["retry_count"] > 0)
                    }
                },
                "validation": validation_result,
                "monitoring_issues": monitoring_issues,
                "logs": workflow_logs,
                "metadata": {
                    "execution_id": execution_id,
                    "started_at": started_at.isoformat(),
                    "completed_at": completed_at.isoformat(),
                    "total_duration_seconds": round(total_duration, 2),
                    "demo_mode": self.demo_mode,
                    "workflow_type": plan_result.get("plan_metadata", {}).get("workflow_type", "unknown")
                }
            }

            logger.info(f"[Workflow] Enhanced execution {execution_id} completed in {total_duration:.2f}s")

            return response

        except Exception as e:
            logger.error(f"[Workflow] Execution {execution_id} failed: {str(e)}", exc_info=True)
            workflow_logs.append({
                "timestamp": datetime.now().isoformat(),
                "phase": "ERROR",
                "action": "WORKFLOW_FAILED",
                "error": str(e)
            })
            raise

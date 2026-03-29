"""
Enhanced Planner Agent Module
Generates enterprise-level workflow plans with dependencies, checkpoints, and failure scenarios.
"""

import logging
import json
from typing import Dict, Any, List
import sys
from pathlib import Path

# Add backend to path
backend_dir = str(Path(__file__).parent.parent)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from agents.base_agent import BaseAgent
from services.demo_llm_service import DemoLLMService

logger = logging.getLogger(__name__)


class EnhancedPlannerAgent(BaseAgent):
    """Advanced agent responsible for creating enterprise-grade workflow plans."""

    def __init__(self, llm_service: DemoLLMService):
        """
        Initialize enhanced planner agent.

        Args:
            llm_service: LLM service for generating plans
        """
        super().__init__("EnhancedPlannerAgent")
        self.llm_service = llm_service

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create an enterprise-grade workflow plan from a task description.

        Args:
            input_data: Dictionary containing 'task' key with task description

        Returns:
            Dictionary containing structured plan with dependencies and metadata
        """
        task = input_data.get("task", "")
        self._log_start(f"Creating enterprise plan for task: {task[:100]}...")

        try:
            # Use LLM if available, otherwise use demo mode
            if hasattr(self.llm_service, 'model_name') and self.llm_service.model_name != "demo-mode":
                response = await self._generate_with_llm(task)
            else:
                response = self._generate_demo_plan(task)

            # Parse and validate response
            if isinstance(response, str):
                plan_data = json.loads(response)
            else:
                plan_data = response

            steps = plan_data.get("steps", [])
            
            # Add logging
            logger.info(f"[{self.name}] Generated {len(steps)} enterprise steps")
            for step in steps:
                logger.info(f"  - Step {step['step_number']}: {step['description']} (Dependencies: {step.get('dependencies', [])})")

            self._log_end(f"Generated {len(steps)} steps with dependencies")
            return {"steps": steps, "original_task": task, "plan_metadata": plan_data.get("metadata", {})}

        except Exception as e:
            self._log_error(str(e))
            raise

    async def _generate_with_llm(self, task: str) -> str:
        """Generate plan using LLM."""
        system_prompt = """You are an expert enterprise workflow architect. Create detailed workflow plans with:

Required structure for each step:
{
  "step_number": int,
  "description": "Clear, actionable description",
  "estimated_duration_seconds": float,
  "dependencies": [list of step numbers this depends on],
  "validation_checkpoint": boolean,
  "failure_scenarios": ["possible failure modes"],
  "retry_policy": {"max_retries": 2, "backoff_seconds": 0.5},
  "criticality": "HIGH/MEDIUM/LOW"
}

Guidelines:
- Create 5-8 comprehensive steps
- Include dependencies between steps
- Mark validation checkpoints for critical steps
- Identify realistic failure scenarios
- Assign criticality levels
- Return ONLY valid JSON"""

        user_prompt = f"Create an enterprise workflow plan for:\n\nTask: {task}"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        return await self.llm_service.generate_with_retry(
            messages=messages,
            temperature=0.7,
            max_tokens=3000,
            response_format="json_object",
        )

    def _generate_demo_plan(self, task: str) -> Dict[str, Any]:
        """Generate realistic enterprise plan for demo mode."""
        task_lower = task.lower()

        # Employee Onboarding Plan
        if "onboard" in task_lower and "employee" in task_lower:
            return {
                "steps": [
                    {
                        "step_number": 1,
                        "description": "Collect employee personal information and documents",
                        "estimated_duration_seconds": 2.5,
                        "dependencies": [],
                        "validation_checkpoint": True,
                        "failure_scenarios": ["Missing required documents", "Invalid data format"],
                        "retry_policy": {"max_retries": 2, "backoff_seconds": 0.5},
                        "criticality": "HIGH"
                    },
                    {
                        "step_number": 2,
                        "description": "Create company email account and IT credentials",
                        "estimated_duration_seconds": 3.0,
                        "dependencies": [1],
                        "validation_checkpoint": True,
                        "failure_scenarios": ["Username already exists", "IT system unavailable"],
                        "retry_policy": {"max_retries": 2, "backoff_seconds": 0.5},
                        "criticality": "HIGH"
                    },
                    {
                        "step_number": 3,
                        "description": "Set up workspace with necessary equipment",
                        "estimated_duration_seconds": 4.0,
                        "dependencies": [1],
                        "validation_checkpoint": False,
                        "failure_scenarios": ["Equipment out of stock", "Workspace not ready"],
                        "retry_policy": {"max_retries": 2, "backoff_seconds": 0.5},
                        "criticality": "MEDIUM"
                    },
                    {
                        "step_number": 4,
                        "description": "Enroll employee in benefits and payroll systems",
                        "estimated_duration_seconds": 3.5,
                        "dependencies": [1, 2],
                        "validation_checkpoint": True,
                        "failure_scenarios": ["Payroll system error", "Benefits enrollment closed"],
                        "retry_policy": {"max_retries": 2, "backoff_seconds": 0.5},
                        "criticality": "HIGH"
                    },
                    {
                        "step_number": 5,
                        "description": "Schedule orientation and training sessions",
                        "estimated_duration_seconds": 2.0,
                        "dependencies": [2, 3],
                        "validation_checkpoint": False,
                        "failure_scenarios": ["Trainer unavailable", "Room booking conflict"],
                        "retry_policy": {"max_retries": 2, "backoff_seconds": 0.5},
                        "criticality": "MEDIUM"
                    },
                    {
                        "step_number": 6,
                        "description": "Grant building access and system permissions",
                        "estimated_duration_seconds": 2.5,
                        "dependencies": [2, 4],
                        "validation_checkpoint": True,
                        "failure_scenarios": ["Access card system down", "Permission escalation error"],
                        "retry_policy": {"max_retries": 2, "backoff_seconds": 0.5},
                        "criticality": "HIGH"
                    }
                ],
                "metadata": {
                    "workflow_type": "employee_onboarding",
                    "total_estimated_duration": 17.5,
                    "critical_path_length": 4,
                    "high_risk_steps": 4
                }
            }

        # Meeting Scheduling Plan
        elif "meeting" in task_lower or "schedule" in task_lower:
            return {
                "steps": [
                    {
                        "step_number": 1,
                        "description": "Identify meeting objectives and required attendees",
                        "estimated_duration_seconds": 2.0,
                        "dependencies": [],
                        "validation_checkpoint": True,
                        "failure_scenarios": ["Unclear objectives", "Missing stakeholder list"],
                        "retry_policy": {"max_retries": 2, "backoff_seconds": 0.5},
                        "criticality": "HIGH"
                    },
                    {
                        "step_number": 2,
                        "description": "Check availability and schedule meeting time",
                        "estimated_duration_seconds": 3.5,
                        "dependencies": [1],
                        "validation_checkpoint": False,
                        "failure_scenarios": ["Calendar conflicts", "Time zone issues"],
                        "retry_policy": {"max_retries": 2, "backoff_seconds": 0.5},
                        "criticality": "MEDIUM"
                    },
                    {
                        "step_number": 3,
                        "description": "Reserve meeting room or setup virtual conference",
                        "estimated_duration_seconds": 2.5,
                        "dependencies": [2],
                        "validation_checkpoint": True,
                        "failure_scenarios": ["Room double-booked", "Video conferencing system down"],
                        "retry_policy": {"max_retries": 2, "backoff_seconds": 0.5},
                        "criticality": "HIGH"
                    },
                    {
                        "step_number": 4,
                        "description": "Prepare agenda and distribute to attendees",
                        "estimated_duration_seconds": 2.0,
                        "dependencies": [1],
                        "validation_checkpoint": False,
                        "failure_scenarios": ["Agenda incomplete", "Distribution list error"],
                        "retry_policy": {"max_retries": 2, "backoff_seconds": 0.5},
                        "criticality": "MEDIUM"
                    },
                    {
                        "step_number": 5,
                        "description": "Send calendar invitations with meeting details",
                        "estimated_duration_seconds": 1.5,
                        "dependencies": [2, 3, 4],
                        "validation_checkpoint": True,
                        "failure_scenarios": ["Email server error", "Invalid email addresses"],
                        "retry_policy": {"max_retries": 2, "backoff_seconds": 0.5},
                        "criticality": "HIGH"
                    },
                    {
                        "step_number": 6,
                        "description": "Arrange necessary equipment and materials",
                        "estimated_duration_seconds": 2.0,
                        "dependencies": [3],
                        "validation_checkpoint": False,
                        "failure_scenarios": ["Projector malfunction", "Materials not printed"],
                        "retry_policy": {"max_retries": 2, "backoff_seconds": 0.5},
                        "criticality": "LOW"
                    }
                ],
                "metadata": {
                    "workflow_type": "meeting_scheduling",
                    "total_estimated_duration": 13.5,
                    "critical_path_length": 4,
                    "high_risk_steps": 3
                }
            }

        # Default Generic Plan
        else:
            return {
                "steps": [
                    {
                        "step_number": 1,
                        "description": f"Analyze requirements for: {task[:50]}...",
                        "estimated_duration_seconds": 2.5,
                        "dependencies": [],
                        "validation_checkpoint": True,
                        "failure_scenarios": ["Requirements unclear", "Missing information"],
                        "retry_policy": {"max_retries": 2, "backoff_seconds": 0.5},
                        "criticality": "HIGH"
                    },
                    {
                        "step_number": 2,
                        "description": "Gather necessary resources and information",
                        "estimated_duration_seconds": 3.0,
                        "dependencies": [1],
                        "validation_checkpoint": False,
                        "failure_scenarios": ["Resource unavailable", "Data access denied"],
                        "retry_policy": {"max_retries": 2, "backoff_seconds": 0.5},
                        "criticality": "MEDIUM"
                    },
                    {
                        "step_number": 3,
                        "description": "Execute primary implementation steps",
                        "estimated_duration_seconds": 4.0,
                        "dependencies": [2],
                        "validation_checkpoint": True,
                        "failure_scenarios": ["Implementation error", "Integration failure"],
                        "retry_policy": {"max_retries": 2, "backoff_seconds": 0.5},
                        "criticality": "HIGH"
                    },
                    {
                        "step_number": 4,
                        "description": "Validate results and perform quality checks",
                        "estimated_duration_seconds": 3.0,
                        "dependencies": [3],
                        "validation_checkpoint": True,
                        "failure_scenarios": ["Validation failed", "Quality threshold not met"],
                        "retry_policy": {"max_retries": 2, "backoff_seconds": 0.5},
                        "criticality": "HIGH"
                    },
                    {
                        "step_number": 5,
                        "description": "Finalize and document completion",
                        "estimated_duration_seconds": 2.0,
                        "dependencies": [4],
                        "validation_checkpoint": False,
                        "failure_scenarios": ["Documentation incomplete", "Sign-off pending"],
                        "retry_policy": {"max_retries": 2, "backoff_seconds": 0.5},
                        "criticality": "MEDIUM"
                    }
                ],
                "metadata": {
                    "workflow_type": "generic",
                    "total_estimated_duration": 14.5,
                    "critical_path_length": 5,
                    "high_risk_steps": 3
                }
            }

"""
Planner Agent Module
Breaks down user tasks into structured workflow steps using LLM.
"""

import logging
from typing import Dict, Any, List
import sys
from pathlib import Path

# Add backend to path
backend_dir = str(Path(__file__).parent.parent)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from agents.base_agent import BaseAgent
from services.llm_service import LLMService

logger = logging.getLogger(__name__)


class PlannerAgent(BaseAgent):
    """Agent responsible for creating workflow plans from user tasks."""

    def __init__(self, llm_service: LLMService):
        """
        Initialize planner agent.

        Args:
            llm_service: LLM service for generating plans
        """
        super().__init__("PlannerAgent")
        self.llm_service = llm_service

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a workflow plan from a task description.

        Args:
            input_data: Dictionary containing 'task' key with task description

        Returns:
            Dictionary containing list of plan steps
        """
        task = input_data.get("task", "")
        self._log_start(f"Planning task: {task[:100]}...")

        try:
            # Create prompt for LLM
            system_prompt = """You are an expert workflow planner. Your task is to break down user requests into clear, actionable steps.

Guidelines:
- Create 4-8 sequential steps
- Each step should be specific and actionable
- Steps should logically build upon each other
- Use clear, concise language
- Return ONLY valid JSON in the following format:

{
    "steps": [
        {"step_number": 1, "description": "First step description"},
        {"step_number": 2, "description": "Second step description"},
        ...
    ]
}"""

            user_prompt = f"Create a detailed workflow plan for this task:\n\nTask: {task}"

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]

            # Get LLM response
            response = await self.llm_service.generate_with_retry(
                messages=messages,
                temperature=0.7,
                max_tokens=2000,
                response_format="json_object",
            )

            # Parse response
            plan_data = self.llm_service.parse_json_response(response)
            steps = plan_data.get("steps", [])

            # Validate steps
            if not steps:
                raise ValueError("No steps generated in plan")

            self._log_end(f"Generated {len(steps)} steps")
            logger.info(f"[{self.name}] Plan steps: {[s['description'] for s in steps]}")

            return {"steps": steps, "original_task": task}

        except Exception as e:
            self._log_error(str(e))
            raise

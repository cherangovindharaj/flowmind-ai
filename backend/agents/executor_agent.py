"""
Executor Agent Module
Executes workflow steps with simulation and retry logic.
"""

import logging
import asyncio
import random
from typing import Dict, Any, List
from datetime import datetime
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class ExecutorAgent(BaseAgent):
    """Agent responsible for executing workflow steps."""

    def __init__(self, max_retries: int = 2):
        """
        Initialize executor agent.

        Args:
            max_retries: Maximum retry attempts for failed steps
        """
        super().__init__("ExecutorAgent")
        self.max_retries = max_retries

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute all steps in the workflow plan.

        Args:
            input_data: Dictionary containing 'steps' list

        Returns:
            Dictionary containing execution results for each step
        """
        steps = input_data.get("steps", [])
        self._log_start(f"Executing {len(steps)} steps")

        execution_results = []

        for step in steps:
            result = await self._execute_step(step)
            execution_results.append(result)

        self._log_end(f"Completed {len(execution_results)} executions")
        return {"execution_results": execution_results}

    async def _execute_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a single step with retry logic.

        Args:
            step: Step dictionary with step_number and description

        Returns:
            ExecutionResult dictionary
        """
        step_number = step.get("step_number", 0)
        description = step.get("description", "Unknown step")

        logger.info(f"[{self.name}] Executing step {step_number}: {description}")

        attempt = 0
        last_error = None

        while attempt <= self.max_retries:
            try:
                # Simulate execution with realistic delay
                start_time = datetime.now()
                await asyncio.sleep(random.uniform(0.5, 1.5))

                # Simulate success/failure (90% success rate for demo)
                success = random.random() > 0.1

                end_time = datetime.now()
                execution_time = (end_time - start_time).total_seconds()

                if success:
                    output = self._generate_success_output(description, step_number)
                    logger.info(f"[{self.name}] Step {step_number} completed successfully")

                    return {
                        "step_number": step_number,
                        "description": description,
                        "status": "success",
                        "output": output,
                        "retry_count": attempt,
                        "execution_time": execution_time,
                    }
                else:
                    # Simulate failure
                    error_msg = self._generate_error_message(description)
                    logger.warning(f"[{self.name}] Step {step_number} failed: {error_msg}")

                    if attempt < self.max_retries:
                        logger.info(f"[{self.name}] Retrying step {step_number} (attempt {attempt + 1}/{self.max_retries})")
                        attempt += 1
                        await asyncio.sleep(0.5)  # Brief delay before retry
                        continue
                    else:
                        # Max retries reached
                        return {
                            "step_number": step_number,
                            "description": description,
                            "status": "failed",
                            "output": f"Failed after {attempt + 1} attempts",
                            "retry_count": attempt,
                            "error_message": error_msg,
                            "execution_time": execution_time,
                        }

            except Exception as e:
                last_error = str(e)
                logger.error(f"[{self.name}] Step {step_number} error: {last_error}")
                if attempt < self.max_retries:
                    attempt += 1
                    await asyncio.sleep(0.5)
                    continue
                else:
                    return {
                        "step_number": step_number,
                        "description": description,
                        "status": "failed",
                        "output": f"Failed after {attempt + 1} attempts",
                        "retry_count": attempt,
                        "error_message": last_error,
                        "execution_time": 0.0,
                    }

        # Should not reach here, but just in case
        return {
            "step_number": step_number,
            "description": description,
            "status": "failed",
            "output": "Unexpected error",
            "retry_count": attempt,
            "error_message": last_error or "Unknown error",
            "execution_time": 0.0,
        }

    def _generate_success_output(self, description: str, step_number: int) -> str:
        """Generate realistic success message for a step."""
        success_messages = {
            "collect": f"Successfully collected all required information for step {step_number}",
            "create": f"Successfully created requested resources for step {step_number}",
            "set": f"Successfully configured settings for step {step_number}",
            "add": f"Successfully added to system for step {step_number}",
            "schedule": f"Successfully scheduled all required sessions for step {step_number}",
            "grant": f"Successfully granted access permissions for step {step_number}",
        }

        # Find matching message type
        desc_lower = description.lower()
        for key, message in success_messages.items():
            if key in desc_lower:
                return message

        return f"Step {step_number} completed successfully: {description}"

    def _generate_error_message(self, description: str) -> str:
        """Generate realistic error message."""
        errors = [
            "Temporary service unavailable",
            "Resource temporarily locked",
            "Network timeout occurred",
            "Database connection failed",
            "API rate limit exceeded",
        ]
        return random.choice(errors)

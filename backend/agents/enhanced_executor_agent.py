"""
Enhanced Executor Agent Module
Executes workflow steps with intelligent retry logic and detailed status tracking.
"""

import logging
import asyncio
import random
from typing import Dict, Any, List
from datetime import datetime
import sys
from pathlib import Path

# Add backend to path
backend_dir = str(Path(__file__).parent.parent)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)


class EnhancedExecutorAgent(BaseAgent):
    """Advanced agent responsible for executing workflow steps with retry logic."""

    def __init__(self, max_retries: int = 2, demo_mode: bool = True):
        """
        Initialize enhanced executor agent.

        Args:
            max_retries: Maximum retry attempts for failed steps
            demo_mode: If True, simulates realistic execution scenarios
        """
        super().__init__("EnhancedExecutorAgent")
        self.max_retries = max_retries
        self.demo_mode = demo_mode

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute all steps in the workflow plan with retry logic.

        Args:
            input_data: Dictionary containing 'steps' list

        Returns:
            Dictionary containing execution results with detailed status
        """
        steps = input_data.get("steps", [])
        self._log_start(f"Executing {len(steps)} enterprise steps")

        execution_results = []
        execution_logs = []

        for step in steps:
            result, logs = await self._execute_step(step)
            execution_results.append(result)
            execution_logs.extend(logs)

        success_count = sum(1 for r in execution_results if r["status"] in ["SUCCESS", "RETRIED_SUCCESS"])
        failed_count = sum(1 for r in execution_results if r["status"] == "FAILED")

        logger.info(f"[{self.name}] Execution complete: {success_count} successful, {failed_count} failed")
        
        return {
            "execution_results": execution_results,
            "execution_logs": execution_logs
        }

    async def _execute_step(self, step: Dict[str, Any]) -> tuple:
        """
        Execute a single step with retry logic and logging.

        Args:
            step: Step dictionary with metadata

        Returns:
            Tuple of (execution_result_dict, logs_list)
        """
        step_number = step.get("step_number", 0)
        description = step.get("description", "Unknown step")
        criticality = step.get("criticality", "MEDIUM")
        retry_policy = step.get("retry_policy", {"max_retries": 2, "backoff_seconds": 0.5})

        logs = []
        attempt = 0
        last_error = None
        
        # Log step start
        logs.append({
            "timestamp": datetime.now().isoformat(),
            "agent": self.name,
            "action": "STEP_STARTED",
            "step_number": step_number,
            "description": description,
            "criticality": criticality
        })
        logger.info(f"[{self.name}] Executing step {step_number}: {description} (Criticality: {criticality})")

        while attempt <= self.max_retries:
            try:
                # Simulate execution with realistic delay based on estimated duration
                estimated_duration = step.get("estimated_duration_seconds", 1.0)
                actual_duration = estimated_duration * random.uniform(0.8, 1.2)
                
                start_time = datetime.now()
                await asyncio.sleep(min(actual_duration, 3.0))  # Cap at 3s for demo

                # In demo mode, simulate realistic failure scenarios
                if self.demo_mode:
                    # Higher failure rate for HIGH criticality steps to show retry logic
                    base_failure_rate = 0.15 if criticality == "HIGH" else 0.10
                    
                    # Force at least one retry scenario for demonstration
                    if step_number == 2 and attempt == 0:
                        success = False  # Force retry on step 2
                    else:
                        success = random.random() > base_failure_rate
                else:
                    success = random.random() > 0.1

                end_time = datetime.now()
                execution_time = (end_time - start_time).total_seconds()

                if success:
                    output = self._generate_success_output(description, step_number, criticality)
                    
                    status = "RETRIED_SUCCESS" if attempt > 0 else "SUCCESS"
                    
                    logs.append({
                        "timestamp": datetime.now().isoformat(),
                        "agent": self.name,
                        "action": f"STEP_{status}",
                        "step_number": step_number,
                        "attempt": attempt + 1,
                        "execution_time": round(execution_time, 2),
                        "output": output[:100]
                    })
                    
                    logger.info(f"[{self.name}] Step {step_number} completed with status: {status}")

                    result = {
                        "step_number": step_number,
                        "description": description,
                        "status": status,
                        "output": output,
                        "retry_count": attempt,
                        "execution_time": round(execution_time, 2),
                        "criticality": criticality,
                        "validation_checkpoint": step.get("validation_checkpoint", False)
                    }

                    return result, logs

                else:
                    # Simulate failure
                    error_msg = self._generate_error_message(description, step_number)
                    
                    logs.append({
                        "timestamp": datetime.now().isoformat(),
                        "agent": self.name,
                        "action": "STEP_FAILED",
                        "step_number": step_number,
                        "attempt": attempt + 1,
                        "error": error_msg
                    })
                    
                    logger.warning(f"[{self.name}] Step {step_number} failed (attempt {attempt + 1}): {error_msg}")

                    if attempt < self.max_retries:
                        backoff = retry_policy.get("backoff_seconds", 0.5)
                        logs.append({
                            "timestamp": datetime.now().isoformat(),
                            "agent": self.name,
                            "action": "RETRY_SCHEDULED",
                            "step_number": step_number,
                            "next_attempt": attempt + 2,
                            "backoff_seconds": backoff
                        })
                        logger.info(f"[{self.name}] Retrying step {step_number} in {backoff}s (attempt {attempt + 1}/{self.max_retries})")
                        attempt += 1
                        await asyncio.sleep(backoff)
                        continue
                    else:
                        # Max retries reached
                        logs.append({
                            "timestamp": datetime.now().isoformat(),
                            "agent": self.name,
                            "action": "STEP_FINAL_FAILURE",
                            "step_number": step_number,
                            "total_attempts": attempt + 1,
                            "error": error_msg
                        })
                        
                        result = {
                            "step_number": step_number,
                            "description": description,
                            "status": "FAILED",
                            "output": f"Failed after {attempt + 1} attempts",
                            "retry_count": attempt,
                            "error_message": error_msg,
                            "execution_time": round(execution_time, 2),
                            "criticality": criticality,
                            "validation_checkpoint": step.get("validation_checkpoint", False)
                        }

                        return result, logs

            except Exception as e:
                last_error = str(e)
                logs.append({
                    "timestamp": datetime.now().isoformat(),
                    "agent": self.name,
                    "action": "STEP_EXCEPTION",
                    "step_number": step_number,
                    "attempt": attempt + 1,
                    "exception": last_error
                })
                
                logger.error(f"[{self.name}] Step {step_number} exception: {last_error}")
                
                if attempt < self.max_retries:
                    attempt += 1
                    await asyncio.sleep(0.5)
                    continue
                else:
                    logs.append({
                        "timestamp": datetime.now().isoformat(),
                        "agent": self.name,
                        "action": "STEP_FINAL_FAILURE",
                        "step_number": step_number,
                        "total_attempts": attempt + 1,
                        "error": last_error
                    })
                    
                    result = {
                        "step_number": step_number,
                        "description": description,
                        "status": "FAILED",
                        "output": f"Failed after {attempt + 1} attempts",
                        "retry_count": attempt,
                        "error_message": last_error,
                        "execution_time": 0.0,
                        "criticality": criticality,
                        "validation_checkpoint": step.get("validation_checkpoint", False)
                    }

                    return result, logs

        # Should not reach here
        raise RuntimeError(f"Unexpected execution flow for step {step_number}")

    def _generate_success_output(self, description: str, step_number: int, criticality: str) -> str:
        """Generate realistic success message for a step."""
        templates = {
            "HIGH": f"[CRITICAL] Successfully completed high-priority step: {description}. All validation checks passed.",
            "MEDIUM": f"Step {step_number} executed successfully: {description}. Quality metrics within acceptable range.",
            "LOW": f"Completed optional step: {description}. No issues detected during execution."
        }
        return templates.get(criticality, f"Step {step_number} completed: {description}")

    def _generate_error_message(self, description: str, step_number: int) -> str:
        """Generate realistic error messages."""
        errors = [
            f"Temporary service unavailable while executing: {description}",
            f"Resource temporarily locked during step {step_number}",
            f"Network timeout occurred processing: {description[:40]}...",
            f"Database connection failed for step {step_number}",
            f"API rate limit exceeded while executing: {description}",
            f"External dependency unavailable: {description[:30]}...",
            f"Validation precondition failed for step {step_number}"
        ]
        return random.choice(errors)

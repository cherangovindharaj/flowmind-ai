"""
Monitor Agent Module
Detects issues and anomalies in workflow execution.
"""

import logging
from typing import Dict, Any, List
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class MonitorAgent(BaseAgent):
    """Agent responsible for monitoring and detecting workflow issues."""

    def __init__(self):
        """Initialize monitor agent."""
        super().__init__("MonitorAgent")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Monitor workflow for issues and anomalies.

        Args:
            input_data: Dictionary containing 'execution_results' and 'plan'

        Returns:
            Dictionary containing list of detected issues
        """
        execution_results = input_data.get("execution_results", [])
        plan = input_data.get("plan", [])

        self._log_start(f"Monitoring {len(execution_results)} execution results")

        issues = []

        # Check for various types of issues
        issues.extend(self._check_failed_steps(execution_results))
        issues.extend(self._check_retry_patterns(execution_results))
        issues.extend(self._check_execution_time(execution_results))
        issues.extend(self._check_incomplete_plan(plan, execution_results))

        # Sort by severity
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        issues.sort(key=lambda x: severity_order.get(x["severity"], 4))

        self._log_end(f"Detected {len(issues)} issues")
        return {"monitoring_issues": issues}

    def _check_failed_steps(self, execution_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Check for failed steps and generate critical/high severity issues."""
        issues = []
        failed_steps = [r for r in execution_results if r.get("status") == "failed"]

        for step in failed_steps:
            step_num = step.get("step_number", 0)
            description = step.get("description", "Unknown step")
            error_msg = step.get("error_message", "Unknown error")

            # Critical if it's an early step (more impactful)
            severity = "critical" if step_num <= 2 else "high"

            issues.append({
                "severity": severity,
                "description": f"Step {step_num} failed: {description}",
                "affected_step": step_num,
                "recommendation": f"Investigate error: {error_msg}. Consider manual intervention or retry.",
            })

        return issues

    def _check_retry_patterns(self, execution_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Check for steps that required multiple retries."""
        issues = []

        for result in execution_results:
            retry_count = result.get("retry_count", 0)
            if retry_count >= 2:
                step_num = result.get("step_number", 0)
                description = result.get("description", "Unknown step")

                severity = "medium" if retry_count == 2 else "high"

                issues.append({
                    "severity": severity,
                    "description": f"Step {step_num} required {retry_count + 1} attempts: {description}",
                    "affected_step": step_num,
                    "recommendation": "Review system stability and resource availability for this step.",
                })

        return issues

    def _check_execution_time(self, execution_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Check for unusually long execution times."""
        issues = []

        for result in execution_results:
            exec_time = result.get("execution_time", 0)
            if exec_time and exec_time > 2.0:  # More than 2 seconds
                step_num = result.get("step_number", 0)
                description = result.get("description", "Unknown step")

                issues.append({
                    "severity": "low",
                    "description": f"Step {step_num} had slow execution ({exec_time:.2f}s): {description}",
                    "affected_step": step_num,
                    "recommendation": "Consider optimizing this step or checking for performance bottlenecks.",
                })

        return issues

    def _check_incomplete_plan(
        self, plan: List[Dict[str, Any]], execution_results: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Check if all planned steps were executed."""
        issues = []

        if not plan:
            return issues

        planned_steps = len(plan)
        executed_steps = len(execution_results)

        if executed_steps < planned_steps:
            missing_count = planned_steps - executed_steps
            issues.append({
                "severity": "critical",
                "description": f"Workflow incomplete: {missing_count} step(s) not executed",
                "affected_step": None,
                "recommendation": "Investigate why planned steps were not executed. Possible system failure.",
            })

        return issues

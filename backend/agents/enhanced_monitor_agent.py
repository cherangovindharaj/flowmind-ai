"""
Enhanced Monitor Agent Module
Detects anomalies, failures, and generates actionable insights with severity classification.
"""

import logging
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


class EnhancedMonitorAgent(BaseAgent):
    """Advanced agent responsible for comprehensive workflow monitoring and anomaly detection."""

    def __init__(self):
        """Initialize enhanced monitor agent."""
        super().__init__("EnhancedMonitorAgent")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Monitor workflow for issues, anomalies, and generate insights.

        Args:
            input_data: Dictionary containing 'execution_results' and 'plan'

        Returns:
            Dictionary containing structured monitoring issues list
        """
        execution_results = input_data.get("execution_results", [])
        plan = input_data.get("steps", [])

        self._log_start(f"Monitoring {len(execution_results)} execution results")

        issues = []
        monitoring_logs = []

        # Run all monitoring checks
        issues.extend(self._check_failed_steps(execution_results))
        issues.extend(self._check_retry_patterns(execution_results))
        issues.extend(self._check_execution_time_anomalies(execution_results))
        issues.extend(self._check_critical_path_failures(execution_results, plan))
        issues.extend(self._check_validation_checkpoint_failures(execution_results))
        issues.extend(self._check_dependency_violations(execution_results, plan))

        # Sort by severity (HIGH first, then MEDIUM, then LOW)
        severity_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
        issues.sort(key=lambda x: severity_order.get(x["severity"], 3))

        # Log detected issues
        for issue in issues:
            monitoring_logs.append({
                "timestamp": datetime.now().isoformat(),
                "agent": self.name,
                "action": "ISSUE_DETECTED",
                "severity": issue["severity"],
                "description": issue["description"][:50]
            })

        logger.info(f"[{self.name}] Monitoring complete: Detected {len(issues)} issues")

        return {
            "monitoring_issues": issues,
            "monitoring_logs": monitoring_logs
        }

    def _check_failed_steps(self, execution_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Check for failed steps and generate HIGH severity issues."""
        issues = []
        failed_steps = [r for r in execution_results if r.get("status") == "FAILED"]

        for step in failed_steps:
            step_num = step.get("step_number", 0)
            description = step.get("description", "Unknown step")
            criticality = step.get("criticality", "MEDIUM")
            error_msg = step.get("error_message", "Unknown error")

            # Escalate severity for HIGH criticality steps
            severity = "HIGH" if criticality == "HIGH" else "MEDIUM"

            issues.append({
                "severity": severity,
                "type": "STEP_FAILURE",
                "description": f"Step {step_num} failed: {description}",
                "affected_step": step_num,
                "error_details": error_msg,
                "recommendation": f"Investigate root cause: {error_msg[:50]}... Consider manual intervention or system restart.",
                "impact": "Workflow completion compromised" if criticality == "HIGH" else "Partial workflow degradation"
            })

        return issues

    def _check_retry_patterns(self, execution_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Check for steps that required multiple retries - indicates system instability."""
        issues = []

        for result in execution_results:
            retry_count = result.get("retry_count", 0)
            if retry_count >= 1:
                step_num = result.get("step_number", 0)
                description = result.get("description", "Unknown step")
                criticality = result.get("criticality", "MEDIUM")

                # More than 2 retries is concerning
                if retry_count >= 2:
                    severity = "HIGH"
                    issue_type = "EXCESSIVE_RETRIES"
                else:
                    severity = "MEDIUM"
                    issue_type = "RETRY_REQUIRED"

                issues.append({
                    "severity": severity,
                    "type": issue_type,
                    "description": f"Step {step_num} required {retry_count + 1} attempts: {description}",
                    "affected_step": step_num,
                    "retry_count": retry_count,
                    "recommendation": "Review system stability, network connectivity, and external dependency health for this step.",
                    "impact": "Increased execution time and resource consumption"
                })

        return issues

    def _check_execution_time_anomalies(self, execution_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Check for unusually long execution times indicating performance issues."""
        issues = []

        for result in execution_results:
            exec_time = result.get("execution_time", 0)
            estimated_time = result.get("estimated_duration_seconds", exec_time)
            
            # If actual time is more than 2x estimated time, flag it
            if exec_time and estimated_time and exec_time > estimated_time * 1.5:
                step_num = result.get("step_number", 0)
                description = result.get("description", "Unknown step")

                issues.append({
                    "severity": "LOW",
                    "type": "PERFORMANCE_DEGRADATION",
                    "description": f"Step {step_num} had slow execution ({exec_time:.2f}s vs {estimated_time:.2f}s estimated)",
                    "affected_step": step_num,
                    "actual_duration": exec_time,
                    "estimated_duration": estimated_time,
                    "recommendation": "Consider optimizing this step or investigating performance bottlenecks.",
                    "impact": "Overall workflow efficiency reduced"
                })

        return issues

    def _check_critical_path_failures(self, execution_results: List[Dict[str, Any]], 
                                     plan: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Check if failures on critical path block workflow completion."""
        issues = []

        if not plan:
            return issues

        # Identify high-criticality failures
        critical_failures = [
            r for r in execution_results 
            if r.get("status") == "FAILED" and r.get("criticality") == "HIGH"
        ]

        for step in critical_failures:
            step_num = step.get("step_number", 0)
            description = step.get("description", "Unknown step")

            issues.append({
                "severity": "HIGH",
                "type": "CRITICAL_PATH_BLOCKER",
                "description": f"Critical path blocked: Step {step_num} failure prevents downstream execution",
                "affected_step": step_num,
                "recommendation": "Immediate attention required. This failure blocks dependent workflow steps.",
                "impact": "Downstream steps cannot execute. Workflow may be incomplete."
            })

        return issues

    def _check_validation_checkpoint_failures(self, execution_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Check for failures at validation checkpoints."""
        issues = []

        checkpoint_failures = [
            r for r in execution_results 
            if r.get("status") == "FAILED" and r.get("validation_checkpoint")
        ]

        for step in checkpoint_failures:
            step_num = step.get("step_number", 0)
            description = step.get("description", "Unknown step")

            issues.append({
                "severity": "HIGH",
                "type": "CHECKPOINT_FAILURE",
                "description": f"Validation checkpoint failed at step {step_num}: {description}",
                "affected_step": step_num,
                "recommendation": "Quality gate failed. Manual review and approval required before proceeding.",
                "impact": "Quality assurance compromised. Risk of propagating errors."
            })

        return issues

    def _check_dependency_violations(self, execution_results: List[Dict[str, Any]], 
                                    plan: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Check if dependency constraints were violated."""
        issues = []

        if not plan:
            return issues

        # Build dependency map
        step_map = {s["step_number"]: s for s in plan}
        
        # Find successful steps whose dependencies failed
        for result in execution_results:
            if result.get("status") in ["SUCCESS", "RETRIED_SUCCESS"]:
                step_num = result.get("step_number", 0)
                step_info = step_map.get(step_num, {})
                dependencies = step_info.get("dependencies", [])

                # Check if any dependency failed
                for dep_num in dependencies:
                    dep_result = next((r for r in execution_results if r.get("step_number") == dep_num), None)
                    if dep_result and dep_result.get("status") == "FAILED":
                        issues.append({
                            "severity": "MEDIUM",
                            "type": "DEPENDENCY_VIOLATION",
                            "description": f"Step {step_num} succeeded despite dependency（failed）dependency {dep_num}",
                            "affected_step": step_num,
                            "failed_dependency": dep_num,
                            "recommendation": "Verify if step execution is valid given failed dependency. May indicate incorrect dependency mapping.",
                            "impact": "Potential data inconsistency or invalid workflow state"
                        })

        return issues

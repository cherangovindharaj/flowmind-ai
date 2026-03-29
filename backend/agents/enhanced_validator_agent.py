"""
Enhanced Validator Agent Module
Analyzes execution results with confidence scoring and detailed reasoning.
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
from services.demo_llm_service import DemoLLMService

logger = logging.getLogger(__name__)


class EnhancedValidatorAgent(BaseAgent):
    """Advanced agent responsible for validating workflow execution with confidence scoring."""

    def __init__(self, llm_service: DemoLLMService):
        """
        Initialize enhanced validator agent.

        Args:
            llm_service: LLM service for validation analysis
        """
        super().__init__("EnhancedValidatorAgent")
        self.llm_service = llm_service

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate workflow execution results with confidence scoring.

        Args:
            input_data: Dictionary containing 'execution_results' and 'original_task'

        Returns:
            Dictionary containing structured validation result
        """
        execution_results = input_data.get("execution_results", [])
        original_task = input_data.get("original_task", "")

        self._log_start(f"Validating {len(execution_results)} execution results")

        try:
            # Analyze results
            successful_steps = [r for r in execution_results if r.get("status") in ["SUCCESS", "RETRIED_SUCCESS"]]
            failed_steps = [r for r in execution_results if r.get("status") == "FAILED"]
            retried_steps = [r for r in execution_results if r.get("retry_count", 0) > 0]

            # Calculate metrics
            total_steps = len(execution_results)
            success_rate = len(successful_steps) / total_steps if total_steps > 0 else 0.0
            
            # Check critical step failures
            critical_failures = [s for s in failed_steps if s.get("criticality") == "HIGH"]
            checkpoint_failures = [s for s in failed_steps if s.get("validation_checkpoint")]

            # Determine validation outcome based on failed steps
            # PASSED only if NO steps failed (retried successes count as success)
            has_failures = len(failed_steps) > 0
            is_valid = not has_failures
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence(success_rate, critical_failures, checkpoint_failures, retried_steps)
            reasoning = self._generate_reasoning(successful_steps, failed_steps, retried_steps, original_task, confidence_score)

            validation_result = {
                "status": "PASSED" if is_valid else "FAILED",
                "confidence_score": round(confidence_score, 2),
                "reasoning": reasoning,
                "metrics": {
                    "total_steps": total_steps,
                    "successful_steps": len(successful_steps),
                    "failed_steps": len(failed_steps),
                    "retried_steps": len(retried_steps),
                    "success_rate": round(success_rate, 2),
                    "critical_failures": len(critical_failures),
                    "checkpoint_failures": len(checkpoint_failures)
                },
                "failed_step_numbers": [s["step_number"] for s in failed_steps],
                "critical_failed_steps": [
                    {
                        "step_number": s["step_number"],
                        "description": s["description"],
                        "error": s.get("error_message", "Unknown error")
                    }
                    for s in critical_failures
                ]
            }

            logger.info(f"[{self.name}] Validation complete: {validation_result['status']} (Confidence: {confidence_score:.2f})")

            return {"validation_result": validation_result}

        except Exception as e:
            self._log_error(str(e))
            # Return conservative validation result on error
            return {
                "validation_result": {
                    "status": "FAILED",
                    "confidence_score": 0.0,
                    "reasoning": f"Validation failed due to error: {str(e)}",
                    "metrics": {},
                    "failed_step_numbers": [],
                    "critical_failed_steps": []
                }
            }

    def _calculate_confidence(self, success_rate: float, critical_failures: List, 
                            checkpoint_failures: List, retried_steps: List) -> float:
        """Calculate confidence score based on multiple factors.
        
        Rules:
        - Perfect execution (no failures, no retries): 95-100%
        - With retries (all succeeded after retry): 85-95%
        - Any failures: below 70%
        """
        
        # Check for any failures - this results in low confidence
        has_failures = len(critical_failures) > 0 or len(checkpoint_failures) > 0
        if has_failures:
            # Severe penalty for failures - confidence below 70%
            failure_penalty = len(critical_failures) * 20 + len(checkpoint_failures) * 15
            base_confidence = 60.0  # Start below 70%
            confidence = max(0, base_confidence - failure_penalty)
            return confidence / 100
        
        # No failures - start with high base confidence
        if success_rate >= 1.0:
            # All steps succeeded (including retried successes)
            base_confidence = 95.0
            
            # Apply minor penalty for retries (each retry reduces by ~3-5%)
            retry_penalty = min(len(retried_steps) * 4, 10)  # Cap at 10% reduction
            confidence = base_confidence - retry_penalty
            
            # Ensure we stay in 85-95% range for successful workflows with retries
            confidence = max(85, min(95, confidence))
        else:
            # Partial success (shouldn't happen if is_valid logic is correct)
            base_confidence = success_rate * 100
            confidence = max(0, min(70, base_confidence))
        
        # Normalize to 0-1 range
        return confidence / 100

    def _generate_reasoning(self, successful_steps: List, failed_steps: List, 
                          retried_steps: List, original_task: str, confidence_score: float) -> str:
        """Generate detailed reasoning for validation decision.
        
        Reasoning structure:
        - If PASSED: Emphasize success, mention retries if applicable
        - If FAILED: Clearly state which steps failed and why workflow is incomplete
        """
        
        reasons = []
        has_failures = len(failed_steps) > 0
        
        # PASSED scenario
        if not has_failures:
            reasons.append("All workflow steps completed successfully.")
            
            if retried_steps:
                retry_count = len(retried_steps)
                reasons.append(f"Retry mechanism automatically recovered {retry_count} step(s) from transient failures.")
            
            if confidence_score >= 0.95:
                reasons.append("Perfect execution with no issues detected.")
            elif confidence_score >= 0.90:
                reasons.append("Excellent execution with minimal recovery needed.")
            else:
                reasons.append("Good execution with automatic error correction.")
            
            reasons.append("Workflow validation passed - ready for deployment.")
        
        # FAILED scenario
        else:
            failure_count = len(failed_steps)
            critical_count = len([s for s in failed_steps if s.get("criticality") == "HIGH"])
            
            reasons.append(f"{failure_count} step(s) failed after all retry attempts.")
            
            if critical_count > 0:
                reasons.append(f"{critical_count} high-priority critical failure(s) detected.")
            
            # List failed step numbers
            failed_numbers = [str(s["step_number"]) for s in failed_steps[:5]]  # Show first 5
            if len(failed_steps) > 5:
                failed_numbers.append(f"+{len(failed_steps) - 5} more")
            reasons.append(f"Failed steps: {', '.join(failed_numbers)}.")
            
            reasons.append("Workflow execution incomplete - manual intervention required.")
        
        # Add metrics context
        total = len(successful_steps) + len(failed_steps)
        success_pct = (len(successful_steps) / total * 100) if total > 0 else 0
        
        if total > 0:
            reasons.append(f"Success rate: {success_pct:.0f}% ({len(successful_steps)}/{total} steps).")
        
        return " ".join(reasons)

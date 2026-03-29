"""
Validator Agent Module
Validates workflow execution results using LLM analysis.
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


class ValidatorAgent(BaseAgent):
    """Agent responsible for validating workflow execution results."""

    def __init__(self, llm_service: LLMService):
        """
        Initialize validator agent.

        Args:
            llm_service: LLM service for validation analysis
        """
        super().__init__("ValidatorAgent")
        self.llm_service = llm_service

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate workflow execution results.

        Args:
            input_data: Dictionary containing 'execution_results' and 'original_task'

        Returns:
            Dictionary containing validation result
        """
        execution_results = input_data.get("execution_results", [])
        original_task = input_data.get("original_task", "")

        self._log_start(f"Validating {len(execution_results)} execution results")

        try:
            # Count successes and failures
            successful_steps = [r for r in execution_results if r.get("status") == "success"]
            failed_steps = [r for r in execution_results if r.get("status") == "failed"]

            # Prepare results summary for LLM
            results_summary = []
            for result in execution_results:
                results_summary.append(
                    f"Step {result['step_number']}: {result['description']} - {result['status'].upper()}"
                )

            # Create prompt for LLM
            system_prompt = """You are an expert workflow validator. Analyze the execution results and determine if the workflow completed successfully.

Criteria for validation:
- All critical steps must be successful
- Minor failures may be acceptable depending on context
- Consider the overall completion percentage
- Provide a confidence score (0.0 to 1.0)

Return ONLY valid JSON in the following format:
{
    "is_valid": true/false,
    "confidence_score": 0.0-1.0,
    "reasoning": "Detailed explanation of your assessment",
    "failed_steps": [list of failed step numbers]
}"""

            user_prompt = f"""Original Task: {original_task}

Execution Results:
{chr(10).join(results_summary)}

Total Steps: {len(execution_results)}
Successful: {len(successful_steps)}
Failed: {len(failed_steps)}

Please validate this workflow execution."""

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]

            # Get LLM response
            response = await self.llm_service.generate_with_retry(
                messages=messages,
                temperature=0.3,  # Lower temperature for more consistent validation
                max_tokens=1000,
                response_format="json_object",
            )

            # Parse response
            validation_data = self.llm_service.parse_json_response(response)

            # Ensure all required fields exist
            validation_result = {
                "is_valid": validation_data.get("is_valid", False),
                "confidence_score": float(validation_data.get("confidence_score", 0.0)),
                "reasoning": validation_data.get("reasoning", "No reasoning provided"),
                "failed_steps": validation_data.get("failed_steps", []),
            }

            status = "PASSED" if validation_result["is_valid"] else "FAILED"
            self._log_end(status)
            logger.info(f"[{self.name}] Validation result: {validation_result['reasoning']}")

            return {"validation_result": validation_result}

        except Exception as e:
            self._log_error(str(e))
            # Return conservative validation result on error
            return {
                "validation_result": {
                    "is_valid": False,
                    "confidence_score": 0.0,
                    "reasoning": f"Validation failed due to error: {str(e)}",
                    "failed_steps": [],
                }
            }

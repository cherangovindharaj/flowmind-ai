"""
Demo LLM Service - For Testing Without OpenAI Credits
Simulates LLM responses for development and testing.
"""

import logging
import json
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class DemoLLMService:
    """Demo LLM service that simulates responses without calling OpenAI."""

    def __init__(self, model_name: str = "demo-mode"):
        """Initialize demo LLM service."""
        self.model_name = model_name
        logger.info(f"DemoLLMService initialized (no API calls will be made)")

    async def chat_completion(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        response_format: Optional[str] = None,
    ) -> str:
        """Generate simulated chat completion."""
        # Extract task from messages
        user_message = ""
        for msg in messages:
            if msg.get("role") == "user":
                user_message = msg.get("content", "")
                break

        # Generate appropriate response based on context
        if "planner" in messages[0].get("content", "").lower():
            return self._generate_plan_response(user_message)
        elif "validator" in messages[0].get("content", "").lower():
            return self._generate_validation_response()
        else:
            return self._generate_default_response()

    def _generate_plan_response(self, user_message: str) -> str:
        """Generate simulated planning response."""
        # Extract task from prompt
        task = user_message.replace("Task:", "").strip()

        # Create generic plan based on common workflows
        if "onboard" in task.lower() and "employee" in task.lower():
            steps = [
                {"step_number": 1, "description": "Collect employee personal information and documents"},
                {"step_number": 2, "description": "Create company email account and IT credentials"},
                {"step_number": 3, "description": "Set up workspace with necessary equipment"},
                {"step_number": 4, "description": "Enroll employee in benefits and payroll systems"},
                {"step_number": 5, "description": "Schedule orientation and training sessions"},
                {"step_number": 6, "description": "Grant building access and system permissions"},
            ]
        elif "meeting" in task.lower() or "schedule" in task.lower():
            steps = [
                {"step_number": 1, "description": "Identify meeting objectives and required attendees"},
                {"step_number": 2, "description": "Check availability and schedule meeting time"},
                {"step_number": 3, "description": "Reserve meeting room or setup virtual conference"},
                {"step_number": 4, "description": "Prepare agenda and distribute to attendees"},
                {"step_number": 5, "description": "Send calendar invitations with meeting details"},
                {"step_number": 6, "description": "Arrange necessary equipment and materials"},
            ]
        elif "refund" in task.lower() or "customer" in task.lower():
            steps = [
                {"step_number": 1, "description": "Verify customer identity and purchase history"},
                {"step_number": 2, "description": "Review refund policy eligibility"},
                {"step_number": 3, "description": "Process refund transaction"},
                {"step_number": 4, "description": "Update customer account and send confirmation"},
                {"step_number": 5, "description": "Document refund reason for quality improvement"},
            ]
        else:
            # Generic 5-step plan
            steps = [
                {"step_number": 1, "description": f"Analyze requirements for: {task[:50]}..."},
                {"step_number": 2, "description": "Gather necessary resources and information"},
                {"step_number": 3, "description": "Execute primary implementation steps"},
                {"step_number": 4, "description": "Validate results and quality checks"},
                {"step_number": 5, "description": "Finalize and document completion"},
            ]

        response = {"steps": steps}
        return json.dumps(response)

    def _generate_validation_response(self) -> str:
        """Generate simulated validation response."""
        response = {
            "is_valid": True,
            "confidence_score": 0.92,
            "reasoning": "All critical workflow steps completed successfully. The execution achieved high completion rate with proper error handling.",
            "failed_steps": []
        }
        return json.dumps(response)

    def _generate_default_response(self) -> str:
        """Generate default response for unknown contexts."""
        response = {
            "is_valid": True,
            "confidence_score": 0.85,
            "reasoning": "Workflow execution completed with acceptable results.",
            "failed_steps": []
        }
        return json.dumps(response)

    def parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """Parse JSON response."""
        try:
            cleaned = response_text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {str(e)}")
            raise ValueError(f"Invalid JSON: {str(e)}")

    async def generate_with_retry(
        self,
        messages: list[dict[str, str]],
        max_retries: int = 2,
        **kwargs,
    ) -> str:
        """Generate completion with retry logic (simulated)."""
        for attempt in range(max_retries + 1):
            try:
                return await self.chat_completion(messages, **kwargs)
            except Exception as e:
                logger.warning(f"Demo generation failed (attempt {attempt + 1}): {str(e)}")
                if attempt < max_retries:
                    continue
                raise
        return await self.chat_completion(messages, **kwargs)

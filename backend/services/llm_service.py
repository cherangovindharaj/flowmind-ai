"""
LLM Service Module
Provides OpenAI API integration for all agents in the FlowMind system.
"""

import os
import json
import logging
from typing import Optional, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class LLMService:
    """Service for interacting with OpenAI language models."""

    def __init__(self, model_name: str = "gpt-4o-mini"):
        """
        Initialize LLM service.

        Args:
            model_name: OpenAI model to use (default: gpt-4o-mini)
        """
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            logger.warning("OPENAI_API_KEY not found in environment")
            raise ValueError("OPENAI_API_KEY is required")

        # Initialize OpenAI client with minimal parameters to avoid httpx compatibility issues
        import httpx
        http_client = httpx.Client()
        self.client = OpenAI(
            api_key=self.api_key,
            http_client=http_client
        )
        
        self.model_name = model_name
        logger.info(f"LLMService initialized with model: {model_name}")

    async def chat_completion(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        response_format: Optional[str] = None,
    ) -> str:
        """
        Get chat completion from OpenAI.

        Args:
            messages: List of message dictionaries
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            response_format: Response format type (e.g., "json_object")

        Returns:
            Generated text response
        """
        try:
            kwargs = {
                "model": self.model_name,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }

            if response_format == "json_object":
                kwargs["response_format"] = {"type": "json_object"}

            response = self.client.chat.completions.create(**kwargs)
            content = response.choices[0].message.content

            logger.debug(f"LLM response received ({len(content)} chars)")
            return content

        except Exception as e:
            error_msg = str(e)
            logger.error(f"LLM API call failed: {error_msg}")
            
            # Check for quota exceeded error
            if "insufficient_quota" in error_msg or "429" in error_msg:
                logger.error("OpenAI API quota exceeded!")
                logger.info("Please add credits to your OpenAI account or use DemoLLMService")
                logger.info("To enable demo mode, modify workflow_service.py to use DemoLLMService")
            
            raise

    def parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse JSON response from LLM.

        Args:
            response_text: Raw response text

        Returns:
            Parsed dictionary
        """
        try:
            # Clean up potential markdown code blocks
            cleaned = response_text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()

            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            logger.error(f"Response text: {response_text}")
            raise ValueError(f"Invalid JSON response: {str(e)}")

    async def generate_with_retry(
        self,
        messages: list[dict[str, str]],
        max_retries: int = 2,
        **kwargs,
    ) -> str:
        """
        Generate completion with retry logic.

        Args:
            messages: List of message dictionaries
            max_retries: Maximum number of retry attempts
            **kwargs: Additional arguments for chat_completion

        Returns:
            Generated text response
        """
        last_error = None

        for attempt in range(max_retries + 1):
            try:
                return await self.chat_completion(messages, **kwargs)
            except Exception as e:
                last_error = e
                logger.warning(f"LLM call failed (attempt {attempt + 1}/{max_retries + 1}): {str(e)}")
                if attempt < max_retries:
                    continue

        logger.error(f"All {max_retries + 1} attempts failed")
        raise last_error

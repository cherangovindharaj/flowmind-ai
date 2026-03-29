"""
Base Agent Module
Provides abstract base class for all agents in the FlowMind system.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Abstract base class for all workflow agents."""

    def __init__(self, name: str):
        """
        Initialize base agent.

        Args:
            name: Human-readable name of the agent
        """
        self.name = name
        logger.info(f"{self.name} initialized")

    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's primary function.

        Args:
            input_data: Input data for the agent to process

        Returns:
            Dictionary containing agent output
        """
        pass

    def _log_start(self, task_description: str):
        """Log the start of agent execution."""
        logger.info(f"[{self.name}] Starting: {task_description}")

    def _log_end(self, status: str):
        """Log the completion of agent execution."""
        logger.info(f"[{self.name}] Completed with status: {status}")

    def _log_error(self, error: str):
        """Log an error during execution."""
        logger.error(f"[{self.name}] Error: {error}")

"""
Pydantic Models for FlowMind API
Defines request/response schemas for workflow execution.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class WorkflowRequest(BaseModel):
    """Request model for workflow execution."""

    task: str = Field(..., description="The task to be executed by the workflow")
    max_retries: int = Field(default=2, description="Maximum retry attempts for failed steps")


class PlanStep(BaseModel):
    """Represents a single step in the workflow plan."""

    step_number: int
    description: str
    status: str = Field(default="pending", description="pending|completed|failed")
    result: Optional[str] = None
    retry_count: int = 0


class ExecutionResult(BaseModel):
    """Result of executing a workflow step."""

    step_number: int
    description: str
    status: str  # success|failed
    output: str
    retry_count: int = 0
    error_message: Optional[str] = None
    execution_time: Optional[float] = None


class ValidationResult(BaseModel):
    """Result of workflow validation."""

    is_valid: bool
    confidence_score: float = Field(ge=0.0, le=1.0)
    reasoning: str
    failed_steps: List[int] = []


class MonitoringIssue(BaseModel):
    """Issue detected by the monitoring agent."""

    severity: str  # low|medium|high|critical
    description: str
    affected_step: Optional[int] = None
    recommendation: str


class WorkflowResponse(BaseModel):
    """Complete response from workflow execution."""

    task: str
    plan: List[PlanStep]
    execution_results: List[ExecutionResult] = []  # Legacy support
    execution: Optional[Dict[str, Any]] = None  # Enhanced format
    validation_result: ValidationResult = None  # Legacy support
    validation: Optional[Dict[str, Any]] = None  # Enhanced format
    monitoring_issues: List[MonitoringIssue]
    logs: List[Dict[str, Any]] = []
    metadata: Optional[Dict[str, Any]] = None
    # Legacy fields (for backward compatibility)
    execution_id: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    total_duration_seconds: Optional[float] = None

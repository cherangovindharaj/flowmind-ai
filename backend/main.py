"""
FlowMind AI - Main FastAPI Application
Autonomous Workflow Agent System
"""

import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from utils.logger import setup_logger
from models.schemas import WorkflowRequest, WorkflowResponse
from services.enhanced_workflow_service import EnhancedWorkflowService

# Setup logging
logger = setup_logger()

# Initialize enhanced workflow service
workflow_service = EnhancedWorkflowService(max_retries=2, demo_mode=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    logger.info("FlowMind AI starting up...")
    yield
    logger.info("FlowMind AI shutting down...")


# Create FastAPI app
app = FastAPI(
    title="FlowMind AI",
    description="Autonomous Workflow Agent System for Enterprise Workflows",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default
        "http://localhost:3000",  # React default
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("CORS configured for frontend access")


@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {
        "name": "FlowMind AI",
        "status": "running",
        "version": "1.0.0",
    }


@app.post("/run-workflow", response_model=WorkflowResponse)
async def run_workflow(request: WorkflowRequest):
    """
    Execute a workflow for the given task.

    Args:
        request: Workflow request containing task description

    Returns:
        Complete workflow response with plan, execution, validation, and monitoring results
    """
    try:
        logger.info(f"Received workflow request for task: {request.task[:100]}...")

        # Execute workflow
        result = await workflow_service.run_workflow(request.task)

        # Extract duration for logging (from metadata or legacy field)
        duration = result.get('metadata', {}).get('total_duration_seconds', 
                   result.get('total_duration_seconds', 0))
        logger.info(f"Workflow completed successfully in {duration:.2f}s")

        return WorkflowResponse(**result)

    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Workflow execution failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Workflow execution failed: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    import sys
    from pathlib import Path
    
    # Add backend directory to Python path
    backend_dir = Path(__file__).parent
    sys.path.insert(0, str(backend_dir))
    
    logger.info("Starting FlowMind AI server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )

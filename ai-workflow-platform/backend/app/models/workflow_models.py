from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class StepStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class StepDefinition(BaseModel):
    name: str
    type: str  # e.g., "ai_task", "human_review", "system_task"
    config: dict[str, Any] = Field(default_factory=dict)


class WorkflowDefinition(BaseModel):
    id: str
    name: str
    steps: list[StepDefinition]
    created_at: datetime = Field(default_factory=datetime.utcnow)


class StepRun(BaseModel):
    name: str
    status: StepStatus = StepStatus.PENDING
    output: dict[str, Any] = Field(default_factory=dict)
    started_at: datetime | None = None
    finished_at: datetime | None = None


class WorkflowRun(BaseModel):
    id: str
    workflow_definition_id: str
    status: StepStatus = StepStatus.PENDING
    current_step: int = 0
    steps: list[StepRun] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)

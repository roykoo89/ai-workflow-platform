from uuid import uuid4

from fastapi import FastAPI, HTTPException

from backend.app.models.workflow_models import (
    StepDefinition,
    StepRun,
    StepStatus,
    WorkflowDefinition,
    WorkflowRun,
)

app = FastAPI(title="AI Workflow Platform")

# In-memory stores for MVP
workflow_definitions: dict[str, WorkflowDefinition] = {}
workflow_runs: dict[str, WorkflowRun] = {}


@app.on_event("startup")
def load_default_workflow() -> None:
    """Preload a minimal workflow so the MVP is immediately runnable."""
    workflow_definitions["grant_app"] = WorkflowDefinition(
        id="grant_app",
        name="Grant Application",
        steps=[
            StepDefinition(name="validate_input", type="system_task"),
            StepDefinition(name="ai_summarize", type="ai_task"),
            StepDefinition(name="human_review", type="human_review"),
        ],
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/workflows")
def list_workflows() -> list[WorkflowDefinition]:
    return list(workflow_definitions.values())


@app.post("/workflow/register")
def register_workflow(workflow: WorkflowDefinition) -> dict[str, str]:
    workflow_definitions[workflow.id] = workflow
    return {"status": "registered", "workflow_id": workflow.id}


@app.post("/workflow/start")
def start_workflow(workflow_id: str) -> dict:
    if workflow_id not in workflow_definitions:
        raise HTTPException(status_code=404, detail="Workflow not found")

    wf_def = workflow_definitions[workflow_id]

    # Initialize StepRuns
    steps = [StepRun(name=step.name) for step in wf_def.steps]
    run_id = str(uuid4())
    wf_run = WorkflowRun(
        id=run_id,
        workflow_definition_id=workflow_id,
        steps=steps,
        status=StepStatus.RUNNING,
        current_step=0,
    )
    workflow_runs[run_id] = wf_run

    return {"run_id": run_id, "status": wf_run.status, "steps": steps}

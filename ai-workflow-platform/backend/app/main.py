from fastapi import FastAPI

app = FastAPI(title="AI Workflow Platform")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

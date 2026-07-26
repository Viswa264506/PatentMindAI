import uuid
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.workflow.orchestrator import PatentMindWorkflow
from backend.config.settings import settings

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for workflow states (for MVP/development)
# In production, this would be stored in PostgreSQL
job_store = {}

class InventionRequest(BaseModel):
    invention: str

@app.post("/api/research")
async def start_research(request: InventionRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    job_store[job_id] = {"status": "running", "state": None}
    
    def run_job(j_id: str, invention: str):
        workflow = PatentMindWorkflow()
        try:
            state = workflow.run(invention)
            job_store[j_id]["status"] = "completed"
            job_store[j_id]["state"] = state.model_dump()
        except Exception as e:
            job_store[j_id]["status"] = "failed"
            job_store[j_id]["error"] = str(e)
            
    background_tasks.add_task(run_job, job_id, request.invention)
    
    return {"job_id": job_id, "status": "started"}

@app.get("/api/research/{job_id}")
async def get_research_status(job_id: str):
    if job_id not in job_store:
        raise HTTPException(status_code=404, detail="Job not found")
    return job_store[job_id]

@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.APP_NAME} API"}

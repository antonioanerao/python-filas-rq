import os
from dotenv import load_dotenv
from redis import Redis
from rq import Queue
from rq.job import Job
from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from tasks import process_job

load_dotenv()

redis_conn = Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
q = Queue("processamento_tarefa", connection=redis_conn)

origins_env = os.getenv("APP_ORIGINS", "")
allowed_origins = [o.strip() for o in origins_env.split(",") if o.strip()]

app = FastAPI(title=os.getenv("APP_NAME"), version=os.getenv("APP_VERSION"))
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def index():
    return {
        "status": "success",
        "message": f"{os.getenv('APP_NAME')} - v{os.getenv('APP_VERSION')}"
    }


@app.post("/enqueue")
async def enqueue(message: str = Form("Hello World!"), notify: bool = Form(...)):
    job = q.enqueue(
        process_job,
        message,
        notify,
        job_timeout=60
    )

    return {
        "task_id": job.get_id(),
        "status": "queued"
    }


@app.get("/status/{task_id}")
async def job_status(task_id: str):
    try:
        job = Job.fetch(task_id, connection=redis_conn)
    except Exception:
        raise HTTPException(status_code=400, detail="Job not found")

    if job.is_queued:
        return {"status": "queued"}
    if job.is_started:
        return {"status": "processing"}
    if job.is_finished:
        result = job.result
        return {"status": "done", "result": result}
    if job.is_failed:
        return {"status": "failed", "error": str(job.exc_info)}

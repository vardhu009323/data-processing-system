
import sys
import json
import subprocess
from pathlib import Path

from fastapi import FastAPI, HTTPException, Depends, Query

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Job

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CPP_ENGINE_DIR = PROJECT_ROOT / "cpp-engine"
sys.path.insert(0, str(CPP_ENGINE_DIR))

from engine import process_numbers

app = FastAPI(title="Data Processing System")


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)



class JobRequest(BaseModel):
    numbers: list[int] = Field(min_length=1, max_length=10000)


def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.get("/")
def home():
    return {"message": "Data Processing System API"}


@app.post("/jobs")
def create_job(
    request: JobRequest,
    session: Session = Depends(get_db)
):
    try:
        result = process_numbers(request.numbers)

    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=504,
            detail="Processing timed out"
        )

    except (
        subprocess.CalledProcessError,
        json.JSONDecodeError
    ):
        raise HTTPException(
            status_code=500,
            detail="The processing engine failed"
        )

    try:
        job = Job(
            status="completed",
            input_size=len(request.numbers),
            result=result
        )

        session.add(job)
        session.commit()
        session.refresh(job)

        return {
            "job_id": job.id,
            "status": job.status,
            "input_size": job.input_size,
            "result": job.result
        }

    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to save the job"
        )


@app.get("/jobs/{job_id}")
def get_job(
    job_id: int,
    session: Session = Depends(get_db)
):
    job = session.get(Job, job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return {
        "job_id": job.id,
        "status": job.status,
        "input_size": job.input_size,
        "result": job.result
    }



@app.get("/jobs")
def get_all_jobs(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    session: Session = Depends(get_db)
):
    jobs = (
        session.query(Job)
        .order_by(Job.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return [
        {
            "job_id": job.id,
            "status": job.status,
            "input_size": job.input_size,
            "result": job.result
        }
        for job in jobs
    ]


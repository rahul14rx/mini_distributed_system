from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import shutil
import os
from .. import models, schemas, database

router = APIRouter()

# --- FOR THE USER (DASHBOARD) ---

@router.post("/", response_model=schemas.JobResponse)
def create_job(job: schemas.JobCreate, db: Session = Depends(database.get_db)):
    new_job = models.Job(command=job.command)
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

@router.get("/", response_model=List[schemas.JobResponse])
def list_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    jobs = db.query(models.Job).order_by(models.Job.id.desc()).offset(skip).limit(limit).all()
    return jobs

@router.get("/{job_id}", response_model=schemas.JobResponse)
def get_job(job_id: int, db: Session = Depends(database.get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

# --- FOR THE WORKER AGENT ---

@router.post("/poll", response_model=schemas.JobResponse)
def poll_for_job(worker_id: str, db: Session = Depends(database.get_db)):
    job = db.query(models.Job).filter(models.Job.status == "QUEUED").order_by(models.Job.created_at.asc()).first()
    if not job:
        raise HTTPException(status_code=404, detail="No jobs available")
    
    job.status = "RUNNING"
    job.worker_id = worker_id
    db.commit()
    db.refresh(job)
    return job

@router.put("/{job_id}/complete")
def complete_job(job_id: int, status: str, log_path: str = None, db: Session = Depends(database.get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job.status = status
    job.completed_at = datetime.now()
    job.log_path = log_path
    db.commit()
    return {"message": "Job updated"}

# --- THE MISSING PIECE (UPLOAD) ---
@router.post("/{job_id}/upload")
def upload_artifact(job_id: int, file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Ensure directory exists
    os.makedirs("storage/artifacts", exist_ok=True)

    # Save file
    filename = f"job_{job_id}_{file.filename}"
    file_location = os.path.join("storage", "artifacts", filename)
    
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    
    job.artifact_path = file_location
    db.commit()
    
    return {"info": f"file saved at {file_location}"}
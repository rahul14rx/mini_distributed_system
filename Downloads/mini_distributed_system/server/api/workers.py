from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from .. import models, schemas, database

router = APIRouter()

@router.post("/register", response_model=schemas.WorkerRegister)
def register_worker(worker: schemas.WorkerRegister, db: Session = Depends(database.get_db)):
    """
    Worker calls this when it starts up.
    """
    # Check if worker exists
    db_worker = db.query(models.Worker).filter(models.Worker.id == worker.id).first()
    
    if db_worker:
        # If exists, just mark it as IDLE and update timestamp
        db_worker.status = "IDLE"
        db_worker.hostname = worker.hostname
        db_worker.last_heartbeat = datetime.now()
    else:
        # Create new worker record
        new_worker = models.Worker(
            id=worker.id,
            hostname=worker.hostname,
            status="IDLE"
        )
        db.add(new_worker)
    
    db.commit()
    return worker

@router.post("/heartbeat")
def heartbeat(heartbeat: schemas.WorkerHeartbeat, db: Session = Depends(database.get_db)):
    """
    Worker calls this every 5-10 seconds to say 'I am alive'.
    """
    db_worker = db.query(models.Worker).filter(models.Worker.id == heartbeat.id).first()
    if not db_worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    db_worker.last_heartbeat = datetime.now()
    db_worker.status = heartbeat.status # Update status (e.g., IDLE -> BUSY)
    db.commit()
    return {"status": "ack"}
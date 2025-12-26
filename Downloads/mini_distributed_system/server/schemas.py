from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Job Schemas
class JobCreate(BaseModel):
    command: str

class JobResponse(JobCreate):
    id: int
    status: str
    worker_id: Optional[str]
    created_at: datetime
    class Config:
        from_attributes = True

# Worker Schemas
class WorkerRegister(BaseModel):
    id: str
    hostname: str

class WorkerHeartbeat(BaseModel):
    id: str
    status: str
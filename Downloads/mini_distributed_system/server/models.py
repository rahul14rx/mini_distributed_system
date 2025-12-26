from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from .database import Base

class Worker(Base):
    __tablename__ = "workers"
    id = Column(String, primary_key=True, index=True) # UUID
    hostname = Column(String)
    status = Column(String, default="IDLE") # IDLE, BUSY, OFFLINE
    last_heartbeat = Column(DateTime(timezone=True), server_default=func.now())

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    command = Column(String)
    status = Column(String, default="QUEUED") # QUEUED, RUNNING, SUCCESS, FAILED
    worker_id = Column(String, ForeignKey("workers.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    log_path = Column(String, nullable=True)
    artifact_path = Column(String, nullable=True)
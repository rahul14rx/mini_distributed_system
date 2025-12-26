from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <--- IMPORT THIS
from .database import engine, Base
from .api import jobs, workers

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini Distributed System")

# --- ADD THIS BLOCK ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for development only)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ----------------------

app.include_router(jobs.router, prefix="/api/jobs", tags=["Jobs"])
app.include_router(workers.router, prefix="/api/workers", tags=["Workers"])

@app.get("/")
def health_check():
    return {"system": "online"}
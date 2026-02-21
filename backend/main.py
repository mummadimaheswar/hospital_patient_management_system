import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import Base, engine
from backend.routes import auth, patients, doctors, appointments, diagnosis, billing

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Hospital Patient Management System",
    description="A complete hospital management API supporting patient registration, appointments, diagnoses, and billing with role-based access control.",
    version="1.0.0",
)

_allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:8501").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(doctors.router)
app.include_router(appointments.router)
app.include_router(diagnosis.router)
app.include_router(billing.router)


@app.get("/", tags=["Health"])
def root():
    return {"message": "Hospital Patient Management System API is running"}

from fastapi import FastAPI
from sqlalchemy import text

from app.db import engine
from app.routers import auth, gardens, plants, species
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AgroSense API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router, prefix="/api/v1")
app.include_router(gardens.router, prefix="/api/v1")
app.include_router(species.router, prefix="/api/v1")
app.include_router(plants.router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/health/db")
def health_db():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"database": "ok"}
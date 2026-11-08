from fastapi import FastAPI
from sqlalchemy import text

from app.db import engine
from app.routers import auth, gardens

app = FastAPI(title="AgroSense API")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(gardens.router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/health/db")
def health_db():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"database": "ok"}
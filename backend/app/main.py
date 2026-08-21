from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import pathlib
import logging
from uuid import uuid4

from .config import settings
from .database import connect_to_mongo, close_db, get_db, is_connected
from .routes.jobs import router as jobs_router
from .routes.analysis import router as analysis_router

app = FastAPI(title="MadaCV Recruit AI - Backend")

# Configure CORS to allow the frontend origin (set `FRONTEND_URL` in .env)
origins = [settings.frontend_url] if settings.frontend_url else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    try:
        await connect_to_mongo()
    except Exception:
        logging.warning("MongoDB connection failed during startup; continuing without DB.")


@app.on_event("shutdown")
async def shutdown_event():
    close_db()


@app.get("/api/health")
async def health():
    return {"status": "ok", "project": "MadaCV Recruit AI"}


@app.get("/api/db-status")
async def db_status():
    """Return whether the backend is connected to MongoDB."""
    try:
        ok = await is_connected()
        return {"db_connected": ok}
    except Exception as e:
        logging.exception("Error checking DB status")
        return {"db_connected": False, "error": str(e)}


@app.get("/api/test-db")
async def test_db_connection():
    """Test MongoDB connection by writing, reading, and deleting a temp document."""
    db = get_db()
    collection = db["connection_test"]
    temp_id = str(uuid4())
    temp_doc = {"_id": temp_id, "test": "mongo-connection", "status": "temporary"}
    inserted = False

    try:
        result = await collection.insert_one(temp_doc)
        inserted = result.acknowledged
        if not inserted:
            return {"database": "connected", "result": "insert_failed"}

        found = await collection.find_one({"_id": temp_id})
        if not found:
            return {"database": "connected", "result": "read_failed"}

        return {"database": "connected", "result": "ok", "document_id": temp_id}
    finally:
        if inserted:
            await collection.delete_one({"_id": temp_id})


app.include_router(jobs_router)
app.include_router(analysis_router)


# Serve simple static frontend. Look for frontend in backend/frontend or ../frontend
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
_candidates = [BASE_DIR / "frontend", BASE_DIR.parent / "frontend"]
FRONTEND_DIR = None
for _d in _candidates:
    if _d.exists():
        FRONTEND_DIR = _d
        break

if FRONTEND_DIR is not None:
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
else:
    logging.info("No frontend directory found to serve static files")

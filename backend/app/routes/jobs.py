from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import uuid4
from datetime import datetime

from ..database import get_db

router = APIRouter(prefix="/api/jobs", tags=["jobs"])

_memory_jobs: List[dict] = []


class JobCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    skills: Optional[List[str]] = Field(default_factory=list)


class JobResponse(JobCreate):
    id: str
    createdAt: str


def _normalize_job_doc(job: dict) -> dict:
    return {
        "id": str(job.get("_id", job.get("id", ""))),
        "title": job.get("title", ""),
        "description": job.get("description", ""),
        "skills": job.get("skills", []),
        "createdAt": job.get("createdAt", ""),
    }


async def _get_jobs_from_db() -> List[dict]:
    db = get_db()
    collection = db["jobs"]
    docs = await collection.find().sort("createdAt", -1).to_list(length=100)
    return [_normalize_job_doc(doc) for doc in docs]


async def _insert_job_in_db(job_data: dict) -> dict:
    db = get_db()
    collection = db["jobs"]
    await collection.insert_one(job_data)
    return _normalize_job_doc(job_data)


@router.get("", response_model=List[JobResponse])
async def list_jobs():
    try:
        return await _get_jobs_from_db()
    except RuntimeError:
        return list(_memory_jobs)


@router.post("", response_model=JobResponse)
async def create_job(job: JobCreate):
    job_id = uuid4().hex
    now = datetime.utcnow().isoformat()
    normalized_skills = [skill.strip() for skill in job.skills if skill.strip()]
    job_doc = {
        "_id": job_id,
        "title": job.title.strip(),
        "description": job.description.strip(),
        "skills": normalized_skills,
        "createdAt": now,
    }

    try:
        return await _insert_job_in_db(job_doc)
    except RuntimeError:
        _memory_jobs.insert(0, _normalize_job_doc(job_doc))
        return _normalize_job_doc(job_doc)


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: str):
    try:
        db = get_db()
        collection = db["jobs"]
        job = await collection.find_one({"_id": job_id})
        if job is None:
            raise HTTPException(status_code=404, detail="Offre non trouvée")
        return _normalize_job_doc(job)
    except RuntimeError:
        for job in _memory_jobs:
            if job["id"] == job_id:
                return job
        raise HTTPException(status_code=404, detail="Offre non trouvée")

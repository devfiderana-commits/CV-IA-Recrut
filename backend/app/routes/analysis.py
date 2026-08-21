from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from uuid import uuid4
from datetime import datetime
from typing import List

from ..database import get_db
from ..services.pdf_service import extract_text_from_pdf
from ..services.scoring_service import score_candidate
from .jobs import _memory_jobs

router = APIRouter(tags=["analysis"])


async def _get_job(job_id: str) -> dict:
    try:
        db = get_db()
        job = await db["jobs"].find_one({"_id": job_id})
        if not job:
            raise HTTPException(status_code=404, detail="Offre non trouvée")
        return job
    except RuntimeError:
        for job in _memory_jobs:
            if job["id"] == job_id:
                return job
        raise HTTPException(status_code=404, detail="Offre non trouvée")


@router.post("/api/analyze")
async def analyze_job(job_id: str = Form(...), files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="Aucun fichier PDF fourni.")

    job = await _get_job(job_id)
    now = datetime.utcnow().isoformat()
    results = []

    db = None
    try:
        db = get_db()
    except RuntimeError:
        db = None

    for upload_file in files:
        if upload_file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail=f"Fichier non pris en charge : {upload_file.filename}")

        extracted_text = await extract_text_from_pdf(upload_file)
        if not extracted_text.strip():
            extracted_text = "(Aucun texte extrait du PDF)"

        candidate_id = uuid4().hex
        candidate_data = {
            "_id": candidate_id,
            "name": upload_file.filename,
            "email": "",
            "filename": upload_file.filename,
            "extractedText": extracted_text,
            "createdAt": now,
        }

        if db is not None:
            await db["candidates"].insert_one(candidate_data)

        scoring = score_candidate(job, candidate_data)
        analysis_data = {
            "_id": uuid4().hex,
            "job_id": job_id,
            "candidate_id": candidate_id,
            "score": scoring["score"],
            "semanticScore": scoring["semanticScore"],
            "skillsScore": scoring["skillsScore"],
            "criteriaScore": scoring["criteriaScore"],
            "matchedSkills": scoring["matchedSkills"],
            "missingSkills": scoring["missingSkills"],
            "createdAt": now,
        }

        if db is not None:
            await db["analyses"].insert_one(analysis_data)

        results.append({
            "candidate": {
                "id": candidate_id,
                "name": candidate_data["name"],
                "email": candidate_data["email"],
            },
            "score": analysis_data["score"],
            "semanticScore": analysis_data["semanticScore"],
            "skillsScore": analysis_data["skillsScore"],
            "criteriaScore": analysis_data["criteriaScore"],
            "matchedSkills": analysis_data["matchedSkills"],
            "missingSkills": analysis_data["missingSkills"],
        })

    return {"results": results}

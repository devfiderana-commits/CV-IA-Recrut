import re
from typing import Dict, List

from .ml_service import embed_text, cosine_similarity


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def _split_words(text: str) -> List[str]:
    return re.findall(r"\b[\w'-]+\b", text.lower())


def _build_skill_pattern(skill: str) -> str:
    token = re.escape(skill.strip().lower())
    return rf"\b{token}\b"


def _build_job_text(job: dict) -> str:
    title = job.get("title", "")
    description = job.get("description", "")
    skills = " ".join([skill for skill in job.get("skills", []) if skill])
    return f"{title} {description} {skills}".strip()


def score_candidate(job: dict, candidate: dict) -> Dict[str, object]:
    candidate_text = candidate.get("extractedText", "")
    normalized_text = _normalize_text(candidate_text)

    skills = [skill.strip() for skill in job.get("skills", []) if skill.strip()]
    matched_skills = []
    for skill in skills:
        if re.search(_build_skill_pattern(skill), normalized_text):
            matched_skills.append(skill)

    missing_skills = [skill for skill in skills if skill not in matched_skills]
    skills_score = len(matched_skills) / max(len(skills), 1)

    description_words = set(_split_words(job.get("description", "")))
    candidate_words = set(_split_words(candidate_text))
    common_words = description_words.intersection(candidate_words)
    criteria_score = len(common_words) / max(len(description_words), 1)

    job_text = _build_job_text(job)
    job_embedding = embed_text(job_text)
    candidate_embedding = embed_text(candidate_text)
    semantic_score = cosine_similarity(job_embedding, candidate_embedding)

    if semantic_score == 0.0:
        semantic_score = min(1.0, skills_score * 0.75 + criteria_score * 0.35)

    final_score = 0.6 * semantic_score + 0.3 * skills_score + 0.1 * criteria_score

    return {
        "score": round(final_score, 2),
        "semanticScore": round(semantic_score, 2),
        "skillsScore": round(skills_score, 2),
        "criteriaScore": round(criteria_score, 2),
        "matchedSkills": matched_skills,
        "missingSkills": missing_skills,
    }

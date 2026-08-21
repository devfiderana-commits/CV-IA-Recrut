# 🇲🇬 MadaCV Recruit AI

**AI-Assisted CV Screening and Candidate Ranking Platform**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python\&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95%2B-009688?logo=fastapi\&logoColor=white)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?logo=mongodb\&logoColor=white)](https://www.mongodb.com/atlas)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-F7DF1E?logo=javascript\&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5\&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3\&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![Git](https://img.shields.io/badge/Git-F05032?logo=git\&logoColor=white)](https://git-scm.com/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?logo=githubactions\&logoColor=white)](https://github.com/features/actions)
[![Render](https://img.shields.io/badge/Render-46E3B7?logo=render\&logoColor=black)](https://render.com/)

---

## Overview

MadaCV Recruit AI is a web-based recruitment assistance platform designed to automate the initial screening and ranking of candidate resumes.

The platform allows recruiters to create a job offer, define required skills, upload candidate CVs, extract their textual content, compare candidates against the job requirements, calculate a compatibility score and generate an explainable ranking.

The system is designed as a **decision-support tool**. Final recruitment decisions remain under the responsibility of the recruiter.

---

## Core Workflow

```text
Job Offer
    |
    v
Required Skills
    |
    v
Candidate CVs
    |
    v
PDF Text Extraction
    |
    v
NLP Processing
    |
    v
Sentence Transformer
    |
    v
Semantic Similarity
    |
    v
Skills Matching
    |
    v
Hybrid Scoring
    |
    v
Candidate Ranking
    |
    v
Recruiter Dashboard
```

---

## Technology Stack

| Layer              | Technology              |
| ------------------ | ----------------------- |
| Frontend           | HTML5, CSS3, JavaScript |
| Backend            | Python, FastAPI         |
| Database           | MongoDB Atlas           |
| PDF Processing     | PyMuPDF                 |
| NLP                | Sentence Transformers   |
| NLP Model          | `all-MiniLM-L6-v2`      |
| Authentication     | JWT                     |
| Testing            | Pytest                  |
| Version Control    | Git, GitHub             |
| CI/CD              | GitHub Actions          |
| Backend Deployment | Render                  |
| MLOps              | MLflow                  |
| API Documentation  | OpenAPI / Swagger       |

---

## AI Pipeline

The platform uses `all-MiniLM-L6-v2` to generate semantic embeddings for job descriptions and candidate resumes.

```text
Job Description
       |
       v
Text Processing
       |
       v
MiniLM
       |
       v
Job Embedding
       |
       | Semantic Comparison
       |
       v
CV Embedding
       ^
       |
     MiniLM
       ^
       |
Extracted CV Text
```

The semantic similarity is then combined with explicit skill matching to produce a final compatibility score.

---

## Scoring Model

The MVP uses a hybrid scoring approach:

| Component           |   Weight |
| ------------------- | -------: |
| Semantic similarity |      60% |
| Skills matching     |      30% |
| Explicit criteria   |      10% |
| **Final score**     | **100%** |

Example:

```text
Candidate: CV07

Semantic similarity:    94%
Skills matching:        87%
Explicit criteria:      90%

Final score:            91%
```

---

## Candidate Analysis

For each candidate, the system provides:

```text
Candidate: CV07
Final Score: 91%

Matched Skills
--------------
Python
FastAPI
Git
Linux
Docker
CI/CD

Missing Skills
--------------
MLflow

Strengths
---------
Backend development
REST API development
Linux environment
Git
Docker
```

The purpose of this analysis is to make the ranking more transparent and easier for the recruiter to review.

---

## Architecture

```text
                    Recruiter
                        |
                        v
              +-------------------+
              |     Frontend      |
              | HTML/CSS/JS       |
              +---------+---------+
                        |
                     REST API
                        |
                        v
              +-------------------+
              |      FastAPI      |
              +---------+---------+
                        |
          +-------------+-------------+
          |                           |
          v                           v
 +----------------+          +------------------+
 | MongoDB Atlas  |          |   NLP Pipeline   |
 |                |          |                  |
 | Users          |          | PyMuPDF          |
 | Jobs           |          | MiniLM           |
 | Candidates     |          | Similarity       |
 | Analyses       |          | Scoring          |
 +----------------+          +------------------+
```

---

## Project Structure

```text
MadaCV-Recruit-AI/
|
+-- frontend/
|   +-- index.html
|   +-- login.html
|   +-- dashboard.html
|   +-- job.html
|   +-- candidates.html
|   +-- analysis.html
|   |
|   +-- css/
|   |   +-- style.css
|   |
|   +-- js/
|       +-- api.js
|       +-- auth.js
|       +-- dashboard.js
|       +-- jobs.js
|       +-- candidates.js
|       +-- analysis.js
|
+-- backend/
|   +-- app/
|   |   +-- main.py
|   |   +-- config.py
|   |   +-- database.py
|   |   |
|   |   +-- models/
|   |   +-- routes/
|   |   +-- services/
|   |
|   +-- requirements.txt
|   +-- .env.example
|
+-- tests/
|
+-- .github/
|   +-- workflows/
|       +-- ci.yml
|
+-- .gitignore
+-- README.md
```

---

## API

### Authentication

```http
POST /api/auth/register
POST /api/auth/login
```

### Jobs

```http
GET    /api/jobs
POST   /api/jobs
GET    /api/jobs/{id}
DELETE /api/jobs/{id}
```

### Candidates

```http
POST /api/candidates/upload
GET  /api/candidates/{id}
```

### Analysis

```http
POST /api/analysis/{job_id}
GET  /api/analysis/{job_id}
GET  /api/analysis/{job_id}/ranking
```

### Health

```http
GET /api/health
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/MadaCV-Recruit-AI.git
cd MadaCV-Recruit-AI
```

### Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Configure environment variables

Create:

```text
backend/.env
```

Example:

```env
MONGODB_URI=mongodb+srv://...
DATABASE_NAME=madacv
JWT_SECRET=your_secret_key
```

Never commit `.env` to GitHub.

### Run the API

```bash
uvicorn app.main:app --reload --port 8000
```

API:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

---

## Testing

Run the test suite:

```bash
pytest
```

Health check:

```bash
curl http://localhost:8000/api/health
```

Expected response:

```json
{
  "status": "ok",
  "project": "MadaCV Recruit AI"
}
```

---

## Deployment

The target deployment architecture is:

```text
GitHub
   |
   +----------------------+
   |                      |
   v                      v
Frontend              GitHub Actions
   |                      |
   |                      v
Static Hosting       Tests / CI
                          |
                          v
                       Render
                          |
                          v
                       FastAPI
                          |
                          v
                    MongoDB Atlas
```

---

## MLOps Roadmap

### MVP

* [x] FastAPI backend
* [x] MongoDB Atlas integration
* [x] PDF text extraction
* [x] NLP embeddings
* [x] Semantic similarity
* [x] Skills matching
* [x] Candidate scoring
* [x] Candidate ranking

### Production

* [ ] Automated testing
* [ ] CI/CD pipeline
* [ ] Structured logging
* [ ] API monitoring
* [ ] Improved error handling
* [ ] Production security hardening

### MLOps

* [ ] MLflow experiment tracking
* [ ] Model versioning
* [ ] Evaluation metrics
* [ ] Model comparison
* [ ] Monitoring
* [ ] Drift detection

### Advanced AI

* [ ] OCR for scanned CVs
* [ ] Improved skill extraction
* [ ] Multilingual CV processing
* [ ] Advanced ranking models
* [ ] Improved explainability

---

## Responsible AI

MadaCV Recruit AI is designed as a recruitment assistance system rather than an autonomous hiring system.

The scoring mechanism evaluates professional relevance between the job requirements and candidate information.

The system should not use irrelevant personal characteristics such as:

* gender;
* religion;
* ethnicity;
* photograph;
* other sensitive characteristics unrelated to professional requirements.

The final hiring decision remains with the recruiter.

---

## Resource Efficiency

The MVP is designed to remain lightweight enough for development on a computer with limited resources.

The architecture deliberately uses:

* native HTML/CSS/JavaScript;
* FastAPI;
* one compact NLP model;
* MongoDB Atlas;
* cloud deployment for backend services;
* a limited number of CVs per analysis during the MVP stage.

This approach avoids unnecessary local resource consumption while keeping the architecture suitable for future scaling.

---

## Project Objectives

MadaCV Recruit AI combines several engineering disciplines:

```text
Artificial Intelligence
        |
        +-- NLP
        +-- Embeddings
        +-- Semantic Similarity
        |
        v
Backend Engineering
        |
        +-- Python
        +-- FastAPI
        +-- REST API
        |
        v
Database Engineering
        |
        +-- MongoDB
        |
        v
DevOps
        |
        +-- Git
        +-- GitHub
        +-- CI/CD
        +-- Cloud Deployment
        |
        v
MLOps
        |
        +-- MLflow
        +-- Experiment Tracking
        +-- Model Versioning
        +-- Monitoring
```

---

## Project Status

**Status: In active development**

The current priority is to complete the MVP before introducing advanced MLOps components.

---

## Author

**RATIARISON Fanilo Fiderana**

Information Technology Student
Madagascar

Areas of interest:

* Artificial Intelligence
* Backend Development
* NLP
* MLOps
* DevOps
* Web Development

---

## License

This project is released under the MIT License.

---

## Vision

MadaCV Recruit AI aims to provide a lightweight, explainable and practical AI-assisted solution for the initial screening of job applications.

**AI + NLP + Backend + Cloud + DevOps + MLOps**

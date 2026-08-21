Oui. Si le frontend est **HTML/CSS/JavaScript pur**, le projet devient encore plus léger et mieux adapté à ton PC avec **4 Go de RAM**.

# 🇲🇬 Audit final — MadaCV Recruit AI

## 1. 🎯 Concept

**MadaCV Recruit AI** est une application web d'aide au recrutement.

Le recruteur :

1. crée ou sélectionne une offre d'emploi ;
2. définit les compétences recherchées ;
3. dépose plusieurs CV, par exemple 10 ;
4. l'application extrait automatiquement le texte ;
5. le système compare chaque CV avec l'offre ;
6. calcule un score d'adéquation ;
7. classe les candidats ;
8. explique les compétences trouvées et manquantes.

⚠️ Le système fournit une **aide à la présélection**. La décision finale appartient toujours au recruteur.

---

# 2. 🏗️ Architecture finale

```text
                         INTERNET
                            │
                            ▼
                ┌─────────────────────┐
                │      FRONTEND       │
                │                     │
                │ HTML                 │
                │ CSS                  │
                │ JavaScript           │
                └──────────┬──────────┘
                           │
                         HTTPS
                           │
                           ▼
                ┌─────────────────────┐
                │       BACKEND       │
                │       FastAPI       │
                │       Render        │
                ├─────────────────────┤
                │ API REST             │
                │ Auth/JWT             │
                │ PDF extraction       │
                │ NLP                  │
                │ Scoring              │
                │ ML model             │
                └──────────┬──────────┘
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
   ┌──────────────────┐       ┌──────────────────┐
   │ MongoDB Atlas     │       │ Stockage CV      │
   │ ☁️ Cloud          │       │ PDF              │
   ├──────────────────┤       └──────────────────┘
   │ jobs             │
   │ candidates       │
   │ analyses         │
   │ users            │
   └──────────────────┘
```

---

# 3. 💻 Frontend

### Technologie

```text
HTML
CSS
JavaScript
```

**Pas de React.**

Pas besoin de :

```text
React
Vite
Node.js frontend
npm
React Router
```

Le frontend peut être extrêmement léger.

Structure :

```text
frontend/
│
├── index.html
├── login.html
├── dashboard.html
├── job.html
├── candidates.html
├── analysis.html
│
├── css/
│   └── style.css
│
└── js/
    ├── api.js
    ├── auth.js
    ├── dashboard.js
    ├── jobs.js
    ├── candidates.js
    └── analysis.js
```

Le JavaScript communiquera avec FastAPI avec `fetch()`.

Exemple :

```text
HTML
 ↓
JavaScript
 ↓
fetch()
 ↓
FastAPI
 ↓
MongoDB / ML
```

---

# 4. ⚙️ Backend

Technologie :

```text
Python
FastAPI
```

Hébergement :

```text
Render
```

Structure recommandée :

```text
backend/
│
├── app/
│   ├── main.py
│   │
│   ├── routes/
│   │   ├── auth.py
│   │   ├── jobs.py
│   │   ├── candidates.py
│   │   └── analysis.py
│   │
│   ├── services/
│   │   ├── pdf_service.py
│   │   ├── ml_service.py
│   │   └── scoring_service.py
│   │
│   ├── models/
│   │   ├── job.py
│   │   ├── candidate.py
│   │   └── analysis.py
│   │
│   ├── database.py
│   └── config.py
│
├── requirements.txt
└── .env
```

---

# 5. 📄 Traitement des CV

Pipeline :

```text
CV.pdf
   ↓
Upload
   ↓
FastAPI
   ↓
PyMuPDF
   ↓
Extraction du texte
   ↓
Nettoyage
   ↓
Analyse NLP
```

Pour le MVP, on accepte principalement les **PDF contenant du texte**.

Un CV scanné comme image nécessitera plus tard :

```text
PDF image
   ↓
OCR
   ↓
Texte
```

L'OCR peut donc être une fonctionnalité **V2**.

---

# 6. 🤖 ML — un seul modèle

On garde **un seul modèle NLP** :

```text
all-MiniLM-L6-v2
```

Son rôle :

> transformer le texte en vecteurs afin de mesurer la similarité sémantique entre l'offre et le CV.

Pipeline :

```text
OFFRE
  ↓
MiniLM
  ↓
Embedding offre
       │
       │ comparaison
       ▼
Embedding CV
  ↑
MiniLM
  ↑
CV
```

Puis :

```text
Embedding offre
       +
Embedding CV
       ↓
Similarité cosinus
       ↓
Score sémantique
```

---

# 7. 📊 Scoring

Je recommande de ne **pas** utiliser uniquement la similarité du modèle.

Le score final peut être :

```text
                    SCORE FINAL
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
       60 %            30 %           10 %
    Similarité       Skills        Critères
    sémantique       détectées     explicites
```

Exemple :

```text
CV07

Similarité :        94 %
Skills :            87 %
Critères :          90 %

Score final :       91 %
```

Résultat :

```text
🥇 CV07 — 91 %
🥈 CV03 — 87 %
🥉 CV09 — 82 %
   CV01 — 76 %
   CV05 — 71 %
```

---

# 8. 🔎 Explication du résultat

Le recruteur doit pouvoir comprendre **pourquoi** un CV obtient son score.

Exemple :

```text
CV07 — Score : 91 %

Compétences trouvées
─────────────────────
✅ Python
✅ FastAPI
✅ Git
✅ Linux
✅ Docker
✅ CI/CD

Compétences manquantes
───────────────────────
⚠️ MLflow

Points forts
────────────
• Expérience backend
• API REST
• Git
• Docker
• Linux
```

Cela rend le système beaucoup plus professionnel qu'un simple :

```text
91 %
```

---

# 9. 🗄️ MongoDB Atlas

MongoDB Atlas reste la base de données cloud.

Collections :

```text
users
jobs
candidates
analyses
```

### jobs

```text
{
    title,
    description,
    skills,
    createdAt
}
```

### candidates

```text
{
    name,
    email,
    cvUrl,
    extractedText,
    createdAt
}
```

### analyses

```text
{
    jobId,
    candidateId,
    score,
    semanticScore,
    skillsScore,
    matchedSkills,
    missingSkills,
    createdAt
}
```

---

# 10. 📁 Stockage des CV

Je recommande :

```text
PDF
 ↓
Stockage fichiers
 ↓
URL
 ↓
MongoDB
```

MongoDB conserve :

```text
candidateId
name
email
cvUrl
extractedText
```

et les résultats d'analyse.

Évite de stocker directement de gros fichiers PDF dans les documents MongoDB pour le MVP.

---

# 11. 🔐 Authentification

Le recruteur dispose d'un compte.

```text
Login
  ↓
FastAPI
  ↓
JWT
  ↓
Dashboard
```

Sécurité :

```text
JWT
Password hashing
HTTPS
CORS
Validation des fichiers
Limite taille PDF
MIME type
.env
```

Les secrets restent dans les variables d'environnement :

```text
MONGO_URI
JWT_SECRET
```

Jamais dans GitHub.

---

# 12. 🌐 API FastAPI

API possible :

```text
POST   /api/auth/register
POST   /api/auth/login

GET    /api/jobs
POST   /api/jobs
GET    /api/jobs/{id}
DELETE /api/jobs/{id}

POST   /api/candidates/upload
GET    /api/candidates/{id}

POST   /api/analysis/{job_id}

GET    /api/analysis/{job_id}
GET    /api/analysis/{job_id}/ranking
```

Le frontend HTML utilise simplement :

```text
fetch()
```

pour appeler ces endpoints.

---

# 13. ☁️ Render

Render héberge :

```text
FastAPI
   │
   ├── API
   ├── PDF processing
   ├── MiniLM
   └── scoring
```

Au démarrage :

```text
Render
 ↓
FastAPI
 ↓
chargement MiniLM
 ↓
API disponible
```

Puis :

```text
POST /api/analysis/{job_id}
```

lance l'analyse.

---

# 14. 🚀 GitHub + CI/CD

Architecture :

```text
VS Code
   ↓
Git
   ↓
GitHub
   ↓
GitHub Actions
   ↓
Tests
   ↓
Deploy
   ↓
Render
```

Tu peux ainsi montrer au jury/recruteur :

```text
Git
GitHub
Branches
Pull Requests
Tests
CI/CD
Déploiement Cloud
```

---

# 15. 🧪 MLOps

Le projet commence simplement.

### Phase 1

```text
Dataset
 ↓
MiniLM
 ↓
Scoring
 ↓
API
```

### Phase 2 — MLflow

```text
ML / évaluation
       ↓
     MLflow
       ├── paramètres
       ├── métriques
       └── versions
```

Puis :

```text
Model v1
Model v2
Model v3
```

Tu peux comparer les versions.

### Phase 3 — monitoring

```text
Analyses
   ↓
Métriques
   ↓
Monitoring
   ↓
Détection éventuelle de dérive
```

**MLflow ne doit donc pas être la première chose que tu installes.**

---

# 16. 🖥️ Ton PC — 4 Go RAM

Avec ton matériel :

### Local

```text
VS Code
Python
FastAPI
HTML
CSS
JavaScript
Git
tests
```

### Cloud

```text
MongoDB Atlas
Render
GitHub
GitHub Actions
MLflow éventuellement
```

### À éviter

```text
❌ Docker Desktop
❌ Kubernetes
❌ gros LLM local
❌ plusieurs modèles NLP
❌ gros entraînement
```

Le choix **HTML/CSS/JS** réduit encore la consommation de ressources côté développement.

---

# 17. ⚠️ Limites et risques

### CV scanné

```text
PDF image
   ↓
OCR
```

→ fonctionnalité V2.

### Biais

Ne pas utiliser :

```text
❌ sexe
❌ âge
❌ origine
❌ religion
❌ photo
```

Le système doit principalement analyser :

```text
✅ compétences
✅ expérience
✅ formation pertinente
✅ technologies
✅ critères professionnels
```

### Interprétation du score

Un score de 91 % signifie :

> **forte correspondance avec les critères de l'offre selon la méthode de scoring utilisée.**

Cela ne signifie pas :

> « ce candidat est objectivement le meilleur ».

---

# 18. 📂 Structure finale du projet

```text
MadaCV-Recruit-AI/
│
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── dashboard.html
│   ├── job.html
│   ├── candidates.html
│   ├── analysis.html
│   │
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       ├── api.js
│       ├── auth.js
│       ├── dashboard.js
│       ├── jobs.js
│       ├── candidates.js
│       └── analysis.js
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── config.py
│   │   │
│   │   ├── routes/
│   │   ├── services/
│   │   └── models/
│   │
│   ├── requirements.txt
│   └── .env.example
│
├── tests/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── .gitignore
└── README.md
```

---

# 19. 🏆 Évaluation finale

| Critère              | Évaluation |
| -------------------- | ---------: |
| Problème réel        |      ⭐⭐⭐⭐⭐ |
| Frontend HTML/CSS/JS |      ⭐⭐⭐⭐⭐ |
| Backend FastAPI      |      ⭐⭐⭐⭐⭐ |
| NLP / IA             |      ⭐⭐⭐⭐⭐ |
| MongoDB Atlas        |      ⭐⭐⭐⭐⭐ |
| CI/CD                |      ⭐⭐⭐⭐⭐ |
| MLOps                |       ⭐⭐⭐⭐ |
| Déploiement          |      ⭐⭐⭐⭐⭐ |
| Faisabilité 4 Go RAM |      ⭐⭐⭐⭐⭐ |
| Portfolio            |      ⭐⭐⭐⭐⭐ |

## Verdict : **9/10**

Le projet est particulièrement cohérent pour un objectif **AI Integration / Backend-MLOps**.

La chaîne finale est :

```text
🇲🇬 MadaCV Recruit AI

HTML
CSS
JavaScript
      ↓
FastAPI
      ↓
PyMuPDF
      ↓
MiniLM
      ↓
Scoring hybride
      ↓
Classement des CV
      ↓
MongoDB Atlas
      ↓
GitHub
      ↓
GitHub Actions
      ↓
Render
      ↓
MLflow
      ↓
Monitoring
```

**Pas de React. Pas de Docker pour le MVP. Un seul modèle ML. Maximum 10 CV au départ.**

C'est cette version que je retiendrais comme **architecture officielle du projet**.


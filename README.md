# LegalEase

AI-Powered Legal Document Generator.

## Technologies

- Python
- FastAPI
- Streamlit
- Google Gemini
- Pydantic
- python-docx
- FPDF2

## Features

- AI legal-document drafting
- Employment contracts
- NDA drafts
- Lease agreements
- Freelance contracts
- Editable document preview
- TXT export
- DOCX export
- PDF export
- FastAPI REST API
- Gemini integration

## Installation

Create virtual environment:

python -m venv .venv

Activate:

Windows:

.venv\Scripts\activate

Install:

pip install -r requirements.txt

Create .env:

GEMINI_API_KEY=YOUR_KEY
GEMINI_MODEL=gemini-1.5-pro
BACKEND_URL=http://127.0.0.1:8000

## Run backend

uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

## Run frontend

streamlit run frontend/app.py

## Test

pytest -q

## API

POST /generate

Request:

{
    "document_type": "NDA",
    "parties": "Alice and ABC Company",
    "terms": "Confidentiality must be maintained",
    "effective_date": "October 1, 2026"
}

Response:

{
    "document_type": "NDA",
    "content": "Generated document..."
}

## Important

LegalEase generates AI-assisted drafts.

It does not replace a qualified legal professional.

Important documents should be reviewed for the applicable jurisdiction before signing or use.
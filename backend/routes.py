from fastapi import APIRouter, HTTPException

from ai_core.gemini_generator import GeminiDocumentGenerator

from backend.schemas import (
    DocumentRequest,
    DocumentResponse
)

def sanitize_text(text: str) -> str:
    return " ".join(text.strip().split())

router = APIRouter()

generator = GeminiDocumentGenerator()


@router.post(
    "/generate",
    response_model=DocumentResponse
)
def generate_document(
    request: DocumentRequest
):

    try:

        document = generator.generate_document(

            document_type=sanitize_text(
                request.document_type
            ),

            parties=sanitize_text(
                request.parties
            ),

            terms=sanitize_text(
                request.terms
            ),

            effective_date=sanitize_text(
                request.effective_date
            ),
        )

        settings = get_settings()

        return DocumentResponse(

            document=document,

            model=settings.gemini_model,

            demo_mode=generator.demo_mode,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=(
                f"Document generation failed: {exc}"
            )
        ) from exc
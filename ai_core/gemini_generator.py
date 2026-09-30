import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


class GeminiDocumentGenerator:
    def __init__(self):
        self.demo_mode = False

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            self.demo_mode = True
            self.client = None
            return

        self.client = genai.Client(api_key=api_key)

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash"
        )

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str
    ):

        if self.demo_mode:
            return self._demo_document(
                document_type,
                parties,
                terms,
                effective_date
            )

        prompt = f"""
Create a professional legal document.

Document Type:
{document_type}

Parties:
{parties}

Terms and Conditions:
{terms}

Effective Date:
{effective_date}

Write the document in clear and professional language.

Include:
1. Title
2. Introduction
3. Parties
4. Terms and Conditions
5. Responsibilities
6. Confidentiality
7. Termination
8. General provisions
9. Signature section

Do not invent personal information that was not provided.
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        if not response or not response.text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return response.text

    def _demo_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str
    ):

        return f"""
{document_type.upper()}

Effective Date: {effective_date}

PARTIES

This agreement is between:

{parties}

TERMS AND CONDITIONS

{terms}

RESPONSIBILITIES

Each party agrees to perform their responsibilities
as described in this agreement.

CONFIDENTIALITY

Both parties agree to keep confidential information
private and not disclose it without proper permission.

TERMINATION

This agreement may be terminated according to the
terms agreed upon by the parties.

GENERAL PROVISIONS

Any changes to this agreement should be made with
the agreement of the parties.

SIGNATURES

Party 1: __________________________

Party 2: __________________________

Date: _____________________________
"""
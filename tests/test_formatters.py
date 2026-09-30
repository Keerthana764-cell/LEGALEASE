from utils.document_formatter import (
    format_docx,
    format_pdf,
    format_txt
)


SAMPLE = """
DRAFT NOTICE

This is an AI-generated draft.

1. PURPOSE

The parties agree to the supplied terms.

2. SIGNATURES

Party A: ________

Party B: ________
"""


def test_txt_formatter():

    result = format_txt(
        SAMPLE
    )

    assert isinstance(
        result,
        bytes
    )

    assert b"DRAFT NOTICE" in result


def test_docx_formatter():

    result = format_docx(
        SAMPLE,
        "Test Agreement"
    )

    # DOCX files are ZIP containers.

    assert result[:2] == b"PK"


def test_pdf_formatter():

    result = format_pdf(
        SAMPLE,
        "Test Agreement"
    )

    assert result.startswith(
        b"%PDF"
    )
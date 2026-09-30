from fastapi.testclient import TestClient

from backend.main import app

import backend.routes as routes


class FakeGenerator:

    def generate_document(
        self,
        **kwargs
    ):

        return """
DRAFT NOTICE

1. PURPOSE

Generated test document.
"""


def test_health():

    client = TestClient(app)

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert response.json() == {
        "status": "healthy"
    }


def test_generate(
    monkeypatch
):

    monkeypatch.setattr(
        routes,
        "_generator",
        FakeGenerator()
    )


    client = TestClient(app)


    response = client.post(

        "/generate",

        json={

            "document_type":
                "NDA",

            "parties":
                "A and B",

            "terms":
                "Keep information confidential",

            "effective_date":
                "2026-10-01"
        }
    )


    assert response.status_code == 200


    data = response.json()


    assert data[
        "document_type"
    ] == "NDA"


    assert (
        "Generated test document"
        in data["content"]
    )


def test_generate_validation():

    client = TestClient(app)


    response = client.post(

        "/generate",

        json={

            "document_type":
                "",

            "parties":
                "A and B",

            "terms":
                "Confidential",

            "effective_date":
                "2026-10-01"
        }
    )


    assert response.status_code == 422
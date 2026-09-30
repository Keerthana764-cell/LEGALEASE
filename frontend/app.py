import html
import os

import requests

import streamlit as st

from dotenv import load_dotenv

load_dotenv()


st.set_page_config(

    page_title="LegalEase",

    page_icon="⚖️",

    layout="wide",
)


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


st.markdown(
    """
    <style>

    .main-title {

        text-align: center;

        font-size: 2.5rem;

        font-weight: 700;

    }

    .subtitle {

        text-align: center;

        color: #777;

        margin-bottom: 1.5rem;

    }

    .preview {

        background: #15171a;

        color: #f4f4f4;

        padding: 24px;

        border-radius: 14px;

        min-height: 420px;

        max-height: 650px;

        overflow: auto;

        white-space: pre-wrap;

        font-family: Georgia, serif;

        line-height: 1.65;

    }

    .notice {

        background: #fff4cc;

        padding: 12px;

        border-radius: 10px;

    }

    </style>
    """,
    unsafe_allow_html=True
)


logo_path = os.path.join(

    os.path.dirname(
        os.path.dirname(__file__)
    ),

    "assets",

    "logo.png"
)


if os.path.exists(logo_path):

    left, center, right = st.columns(
        [1, 2, 1]
    )

    with center:

        st.image(
            logo_path,
            width=110
        )


st.markdown(
    '<div class="main-title">LegalEase</div>',
    unsafe_allow_html=True
)


st.markdown(
    '<div class="subtitle">'
    'AI-assisted legal document drafting'
    '</div>',
    unsafe_allow_html=True
)


st.markdown(
    '<div class="notice">'
    'Review every generated draft carefully. '
    'LegalEase is not a lawyer and generated '
    'documents are not legal advice.'
    '</div>',
    unsafe_allow_html=True
)


st.divider()


with st.form("document_form"):

    col1, col2 = st.columns(2)

    with col1:

        document_type = st.selectbox(

            "Document Type",

            [

                "Employment Contract",

                "Non-Disclosure Agreement",

                "Lease Agreement",

                "Freelance Work Contract",

                "Service Agreement",

                "General Agreement",

            ],
        )


        parties = st.text_area(

            "Parties Involved",

            placeholder=(
                "Jane Doe (Service Provider), "
                "Example Labs Pvt Ltd (Client)"
            ),

            height=120,
        )


    with col2:

        effective_date = st.text_input(

            "Effective Date",

            placeholder=(
                "27 September 2026"
            ),
        )


        terms = st.text_area(

            "Terms & Conditions",

            placeholder=(
                "Payment within 30 days; "
                "Confidentiality must be maintained; "
                "Either party may terminate with 30 days notice"
            ),

            height=120,
        )


    submitted = st.form_submit_button(

        "Generate Document",

        type="primary",

        use_container_width=True
    )


if submitted:

    if (
        not parties.strip()
        or not terms.strip()
        or not effective_date.strip()
    ):

        st.error(
            "Please fill in all required fields."
        )

    else:

        payload = {

            "document_type": document_type,

            "parties": parties,

            "terms": terms,

            "effective_date": effective_date,
        }


        try:

            with st.spinner(
                "Generating legal document..."
            ):

                response = requests.post(

                    f"{BACKEND_URL}/generate",

                    json=payload,

                    timeout=90,
                )


            if response.ok:

                data = response.json()

                st.session_state.document = (
                    data["document"]
                )

                st.session_state.model = (
                    data["model"]
                )

                st.session_state.demo_mode = (
                    data["demo_mode"]
                )

                st.success(
                    "Document generated successfully."
                )

            else:

                try:

                    detail = response.json().get(
                        "detail",
                        response.text
                    )

                except Exception:

                    detail = response.text


                st.error(
                    f"Backend error: {detail}"
                )


        except requests.RequestException as exc:

            st.error(
                "Could not connect to FastAPI. "
                "Make sure the backend is running."
            )

            st.caption(
                str(exc)
            )


if "document" in st.session_state:

    st.divider()

    mode = (

        "Demo mode"

        if st.session_state.get(
            "demo_mode"
        )

        else "Gemini AI"
    )


    st.caption(

        f"Generation source: {mode} | "
        f"Model: {st.session_state.get('model', 'unknown')}"
    )


    st.subheader(
        "Editable Document"
    )


    edited = st.text_area(

        "Edit the generated text "
        "before exporting.",

        value=st.session_state.document,

        height=600,

        label_visibility="collapsed",
    )


    st.session_state.document = edited


    st.subheader(
        "Preview"
    )


    preview = (
        html.escape(edited)
        .replace("\n", "<br>")
    )


    st.markdown(

        f'<div class="preview">'
        f'{preview}'
        f'</div>',

        unsafe_allow_html=True
    )


    st.subheader(
        "Download"
    )


    c1, c2, c3 = st.columns(3)


    with c1:

        st.download_button(

            "Download TXT",

            export_txt(edited),

            file_name=(
                "legalease_document.txt"
            ),

            mime="text/plain",

            use_container_width=True,
        )


    with c2:

        st.download_button(

            "Download DOCX",

            export_docx(
                edited,
                document_type
            ),

            file_name=(
                "legalease_document.docx"
            ),

            mime=(
                "application/"
                "vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),

            use_container_width=True,
        )


    with c3:

        st.download_button(

            "Download PDF",

            export_pdf(
                edited,
                document_type
            ),

            file_name=(
                "legalease_document.pdf"
            ),

            mime="application/pdf",

            use_container_width=True,
        )
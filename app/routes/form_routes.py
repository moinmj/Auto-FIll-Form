from fastapi import APIRouter, UploadFile, File, HTTPException, Body, Form, APIRouter
import requests
from app.services.form_analyzer import analyze_form
from app.services.field_extractor import extract_fields
from app.services.decision_engine import enhanced_decision_engine
from app.services.autofill_engine import prepare_autofill_data, autofill_form
from app.ml.document_parser import extract_text_from_image, extract_entities
from app.chatbot.chatbot_engine import generate_smart_flow
from app.services.decision_engine import suggest_documents
import os
from app.services.form_analyzer import analyze_form
from app.services.form_filler import fill_form
from pydantic import BaseModel
from typing import Dict
router = APIRouter()

@router.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):

    os.makedirs("data", exist_ok=True)

    file_location = os.path.join("data", file.filename)

    with open(file_location, "wb") as f:
        f.write(await file.read())

    # OCR
    text = extract_text_from_image(file_location)

    # Extract structured data
    data = extract_entities(text)

    return {
        "extracted_text": text,
        "structured_data": data
    }


@router.get("/autofill-form")
def autofill(url: str):

    # Step 1: Analyze form
    raw_fields = analyze_form(url)

    # Step 2: Extract structured fields
    structured_fields = extract_fields(raw_fields)

    # Step 3: Decision engine
    # 🔥 Simulated document data (later comes from OCR)
    document_data = {
        "name": "Moin Jan Rashid",
        "phone": "9876543210"
    }

    decisions = enhanced_decision_engine(structured_fields, document_data)

    # Step 4: Simulated user input
    user_responses = {
    "custname": "Moin Jan Rashid",
    "custtel": "9876543210",
    "custemail": "moin@example.com",
    "size": "Medium",
    "topping": "Bacon",
    "delivery": "18:30"
    }

    # Step 5: Prepare payload
    final_payload = prepare_autofill_data(decisions, user_responses)

    # 🔥 Step 6: Autofill using Selenium
    autofill_form(url, final_payload)

    return {
        "message": "Form opened and autofilled",
        "final_payload": final_payload
    }
@router.post("/smart-autofill")
async def smart_autofill(
    url: str=Form(...),
    file: UploadFile = File(None)
):
    try:
        

    
        import os

        # Step 1: Analyze form
        raw_fields = analyze_form(url)
        structured_fields = extract_fields(raw_fields)

        # 🔥 Step 2: Suggest documents
        suggested_docs = suggest_documents(structured_fields)

        document_data = {}

        # Step 3: Process document if uploaded
        if file:
            os.makedirs("data", exist_ok=True)
            file_location = os.path.join("data", file.filename)

            with open(file_location, "wb") as f:
                f.write(await file.read())

            text = extract_text_from_image(file_location)
            document_data = extract_entities(text)

        # Step 4: Decision engine
        decisions = enhanced_decision_engine(structured_fields, document_data)
        # 🔥 Identify missing fields (those we need to ask user)

        missing_fields = [
            d["field"] for d in decisions
            if d["action"] == "ask_user"
        ]

        # 🔥 Step 5: Generate chatbot flow
        chatbot_flow = generate_smart_flow(decisions, suggested_docs)

        # Step 6: Simulated responses (temporary)
        user_responses = {
            "size": "Medium",
            "topping": "Bacon",
            "delivery": "18:30"
        }

        # Step 7: Prepare payload
        final_payload = prepare_autofill_data(decisions, user_responses)

        # Step 8: Autofill
        autofill_form(url, final_payload)

        return {
            "suggested_documents": suggested_docs,
            "chatbot_flow": chatbot_flow,
            "document_data": document_data,
            "missing_fields": missing_fields,   # ✅ ADD THIS
            "decisions": decisions,
            "final_payload": final_payload
        }
    except Exception as e: 
        print("❌ ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
@router.post("/submit-responses")
async def submit_responses(
    url: str = Body(...),
    decisions: list = Body(...),
    user_responses: dict = Body(...)
):
    """
    Receive user responses and perform final autofill
    """

    # 🔥 Prepare final payload
    final_payload = prepare_autofill_data(decisions, user_responses)

    # 🔥 Autofill using Selenium
    autofill_form(url, final_payload)

    return {
        "message": "Form autofilled successfully",
        "final_payload": final_payload
    }
@router.get("/analyze-form")
def analyze_form_api(url: str):
    result = analyze_form(url)
    return {"fields": result}

class AutoFillRequest(BaseModel):
    url: str
    payload: Dict[str, str]


@router.post("/auto-fill-browser")
def autofill_browser(request: AutoFillRequest):
    print("✅ Incoming request:", request)

    success = fill_form(request.url, request.payload)

    return {"status": "success" if success else "failed"}

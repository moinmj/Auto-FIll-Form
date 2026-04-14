import pytesseract
import cv2
import re
from app.ml.llm_extractor import extract_entities_llm

# 🔥 Set Tesseract path (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# ==============================
# OCR FUNCTION
# ==============================
def extract_text_from_image(image_path):
    """
    Extract raw text from image using OCR
    """

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(f"Image not loaded properly. Check path: {image_path}")

    # 🔥 Preprocessing (improves OCR accuracy)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    text = pytesseract.image_to_string(thresh)

    print("🔍 OCR TEXT:\n", text)  # Debug

    return text


# ==============================
# FALLBACK (RULE-BASED)
# ==============================
def extract_entities_fallback(text):
    """
    Basic regex fallback if LLM fails
    """
    data = {}

    # Phone
    phone_match = re.search(r"\b\d{10}\b", text)
    if phone_match:
        data["phone"] = phone_match.group()

    # Email
    email_match = re.search(r"\S+@\S+", text)
    if email_match:
        data["email"] = email_match.group()

    # Very strict name detection (avoid address)
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    for line in lines:
        if any(char.isdigit() for char in line):
            continue

        if any(word in line.lower() for word in [
            "road", "street", "nagar", "area",
            "colony", "sector", "block", "district"
        ]):
            continue

        words = line.split()

        if 1 < len(words) <= 3:
            if all(w[0].isupper() for w in words):
                data["name"] = line
                break

    return data


# ==============================
# MAIN ENTITY EXTRACTION
# ==============================
def extract_entities(text):
    """
    Hybrid extraction:
    1. Try LLM (Groq)
    2. Fallback to regex if needed
    """

    # 🔥 STEP 1: Try LLM
    llm_data = extract_entities_llm(text)

    print("🤖 LLM OUTPUT:", llm_data)
    
    if llm_data.get("email") and len(llm_data["email"]) < 8:
        llm_data["email"] = None

    # 🔥 STEP 2: Validate LLM output
    if llm_data and any(llm_data.values()):
        return llm_data

    # 🔥 STEP 3: Fallback
    print("⚠️ Using fallback extraction...")
    return extract_entities_fallback(text)
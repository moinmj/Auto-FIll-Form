import re

IMPORTANT_FIELDS = ["name", "phone", "email", "address"]


def enhanced_decision_engine(structured_fields, document_data=None):
    """
    Decide how to handle each field based on:
    - Document availability
    - Field type
    - Field category
    - Validation of extracted data
    """

    decisions = []

    for field in structured_fields:
        mapped = field.get("mapped_field")
        name = field.get("name")
        label = (field.get("original_label") or "").lower()
        field_type = field.get("type")
        category = field.get("category")
        options = field.get("options", None)

        decision = {
            "field": name,
            "mapped_field": mapped,
            "original_label": field.get("original_label"),
            "action": None,
            "value": None,
            "options": options
        }

        # 🔥 1. FILE UPLOAD
        if field_type == "file":
            decision["action"] = "require_upload"

        # 🔥 2. DOCUMENT DATA HANDLING
        elif document_data and mapped in document_data:

            value = document_data.get(mapped)

            # ✅ NAME VALIDATION
            if mapped == "name":
                if value and isinstance(value, str):
                    if any(word in value.lower() for word in [
                        "road", "street", "nagar", "area",
                        "colony", "sector", "block", "district"
                    ]) or any(char.isdigit() for char in value):
                        decision["action"] = "ask_user"
                    else:
                        decision["action"] = "auto_fill"
                        decision["value"] = value
                else:
                    decision["action"] = "ask_user"

            # ✅ PHONE VALIDATION
            elif mapped == "phone":
                if value and isinstance(value, str) and value.isdigit() and len(value) == 10:
                    decision["action"] = "auto_fill"
                    decision["value"] = value
                else:
                    decision["action"] = "ask_user"

            # ✅ EMAIL (ALWAYS ASK USER)
            elif mapped == "email":

                email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

                raw_text = document_data.get("raw_text", "")

                if value and re.match(email_pattern, value) and value in raw_text:
                    decision["action"] = "auto_fill"
                    decision["value"] = value
                else:
                    decision["action"] = "ask_user"

            # ✅ OTHER FIELDS
            else:
                if value:
                    decision["action"] = "auto_fill"
                    decision["value"] = value
                else:
                    decision["action"] = "ask_user"

        # 🔥 3. IMPORTANT FIELDS (fallback)
        elif (
            mapped in IMPORTANT_FIELDS or
            any(k in label for k in IMPORTANT_FIELDS) or
            any(k in (name or "").lower() for k in IMPORTANT_FIELDS)
        ):
            decision["action"] = "ask_user"

        # 🔥 4. PREFERENCES
        elif category == "preferences":
            decision["action"] = "ask_user"

        # 🔥 5. OPTIONAL
        else:
            decision["action"] = "optional"

        # ✅ IMPORTANT: APPEND DECISION
        decisions.append(decision)

    # ✅ IMPORTANT: ALWAYS RETURN
    return decisions


def suggest_documents(structured_fields):
    """
    Suggest documents based on required fields
    """

    required_fields = [f.get("mapped_field") for f in structured_fields]

    documents = []

    if "name" in required_fields and "dob" in required_fields:
        documents.append("Aadhar Card")

    if "name" in required_fields and "address" in required_fields:
        documents.append("Passport")

    if "name" in required_fields and "phone" in required_fields:
        documents.append("Driving License")

    return list(set(documents))
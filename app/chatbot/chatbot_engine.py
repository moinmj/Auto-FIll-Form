def generate_smart_flow(decisions, suggested_documents=None):
    """
    Generate intelligent interaction flow:
    - Ask for document first
    - Ask only missing/required fields
    - Clearly indicate missing document data
    """

    flow = []

    # 🔥 STEP 1: Document prompt
    if suggested_documents:
        doc_list = ", ".join(suggested_documents)
        flow.append({
            "type": "document_prompt",
            "message": f"Would you like to upload a document ({doc_list}) to autofill the form?"
        })

    # 🔥 STEP 2: Iterate decisions
    for item in decisions or []:
        action = item.get("action")
        field = item.get("field")
        label = item.get("original_label") or field
        options = item.get("options")
        mapped = item.get("mapped_field")

        # 📄 FILE UPLOAD
        if action == "require_upload":
            flow.append({
                "type": "file_upload",
                "field": field,
                "message": f"Please upload the required file for {label}"
            })

        # ❓ ASK USER (SMART MESSAGING)
        elif action == "ask_user":

            # 🔥 Better message if missing from document
            if mapped in ["name", "phone", "email", "address"]:
                message = f"{label} not found in uploaded document. Please enter it manually."
            else:
                message = f"Please provide your {label}"

            # 🔘 OPTIONS (radio/checkbox)
            if options:
                flow.append({
                    "type": "choice",
                    "field": field,
                    "message": message,
                    "options": options
                })
            else:
                flow.append({
                    "type": "input",
                    "field": field,
                    "message": message
                })

    return flow
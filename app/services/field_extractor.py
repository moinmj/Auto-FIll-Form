from app.ml.field_mapper import map_field_with_llm
def normalize_label(label: str):
    """
    Clean and normalize label text
    """
    return label.lower().strip().replace(":", "")


def map_field(label: str):
    """
    Map label to standardized field
    """
    label = normalize_label(label)

    # Name
    if "name" in label:
        return "name"

    # Email
    if "email" in label or "e-mail" in label:
        return "email"

    # Phone
    if "phone" in label or "tel" in label or "mobile" in label:
        return "phone"

    # Address
    if "address" in label:
        return "address"

    # Date of Birth
    if "dob" in label or "date of birth" in label:
        return "dob"

    # Time / Delivery
    if "time" in label:
        return "time"

    # Comments / Instructions
    if "comment" in label or "instruction" in label:
        return "comments"

    # Default fallback
    return "unknown"

def categorize_field(mapped_field):
    if mapped_field in ["name", "dob"]:
        return "personal_info"

    if mapped_field in ["email", "phone"]:
        return "contact_info"

    if mapped_field in ["address"]:
        return "address_info"

    # 🔥 ADD THIS BLOCK
    if mapped_field == "time":
        return "preferences"

    if mapped_field == "unknown":
        return "preferences"

    return "other"

def extract_fields(form_fields):
    structured_data = []

    for field in form_fields:
        label = field.get("label", "")

        # 🔥 HYBRID MAPPING
        rule_based = map_field(label)

        if rule_based != "unknown":
            mapped_name = rule_based
        else:
            mapped_name = map_field_with_llm(label)

        category = categorize_field(mapped_name)

        structured_field = {
            "original_label": label,
            "mapped_field": mapped_name,
            "category": category,
            "type": field.get("type"),
            "name": field.get("name"),
            "options": field.get("options", None)
        }

        structured_data.append(structured_field)

    return structured_data
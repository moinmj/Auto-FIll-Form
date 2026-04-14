import re


def extract_entities(text):
    data = {}

    lines = [l.strip() for l in text.split("\n") if l.strip()]

    # 🔥 PHONE
    phone_match = re.search(r'\b\d{10}\b', text)
    if phone_match:
        data["phone"] = phone_match.group()

    # 🔥 EMAIL
    email_match = re.search(r'\S+@\S+', text)
    if email_match:
        data["email"] = email_match.group()

    # 🔥 NAME (STRICT RULES)
    for line in lines:

        # ❌ Skip if contains numbers
        if any(char.isdigit() for char in line):
            continue

        # ❌ Skip address keywords
        if any(word in line.lower() for word in [
            "road", "street", "colony", "nagar",
            "sector", "area", "block", "district"
        ]):
            continue

        words = line.split()

        # ✅ Name = 2–3 words, capitalized
        if 1 < len(words) <= 3:
            if all(w[0].isupper() for w in words):
                data["name"] = line
                break

    return data
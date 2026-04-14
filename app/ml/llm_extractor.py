import os
from groq import Groq
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)


def extract_entities_llm(text):
    """
    Use Groq LLM to extract structured data
    """

    prompt = f"""
    You are an AI that extracts structured personal information from OCR text.

    Extract ONLY the following fields:
    - name
    - phone
    - email
    - address

    Return STRICT JSON ONLY.

    Rules:
    If a field is not clearly written in the text, return null.
    DO NOT create fake values.
    1. Name:
    - Usually 2–3 words
    - Contains NO numbers
    - Should NOT contain location words

    2. Address:
    - Contains location indicators like:
        road, street, nagar, colony, area, sector, block, district

    3. VERY IMPORTANT:
    - If a line looks like an address, DO NOT classify it as name
    - If unsure → return null

    Examples:

    Input:
    "Umerabad Zainakote\nPhone: 7298449558"

    Output:
    {{
    "name": null,
    "phone": "7298449558",
    "email": null,
    "address": "Umerabad Zainakote"
    }}

    ---

    Input:
    "John Doe\nEmail: john@gmail.com"

    Output:
    {{
    "name": "John Doe",
    "phone": null,
    "email": "john@gmail.com",
    "address": null
    }}

    ---

    Now extract from:

    {text}
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",   # 🔥 Best for accuracy
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        content = response.choices[0].message.content

        # 🔥 Clean response (sometimes LLM adds text)
        content = content.strip()

        # Extract JSON safely
        start = content.find("{")
        end = content.rfind("}") + 1

        json_str = content[start:end]

        return json.loads(json_str)

    except Exception as e:
        print("LLM Extraction Error:", e)
        return {}
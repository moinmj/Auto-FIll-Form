import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def map_field_with_llm(label):
    prompt = f"""
    You are an intelligent form understanding system.

    Map the following form field label to one of these categories:

    name, phone, email, address, time, comments, preference, unknown

    Only return ONE word from the list.

    Label: "{label}"
    """

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content.strip().lower()

        return result

    except Exception as e:
        print("LLM mapping error:", e)
        return "unknown"
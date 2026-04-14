from app.ml.llm_extractor import extract_entities_llm

text = """
Umerabad Zainakote
Phone: 7298449558
"""

data = extract_entities_llm(text)

print("\n=== LLM OUTPUT ===\n")
print(data)
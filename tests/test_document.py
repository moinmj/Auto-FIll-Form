from app.ml.document_parser import extract_text_from_image, extract_entities

text = extract_text_from_image("test_image.jpg")

data = extract_entities(text)

print("\n=== FINAL EXTRACTED DATA ===\n")
print(data)
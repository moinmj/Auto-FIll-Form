from app.ml.document_parser import extract_text_from_image

text = extract_text_from_image("test_image.jpg")
print("\n=== OCR OUTPUT ===\n")
print(text)
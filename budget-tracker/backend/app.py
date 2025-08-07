from ocr.ocr_processor import extract_text_from_image
from nlp.nlp_parser import parse_receipt_text

if __name__ == "__main__":
    raw_text = extract_text_from_image("data/sample_receipts/test4.webp")
    print("RAW TEXT:\n", raw_text)

    items = parse_receipt_text(raw_text)
    print("\nPARSED ITEMS:")
    for item in items:
        print(item)

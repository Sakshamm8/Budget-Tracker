import spacy
import re

nlp = spacy.load("en_core_web_sm")

def clean_item_name(text):
    # Remove quantity or unit if present (e.g., "1 kg", "2x", "Pack of 3")
    text = re.sub(r"(\b\d+\s*(kg|g|ml|l|pcs|x)?\b)", "", text, flags=re.IGNORECASE)
    doc = nlp(text)

    # Keep only nouns and adjectives (optional)
    filtered_tokens = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN", "ADJ"]]

    return " ".join(filtered_tokens).strip()

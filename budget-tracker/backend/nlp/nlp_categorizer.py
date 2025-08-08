import spacy
import re

nlp = spacy.load("en_core_web_sm")

def clean_item_name(text):
    text = re.sub(r"(\b\d+\s*(kg|g|ml|l|pcs|x|pack|lb|oz)?\b)", "", text, flags=re.IGNORECASE)
    doc = nlp(text)
    tokens = [t.text for t in doc if t.pos_ in ("NOUN","PROPN","ADJ")]
    return " ".join(tokens).strip()

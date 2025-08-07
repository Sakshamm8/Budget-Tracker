from nlp.nlp_categorizer import clean_item_name, predict_category
import re 

def parse_receipt_text(text):
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    items = []

    # Filters
    skip_keywords = ['subtotal', 'total', 'change', 'cash']
    price_pattern = re.compile(r"\$?(\d+\.\d{2})")

    i = 0
    while i < len(lines) - 1:
        name_line = lines[i].lower()
        price_line = lines[i+1].lower()

        # Skip totals or garbage
        if any(keyword in name_line for keyword in skip_keywords):
            i += 1
            continue

        price_match = price_pattern.match(price_line)
        if price_match:
            cleaned_name = clean_item_name(lines[i])
            price = float(price_match.group(1))
            items.append({
                "name": cleaned_name,
                "price": price,
            })
            i += 2  # move past name + price
        else:
            i += 1  # move to next line

    return items

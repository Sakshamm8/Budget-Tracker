import re
from nlp.normalize import normalize_line
from nlp.nlp_categorizer import clean_item_name

# Price pattern allows 1.23, 12.34, 3,45, and picks last price in a line
PRICE_RE = re.compile(r"(\$?\s*\d{1,3}(?:[.,]\d{2}))")

SKIP_WORDS = {"subtotal","total","tax","change","cash","payment","visa","master","thank","balance"}

def _is_skip(line: str) -> bool:
    low = line.lower()
    return any(w in low for w in SKIP_WORDS)

def _to_float(price_str: str) -> float:
    s = price_str.replace("$","").replace(" ", "")
    s = s.replace(",", ".")
    return float(s)

def parse_receipt_text(text: str):
    raw_lines = [ln for ln in text.split("\n")]
    # Normalize & keep non-empty
    lines = [normalize_line(ln) for ln in raw_lines if normalize_line(ln)]

    items = []
    last_name_line = None

    i = 0
    while i < len(lines):
        line = lines[i]

        # Skip obvious non-item sections
        if _is_skip(line) or len(line) < 2:
            i += 1
            continue

        # Try to find price on the same line
        same_line_prices = PRICE_RE.findall(line)
        if same_line_prices:
            price_str = same_line_prices[-1]  # rightmost price on the line
            price = _to_float(price_str)
            name_part = line[: line.rfind(price_str)].strip()
            name = clean_item_name(name_part) or name_part

            # guard against junk like "ee" or short noise
            if len(name) >= 3 and not _is_skip(name):
                items.append({"name": name, "price": price})
                last_name_line = None
            i += 1
            continue

        # If no price on this line, check if the *next* line is just a price
        if i + 1 < len(lines):
            nxt = lines[i+1]
            if PRICE_RE.fullmatch(nxt) or PRICE_RE.match(nxt):
                # treat current as name, next as price
                if not _is_skip(line):
                    name = clean_item_name(line) or line
                    price = _to_float(PRICE_RE.search(nxt).group(1))
                    if len(name) >= 3 and not _is_skip(name):
                        items.append({"name": name, "price": price})
                        i += 2
                        continue

        # Fallthrough: remember this as potential name, move on
        last_name_line = line
        i += 1

    # Final sweep: drop any accidental totals sneaking in
    items = [it for it in items if not _is_skip(it["name"])]

    return items

import re
import unicodedata

_DOT_LEADER = re.compile(r"[.\-—–]{2,}")  # long runs of dots/dashes
_WEIRD_WS   = re.compile(r"\s+")

def _fix_lookalikes(s: str) -> str:
    # Normalize unicode & common OCR glyph confusions near digits
    s = unicodedata.normalize("NFKC", s)
    # Replace fancy quotes/dashes
    s = s.replace("’", "'").replace("“", '"').replace("”", '"').replace("–", "-").replace("—", "-")
    # Common digit look-alikes (only inside number-ish chunks)
    # Replace hyphen between digits with dot for cents: 6-38 -> 6.38
    s = re.sub(r"(?<=\d)[\-](?=\d{2}\b)", ".", s)

    # Fix O/0, I/l -> 1, S/§ -> 5 when inside numbers
    def repl_num_lookalikes(m):
        chunk = list(m.group(0))
        for i, ch in enumerate(chunk):
            if ch in ("O", "o"):
                chunk[i] = "0"
            elif ch in ("I", "l", "¡"):
                chunk[i] = "1"
            elif ch in ("S", "§"):
                chunk[i] = "5"
            elif ch == "B":
                chunk[i] = "8"
        return "".join(chunk)

    s = re.sub(r"(?<!\w)[A-Za-z§BIlO0S5]{1,}\d+[A-Za-z§BIlO0S5\d]*", repl_num_lookalikes, s)
    s = re.sub(r"\d+[A-Za-z§BIlO0S5]+", repl_num_lookalikes, s)

    # Remove dot leaders / long dash runs that split name & price
    s = _DOT_LEADER.sub(" ", s)
    # Collapse whitespace
    s = _WEIRD_WS.sub(" ", s).strip()
    return s

def normalize_line(line: str) -> str:
    return _fix_lookalikes(line)

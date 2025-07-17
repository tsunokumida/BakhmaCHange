def is_valid_amount(text: str) -> bool:
    try:
        value = float(text.strip())
        return value > 0
    except ValueError:
        return False

def is_valid_currency_pair(pair: str) -> bool:
    if '/' not in pair:
        return False
    parts = pair.upper().split('/')
    return len(parts) == 2 and all(len(p) == 3 and p.isalpha() for p in parts)

import re


def parse_scanned_receipt(text):
    if not text:
        return {"name": "", "qty": 1, "price": 0.0, "delivery": 0.0}

    cleaned = text.replace("\r", " ").replace("\n", " ")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    name = ""
    for line in lines:
        if len(line) > 2 and not re.search(r"\d", line):
            name = line
            break
    if not name:
        name = "Receipt Item"

    qty = 1
    qty_match = re.search(r"(?:qty|quantity|pcs|pieces|units?)\s*[:=]?\s*(\d+)", cleaned, re.I)
    if qty_match:
        qty = int(qty_match.group(1))

    price = 0.0
    amount_match = re.search(r"(?:total|amount|payable|grand total|total due|net|php)\s*[:=]?\s*php\s*([0-9,]+(?:\.\d+)?)", cleaned, re.I)
    if amount_match:
        price = float(amount_match.group(1).replace(",", ""))
    else:
        numeric_matches = [float(match.replace(",", "")) for match in re.findall(r"(?:php\s*)?(\d+(?:,\d{3})*(?:\.\d+)?)", cleaned)]
        if numeric_matches:
            price = max(numeric_matches)

    if qty > 0 and price > 0 and price < 1000:
        price = price / qty

    delivery = 0.0
    delivery_match = re.search(r"(?:delivery|shipping|freight|transport)\s*[:=]?\s*php\s*([0-9,]+(?:\.\d+)?)", cleaned, re.I)
    if delivery_match:
        delivery = float(delivery_match.group(1).replace(",", ""))

    return {"name": name.strip(), "qty": qty, "price": float(price), "delivery": float(delivery)}

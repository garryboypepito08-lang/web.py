def is_month_closed(closes, month):
    close = closes.get(month, {}) if isinstance(closes, dict) else {}
    return bool(close.get("closed"))


def close_month(closes, month, note="", closed_by=""):
    if not isinstance(closes, dict):
        closes = {}
    current = closes.get(month, {})
    current.update({
        "closed": True,
        "closed_at": __import__("datetime").datetime.now().isoformat(),
        "closed_by": closed_by or "System",
        "note": note,
    })
    closes[month] = current
    return closes


def month_summary(records):
    if not records:
        return {"spent": 0.0, "labor": 0.0, "materials": 0.0, "total": 0.0, "remaining": 0.0}
    if isinstance(records, dict):
        records = records.get("records", []) + records.get("labor_records", []) + records.get("payroll_expenses", [])
    spent = 0.0
    labor = 0.0
    materials = 0.0
    for item in records:
        if not isinstance(item, dict):
            continue
        if item.get("type") in {"material", "expense"}:
            materials += float(item.get("amount", 0) or 0)
        if item.get("net") is not None:
            labor += float(item.get("net", 0) or 0)
        if item.get("price") is not None and item.get("type") == "payroll_expense":
            spent += float(item.get("price", 0) or 0)
        if item.get("amount") is not None and item.get("type") in {"material", "expense"}:
            spent += float(item.get("amount", 0) or 0)
    total = materials + labor + spent
    return {"spent": spent, "labor": labor, "materials": materials, "total": total, "remaining": max(0.0, total - materials)}

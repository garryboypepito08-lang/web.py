FULL_DAY_RATES = {
    "Labor": 500.0,
    "Carpenter": 650.0,
    "Mason": 700.0,
    "Painter": 600.0,
    "Electrician": 700.0,
    "Plumber": 650.0,
    "Helper": 450.0,
}

TIER_TABLE = {
    "Labor": {"full": 1.0, "partial": 0.5},
    "Carpenter": {"full": 1.0, "partial": 0.5},
    "Mason": {"full": 1.0, "partial": 0.5},
    "Painter": {"full": 1.0, "partial": 0.5},
    "Electrician": {"full": 1.0, "partial": 0.5},
    "Plumber": {"full": 1.0, "partial": 0.5},
    "Helper": {"full": 1.0, "partial": 0.5},
}


def get_partial_rate(days, role):
    if days <= 0:
        return 0.0
    rate = FULL_DAY_RATES.get(role, FULL_DAY_RATES["Labor"])
    return rate * float(days)


def calculate_labor_pay(days, role):
    rate = FULL_DAY_RATES.get(role, FULL_DAY_RATES["Labor"])
    total_days = float(days or 0.0)
    gross_pay = rate * total_days
    full_pay = gross_pay
    partial_pay = rate * min(total_days, 1.0)
    return gross_pay, full_pay, partial_pay

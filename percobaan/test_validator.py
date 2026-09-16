from validator import validate_records, validate_unique_ids

# --- 15.2 Uji validasi normal ---
print("=== Uji validasi normal ===")

records = [
    {
        "id": 1,
        "customer": "customer_001",
        "amount": 10000,
        "updated_at": "2026-09-01T08:10:00+00:00",
    }
]

validate_records(records)
print("Validation passed")

# --- 15.3 Uji error: field hilang ---
print()
print("=== Uji error: field 'amount' hilang ===")

bad_records = [
    {
        "id": 1,
        "customer": "customer_001",
        "updated_at": "2026-09-01",
    }
]

try:
    validate_records(bad_records)
except ValueError as error:
    print(f"ValueError: {error}")   # Target: ValueError: Missing fields: ['amount']

# --- 15.4 Uji validasi duplikasi ---
print()
print("=== Uji validasi duplikasi id ===")

duplicate_records = [
    {"id": 1, "customer": "A", "amount": 100, "updated_at": "2026-09-01"},
    {"id": 1, "customer": "B", "amount": 200, "updated_at": "2026-09-02"},
]

try:
    validate_unique_ids(duplicate_records)
except ValueError as error:
    print(f"ValueError: {error}")   # Target: ValueError: Duplicate id detected

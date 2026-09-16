from storage import save_records, read_records

# --- 16.3 Menulis Parquet ---
print("=== Menulis Parquet ===")

records = [
    {
        "id": 1,
        "customer": "Andi",
        "amount": 10000,
        "updated_at": "2026-09-01T08:00:00+00:00",
    },
    {
        "id": 2,
        "customer": "Budi",
        "amount": 20000,
        "updated_at": "2026-09-01T09:00:00+00:00",
    },
]

output_file = "data/transactions.parquet"

save_records(records, output_file)
print("Parquet saved")

# --- 16.4 Membaca Kembali ---
print()
print("=== Membaca Kembali ===")

df = read_records(output_file)
print(df)

# --- 16.5 Validasi Output ---
print()
print("=== Validasi Output ===")

import pandas as pd

input_df = pd.DataFrame(records)

assert len(df) == len(input_df)
assert list(df.columns) == list(input_df.columns)

print("Parquet validation passed")

# --- 16.6 Eksperimen Compression ---
print()
print("=== Eksperimen Compression (snappy vs gzip) ===")

path_snappy = Path_ = "data/transactions_snappy.parquet"
path_gzip = "data/transactions_gzip.parquet"

input_df.to_parquet(path_snappy, index=False, compression="snappy")
input_df.to_parquet(path_gzip, index=False, compression="gzip")

import os

size_snappy = os.path.getsize(path_snappy)
size_gzip = os.path.getsize(path_gzip)

print(f"Ukuran snappy: {size_snappy} bytes")
print(f"Ukuran gzip:   {size_gzip} bytes")
print("(Untuk dataset kecil seperti ini perbedaan bisa tidak signifikan / gzip bisa lebih besar karena overhead header)")

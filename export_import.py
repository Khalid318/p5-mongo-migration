# Exporte la collection patients en JSON et CSV (dossier data/)

import os
import json, csv
from pymongo import MongoClient

DB_NAME = "healthcare_db"
COLL_NAME = "patients"
JSON_OUT = "data/patients_export.json"
CSV_OUT  = "data/patients_export.csv"

# Champs
FIELDS = [
    "Name", "Age", "Gender", "Medical Condition",
    "Hospital", "Doctor", "Insurance Provider",
    "Date of Admission", "Discharge Date", "Billing Amount"
]

# Connexion Mongo
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
client.admin.command("ping")
col = client[DB_NAME][COLL_NAME]

# export JSON (sans _id)
docs = list(col.find({}, {"_id": 0}))
with open(JSON_OUT, "w", encoding="utf-8") as f:
    json.dump(docs, f, ensure_ascii=False, default=str)
print(f"JSON exporté -> {JSON_OUT} ({len(docs)} documents)")

# export CSV
with open(CSV_OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    w.writeheader()
    n = 0
    for d in col.find({}, {k: 1 for k in FIELDS}):
        # dates -> string pour le CSV
        for k in ("Date of Admission", "Discharge Date"):
            if d.get(k) is not None:
                d[k] = str(d[k])
        w.writerow({k: d.get(k) for k in FIELDS})
        n += 1
print(f"CSV exporté  -> {CSV_OUT} ({n} lignes)")

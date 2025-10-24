# lire le CSV et l'insérer dans MongoDB (healthcare_db.patients)
import pandas as pd
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import OperationFailure

CSV_PATH = "data/healthcare_dataset.csv"  # ou _cleaned.csv si tu préfères
DB_NAME = "healthcare_db"
COLL_NAME = "patients"

def main():
    # connexion Mongo local
    client = MongoClient("mongodb://localhost:27017")
    col = client[DB_NAME][COLL_NAME]

    # lire le CSV
    df = pd.read_csv(CSV_PATH)

    # typer des colonnes
    df["Age"] = pd.to_numeric(df["Age"], errors="coerce").astype("Int64")
    df["Billing Amount"] = pd.to_numeric(df["Billing Amount"], errors="coerce").round(2)
    df["Date of Admission"] = pd.to_datetime(df["Date of Admission"], errors="coerce")
    df["Discharge Date"] = pd.to_datetime(df["Discharge Date"], errors="coerce")

    # Name en Title Case (+ strip)
    df["Name"] = df["Name"].astype(str).str.strip().str.title()

    # Gestion des doublons
    dedup_cols = [
        "Name",
        "Date of Admission",
        "Doctor",
        "Hospital",
        "Billing Amount",
        "Insurance Provider",
        "Discharge Date",
    ]
    before = len(df)
    df = df.drop_duplicates(subset=dedup_cols, keep="first")
    after = len(df)

    # gestion des NaN
    df = df.where(pd.notnull(df), None)

    # empêcher les doublons en cas de relance
    col.delete_many({})

    # insertion en base
    records = df.to_dict(orient="records")
    col.insert_many(records)
    print(f"✅ Import OK : {len(records)} documents (doublons retirés : {before - after})")

    # index usuels
    col.create_index([("Name", ASCENDING)])
    col.create_index([("Doctor", ASCENDING), ("Date of Admission", DESCENDING)])
    col.create_index([("Date of Admission", DESCENDING)])

    # index UNIQUE pour protéger contre les doublons futurs
    try:
        col.create_index(
            [(f, ASCENDING) for f in dedup_cols],
            unique=True,
            name="uniq_patient_encounter"
        )
        print("✅ Index unique créé : uniq_patient_encounter")
    except OperationFailure as e:
        # l'index existe déjà ou des doublons empêchent sa création
        print(f"ℹ️ Index unique non créé : {e}")

    print("✅ Index standards : Name, Doctor+Date, Date of Admission")

if __name__ == "__main__":
    main()


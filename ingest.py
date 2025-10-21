
# lire le CSV nettoyé et l'insérer dans MongoDB (healthcare_db.patients)
import pandas as pd
from pymongo import MongoClient, ASCENDING, DESCENDING

CSV_PATH = "data/healthcare_dataset_cleaned.csv"
DB_NAME = "healthcare_db"
COLL_NAME = "patients"

def main():
    #  connexion Mongo local
    client = MongoClient("mongodb://localhost:27017")
    col = client[DB_NAME][COLL_NAME]


    # lire le CSV
    df = pd.read_csv(CSV_PATH)

    # typer des colonnes
    df["Age"] = pd.to_numeric(df["Age"], errors="coerce").astype("Int64")
    df["Billing Amount"] = pd.to_numeric(df["Billing Amount"], errors="coerce")
    df["Date of Admission"] = pd.to_datetime(df["Date of Admission"], errors="coerce")
    df["Discharge Date"] = pd.to_datetime(df["Discharge Date"], errors="coerce")

    # gestion des NaN
    df = df.where(pd.notnull(df), None)


    col.delete_many({})  # empêcher les doublons en cas de relance

    # insertion en base
    records = df.to_dict(orient="records")
    col.insert_many(records)
    print(f"Import OK : {len(records)} documents")



    # index
    col.create_index([("Name", ASCENDING)])
    col.create_index([("Doctor", ASCENDING), ("Date of Admission", DESCENDING)])
    col.create_index([("Date of Admission", DESCENDING)])
    print("✅ Index créés : Name, Doctor+Date, Date of Admission")

if __name__ == "__main__":
    main()

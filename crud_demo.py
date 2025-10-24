
# Démonstration CRUD sur la collection patients (Create, Read, Update, Delete)

from datetime import datetime
from pymongo import MongoClient

DB_NAME = "healthcare_db"
COLL_NAME = "patients"
TEST_NAME = "Akira Toriyama"


def get_collection():
    client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=2000)
    client.admin.command("ping")
    return client[DB_NAME][COLL_NAME]


def create_doc(col):
    print("\n========== CREATE ==========\n")

    # nettoyage préalable si un document test existe déjà
    col.delete_many({"Name": TEST_NAME})

    doc = {
        "Name": TEST_NAME,
        "Age": 68,
        "Gender": "Male",
        "Medical Condition": "Inspiration Overflow",
        "Hospital": "Capsule Corp Medical Center",
        "Doctor": "Dr. Brief",
        "Date of Admission": datetime(2025, 3, 1),
        "Discharge Date": None,
        "Billing Amount": 25000.00,
        "Insurance Provider": "Shenron Health",
    }
    res = col.insert_one(doc)
    print(f"Document inséré avec _id : {res.inserted_id}")


def read_doc(col):
    print("\n=========== READ ===========\n")
    doc = col.find_one(
        {"Name": TEST_NAME},
        {"_id": 0, "Name": 1, "Hospital": 1, "Doctor": 1, "Billing Amount": 1, "Date of Admission": 1},
    )
    if doc:
        print("Document trouvé :")
        print(doc)
    else:
        print("Aucun document trouvé pour ce patient.")


def update_doc(col):
    print("\n========== UPDATE ==========\n")
    res = col.update_one(
        {"Name": TEST_NAME},
        {"$set": {"Billing Amount": 27500.00}}
    )
    print(f"Documents modifiés : {res.modified_count}")

    # Relecture après mise à jour
    updated = col.find_one({"Name": TEST_NAME}, {"_id": 0, "Name": 1, "Billing Amount": 1})
    print("Après mise à jour :")
    print(updated if updated else "Introuvable après update.")


def delete_doc(col):
    print("\n========== DELETE ==========\n")
    res = col.delete_one({"Name": TEST_NAME})
    print(f"Documents supprimés : {res.deleted_count}")

    exists = col.find_one({"Name": TEST_NAME})
    print("Présence après suppression :", "Oui" if exists else "Non")


def main():
    print("\n===== Démonstration CRUD (patients) =====")
    try:
        col = get_collection()
    except Exception as e:
        print("Erreur de connexion à MongoDB. Vérifiez que le service est actif (docker ps).")
        print(f"Détail : {e}")
        return

    create_doc(col)
    read_doc(col)
    update_doc(col)
    delete_doc(col)

    print("\nTerminé.\n")


if __name__ == "__main__":
    main()

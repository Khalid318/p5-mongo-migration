
# Tests : ingestion + CRUD + export

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import os
import subprocess
from pymongo import MongoClient

DB_NAME = "healthcare_db"
COLL_NAME = "patients"


def run_script(script):
    """Exécute un script Python en sous-processus."""
    result = subprocess.run(["python", script], capture_output=True, text=True)
    assert result.returncode == 0, f"Erreur dans {script} : {result.stderr}"


def test_ingestion():
    """Test ingestion MongoDB."""
    run_script("ingest.py")
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
    client = MongoClient(MONGO_URI)
    col = client[DB_NAME][COLL_NAME]
    assert col.count_documents({}) > 0, "La base Mongo est vide après ingestion."


def test_crud():
    """Test CRUD sur patient fictif."""
    run_script("crud_demo.py")
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
    client = MongoClient(MONGO_URI)
    col = client[DB_NAME][COLL_NAME]
    assert col.find_one({"Name": "Akira Toriyama"}) is None, "CRUD : le document test n'a pas été supprimé."


def test_export():
    """Test export JSON/CSV."""
    run_script("export_import.py")
    assert os.path.exists("data/patients_export.json"), "Export JSON manquant."
    assert os.path.exists("data/patients_export.csv"), "Export CSV manquant."

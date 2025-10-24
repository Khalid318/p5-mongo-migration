# Migration de données médicales vers MongoDB – Partie 1

Ce projet consiste à migrer un fichier CSV contenant des données médicales vers une base NoSQL MongoDB. L’objectif est de réaliser une ingestion propre et fiable des données, tout en découvrant les bases de MongoDB et de la manipulation de données en Python.

---

## Objectifs de cette première partie

- Lire et analyser un fichier CSV  
- Nettoyer et typer les données  
- Supprimer les doublons  
- Charger les données propres dans MongoDB  
- Créer des index pour améliorer les performances  
- Réaliser des opérations CRUD de base  
- Exporter les données JSON / CSV  
- Automatiser des tests avec `pytest`

---

## Technologies utilisées

| Outil / Lib | Rôle |
|--------------|------|
| Python | Scripts d’ingestion et manipulation |
| Pandas | Nettoyage des données |
| PyMongo | Connexion MongoDB |
| MongoDB | Base NoSQL |
| Pytest | Tests automatisés |
| Docker (Partie 2) | Conteneurisation |

---


## Installation

### 1. Cloner le projet
```bash
git clone https://github.com/Khalid318/p5-mongo-migration.git
cd p5-mongo-migration
```

### 2. Créer l'environnement Python
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### Lancer MongoDB (local avec Docker)
```bash
docker run -d --name mongo -p 27017:27017 mongo:latest
```
___

### Scripts disponibles
| Script                   | Description                                            |
| ------------------------ | ------------------------------------------------------ |
| `ingest.py`              | Ingestion CSV → MongoDB (typage, déduplication, index) |
| `crud_demo.py`           | Démonstration CRUD                                     |
| `export_import.py`       | Export JSON et CSV                                     |
| `tests/test_pipeline.py` | Tests automatisés (pytest)                             |

___

### Commandes utiles

##### Migration CSV → MongoDB
```bash
python ingest.py
```

##### CRUD test
```bash
python crud_demo.py
```

##### Export JSON/CSV
```bash
python export_import.py
```

##### Lancer les tests automatisés
```bash
./.venv/bin/python -m pytest -q
```

___

### Qualité des données

Avant insertion dans MongoDB :

- Conversion des types (int, float, datetime)

- Formatage (Name.title())

- Suppression des doublons

- Remplacement des NaN par None

- Index MongoDB ajoutés pour optimiser les requêtes

___

### Structure du projet

```text
p5-mongo-migration/
├── data/
│   └── healthcare_dataset.csv
├── ingest.py
├── crud_demo.py
├── export_import.py
├── tests/
│   └── test_pipeline.py
├── requirements.txt
└── README.md
```



## Suite

Partie 2 : Dockerisation du projet (MongoDB + scripts).


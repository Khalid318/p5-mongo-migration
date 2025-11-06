# Projet Migration de données vers MongoDB

Projet de formation où je migre un CSV de données médicales (55 500 lignes) vers MongoDB. L'idée c'est de faire un pipeline propre qui nettoie les données, supprime les doublons, et charge tout ça dans une base MongoDB.

Tout est dockerisé pour que ça tourne sur n'importe quelle machine sans galère d'installation.

## Ce que fait le projet

- Lit un gros fichier CSV (données de santé)
- Nettoie les données avec Pandas (typage, suppression des doublons...)
- Charge tout dans MongoDB (50 000 documents au final)
- Crée des index pour que les recherches soient rapides
- Fait des opérations CRUD de base
- Exporte les données en JSON/CSV
- Tests automatiques avec pytest
- MongoDB sécurisé avec authentification

## Technologies utilisées

- **Python 3.11** - Pour les scripts
- **Pandas** - Pour nettoyer les données
- **PyMongo** - Pour parler à MongoDB
- **MongoDB 7.0** - La base NoSQL
- **Pytest** - Tests automatiques
- **Docker** - Pour tout mettre dans des conteneurs

## Installation

### Ce dont tu as besoin

- Docker et Docker Compose installés
- Git
- Un peu d'espace disque (~2 Go)

Pour vérifier que Docker est bien installé :
```bash
docker --version
docker compose version
```

### Lancer le projet

**1. Clone le repo**
```bash
git clone https://github.com/Khalid318/p5-mongo-migration.git
cd p5-mongo-migration
```

**2. Configure les mots de passe**

Copie le fichier template :
```bash
cp .env.example .env
```

Puis édite `.env` et change les mots de passe :
```bash
nano .env
```

Mets tes propres mots de passe ici :
```
MONGO_ROOT_USER=admin
MONGO_ROOT_PASSWORD=ton_mot_de_passe_ici

MONGO_APP_USER=healthcare_user
MONGO_APP_PASSWORD=ton_autre_mot_de_passe

MONGO_DATABASE=healthcare_db
```

**3. Démarre MongoDB**
```bash
docker compose up -d mongo
```

Attends quelques secondes (~10-15 sec) que MongoDB soit prêt.

**4. Vérifie que c'est bon**
```bash
docker compose ps
```

Tu devrais voir `p5_mongo` avec le statut `healthy`.

**5. Construis l'application**
```bash
docker compose build app
```

**6. Lance l'ingestion**
```bash
docker compose run --rm app python ingest.py
```

Si tout va bien, tu devrais voir :
```
Import OK : 50000 documents (doublons retirés : 5500)
Index unique créé : uniq_patient_encounter
Index standards : Name, Doctor+Date, Date of Admission
```

## Utilisation

### Les scripts disponibles

**Ingestion des données**
```bash
docker compose run --rm app python ingest.py
```
Lit le CSV, nettoie, supprime les doublons, charge dans MongoDB.

**Démo CRUD**
```bash
docker compose run --rm app python crud_demo.py
```
Montre comment faire du Create, Read, Update, Delete sur MongoDB.

**Export des données**
```bash
docker compose run --rm app python export_import.py
```
Exporte les données en JSON et CSV.

**Tests**
```bash
docker compose run --rm app pytest tests/ -v
```
Lance les 3 tests automatiques. Normalement ils doivent tous passer.

### Vérifier les données dans MongoDB

Pour te connecter à MongoDB et voir ce qu'il y a dedans :
```bash
docker exec -it p5_mongo mongosh -u healthcare_user -p <TON_PASSWORD> --authenticationDatabase healthcare_db
```

Une fois connecté, tu peux faire :
```javascript
use healthcare_db
db.patients.countDocuments()  // Doit afficher 50000
db.patients.findOne()          // Voir un exemple de document
db.patients.getIndexes()       // Voir les index créés
exit
```

## Tests

Pour lancer les tests :
```bash
docker compose run --rm app pytest tests/ -v
```

Tu devrais voir :
```
tests/test_pipeline.py::test_ingestion PASSED
tests/test_pipeline.py::test_crud PASSED
tests/test_pipeline.py::test_export PASSED

3 passed
```

Si un test plante, regarde les logs pour voir ce qui s'est passé.

## Architecture Docker

Le projet utilise Docker Compose pour orchestrer 2 conteneurs :

**MongoDB** : La base de données
- Port 27017
- Les données sont persistées dans un volume Docker (elles restent même si tu arrêtes le conteneur)
- Authentification activée

**App Python** : Les scripts
- Lance les scripts d'ingestion, CRUD, export
- Lance les tests

### Commandes Docker utiles

```bash
# Démarrer MongoDB
docker compose up -d mongo

# Voir ce qui tourne
docker compose ps

# Voir les logs
docker compose logs -f mongo

# Arrêter tout
docker compose down

# Arrêter et supprimer les données (attention !)
docker compose down -v

# Reconstruire l'app (si tu changes des trucs)
docker compose build app
```

## Sécurité

J'ai configuré MongoDB avec authentification obligatoire (pas de connexion anonyme).

Il y a 2 utilisateurs :

**admin** (root)
- Peut tout faire sur MongoDB
- Utilisé uniquement pour l'administration
- Ne JAMAIS l'utiliser dans l'application

**healthcare_user** (utilisateur application)
- Peut juste lire/écrire dans la base healthcare_db
- Peut créer des index
- C'est celui utilisé par les scripts Python

Pourquoi 2 utilisateurs ? Principe du moindre privilège. Si quelqu'un vole les credentials de l'app, il ne peut pas tout détruire, juste accéder à une base.

Les mots de passe sont dans le fichier `.env` qui est dans `.gitignore` (donc jamais envoyé sur GitHub).

## Comment ça marche

Le pipeline fait ces étapes automatiquement :

1. **Lecture du CSV** (55 500 lignes)
2. **Nettoyage avec Pandas**
   - Conversion des types (dates, nombres, etc.)
   - Formatage des noms (majuscules aux bons endroits)
   - Remplacement des valeurs manquantes
3. **Suppression des doublons**
   - Critère : même nom + même date d'admission
   - 5 500 doublons supprimés (10% des données)
4. **Chargement dans MongoDB**
   - 50 000 documents insérés
5. **Création des index**
   - Index unique pour éviter les futurs doublons
   - Index sur Name, Date, Doctor pour les recherches rapides
6. **Validation**
   - 3 tests automatiques vérifient que tout est OK

## Résultats

- 55 500 lignes au départ
- 5 500 doublons supprimés (10%)
- 50 000 documents dans MongoDB
- 5 index créés (1 unique + 4 standards)
- Temps d'ingestion : environ 5 secondes
- Recherche par nom : moins de 1 ms avec les index
- 3 tests qui passent

## Structure du projet

```
p5-mongo-migration/
├── data/
│   └── healthcare_dataset.csv      # Les données
├── tests/
│   └── test_pipeline.py            # Tests
├── mongo-init/
│   └── 01-create-app-user.js       # Script pour créer le user MongoDB
├── ingest.py                       # Script principal d'ingestion
├── crud_demo.py                    # Démo CRUD
├── export_import.py                # Export des données
├── requirements.txt                # Dépendances Python
├── Dockerfile                      # Image Docker
├── docker-compose.yml              # Orchestration
├── .dockerignore
├── .gitignore
├── .env.example                    # Template pour les mots de passe
└── README.md
```

## Problèmes courants

**Port 27017 déjà utilisé**

Si tu as MongoDB qui tourne déjà en local :
```bash
sudo lsof -i :27017
sudo systemctl stop mongod  # Linux
```

**MongoDB ne démarre pas**

Regarde les logs :
```bash
docker compose logs mongo
```

Si ça prend trop de temps, redémarre :
```bash
docker compose down
docker compose up -d mongo
```

**Erreur d'authentification**

Vérifie que tu as bien configuré `.env` avec tes mots de passe.

Si besoin, recrée les utilisateurs :
```bash
docker compose down -v  # Supprime tout
docker compose up -d mongo  # Recrée les users
```

**Les tests plantent**

Vérifie que MongoDB est bien démarré et "healthy" :
```bash
docker compose ps
```

## Améliorations possibles

- Ajouter un dashboard pour visualiser les données
- Déployer sur AWS (j'ai regardé ECS + DocumentDB)
- Ajouter plus de tests

## Ressources

- [MongoDB Docs](https://www.mongodb.com/docs/)
- [PyMongo](https://pymongo.readthedocs.io/)
- [Docker](https://docs.docker.com/)

---

Projet réalisé dans le cadre d'une formation Data Engineering.

// ==========================================
// Script d'initialisation MongoDB
// ==========================================
// Exécuté automatiquement au premier démarrage de MongoDB
// Objectif : Créer l'utilisateur applicatif avec droits limités

print('=== Début création utilisateur applicatif ===');

// Se connecter à la base de l'application
db = db.getSiblingDB(process.env.MONGO_INITDB_DATABASE || 'healthcare_db');

// Créer l'utilisateur applicatif
db.createUser({
  user: process.env.MONGO_APP_USER || 'healthcare_user',
  pwd: process.env.MONGO_APP_PASSWORD || 'healthcare_pass',
  roles: [
    {
      // Rôle 1 : readWrite

      role: 'readWrite',
      db: process.env.MONGO_INITDB_DATABASE || 'healthcare_db'
    },
    {
      // Rôle 2 : dbAdmin

      role: 'dbAdmin',
      db: process.env.MONGO_INITDB_DATABASE || 'healthcare_db'
    }
  ]
});

print('✓ Utilisateur applicatif créé avec succès');
print('  - User: ' + (process.env.MONGO_APP_USER || 'healthcare_user'));
print('  - Roles: readWrite + dbAdmin sur ' + (process.env.MONGO_INITDB_DATABASE || 'healthcare_db'));
print('=== Fin création utilisateur ===');

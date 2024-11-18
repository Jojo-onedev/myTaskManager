import sqlite3

# Connexion à la base de données (un fichier nommé tasks.db sera créé)
connection = sqlite3.connect("tasks.db")
cursor = connection.cursor()

# Création d'une table pour les tâches
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    done BOOLEAN NOT NULL DEFAULT 0
)
""")

# Sauvegarde et fermeture de la connexion
connection.commit()
# connection.close()

print("Base de données initialisée !")

# Exécuter la requête pour afficher toutes les tâches
cursor.execute("SELECT * FROM tasks;")
tasks = cursor.fetchall()

# Afficher les tâches
for task in tasks:
    print(task)

connection.close()
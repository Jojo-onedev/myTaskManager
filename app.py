from flask import Flask, flash, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Une liste en mémoire pour stocker les tâches
tasks = []


def get_db_connection():
    connection = sqlite3.connect("tasks.db")
    connection.row_factory = sqlite3.Row  # Permet d'accéder aux colonnes par nom
    return connection


@app.route("/")
def home():
    connection = get_db_connection()
    tasks = connection.execute("SELECT * FROM tasks").fetchall()
    connection.close()
    return render_template("index.html", tasks=tasks)



@app.route("/add", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        task_name = request.form["task_name"]
        connection = get_db_connection()
        connection.execute("INSERT INTO tasks (name, done) VALUES (?, ?)", (task_name, 0))
        connection.commit()
        connection.close()
        return redirect("/")

    # Affiche le formulaire d'ajout pour la méthode GET
    return render_template("add.html")



@app.route("/done/<int:task_id>")
def mark_done(task_id):
    connection = get_db_connection()
    connection.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
    print(f"Task {task_id} marked as done.")  # Ajoute cette ligne pour vérifier si la fonction est bien exécutée
    connection.commit()
    connection.close()
    return redirect("/")


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    connection = get_db_connection()
    connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    print(f"Task {task_id} deleted.")  # Ajoute cette ligne pour vérifier si la fonction est bien exécutée
    connection.commit()
    connection.close()
    flash("Tâche supprimée avec succès.")
    return redirect("/")


@app.route("/edit/<int:task_id>")
def edit_task(task_id):
    # Récupérer la tâche à partir de la base de données
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    conn.close()

    if not task:
        return "Tâche introuvable", 404
    return render_template("edit.html", task={"id": task[0], "name": task[1]})

@app.route("/edit/<int:task_id>", methods=["POST"])
def update_task(task_id):
    new_name = request.form['name']

    # Mettre à jour la base de données
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET name = ? WHERE id = ?", (new_name, task_id))
    conn.commit()
    conn.close()

    print("La tâche a été mise à jour avec succès.")
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

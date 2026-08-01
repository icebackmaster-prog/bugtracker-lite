from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Create database
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS bugs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        priority TEXT NOT NULL,
        status TEXT DEFAULT 'Open'
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    bugs = conn.execute("SELECT * FROM bugs ORDER BY id DESC").fetchall()
    conn.close()

    return render_template("dashboard.html", bugs=bugs)

@app.route("/submit", methods=["GET", "POST"])
def submit_bug():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        priority = request.form["priority"]

        conn = sqlite3.connect("database.db")
        conn.execute(
            "INSERT INTO bugs (title, description, priority) VALUES (?, ?, ?)",
            (title, description, priority)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("home"))

    return render_template("submit_bug.html")

if __name__ == "__main__":
    app.run(debug=True)

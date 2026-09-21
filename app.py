from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

# DATABÁZE

spojeni = sqlite3.connect('databaze.db')
kurzor = spojeni.cursor()

kurzor.execute('''
    CREATE TABLE IF NOT EXISTS prispevky (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        jazyk TEXT,
        text TEXT
    )
''')

kurzor.execute('''
    CREATE TABLE IF NOT EXISTS uzivatele (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

spojeni.commit()
spojeni.close()
app = Flask(__name__)
app.config['SECRET_KEY'] = '123'

def get_db_connection():
    conn = sqlite3.connect('databaze.db')
    conn.row_factory = sqlite3.Row  
    return conn

USERNAME = "admin"
PASSWORD = "heslo"

#prispevky = {} # <----- Udělala jsem z toho slovník protože se mi příspěvky ukazovali ve všech jazycích

# SEZNAM JAZYKŮ

@app.route("/home")
def home():

    temata = ["Python", "Java Script", "Type Script", "C#", "C++"]

    return render_template("index.html", temata=temata)

# ODESLÁNÍ/SMAZÁNÍ PŘÍSPĚVKU (PŘES SQLITE DATABÁZI)

@app.route("/tema/<jazyk>", methods=["GET", "POST"])
def ukaz_tema(jazyk):
    conn = get_db_connection()

    if request.method == "POST":
        napsany_text = request.form.get("prispevek")
        smazat_id = request.form.get("smazani_id")
        komentovat = request.form.get("komentar_id")

        if napsany_text:
            conn.execute('INSERT INTO prispevky (jazyk, text) VALUES (?, ?)', (jazyk, napsany_text))
            conn.commit()
            print(f"Uživatel uložil do DB pro {jazyk}: {napsany_text}")

        elif smazat_id:
            conn.execute('DELETE FROM prispevky WHERE id = ?', (smazat_id,))
            conn.commit()

        elif komentovat:
            conn.execute('INSERT INTO PRISPEVKY (jazyk, text) VALUES (?, ?)', (jazyk, komentovat))
            conn.commit()

    nactene_prispevky = conn.execute('SELECT * FROM prispevky WHERE jazyk = ?', (jazyk,)).fetchall()
    conn.close()

    return render_template("post.html", nazev=jazyk, prispevky=nactene_prispevky)

# REGISTRACE

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return render_template("register.html", error="Vyplň jméno i heslo >:((")

        conn = get_db_connection()

        existujici = conn.execute('SELECT * FROM uzivatele WHERE username = ?', (username,)).fetchone()

        if existujici:
            conn.close()
            return render_template("register.html", error="To je už zabraný O.O")

        hashed_password = generate_password_hash(password)

        conn.execute('INSERT INTO uzivatele (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")


# CESTY

@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)





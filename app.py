from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'

USERNAME = "admin"
PASSWORD = "heslo"

prispevky = {} # <----- Udělala jsem z toho slovník protože se mi příspěvky ukazovali ve všech jazycích

# SEZNAM JAZYKŮ

@app.route("/home")
def home():

    temata = ["Python", "Java Script", "Type Script", "C#", "C++"]

    return render_template("index.html", temata=temata)

# ODESLÁNÍ/SMAZÁNÍ PŘÍSPĚVKU

@app.route("/tema/<jazyk>", methods=["GET", "POST",])
def ukaz_tema(jazyk):

    if jazyk not in prispevky:
        prispevky[jazyk] = [] # <----- teď se to ukládá do slovníku jako nový samostatný seznam 

    if request.method == "POST":
        napsany_text = request.form.get("prispevek")
        if napsany_text:
            prispevky[jazyk].append(napsany_text)

            print(f"uživatel napsal do fóra {jazyk} tohle: {napsany_text}") # <----- Jen zpráva do konzole

        elif request.form.get("smazani_index"):
            prispevky[jazyk].pop(int(request.form.get("smazani_index")))

    return render_template("post.html", nazev=jazyk, prispevky=prispevky[jazyk])

# REGISTRACE

app.route("/registrace", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == USERNAME and password == PASSWORD:
            return redirect(url_for("Vítejte"))
        else:
            return render_template("login.html",
                                   error="Nesprávné jméno nebo heslo")
    return render_template("login.html")


# CESTY

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")   

@app.route("/home")
def hlavniStranka():
    return render_template("home.html") 

if __name__ == "__main__":
    app.run(debug=True)





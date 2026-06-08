from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '123'

prispevky = []

@app.route("/")
def home():

    temata = ["Python", "Java Script", "Type Script", "C#", "C++"]

    return render_template("index.html", temata=temata)



@app.route("/tema/<jazyk>", methods=["GET", "POST",])
def ukaz_tema(jazyk):
    if request.method == "POST":
        napsany_text = request.form.get("prispevek")
        if napsany_text:
            prispevky.append(napsany_text)

        elif request.form.get("smazani_index"):
            prispevky.pop(int(request.form.get("smazani_index")))

        print(f"uživatel napsal do fóra {jazyk} tohle: {napsany_text}") 

    return render_template("post.html", nazev=jazyk, prispevky=prispevky)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")   

if __name__ == "__main__":
    app.run(debug=True)


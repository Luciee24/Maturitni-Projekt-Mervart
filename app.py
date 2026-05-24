from flask import Flask, render_template, request

app = Flask(__name__)

prispevky = []

@app.route("/")
def home():

    temata = ["Python", "Java Script", "Type Script", "C#", "C++"]

    return render_template("index.html", temata=temata)



@app.route("/tema/<jazyk>", methods=["GET", "POST"])
def ukaz_tema(jazyk):
    if request.method == "POST":
        napsany_text = request.form.get("prispevek")
        if napsany_text:
            prispevky.append(napsany_text)
        print(f"uživatel napsal do fóra {jazyk} tohle: {napsany_text}")
    
    return render_template("post.html", nazev=jazyk, prispevky=prispevky)

if __name__ == "__main__":
    app.run(debug=True)





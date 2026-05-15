import sqlite3
import random
from flask import Flask, render_template, session, request, redirect
import os
from utility import *

app = Flask(__name__)
app.secret_key = os.urandom(12)

initiate_data()

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        if "join" in request.form:
            return redirect(f"/lobby/{request.form['join code']}")
    return render_template("home.html")

@app.route('/create', methods=["GET", "POST"])
def create_game():
    g_id = random.randint(0, 9999)
    while (len(fetch("games", f"serverid={g_id}", "*")) != 0):
        g_id = random.randint(0, 9999)
    add_game(g_id, "p1")
    return redirect(f"/lobby/{g_id}")

@app.route('/game/<g_id>', methods=["GET", "POST"])
def game(g_id):
    data = fetch("games", f"serverid={g_id}", "*")
    #print(data[0][12])
    return render_template("imposter.html", category=data[0][11], word=data[0][12])

@app.route('/lobby/<g_id>', methods=["GET", "POST"])
def lobby(g_id):
    data = fetch("games", f"serverid={g_id}", "*")
    print(data)
    if (len(data) > 0):
        return render_template("lobby.html", ID=g_id)
    else:
        return redirect("/")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        if not request.form['username'] in usernames:
            return render_template("login.html",
                error="Wrong &nbsp username &nbsp or &nbsp password!<br><br>",
                normal=True)
        elif request.form['password'] != fetch("players", "username = ?", "password", (request.form['username'],))[0][0]:
                return render_template("login.html",
                    error="Wrong &nbsp username &nbsp or &nbsp password!<br><br>",
                    normal=True)
        else:
            session["u_rowid"] = fetch("user_base", "username = ?", "rowid", (request.form['username'],))[0]
    if 'u_rowid' in session:
        return redirect("/")
    session.clear()

    return render_template("login.html")

if __name__ == "__main__":
    app.debug = False
    app.run(host='0.0.0.0')

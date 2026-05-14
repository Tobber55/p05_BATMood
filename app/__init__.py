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

@app.route('/imposter', methods=["GET", "POST"])
def imposter():
    return render_template("imposter.html")

@app.route('/lobby/<g_id>', methods=["GET", "POST"])
def lobby(g_id):
    data = fetch("games", f"serverid={g_id}", "*") 
    print(data)
    if (len(data) > 0):
        return render_template("lobby.html", ID=g_id)
    else:
        return redirect("/")

if __name__ == "__main__":
    app.debug = False
    app.run(host='0.0.0.0')

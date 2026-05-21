import sqlite3
import random
from flask import Flask, render_template, session, request, redirect
from flask_socketio import SocketIO, emit, join_room, leave_room, send
import os
from utility import *
from game import *

app = Flask(__name__)
app.secret_key = os.urandom(12)
socketio = SocketIO(app)
initiate_data()

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        if "join" in request.form:
            return redirect(f"/lobby/{request.form['join code']}")
    if 'u_name' in session:
        return render_template("home.html", user=session["u_name"])
    return render_template("home.html", user="guest")

@app.route('/create', methods=["GET", "POST"])
def create_game():
    g_id = random.randint(0, 9999)
    while (len(fetch("games", f"serverid={g_id}", "*")) != 0):
        g_id = random.randint(0, 9999)
    add_game(g_id, session["u_name"])
    return redirect(f"/lobby/{g_id}")

@app.route('/game/<g_id>', methods=["GET", "POST"])
def game(g_id):
    data = fetch("games", f"serverid={g_id}", "*")
    players = []
    for i in data[0][2:6]:
        if i != '':
            players.append(i)
    log = []

    if data[0][13] == session["u_name"]:
        return render_template("imposter.html", category=data[0][11], word="IMPOSTER", lenPlayers=len(players), players=players, log=log, g_id=g_id)
    else:
        return render_template("imposter.html", category=data[0][11], word=data[0][12], lenPlayers=len(players), players=players, log=log, g_id=g_id)

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
    usernames = [row[0] for row in fetch("players", "TRUE", "username")]
    if request.method == 'POST':
        if not request.form['username'] in usernames:
            return render_template("login.html",
                error="Wrong &nbsp username &nbsp or &nbsp password!<br><br>")
        elif request.form['password'] != fetch("players", "username = ?", "password", (request.form['username'],))[0][0]:
                return render_template("login.html",
                    error="Wrong &nbsp username &nbsp or &nbsp password!<br><br>")
        else:
            session["u_name"] = request.form['username']
    if 'u_name' in session:
        return redirect("/")
    session.clear()

    return render_template("login.html")

@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.pop("u_name", None)
    return redirect("/")

@app.route('/register', methods=["GET", "POST"])
def register():
    if 'u_name' in session:
        return redirect("/")
    if request.method == "POST":
        if not request.form['password'] == request.form['confirm']:
            return render_template("register.html",
                                   error="Passwords do not match, please try again! <br><br>")
        if not create_user(request.form['username'], request.form['password']):
            return render_template("register.html",
                                   error="Username already taken, please try again! <br><br>")
        else:
            return redirect("/login")
    return render_template("register.html")

@socketio.on('join_server')
def join(data):
    join_room(data)

@socketio.on('leave_server')
def leave(data):
    leave_room(data)
    print("bleh")

if __name__ == "__main__":
    app.debug = True
    socketio.run(app)

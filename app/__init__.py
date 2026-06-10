import sqlite3
import random
from flask import Flask, render_template, session, request, redirect
from flask_socketio import SocketIO, rooms, emit, join_room, leave_room, send
import os
from utility import *
from game import *

app = Flask(__name__)
app.secret_key = "superdupersecret"
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
initiate_data()

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        if "join" in request.form:
            return redirect(f"/lobby/{request.form['join code']}")
    if 'u_name' in session:
        return render_template("home.html", user=session["u_name"], party="/profile", image="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%2Fid%2FOIP.bPDvdqDn6Y_dpzI7XaS5-AHaHa%3Fpid%3DApi&f=1&ipt=93d7b18a65a202d81aa30c54b09fd4d4a749e321c42fcaf5657d138a96aa3ea7&ipo=images")
    return render_template("home.html", user="guest", party="/login", image="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.pinimg.com%2F474x%2Fae%2Fae%2F25%2Faeae25799b8763a924f5001c6297cf0e.jpg%3Fnii%3Dt&f=1&nofb=1&ipt=a463127ae3c71405a6bcaa6f8b2606c9fd3b859de74153d86a5c9dc2770e3e37")

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

    if fetch("games", f"serverid={g_id}", "specialPlayer")[0][0] == "":
        imp = random.choice(players)
        imposter(imp, g_id)

    playerN = 0
    playerF = 0
    if fetch("games", f"serverid={g_id}", "firstPlayer")[0][0] == "":
        playerF = chooseStartPlayer(g_id)
    else:
        playerF = fetch("games", f"serverid={g_id}", "firstPlayer")[0][0]


    if fetch("games", f"serverid={g_id}", "player1")[0][0] == session["u_name"]:
        playerN = 1
    elif fetch("games", f"serverid={g_id}", "player2")[0][0] == session["u_name"]:
        playerN = 2
    elif fetch("games", f"serverid={g_id}", "player3")[0][0] == session["u_name"]:
        playerN = 3
    elif fetch("games", f"serverid={g_id}", "player4")[0][0] == session["u_name"]:
        playerN = 4

    if data[0][8] == session["u_name"]:
        return render_template("imposter.html", category=data[0][6], word="YOU ARE THE IMPOSTER",
                               g_id=g_id,
                               playerN=playerN, playerF=playerF, username=session["u_name"], playerM=len(players))
    else:
        return render_template("imposter.html", category=data[0][6], word=data[0][7],
                               g_id=g_id,
                               playerN=playerN, playerF=playerF, username=session["u_name"], playerM=len(players))

@app.route('/lobby/<g_id>', methods=["GET", "POST"])
def lobby(g_id):
    data = fetch("games", f"serverid={g_id}", "*")
    if (len(data) > 0):
        if request.method == 'POST':
            if "ready" in request.form:
                if (join_game(session["u_name"], g_id)):
                    if (fetch("games", f"serverid={g_id}", "player1")[0][0] == session["u_name"]):
                        return render_template("lobby.html", ID=g_id, ready=True, host=True)
                    return render_template("lobby.html", ID=g_id, ready=True, host=False)
            if "start" in request.form:
                chooseStartPlayer(g_id)
                return redirect(f"/game/{g_id}")
        if (fetch("games", f"serverid={g_id}", "player1")[0][0] == session["u_name"]):
            return render_template("lobby.html", ID=g_id, ready=True, host=True)
        return render_template("lobby.html", ID=g_id, ready=False, host=False)
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

@app.route('/profile', methods=["GET", "POST"])
def profile():
    return render_template("profile.html")

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
    print(rooms())

@socketio.on('reload')
def reload(data):
    emit('reload', room=data)

@socketio.on('joinGame')
def joinGame(g_id):
    emit('joinGame', room=g_id)

@socketio.on('input')
def input(g_id, input):
    emit('input', input, room=g_id)

@socketio.on('turn')
def turn(g_id, turn):
    emit('turn', turn, room=g_id)

if __name__ == "__main__":
    app.debug = True
    socketio.run(app)

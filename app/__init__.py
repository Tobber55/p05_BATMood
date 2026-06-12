import sqlite3
import random
from flask import Flask, render_template, session, request, redirect, jsonify, url_for
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
            if 'u_name' not in session:
                return redirect("/login")
            return redirect(f"/lobby/{request.form['join code']}")
    if 'u_name' in session:
        user = "'" + session['u_name'] + "'"
        wins = fetch("players", f"username={user}", "wins")[0][0]
        losses = fetch("players", f"username={user}", "losses")[0][0]
        return render_template("home.html", user=session["u_name"], party="/", image="../static/pfp.png", wins=wins, losses=losses, inn=True)
    return render_template("home.html", user="guest", party="/login", image="../static/defaultpfp.jpg", wins="N/A", losses="N/A", inn=False)

@app.route('/create', methods=["GET", "POST"])
def create_game():
    if 'u_name' not in session:
        return redirect("/login")
    g_id = random.randint(0, 9999)
    while (len(fetch("games", f"serverid={g_id}", "*")) != 0):
        g_id = random.randint(0, 9999)
    add_game(g_id, session["u_name"])
    return redirect(f"/lobby/{g_id}")

@app.route('/game/<g_id>', methods=["GET", "POST"])
def game(g_id):
    if exists("games", f"serverid={g_id}"):
        data = fetch("games", f"serverid={g_id}", "*")
        players = []
        for i in data[0][2:6]:
            if i != '':
                players.append(i)

        imp = ""
        if fetch("games", f"serverid={g_id}", "specialPlayer")[0][0] == "":
            imp = random.choice(players)
            imposter(imp, g_id)
        else:
            imp = fetch("games", f"serverid={g_id}", "specialPlayer")[0][0]

        playerN = 0
        playerF = 0
        if fetch("games", f"serverid={g_id}", "firstPlayer")[0][0] == "":
            playerF = chooseStartPlayer(g_id)
        else:
            playerF = fetch("games", f"serverid={g_id}", "firstPlayer")[0][0]

        one = fetch("games", f"serverid={g_id}", "player1")[0][0]
        two = fetch("games", f"serverid={g_id}", "player2")[0][0]
        three = fetch("games", f"serverid={g_id}", "player3")[0][0]
        four = fetch("games", f"serverid={g_id}", "player4")[0][0]

        if one == session["u_name"]: playerN = 1
        elif two == session["u_name"]: playerN = 2
        elif three == session["u_name"]: playerN = 3
        elif four == session["u_name"]: playerN = 4
    else:
        return redirect("/")
    if request.method == 'POST':
        if exists("games", f"serverid={g_id}"):
            remove_game(str(g_id))
            if request.get_json()["imp"]:
                if imp == session["u_name"]:
                    updateStat(session["u_name"], True)
                else:
                    updateStat(session["u_name"], False)
                return jsonify({
                    'success': True,
                }), 200
            else:
                if imp == session["u_name"]:
                    updateStat(session["u_name"], False)
                else:
                    updateStat(session["u_name"], True)
                return jsonify({
                    'success': True,
                }), 200

    if imp == session["u_name"]:
        return render_template("imposter.html", category=data[0][6], word="YOU ARE THE IMPOSTER",
                               g_id=g_id, one=one, two=two, three=three, four=four, imp=imp,
                               playerN=playerN, playerF=playerF, username=session["u_name"], playerM=len(players))
    else:
        return render_template("imposter.html", category=data[0][6], word=data[0][7],
                               g_id=g_id, one=one, two=two, three=three, four=four, imp=imp,
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

@socketio.on("vote")
def vote(g_id, data):
    emit('vote', data, room=g_id)

@socketio.on("gameEnd")
def gameEnd(g_id, imp):
    emit("gameEnd", imp, room=g_id)

if __name__ == "__main__":
    app.debug = True
    socketio.run(app)

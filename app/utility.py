import sqlite3
from game import *
DB_FILE = "data.db"

def fetch(table, criteria, data, params=()):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    query = f"SELECT {data} FROM {table} WHERE {criteria}"
    c.execute(query, params)
    data = c.fetchall()
    db.commit()
    db.close()
    return data

def create_user(username, password):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT username FROM players")
    list = [username[0] for username in c.fetchall()]
    if not username in list:
        c.execute("INSERT INTO players VALUES (?, ?, ?, ?)",(username, password, 0, 0))
        db.commit()
        db.close()
        return True
    db.commit()
    db.close()
    return False

def join_game(username, gameid):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    p1 = fetch("games", f"serverid={gameid}", "player1")[0][0];
    p2 = fetch("games", f"serverid={gameid}", "player2")[0][0];
    p3 = fetch("games", f"serverid={gameid}", "player3")[0][0];
    p4 = fetch("games", f"serverid={gameid}", "player4")[0][0];

    if (len(fetch("games", f"serverid={gameid}", "*")) != 0):
        if (p1 == ""):
            c.execute("UPDATE games SET player1 = ? WHERE serverid = ?", (username, gameid))
            db.commit()
            db.close()
            return True
        elif (p2 == ""):
            c.execute("UPDATE games SET player2 = ? WHERE serverid = ?", (username, gameid))
            db.commit()
            db.close()
            return True
        elif (p3 == ""):
            c.execute("UPDATE games SET player3 = ? WHERE serverid = ?", (username, gameid))
            db.commit()
            db.close()
            return True
        elif (p4 == ""):
            c.execute("UPDATE games SET player4 = ? WHERE serverid = ?", (username, gameid))
            db.commit()
            db.close()
            return True
    if (username == p1 or username == p2 or username == p3 or username == p4):
        db.commit()
        db.close()
        return True
    db.commit()
    db.close()
    return False

def chooseStartPlayer(g_id):
    data = fetch("games", f"serverid={g_id}", "*")
    players = 0
    for i in data[0][2:6]:
        if i != '':
            players += 1
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    playerN = random.randint(1, players)
    c.execute("UPDATE games SET firstPlayer = ? WHERE serverid = ?", (playerN, g_id))
    db.commit()
    db.close()
    return playerN

def imposter(user, g_id):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("UPDATE games SET specialPlayer = ? WHERE serverid = ?", (user, g_id))
    db.commit()
    db.close()

def add_game(g_id, p_id):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    word = RandomizeWord()
    c.execute("INSERT INTO games VALUES (?, 0, ?, '', '', '', ?, ?, '', 0)",
              (g_id, p_id, word[0], word[1]))
    db.commit()
    db.close()

def initiate_data():
    db = sqlite3.connect("data.db")
    #games = sqlite3.connect("games.db")

    c = db.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS players(
            username TEXT UNIQUE,
            password TEXT,
            wins INT,
            losses INT
        )
        """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS games(
            serverID INT UNIQUE,
            gameID INT,
            player1 TEXT,
            player2 TEXT,
            player3 TEXT,
            player4 TEXT,
            category TEXT,
            word TEXT,
            specialPlayer TEXT,
            firstPlayer INT
        )""")

    db.commit()
    db.close()

import sqlite3
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


def add_game(g_id, p_id):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("INSERT INTO games VALUES (?, 0, ?, '', '', '', '', '', '', '', '', '', 'Mood', '')",
              (g_id, p_id))
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
            input1 TEXT,
            input2 TEXT,
            input3 TEXT,
            input4 TEXT,
            inputLog TEXT,
            category TEXT,
            word TEXT,
            specialPlayer TEXT
        )""")

    db.commit()
    db.close()

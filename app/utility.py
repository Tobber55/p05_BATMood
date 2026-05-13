def fetch(table, criteria, data, params=()):
    db = get_db()
    c = db.cursor()
    query = f"SELECT {data} FROM {table} WHERE {criteria}"
    c.execute(query, params)
    data = c.fetchall()
    db.commit()
    db.close()
    return data


def initiate_data():
    db = sqlite3.connect("data.db")
    #games = sqlite3.connect("games.db")

    c = db.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS players(
            username TEXT UNIQUE,
            password TEXT,
            wins INT,
            losses INT,
            ingame INT
        )
        """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS games(
            serverID TEXT UNIQUE,
            gameID INT,
            player1 TEXT,
            player2 TEXT,
            player3 TEXT,
            player4 TEXT,
            player5 TEXT,
            player6 TEXT
        )""")

    db.commit()
    db.close()

import sqlite3
import json
import os
DB_FILE = os.path.join(os.path.dirname(__file__), "data.db")

def fetch(table, criteria, data, params=()):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    query = f"SELECT {data} FROM {table} WHERE {criteria}"
    c.execute(query, params)
    data = c.fetchall()
    db.commit()
    db.close()
    return data

def update_game_field(serverid, field, value):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute(f"UPDATE games SET {field} = ? WHERE serverID = ?", (value, serverid))
    db.commit()
    db.close()

def create_user(username, password):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    existing = fetch("players", "username = ?", "username", (username,))
    if not existing:
        c.execute("INSERT INTO players (username, password, wins, losses) VALUES (?, ?, ?, ?)",
                  (username, password, 0, 0))
        db.commit()
        db.close()
        return True
    db.close()
    return False

def update_player_wins_losses(username, is_win):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    if is_win:
        c.execute("UPDATE players SET wins = wins + 1 WHERE username = ?", (username,))
    else:
        c.execute("UPDATE players SET losses = losses + 1 WHERE username = ?", (username,))
    db.commit()
    db.close()

def update_player_stats(game_id, imposter, imposter_won):
    players = fetch("games", f"serverID = {game_id}", "player1, player2, player3, player4, player5, player6")[0]
    for player in players:
        if player:
            if imposter_won:
                if player == imposter:
                    update_player_wins_losses(player, True)
                else:
                    update_player_wins_losses(player, False)
            else:
                if player == imposter:
                    update_player_wins_losses(player, False)
                else:
                    update_player_wins_losses(player, True)

def count_players_in_game(game_id):
    game = fetch("games", f"serverID = {game_id}", "player1, player2, player3, player4, player5, player6")[0]
    return sum(1 for p in game if p)

def join_game(username, gameid):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    game = fetch("games", f"serverid=?", "player1, player2, player3, player4, player5, player6", (gameid,))
    if not game:
        db.close()
        return False
    
    players = list(game[0])
    if username in players:
        db.close()
        return True
    
    for i in range(6):
        if not players[i]:
            c.execute(f"UPDATE games SET player{i+1} = ? WHERE serverid = ?", (username, gameid))
            db.commit()
            db.close()
            return True
    db.close()
    return False

def add_game(g_id, p_id):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("""INSERT INTO games 
        (serverID, gameID, player1, player2, player3, player4, player5, player6, 
         input1, input2, input3, input4, input5, input6, inputLog, category, word, specialPlayer,
         game_phase, round_num, ready1, ready2, ready3, ready4, ready5, ready6,
         decision1, decision2, decision3, decision4, decision5, decision6,
         vote_target1, vote_target2, vote_target3, vote_target4, vote_target5, vote_target6,
         game_winner, imposter_guess)
        VALUES (?, 0, ?, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 
                'lobby', 0, 0,0,0,0,0,0, NULL,NULL,NULL,NULL,NULL,NULL, 
                NULL,NULL,NULL,NULL,NULL,NULL, NULL, NULL)""",
        (g_id, p_id))
    db.commit()
    db.close()

def start_game(game_id):
    from game import RandomizeWord
    category, word = RandomizeWord()
    players = fetch("games", f"serverID = {game_id}", "player1, player2, player3, player4, player5, player6")[0]
    active_players = [p for p in players if p]
    imposter = random.choice(active_players)
    
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("""UPDATE games SET 
        category = ?, word = ?, specialPlayer = ?, game_phase = 'collecting_hints', round_num = 1,
        input1 = '', input2 = '', input3 = '', input4 = '', input5 = '', input6 = '',
        inputLog = '[]'
        WHERE serverID = ?""", (category, word, imposter, game_id))
    db.commit()
    db.close()

def initiate_data():
    db = sqlite3.connect(DB_FILE)
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
            player5 TEXT,
            player6 TEXT,
            input1 TEXT,
            input2 TEXT,
            input3 TEXT,
            input4 TEXT,
            input5 TEXT,
            input6 TEXT,
            inputLog TEXT,
            category TEXT,
            word TEXT,
            specialPlayer TEXT,
            game_phase TEXT,
            round_num INT,
            ready1 INT,
            ready2 INT,
            ready3 INT,
            ready4 INT,
            ready5 INT,
            ready6 INT,
            decision1 TEXT,
            decision2 TEXT,
            decision3 TEXT,
            decision4 TEXT,
            decision5 TEXT,
            decision6 TEXT,
            vote_target1 INT,
            vote_target2 INT,
            vote_target3 INT,
            vote_target4 INT,
            vote_target5 INT,
            vote_target6 INT,
            game_winner TEXT,
            imposter_guess TEXT
        )
    """)
    
    db.commit()
    db.close()

import random
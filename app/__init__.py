import sqlite3
import random
from flask import Flask, render_template, session, request, redirect, url_for
import os
from utility import *

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))
print(f"Secret key set: {app.secret_key[:10]}...")

initiate_data()
print("Database initialized")

@app.before_request
def require_login():
    allowed_routes = ['login', 'register', 'static']
    if request.endpoint not in allowed_routes and 'u_name' not in session:
        return redirect(url_for('login', next=request.url))

@app.route('/', methods=["GET", "POST"])
def home():
    error = None
    if request.method == 'POST':
        if "join" in request.form:
            code = request.form['join code'].strip()
            game = fetch("games", "serverid = ?", "*", (code,))
            if game:
                return redirect(f"/lobby/{code}")
            else:
                error = "Invalid game code. Please check and try again."
    
    user = session.get("u_name", "guest")
    return render_template("home.html", user=user, 
                          party="/profile" if user != "guest" else "/login",
                          image="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%2Fid%2FOIP.bPDvdqDn6Y_dpzI7XaS5-AHaHa%3Fpid%3DApi&f=1&ipt=93d7b18a65a202d81aa30c54b09fd4d4a749e321c42fcaf5657d138a96aa3ea7&ipo=images",
                          error=error)

@app.route('/create')
def create_game():
    if 'u_name' not in session:
        return redirect(url_for('login'))
    g_id = random.randint(1000, 9999)
    while fetch("games", f"serverid={g_id}", "*"):
        g_id = random.randint(1000, 9999)
    add_game(g_id, session["u_name"])
    return redirect(f"/lobby/{g_id}")

@app.route('/lobby/<g_id>', methods=["GET", "POST"])
def lobby(g_id):
    game = fetch("games", "serverid=?", "*", (g_id,))
    if not game:
        return redirect(url_for('home'))
    
    game = game[0]
    if game[18] != 'lobby':
        return redirect(f"/game/{g_id}")
    
    players = [game[2], game[3], game[4], game[5], game[6], game[7]]
    current_user = session['u_name']
    
    if current_user not in players:
        if not join_game(current_user, g_id):
            return redirect(url_for('home'))
        game = fetch("games", "serverid=?", "*", (g_id,))[0]
        players = [game[2], game[3], game[4], game[5], game[6], game[7]]
    
    player_index = players.index(current_user)
    ready_col = 20 + player_index
    is_ready = bool(game[ready_col])
    
    if request.method == 'POST':
        if 'ready' in request.form:
            new_ready = 0 if is_ready else 1
            update_game_field(g_id, f"ready{player_index+1}", new_ready)
            return redirect(f"/lobby/{g_id}")
        elif 'start' in request.form and game[2] == current_user:
            all_ready = True
            for i in range(6):
                if players[i] and not game[20 + i]:
                    all_ready = False
                    break
            if all_ready and count_players_in_game(g_id) >= 2:
                start_game(g_id)
                return redirect(f"/game/{g_id}")
            else:
                return redirect(f"/lobby/{g_id}")
    
    ready_status = [(players[i], bool(game[20 + i])) for i in range(6) if players[i]]
    all_ready = all(ready for _, ready in ready_status) and len(ready_status) >= 2
    return render_template("lobby.html", ID=g_id, players=ready_status, 
                          host=(game[2] == current_user),
                          is_ready=is_ready,
                          all_ready=all_ready)

@app.route('/game/<g_id>', methods=["GET", "POST"])
def game(g_id):
    game_data = fetch("games", "serverid=?", "*", (g_id,))
    if not game_data:
        return redirect(url_for('home'))
    
    game = game_data[0]
    players = [game[2], game[3], game[4], game[5], game[6], game[7]]
    current_user = session['u_name']
    
    if current_user not in players:
        return redirect(url_for('home'))
    
    player_index = players.index(current_user)
    game_phase = game[18]
    round_num = game[19]
    category = game[15]
    word = game[16]
    imposter = game[17]
    is_imposter = (imposter == current_user)
    
    import json
    hint_history = []
    if game[14]:
        try:
            hint_history = json.loads(game[14])
        except:
            hint_history = []
    
    current_hints = {}
    for i in range(6):
        if players[i]:
            current_hints[players[i]] = game[8 + i] or ""
    
    if request.method == 'POST':
        if game_phase == 'collecting_hints':
            hint = request.form.get('hint', '').strip()
            if hint and len(hint) <= 50:
                update_game_field(g_id, f"input{player_index+1}", hint)
                game_data = fetch("games", "serverid=?", "*", (g_id,))
                if not game_data:
                    return redirect(url_for('home'))
                game = game_data[0]
                players = [game[2], game[3], game[4], game[5], game[6], game[7]]
                
                all_submitted = True
                for i in range(6):
                    if players[i] and not game[8 + i]:
                        all_submitted = False
                        break
                
                if all_submitted:
                    round_hints = {}
                    for i in range(6):
                        if players[i]:
                            round_hints[players[i]] = game[8 + i]
                    hint_history.append({"round": round_num, "hints": round_hints})
                    update_game_field(g_id, "inputLog", json.dumps(hint_history))
                    update_game_field(g_id, "game_phase", "voting_decision")
                    for i in range(6):
                        update_game_field(g_id, f"decision{i+1}", None)
                return redirect(f"/game/{g_id}")
        
        elif game_phase == 'voting_decision':
            decision = request.form.get('decision')
            if decision in ['another_round', 'eliminate']:
                update_game_field(g_id, f"decision{player_index+1}", decision)
                game_data = fetch("games", "serverid=?", "*", (g_id,))
                if not game_data:
                    return redirect(url_for('home'))
                game = game_data[0]
                players = [game[2], game[3], game[4], game[5], game[6], game[7]]
                
                all_decided = True
                for i in range(6):
                    if players[i] and game[26 + i] is None:
                        all_decided = False
                        break
                if all_decided:
                    another_count = 0
                    eliminate_count = 0
                    for i in range(6):
                        if players[i]:
                            if game[26 + i] == 'another_round':
                                another_count += 1
                            elif game[26 + i] == 'eliminate':
                                eliminate_count += 1
                    if eliminate_count > another_count:
                        update_game_field(g_id, "game_phase", "voting_elimination")
                        for i in range(6):
                            update_game_field(g_id, f"vote_target{i+1}", None)
                    else:
                        new_round = round_num + 1
                        update_game_field(g_id, "round_num", new_round)
                        update_game_field(g_id, "game_phase", "collecting_hints")
                        for i in range(6):
                            update_game_field(g_id, f"input{i+1}", "")
                    for i in range(6):
                        update_game_field(g_id, f"decision{i+1}", None)
                return redirect(f"/game/{g_id}")
        
        elif game_phase == 'voting_elimination':
            vote_target = request.form.get('vote_target')
            if vote_target and vote_target != current_user and vote_target in players:
                target_index = players.index(vote_target)
                update_game_field(g_id, f"vote_target{player_index+1}", target_index)
                game_data = fetch("games", "serverid=?", "*", (g_id,))
                if not game_data:
                    return redirect(url_for('home'))
                game = game_data[0]
                players = [game[2], game[3], game[4], game[5], game[6], game[7]]
                
                all_voted = True
                for i in range(6):
                    if players[i] and game[32 + i] is None:
                        all_voted = False
                        break
                if all_voted:
                    vote_counts = {}
                    for i in range(6):
                        if players[i]:
                            target_idx = game[32 + i]
                            if target_idx is not None:
                                vote_counts[target_idx] = vote_counts.get(target_idx, 0) + 1
                    if vote_counts:
                        max_votes = max(vote_counts.values())
                        candidates = [idx for idx, count in vote_counts.items() if count == max_votes]
                        eliminated_idx = random.choice(candidates)
                        eliminated_player = players[eliminated_idx]
                        if eliminated_player == imposter:
                            update_game_field(g_id, "game_phase", "imposter_guess")
                            update_game_field(g_id, "imposter_guess", "")
                        else:
                            update_game_field(g_id, "game_phase", "game_over")
                            update_game_field(g_id, "game_winner", "imposter")
                            update_player_stats(g_id, imposter, True)
                    else:
                        update_game_field(g_id, "game_phase", "collecting_hints")
                    for i in range(6):
                        update_game_field(g_id, f"vote_target{i+1}", None)
                return redirect(f"/game/{g_id}")
        
        elif game_phase == 'imposter_guess' and is_imposter:
            guess = request.form.get('guess', '').strip()
            if guess:
                update_game_field(g_id, "imposter_guess", guess)
                if guess.lower() == word.lower():
                    update_game_field(g_id, "game_winner", "imposter")
                    update_player_stats(g_id, imposter, True)
                else:
                    update_game_field(g_id, "game_winner", "others")
                    for i in range(6):
                        if players[i] and players[i] != imposter:
                            update_player_wins_losses(players[i], True)
                    if imposter:
                        update_player_wins_losses(imposter, False)
                update_game_field(g_id, "game_phase", "game_over")
                for i in range(6):
                    update_game_field(g_id, f"input{i+1}", "")
                return redirect(f"/game/{g_id}")
    
    game_data = fetch("games", "serverid=?", "*", (g_id,))
    if not game_data:
        return redirect(url_for('home'))
    game = game_data[0]
    players = [game[2], game[3], game[4], game[5], game[6], game[7]]
    game_phase = game[18]
    round_num = game[19]
    category = game[15]
    word = game[16]
    imposter = game[17]
    is_imposter = (imposter == current_user)
    
    current_hints = {players[i]: game[8 + i] or "" for i in range(6) if players[i]}
    hint_history = []
    if game[14]:
        try:
            hint_history = json.loads(game[14])
        except:
            hint_history = []
    
    other_hints = {p: h for p, h in current_hints.items() if p != current_user}
    active_players = [p for p in players if p]
    
    decisions_made = None
    votes_made = None
    if game_phase == 'voting_decision':
        decisions_made = sum(1 for i in range(6) if players[i] and game[26 + i] is not None)
    elif game_phase == 'voting_elimination':
        votes_made = sum(1 for i in range(6) if players[i] and game[32 + i] is not None)
    
    has_voted_decision = False
    has_voted_target = False
    if game_phase == 'voting_decision':
        has_voted_decision = game[26 + player_index] is not None
    elif game_phase == 'voting_elimination':
        has_voted_target = game[32 + player_index] is not None
    
    return render_template("game.html", 
                         game_id=g_id,
                         phase=game_phase,
                         round_num=round_num,
                         category=category,
                         word=word if not is_imposter else None,
                         is_imposter=is_imposter,
                         current_hints=current_hints,
                         other_hints=other_hints,
                         hint_history=hint_history,
                         players=active_players,
                         current_user=current_user,
                         decisions_made=decisions_made,
                         votes_made=votes_made,
                         winner=game[38] if game_phase == 'game_over' else None,
                         has_voted_decision=has_voted_decision,
                         has_voted_target=has_voted_target)

@app.route('/login', methods=["GET", "POST"])
def login():
    next_url = request.args.get('next')
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        print(f"Login attempt: username={username}, password={password[:3]}...")
        user = fetch("players", "username = ?", "*", (username,))
        print(f"Query result: {user}")
        if user and user[0][1] == password:
            session['u_name'] = username
            session.permanent = True
            print(f"Login successful for {username}, session set")
            target = next_url if next_url else url_for('home')
            return redirect(target)
        else:
            error = "Invalid username or password!"
            print("Login failed: invalid credentials")
    return render_template("login.html", error=error)

@app.route('/profile')
def profile():
    if 'u_name' not in session:
        return redirect(url_for('login'))
    user_data = fetch("players", "username = ?", "*", (session['u_name'],))
    if user_data:
        wins = user_data[0][2]
        losses = user_data[0][3]
        return render_template("profile.html", username=session['u_name'], wins=wins, losses=losses)
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('u_name', None)
    return redirect(url_for('home'))

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm', '')
        if password != confirm:
            return render_template("register.html", error="Passwords do not match!")
        if create_user(username, password):
            return redirect(url_for('login'))
        else:
            return render_template("register.html", error="Username already taken!")
    return render_template("register.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
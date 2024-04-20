from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Fonction pour créer la table dans la base de données
def create_table_mmr():
    conn = sqlite3.connect('db/mmr_database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS mmr_data
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 player_id TEXT NOT NULL,
                 timestamp TEXT NOT NULL,
                 gamemode TEXT NOT NULL,
                 mmr INTEGER NOT NULL)''')
    
    conn.commit()
    conn.close()


# Base de données des utilisateurs (ID, Nom)
def create_table_player():
    conn = sqlite3.connect('db/player_database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS player_data
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 player_id TEXT NOT NULL,
                 player_name TEXT NOT NULL,
                 UNIQUE(player_id))''')  # Définir player_id comme unique pour éviter les doublons
    conn.commit()
    conn.close()

# Fonction pour insérer ou mettre à jour les données dans la base de données
def insert_or_update_player(player_id, player_name):
    conn = sqlite3.connect('db/player_database.db')
    c = conn.cursor()
    # Vérifier si l'ID du joueur existe déjà dans la base de données
    c.execute("SELECT * FROM player_data WHERE player_id=?", (player_id,))
    existing_player = c.fetchone()
    if existing_player:
        # Si l'ID existe déjà, mettre à jour le nom du joueur
        if existing_player[1] != player_name:  # Vérifier si le nom a changé
            c.execute("UPDATE player_data SET player_name=? WHERE player_id=?", (player_name, player_id))
    else:
        # Si l'ID n'existe pas, insérer un nouvel utilisateur
        c.execute("INSERT INTO player_data (player_id, player_name) VALUES (?, ?)", (player_id, player_name))
    conn.commit()
    conn.close()

# Fonction pour insérer les données dans la base de données
def insert_data(player_id, timestamp, gamemode, mmr):
    conn = sqlite3.connect('db/mmr_database.db')
    c = conn.cursor()
    c.execute("INSERT INTO mmr_data (player_id, timestamp, gamemode, mmr) VALUES (?, ?, ?, ?)", (player_id, timestamp, gamemode, mmr))
    conn.commit()
    conn.close()

@app.route('/sendPlayerData', methods=['POST'])
def send_player_data():
    # Vérifie si les paramètres requis sont présents
    if 'player_id' not in request.json or 'timestamp' not in request.json or 'elo' not in request.json or 'gamemode' not in request.json:
        print("missing params")
        print(request.json)
        return jsonify({'error': 'Missing parameters'}), 400
    
    # Récupère les paramètres de la requête
    player_id = request.json['player_id']
    timestamp = request.json['timestamp']
    mmr = request.json['elo']
    gamemode = request.json['gamemode']
    
    # ======
    print(player_id)
    print(timestamp)
    print(mmr)
    print(gamemode)
    # ======
    
    # Insère les données dans la base de données
    insert_data(player_id, timestamp, gamemode, mmr)
    
    return jsonify({'message': 'Data received and stored successfully'}), 200

@app.route('/initPlayer', methods=['POST'])
def init_player():
    # Vérifie si les paramètres requis sont présents
    if 'player_id' not in request.json or 'player_name' not in request.json:
        return jsonify({'error': 'Missing params'}), 400
    # Récupère les paramètres de la requête
    player_id = request.json['player_id']
    player_name = request.json['player_name']
    insert_or_update_player(player_id, player_name)
    return jsonify({"message":f"player {player_name} ready [{player_id}]"})
    

# Fonction pour récupérer les données de la base de données
def get_data(player_id):
    conn = sqlite3.connect('db/mmr_database.db')
    c = conn.cursor()
    c.execute("SELECT gamemode, mmr FROM mmr_data WHERE player_id = ?", (player_id,))
    data = c.fetchall()
    conn.close()
    return data

# Fonction pour récupérer les données de la base de données
def get_player():
    conn = sqlite3.connect('db/player_database.db')
    c = conn.cursor()
    c.execute("SELECT player_id, player_name FROM player_data")
    data = c.fetchall()
    conn.close()
    return data

@app.route('/')
def index():
    data = get_player()
    print(data)
    return render_template('index.html', data=data)

# Route pour charger les données d'un utilisateur et afficher le graphique
@app.route('/LoadUser')
def load_user():
    player_id = request.args.get('user')  # Récupérer l'ID de l'utilisateur depuis les paramètres de requête
    if player_id:
        user_data = get_data(player_id)
        if user_data:
            # Si des données utilisateur sont trouvées, les transmettre au template graph.html
            return render_template('graph.html', data=user_data)
        else:
            return "Utilisateur non trouvé dans la base de données."
    else:
        return "ID de l'utilisateur non spécifié dans les paramètres de la requête."


if __name__ == '__main__':
    create_table_mmr()  # Crée la table si elle n'existe pas déjà
    create_table_player()
    app.run(debug=False, port=5000, host='0.0.0.0')


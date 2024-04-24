from flask import Flask, request, jsonify, render_template
import datetime

import database
from gamemode import GameMode

app = Flask(__name__)


# -------
# BACKEND
# -------

@app.route('/initPlayer', methods=['POST'])
def init_player():
    print(f"initPlayer => {request.json}")
    # Vérifie si les paramètres requis sont présents
    if 'player_id' not in request.json or 'player_name' not in request.json:
        return jsonify({'error': 'Missing params'}), 400
    # Récupère les paramètres de la requête
    player_id = request.json['player_id']
    player_name = request.json['player_name']
    database.insert_or_update_player(player_id, player_name)
    return jsonify({"message":f"player {player_name} ready [{player_id}]"})


@app.route('/updateMmr', methods=['POST'])
def updateMmr():
    print(f"updateMmr => {request.json}")
    requirements = [
        'player_id',
        'timestamp',
        'mmr',
        'gamemode_id'
    ]
    missing_param = False
    for r in requirements:
        if r not in request.json:
            print(f"missing params {r}")
            missing_param = True

    if missing_param:
        return jsonify({'error': 'Missing parameters'}), 400
    
    # Récupère les paramètres de la requête
    player_id = request.json['player_id']
    timestamp = request.json['timestamp']
    mmr = request.json['mmr']
    gamemode_id = request.json['gamemode_id']
    
    if not GameMode(gamemode_id):
        return
    
    # Insère les données dans la base de données
    database.insert_data(player_id, timestamp, gamemode_id, mmr)
    
    return jsonify({'message': 'Data received and stored successfully'}), 200

@app.route('/updateHistorique', methods=['POST'])
def updateHistorique():
    print("test")
    print(f"updateHistorique => {request.json}")
    requirements = [
        'player_id',
        'timestamp',
        'victory',
        'mmr_won',
        'gamemode_id'
    ]
    missing_param = False
    for r in requirements:
        if r not in request.json:
            print(f"missing params {r}")
            missing_param = True

    if missing_param:
        return jsonify({'error': 'Missing parameters'}), 400
    
    if not GameMode(request.json['gamemode_id']):
        return

    database.insert_history(request.json['player_id'],
    request.json['timestamp'],
    request.json['victory'],
    False,
    request.json['mmr_won'],
    request.json['gamemode_id'])
    
    return jsonify({'message': 'Historique mis a jour'}), 200


# --------
# FRONTEND
# --------

@app.route('/user')
def user():
    player_id = request.args.get('user')
    player_detail = database.get_player_details(player_id)
    if not player_detail:
        return "Utilisateur non trouvé dans la base de données."
    ranks = database.get_all_ranks(player_detail['player_id'])
    gamemode_ids = [rank['gamemode_id'] for rank in ranks] 
    historique = database.get_historique(player_id) 
    return render_template('user.html', player=player_detail, ranks=ranks, gamemode_ids=gamemode_ids, historique=historique, Gamemode=GameMode)

# Route pour charger les données d'un utilisateur et afficher le graphique
@app.route('/gamemode_id')
def load_user():
    player_id = request.args.get('user')  # Récupérer l'ID de l'utilisateur depuis les paramètres de requête
    gamemode_id = request.args.get('gamemode_id')
    if player_id:
        user_data = database.get_data(player_id, gamemode_id)
        mmr_array = []
        date_array = []
        for data in user_data:
            mmr = data[0]
            mmr_array.append(mmr)
            timestamp = data[1]
            datetime_object = datetime.datetime.fromtimestamp(int(timestamp))
            date_array.append(datetime_object.strftime("%Y-%m-%d %H:%M:%S"))
        print(date_array)

        if user_data:
            # Si des données utilisateur sont trouvées, les transmettre au template graph.html
            return render_template('graph.html', mmr_array=mmr_array, date_array=date_array)
        else:
            return "Utilisateur non trouvé dans la base de données."
    else:
        return "ID de l'utilisateur non spécifié dans les paramètres de la requête."

# Route pour charger les données d'un utilisateur et afficher le graphique
@app.route('/historique')
def histo_user():
    player_id = request.args.get('user')  # Récupérer l'ID de l'utilisateur depuis les paramètres de requête
    if player_id:
        historique = database.get_historique(player_id)
        if historique:
            # Si des données utilisateur sont trouvées, les transmettre au template graph.html
            return render_template('historique.html', historique=historique, Gamemode=GameMode)
        else:
            return "Utilisateur non trouvé dans la base de données."
    else:
        return "ID de l'utilisateur non spécifié dans les paramètres de la requête."

@app.route('/')
def index():
    data = database.get_all_player()
    return render_template('index.html', data=data)


if __name__ == '__main__':
    # Creent les tables si elles n'existent pas
    database.create_table()
    app.run(debug=True, port=5000, host='0.0.0.0')
    


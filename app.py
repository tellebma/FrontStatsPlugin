from flask import Flask, request, jsonify, render_template
import datetime

import database

app = Flask(__name__)

# -------
# BACKEND
# -------

@app.route('/sendPlayerData', methods=['POST'])
def send_player_data():
    # Vérifie si les paramètres requis sont présents
    if 'player_id' not in request.json or 'timestamp' not in request.json or 'elo' not in request.json or 'gamemode' not in request.json:
        print("missing params")
        print(request.json)
        return jsonify({'error': 'Missing parameters'}), 400
    
    # Récupère les paramètres de la requête
    player_id = request.json['player_id']
    timestamp = request.json['timestamp'][:-3]
    mmr = request.json['elo']
    gamemode = request.json['gamemode']
    
    # ======
    print(player_id)
    print(timestamp)
    print(mmr)
    print(gamemode)
    # ======
    
    # Insère les données dans la base de données
    database.insert_data(player_id, timestamp, gamemode, mmr)
    
    return jsonify({'message': 'Data received and stored successfully'}), 200

@app.route('/initPlayer', methods=['POST'])
def init_player():
    # Vérifie si les paramètres requis sont présents
    if 'player_id' not in request.json or 'player_name' not in request.json:
        return jsonify({'error': 'Missing params'}), 400
    # Récupère les paramètres de la requête
    player_id = request.json['player_id']
    player_name = request.json['player_name']
    database.insert_or_update_player(player_id, player_name)
    return jsonify({"message":f"player {player_name} ready [{player_id}]"})
    


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
    gamemodes = [rank['gamemode'] for rank in ranks] 
    print(gamemodes)
    return render_template('user.html', player=player_detail, ranks=ranks, gamemodes=gamemodes)



# Route pour charger les données d'un utilisateur et afficher le graphique
@app.route('/gamemode')
def load_user():
    player_id = request.args.get('user')  # Récupérer l'ID de l'utilisateur depuis les paramètres de requête
    gamemode = request.args.get('gamemode')
    if player_id:
        user_data = database.get_data(player_id, gamemode)
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
        user_data = database.get_historique(player_id)
        if user_data:
            # Si des données utilisateur sont trouvées, les transmettre au template graph.html
            return render_template('historique.html', data=user_data)
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
    database.create_table_mmr()
    database. create_table_player()

    # database.insert_data(76561198139320709, 1713735254, "RankedTeamDoubles", 1036)
    # database.insert_data(76561198139320709, 1713693250, "RankedTeamDoubles", 952)
    # database.insert_data(76561198139320709, 1713389654, "RankedTeamDoubles", 574)
    # database.insert_data(76561198139320709, 1708547777, "RankedSingle", 785)
    # database.insert_data(76561198139320709, 1713693559, "RankedTeamStandard", 685)
    # database.insert_data(26593207611981309, 1613693559, "RankedTeamStandard", 685)
    # database.insert_data(26593207611981309, 1613693559, "RankedTeamStandard", 885)

    app.run(debug=True, port=5000, host='0.0.0.0')


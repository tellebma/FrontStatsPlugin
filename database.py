# --------------
# 
# 
# --------------
import sqlite3
from utils import dict_factory


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



# Fonction pour récupérer les données de la base de données
def get_data(player_id, gamemode):
    conn = sqlite3.connect('db/mmr_database.db')
    c = conn.cursor()
    c.execute("SELECT mmr, timestamp FROM mmr_data WHERE player_id = ? AND gamemode = ? ORDER BY timestamp", (player_id, gamemode))
    data = c.fetchall()
    conn.close()
    return data

def get_historique(player_id):
    conn = sqlite3.connect('db/mmr_database.db')
    c = conn.cursor()
    c.execute("SELECT gamemode, mmr FROM mmr_data WHERE player_id = ?", (player_id,))
    data = c.fetchall()
    conn.close()
    return data

# Fonction pour récupérer les données de la base de données
def get_all_player():
    conn = sqlite3.connect('db/player_database.db')
    c = conn.cursor()
    c.execute("SELECT player_id, player_name FROM player_data")
    data = c.fetchall()
    conn.close()
    return data

def get_player_details(player_id):
    conn = sqlite3.connect('db/player_database.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("SELECT player_id, player_name FROM player_data WHERE player_id = ?", (player_id,))
    player_details = c.fetchone()
    conn.close()
    return player_details

def get_possible_gamemode():
    conn = sqlite3.connect('db/mmr_database.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT gamemode FROM mmr_data;")
    data = c.fetchall()
    conn.close()
    return data

def get_all_ranks(player_id):
    conn = sqlite3.connect('db/mmr_database.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("SELECT gamemode, MAX(timestamp) as timestamp_atm_mmr, mmr  FROM mmr_data WHERE player_id = ? GROUP BY gamemode ", (player_id,))
    ranks_atm = c.fetchall()
    print(ranks_atm)
    c.execute("SELECT gamemode, MAX(mmr) as max_mmr, timestamp as max_mmr_timestamp FROM mmr_data WHERE player_id = ? GROUP BY gamemode", (player_id,))
    ranks_max = c.fetchall()
    print(ranks_max)
    
    mmr_dict = {entry['gamemode']: entry for entry in ranks_max}

    for entry in ranks_atm:
        gamemode = entry['gamemode']
        max_mmr_entry = mmr_dict.get(gamemode)
        if max_mmr_entry:
            entry.update(max_mmr_entry)

    print(ranks_atm)

    conn.close()
    return ranks_atm



from models.player_metadata import players_stats
from services.database_Service import conn as db_conn
from sqlalchemy import text,Table, Column, Integer, String, MetaData, Float

def get_l1_l2(limit: int, page: int) -> (int, int):
    l2 = (page * limit)
    l1 = l2 - limit
    return (l1, l2)

def get_player_information_normal(limit: int, page: int):
    l1, l2 = get_l1_l2(limit, page)
    query = text("SELECT * FROM players_stats ORDER BY id LIMIT :l1,:l2")
    players = []
    try:
        result = db_conn.execute(query, {"l1": l2, "l2": l2})
        for player in result:
            tpi = player["TS%"] + player["3PAr"] + player["FTr"] + player["ORB%"] + player["DRB%"] + player["TRB%"] + \
                  player["AST%"]
            tpi += player["STL%"] + player["BLK%"] + player["TOV%"] + player["USG%"] + player["OWS"] + player["DWS"]
            tpi += player["WS"] + player["WS/48"] + player["OBPM"] + player["DBPM"] + player["BPM"] + player["VORP"]
            tpi /= 20
            players.append({
                "id": player["id"],
                "Rk": player["Rk"],
                "Player": player["Player"],
                "Pos": player["Pos"],
                "Age": player["Age"],
                "Tm": player["Tm"],
                "tpi": tpi
            })
        return {
            "msg": "success",
            "data": players
        }
    except:
        return {
            "msg": "Bad Request"
        }, 500


def get_player_information_by_name(limit: int, page: int, player_name: str):
    l1, l2 = get_l1_l2(limit, page)
    query = text("SELECT * FROM players_stats WHERE Player LIKE :name;")
    players = []
    result = db_conn.execute(query, {"name": f"%{player_name}%"})
    for player in result:
        print(player)
        tpi = player["TS%"] + player["3PAr"] + player["FTr"] + player["ORB%"] + player["DRB%"] + player["TRB%"] + \
              player["AST%"]
        tpi += player["STL%"] + player["BLK%"] + player["TOV%"] + player["USG%"] + player["OWS"] + player["DWS"]
        tpi += player["WS"] + player["WS/48"] + player["OBPM"] + player["DBPM"] + player["BPM"] + player["VORP"]
        tpi /= 20
        players.append({
            "id": player["id"],
            "Rk": player["Rk"],
            "Player": player["Player"],
            "Pos": player["Pos"],
            "Age": player["Age"],
            "Tm": player["Tm"],
            "tpi": tpi
        })
    return {
        "msg": "success",
        "data": players
    }
    try:
        result = db_conn.execute(query, {"l1": l2, "l2": l2})
        for player in result:
            tpi = player["TS%"] + player["3PAr"] + player["FTr"] + player["ORB%"] + player["DRB%"] + player["TRB%"] + \
                  player["AST%"]
            tpi += player["STL%"] + player["BLK%"] + player["TOV%"] + player["USG%"] + player["OWS"] + player["DWS"]
            tpi += player["WS"] + player["WS/48"] + player["OBPM"] + player["DBPM"] + player["BPM"] + player["VORP"]
            tpi /= 20
            players.append({
                "id": player["id"],
                "Rk": player["Rk"],
                "Player": player["Player"],
                "Pos": player["Pos"],
                "Age": player["Age"],
                "Tm": player["Tm"],
                "tpi": tpi
            })
        return {
            "msg": "success",
            "data": players
        }
    except:
        return {
            "msg": "Bad Request"
        }, 500


def add_new_player(data):
    try:
        values = {
            'Rk': int(data["Rk"]),
            'Player': data["Player"],
            'Pos': data["Pos"],
            'Age': int(data["Age"]),
            'Tm': data["Tm"],
            'G': data["G"],
            'MP': 3623,
            'PER': 31.7,
            'TS%': 0.6,
            '3PAr': 0.021,
            'FTr': 0.4,
            'ORB%': 4.4,
            'DRB%': 23.5,
            'TRB%': 13.9,
            'AST%': 30.5,
            'STL%': 3.1,
            'BLK%': 1.5,
            'TOV%': 11.2,
            'USG%': 33.9,
            'OWS': 18.0,
            'DWS': 3.2,
            'WS': 21.2,
            'WS/48': 0.27,
            'OBPM': 14.7,
            'DBPM': 3.2,
            'BPM': 17.9,
            'VORP': 12.7
        }
        result = db_conn.execute(players_stats.insert().values(values))
        if result.rowcount > 0:
            return {
                "msg": "Success"
            }
        return {
            "msg": "Fail to add Player"
        }, 500
    except:
        return {
            "msg": "Internal Server Error"
        }, 500

def update_player_name(player_rk: int, new_name: str):
    query = text("UPDATE players_stats SET Player = :new_name WHERE Rk = :rk;")
    try:
        result = db_conn.execute(query, {"new_name": new_name, "rk": player_rk})
        if result.rowcount > 0:
            return {
                "msg": "Success, Player name has been updated!"
            }
        return  {
            "msg": "Rk not found"
        }, 404
    except:
        return  {
            "msg": "Update Player Gagal"
        }, 500
    pass

def delete_player_info(player_rk: int):
    query = text("DELETE FROM players_stats WHERE Rk = :rk;")
    try:
        result = db_conn.execute(query, {"rk": player_rk})
        print()
        if result.rowcount < 1:
            return {
                "msg": "Fails, Player is not deleted"
            }, 300
        return {
                   "msg": "Success, Player has been deleted"
               }, 200
    except:
        return {
                   "msg": "Fails, Player is not deleted"
               }, 300

from services.database_Service import conn as db_conn
from sqlalchemy import text

def get_l1_l2(limit: int, page: int) -> (int, int):
    l2 = page * limit
    l1 = l2 - limit
    return (l1, l2)

def get_player_information_normal(limit: int, page: int):
    l1, l2 = get_l1_l2(limit, page)
    query = text("SELECT * FROM players_stats LIMIT :l1,:l2")
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
    query = text("SELECT * FROM players_stats WHERE Player LIKE :name LIMIT :l1,:l2")
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

def add_new_player(rk: int, player_name: str):
    pass

def update_player_name(player_rk: int, new_name: str):
    pass

def delete_player_info(player_rk: int):
    query = text("DELETE FROM players_stats WHERE Rk = :rk;")
    try:
        result = db_conn.execute(query, {"rk": player_rk})
        if result.rowcount > 0:
            return
        return
    except:
        return

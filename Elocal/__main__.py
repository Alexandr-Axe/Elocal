from datetime import date
from fencing_elo.db import init_db, insert_player, get_player_by_id, get_all_players

init_db()

print(f"Hráč ID 1: {get_player_by_id(1)}")
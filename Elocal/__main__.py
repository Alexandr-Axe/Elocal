from fencing_elo.db import init_db, insert_player, get_player_by_id, get_all_players, delete_duplicate_players, get_player_by_name
from fencing_elo.services import calculate_k_factor, record_match

init_db()

for player in get_all_players():
    print(f"{player.first_name} {player.last_name}: ELO {player.current_elo}")
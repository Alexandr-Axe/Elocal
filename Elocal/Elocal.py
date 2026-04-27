from calculator import *

player_rating = 1309
opponent_rating = 1297
player_k = calculate_k_factor(player_rating, None)
index = -15

new_player_rating = calculate_new_elo(player_rating, opponent_rating, index, player_k)
print(f"Old player rating: {player_rating}")
print(f"Change of ELO: {new_player_rating - player_rating}")
print(f"New player rating: {new_player_rating}")
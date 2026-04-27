from datetime import date

from .elo_core import calculate_new_elo
from .k_factor import calculate_k_factor
from .db import get_connection
from .models import Player


def update_player_elo(player: Player,
                      opponent: Player,
                      index: int,
                      match_date: date) -> Player:
    """
    Calculates the new Elo rating for a player after a match and returns the updated player.
    """
    k = calculate_k_factor(player.current_elo, player.last_match_date or match_date, today=match_date)
    new_elo = calculate_new_elo(
        player_rating=player.current_elo,
        opponent_rating=opponent.current_elo,
        index=index,
        k=k,
    )

    player.current_elo = new_elo
    player.max_elo = max(player.max_elo, new_elo)
    player.last_match_date = match_date
    return player
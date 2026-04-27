from datetime import date

from .elo_core import calculate_new_elo
from .k_factor import calculate_k_factor
from .db import get_connection, get_player_by_id, update_player, insert_match
from .models import Player


def update_player_elo(player: Player,
                      opponent: Player,
                      index: int,
                      match_date: date) -> Player:
    """
    Calculates the new Elo rating for a player after a match and returns the updated player.
    """
    k = calculate_k_factor(
        player.current_elo,
        player.last_match_date or match_date,
        today=match_date
    )

    new_elo = calculate_new_elo(
        player_rating=player.current_elo,
        opponent_rating=opponent.current_elo,
        index=index,
        k_factor=k,
    )

    if player.first_match_date is None:
        player.first_match_date = match_date

    player.current_elo = new_elo
    player.max_elo = max(player.max_elo, new_elo)
    player.last_match_date = match_date
    return player


def record_match(player_a_id: int,
                 player_b_id: int,
                 index_a: int,
                 match_date: date) -> int:
    """
    Records a match, recalculates both players' Elo, updates them in the database,
    stores the match, and returns the created match ID.

    index_a:
    - positive => player A won
    - negative => player A lost
    """
    index_b = -index_a

    conn = get_connection()
    try:
        player_a = get_player_by_id(player_a_id, conn=conn)
        player_b = get_player_by_id(player_b_id, conn=conn)

        if player_a is None:
            raise ValueError(f"Player A with id {player_a_id} was not found.")
        if player_b is None:
            raise ValueError(f"Player B with id {player_b_id} was not found.")
        if player_a_id == player_b_id:
            raise ValueError("A player cannot fence against themselves.")
        if index_a == 0:
            raise ValueError("Index cannot be zero. A match must have a winner and a loser.")

        original_a_elo = player_a.current_elo
        original_b_elo = player_b.current_elo

        updated_a = update_player_elo(player_a, player_b, index_a, match_date)
        updated_b = update_player_elo(player_b, player_a, index_b, match_date)

        update_player(updated_a, conn=conn)
        update_player(updated_b, conn=conn)

        match_id = insert_match(
            match_date=match_date,
            player_a_id=player_a_id,
            player_b_id=player_b_id,
            index_a=index_a,
            index_b=index_b,
            conn=conn
        )

        conn.commit()

        print(
            f"Match recorded. "
            f"A: {original_a_elo} -> {updated_a.current_elo}, "
            f"B: {original_b_elo} -> {updated_b.current_elo}"
        )

        return match_id

    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
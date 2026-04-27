import math

def calculate_win_likelihood(player_rating, opponent_rating):
    """
    Calculate the likelihood of a player winning against an opponent based on their ratings.
    
    Parameters:
    player_rating (float): The rating of the player.
    opponent_rating (float): The rating of the opponent.
    
    Returns:
    float: The likelihood of the player winning, expressed as a percentage.
    """
    # Calculation based on the FIDE Elo rating system with logistic function

    scale = 400
    base = 10
    R_b = opponent_rating
    R_a = player_rating

    power = (R_b - R_a) / scale
    denominator = 1 + math.pow(base, power)

    expected_score = 1 / denominator
    
    return expected_score
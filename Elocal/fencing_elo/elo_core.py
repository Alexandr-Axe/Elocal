import math
from datetime import date

def calculate_win_likelihood(player_rating, opponent_rating):
    """
    Calculate the likelihood of a player winning against an opponent based on their ratings.
    
    Parameters:
    player_rating (int): The rating of the player.
    opponent_rating (int): The rating of the opponent.
    
    Returns:
    float: The likelihood of the player winning.
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

def calculate_margin_multiplier(index):
    """
    Calculate a margin-of-victory multiplier based on the combat outcome difference (index).

    This function increases the impact of a result on the rating update when the
    fight is won or lost by a larger margin.

    The formula is:
        m = 1 + 0.5 * (1 - exp(-|index| / 4))

    Parameters:
    index (int): Score difference between given and received points.

    Returns:
    float: Margin multiplier m >= 1, where:
           - m is close to 1 for small margins,
           - m approaches 1.5 for very large margins.
    """

    x = abs(index)

    return 1 + 0.5 * (1 - math.exp(-x / 4))

def calculate_new_elo(player_rating, opponent_rating, index, k_factor = 40):
    """
    Calculate the new Elo rating for a player after a match.
    
    Parameters:
    player_rating (int): The current rating of the player.
    opponent_rating (int): The rating of the opponent.
    index (int): Score difference between given and received points.
    k_factor (int): The K-factor to use in the calculation.
    
    Returns:
    int: The new Elo rating for the player.
    """
    expected_score = calculate_win_likelihood(player_rating, opponent_rating)
    score = 1 if index > 0 else 0
    margin_multiplier = calculate_margin_multiplier(index)
    
    elo_change = k_factor * margin_multiplier * (score - expected_score)
    new_rating = round(player_rating + elo_change)
    
    return new_rating
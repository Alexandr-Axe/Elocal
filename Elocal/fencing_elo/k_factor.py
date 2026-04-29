from datetime import date

def calculate_k_factor(player_rating, first_tournament_date, today=None):
    """
    Calculate the K-factor (coefficient of growth) for a player based on their rating and fencing period.
    Rules:
    - If the player has ELO > 2399, K = 24.
    - If the player has ELO <= 2399, K is determined by the time since their first tournament:
    0 years or less: K = 40
    1 year: K = 39
    2 years: K = 38
    3 years: K = 36
    4 years: K = 34
    ...
    minimum is 24
    
    Parameters:
    player_rating (int): The rating of the player.
    
    Returns:
    int: The K-factor for the player.
    """

    if today is None:
        today = date.today()

    if first_tournament_date is None:
        return 40

    if player_rating >= 2400:
        return 24

    days_since_first_tournament = (today - first_tournament_date).days
    years_since_first_tournament = days_since_first_tournament // 365

    if years_since_first_tournament <= 0:
        return 40
    elif years_since_first_tournament == 1:
        return 39
    elif years_since_first_tournament == 2:
        return 38
    else:
        k = 38 - 2 * (years_since_first_tournament - 2)
        return max(24, k)
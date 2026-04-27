from dataclasses import dataclass
from datetime import date

@dataclass
class Player:
    id: int | None
    first_name: str
    last_name: str
    team: str | None
    first_match_date: date | None
    last_match_date: date | None
    current_elo: int
    max_elo: int


@dataclass
class Match:
    id: int | None
    date: date
    player_a_id: int
    player_b_id: int
    index_a: int
    index_b: int
import sqlite3
from pathlib import Path
from datetime import date
from typing import Optional, List

from .models import Player, Match

# Base directory of the project (two levels up from this file)
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "fencing_elo.db"


def get_connection() -> sqlite3.Connection:
    """
    Open a SQLite connection to the fencing_elo database.
    Ensures the data directory exists.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    """
    Create the database tables if they do not exist.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            team TEXT,
            first_match_date TEXT,
            last_match_date TEXT,
            current_elo REAL NOT NULL,
            max_elo REAL NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            player_a_id INTEGER NOT NULL,
            player_b_id INTEGER NOT NULL,
            index_a INTEGER NOT NULL,
            index_b INTEGER NOT NULL,
            FOREIGN KEY (player_a_id) REFERENCES players(id),
            FOREIGN KEY (player_b_id) REFERENCES players(id)
        )
    """)

    conn.commit()
    conn.close()

def row_to_player(row: sqlite3.Row) -> Player:
    """
    Convert a DB row into a Player dataclass instance.
    """
    return Player(
        id=row["id"],
        first_name=row["first_name"],
        last_name=row["last_name"],
        team=row["team"],
        first_match_date=date.fromisoformat(row["first_match_date"])
        if row["first_match_date"] else None,
        last_match_date=date.fromisoformat(row["last_match_date"])
        if row["last_match_date"] else None,
        current_elo=row["current_elo"],
        max_elo=row["max_elo"],
    )


def row_to_match(row: sqlite3.Row) -> Match:
    """
    Convert a DB row into a Match dataclass instance.
    """
    return Match(
        id=row["id"],
        date=date.fromisoformat(row["date"]),
        player_a_id=row["player_a_id"],
        player_b_id=row["player_b_id"],
        index_a=row["index_a"],
        index_b=row["index_b"],
    )

def insert_player(first_name: str,
                  last_name: str,
                  team: Optional[str] = None,
                  first_match_date: Optional[date] = None,
                  last_match_date: Optional[date] = None,
                  current_elo: float = 1000.0,
                  max_elo: float = 1000.0) -> int:
    """
    Insert a new player and return its ID.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO players (
            first_name,
            last_name,
            team,
            first_match_date,
            last_match_date,
            current_elo,
            max_elo
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        first_name,
        last_name,
        team,
        first_match_date.isoformat() if first_match_date else None,
        last_match_date.isoformat() if last_match_date else None,
        current_elo,
        max_elo,
    ))

    conn.commit()
    player_id = cur.lastrowid
    conn.close()
    return player_id


def get_player_by_id(player_id: int,
                     conn: Optional[sqlite3.Connection] = None) -> Optional[Player]:
    """
    Fetch a player by ID. If conn is provided, it is reused (no closing).
    """
    owns_connection = conn is None
    if conn is None:
        conn = get_connection()

    cur = conn.cursor()
    cur.execute("SELECT * FROM players WHERE id = ? ORDER BY last_name, first_name", (player_id,))
    row = cur.fetchone()

    if owns_connection:
        conn.close()

    if row is None:
        return None

    return row_to_player(row)


def get_all_players() -> List[Player]:
    """
    Return all players ordered by last_name, first_name.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM players ORDER BY last_name, first_name")
    rows = cur.fetchall()
    conn.close()

    return [row_to_player(row) for row in rows]


def update_player(player: Player,
                  conn: Optional[sqlite3.Connection] = None) -> None:
    """
    Update an existing player in the database.
    If conn is provided, commit/close is handled by the caller.
    """
    if player.id is None:
        raise ValueError("Cannot update player without id.")

    owns_connection = conn is None
    if conn is None:
        conn = get_connection()

    cur = conn.cursor()
    cur.execute("""
        UPDATE players
        SET
            first_name = ?,
            last_name = ?,
            team = ?,
            first_match_date = ?,
            last_match_date = ?,
            current_elo = ?,
            max_elo = ?
        WHERE id = ?
    """, (
        player.first_name,
        player.last_name,
        player.team,
        player.first_match_date.isoformat() if player.first_match_date else None,
        player.last_match_date.isoformat() if player.last_match_date else None,
        player.current_elo,
        player.max_elo,
        player.id,
    ))

    if owns_connection:
        conn.commit()
        conn.close()

def insert_match(match_date: date,
                 player_a_id: int,
                 player_b_id: int,
                 index_a: int,
                 conn: Optional[sqlite3.Connection] = None) -> int:
    """
    Insert a match into the database.

    Only index_a is required; index_b is automatically computed as -index_a.
    """
    if player_a_id == player_b_id:
        raise ValueError("player_a_id and player_b_id must be different.")

    if index_a == 0:
        raise ValueError("index_a cannot be zero; there must be a winner and a loser.")

    index_b = -index_a

    owns_connection = conn is None
    if conn is None:
        conn = get_connection()

    cur = conn.cursor()
    cur.execute("""
        INSERT INTO matches (date, player_a_id, player_b_id, index_a, index_b)
        VALUES (?, ?, ?, ?, ?)
    """, (
        match_date.isoformat(),
        player_a_id,
        player_b_id,
        index_a,
        index_b,
    ))

    match_id = cur.lastrowid

    if owns_connection:
        conn.commit()
        conn.close()

    return match_id


def get_matches_for_player(player_id: int) -> List[Match]:
    """
    Return all matches where the player participated (as A or B).
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM matches
        WHERE player_a_id = ? OR player_b_id = ?
        ORDER BY date
    """, (player_id, player_id))

    rows = cur.fetchall()
    conn.close()

    return [row_to_match(row) for row in rows]
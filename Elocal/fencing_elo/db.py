import sqlite3
from pathlib import Path
from datetime import date
from typing import Iterable, Optional

from .models import Player, Match

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "fencing_elo.db"

def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
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
        current_elo INTEGER NOT NULL,
        max_elo INTEGER NOT NULL
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

def insert_player(first_name: str,
                  last_name: str,
                  team: Optional[str] = None,
                  first_match_date: Optional[date] = None,
                  last_match_date: Optional[date] = None,
                  current_elo: float = 1000,
                  max_elo: float = 1000) -> int:
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
    ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        first_name,
        last_name,
        team,
        first_match_date.isoformat() if first_match_date else None,
        last_match_date.isoformat() if last_match_date else None,
        current_elo,
        max_elo
    ))

    conn.commit()
    player_id = cur.lastrowid
    conn.close()
    return player_id


def row_to_player(row) -> Player:
    return Player(
        id=row["id"],
        first_name=row["first_name"],
        last_name=row["last_name"],
        team=row["team"],
        first_match_date=date.fromisoformat(row["first_match_date"]) if row["first_match_date"] else None,
        last_match_date=date.fromisoformat(row["last_match_date"]) if row["last_match_date"] else None,
        current_elo=row["current_elo"],
        max_elo=row["max_elo"]
    )


def get_player_by_id(player_id: int) -> Optional[Player]:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM players WHERE id = ?", (player_id,))
    row = cur.fetchone()

    conn.close()

    if row is None:
        return None

    return row_to_player(row)


def get_all_players() -> list[Player]:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM players ORDER BY last_name, first_name")
    rows = cur.fetchall()

    conn.close()

    return [row_to_player(row) for row in rows]
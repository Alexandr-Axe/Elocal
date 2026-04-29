# Elocal — Fencing ELO

A small tool for managing fencers' ELO ratings and storing matches in a SQLite database.

## Features
- Store players and matches in a local SQLite database (`data/fencing_elo.db`)
- Basic operations: insert player, get player, stored matches
- ELO calculations (services module)

## Requirements
- Python 3.10 or newer (uses PEP 604 union operator `|`)
- No external dependencies (uses `sqlite3` and standard library), unless otherwise specified

## Installation / Quick start
1. Clone the repository:
   git clone https://github.com/USERNAME/REPO.git
2. Create and activate a virtual environment (recommended):
   python -m venv .venv
   - Windows: `.venv\Scripts\activate`
   - Unix/macOS: `source .venv/bin/activate`
3. (Optional) Install dependencies:
   pip install -r requirements.txt
4. Run the application:
   - From the package: `python -m Elocal`
   - Or directly: `python __main__.py`

On run, the SQLite database should be created in the `data/` folder (depending on implementation).

## Project structure (selected files)
- `Elocal/` — main package
  - `__main__.py` — example launcher (DB initialization, inserting sample players)
  - `fencing_elo/db.py` — database access (connection, CRUD)
  - `fencing_elo/models.py` — data models (`Player`, `Match`)
  - `fencing_elo/services.py` — business logic (e.g., ELO calculation, recording a match)

## Database
- Location: `data/fencing_elo.db` (relative to the repository)
- Uses SQLite (`sqlite3`). Initialization scripts should create `players` and `matches` tables.

## Running tests
- If there are tests (e.g., in `tests/`), run:
  pytest

## Contributing
- Send pull requests and issues with bug reports or improvement suggestions.
- Keep code clean and add tests for new functionality.

## License
- Specify the license here (e.g., MIT). If none, add a `LICENSE` file.

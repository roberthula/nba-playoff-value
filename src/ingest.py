"""
src/ingest.py
-------------
Download Basketball-Reference *advanced* stats CSVs (2000-2024) for both
regular season and playoffs, store the raw files under data/raw/, and
bulk-load them into DuckDB tables (adv_regular, adv_playoffs).

Usage:
    python src/ingest.py
"""

from __future__ import annotations

import pathlib
import time
from typing import Literal

import duckdb
import pandas as pd
import requests
 
 
START_YEAR: int = 2000
END_YEAR: int = 2024
RAW_DIR = pathlib.Path("data/raw")          # CSVs land here
DB_FILE = pathlib.Path("nba.duckdb")        # DuckDB database file
BASE = "https://www.basketball-reference.com"
HEADERS = {"User-Agent": "Mozilla/5.0"}     # polite header
SLEEP = 1.0                                 # seconds between requests
 


def csv_url(year: int, playoffs: bool) -> str:
    path = (
        f"leagues/NBA_{year}_advanced.csv"
        if not playoffs
        else f"playoffs/NBA_{year}_advanced.csv"
    )
    return f"{BASE}/{path}"


def download_csv(year: int, playoffs: bool) -> pathlib.Path:
    """Download one CSV and return the local file path."""
    url = csv_url(year, playoffs)
    subdir = "playoffs" if playoffs else "regular"
    out_path = RAW_DIR / subdir / f"{year}.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"↳ {url}")
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()

    # Write directly to disk
    out_path.write_bytes(r.content)
    time.sleep(SLEEP)
    return out_path


def download_all() -> None:
    for yr in range(START_YEAR, END_YEAR + 1):
        for po in (False, True):
            download_csv(yr, po)


def load_duckdb() -> None:
    con = duckdb.connect(DB_FILE)

    # Drop & recreate tables each run (idempotent ingest)
    con.execute("DROP TABLE IF EXISTS adv_regular;")
    con.execute("DROP TABLE IF EXISTS adv_playoffs;")

    con.execute(
        """
        CREATE TABLE adv_regular AS
        SELECT * FROM read_csv_auto('data/raw/regular/*.csv');
        """
    )
    con.execute(
        """
        CREATE TABLE adv_playoffs AS
        SELECT * FROM read_csv_auto('data/raw/playoffs/*.csv');
        """
    )

    reg_rows, = con.execute("SELECT COUNT(*) FROM adv_regular").fetchone()
    po_rows,  = con.execute("SELECT COUNT(*) FROM adv_playoffs").fetchone()
    print(f"Rows loaded → {reg_rows} regular | {po_rows} playoffs")

    con.close()


def main(action: Literal["all", "download", "load"] = "all") -> None:
    if action in ("all", "download"):
        download_all()
    if action in ("all", "load"):
        load_duckdb()
    print("✓ Ingest complete → nba.duckdb")


if __name__ == "__main__":
    main()


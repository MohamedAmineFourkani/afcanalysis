import pandas as pd
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

def get_available_years():
    """Get list of available tournament years."""
    match_files = list((DATA_DIR / "matches").glob("afcon-matches-*.csv"))
    years = sorted([int(f.stem.split("-")[-1]) for f in match_files])
    return years

def load_matches(year=None):
    """Load match data for a given year or all years."""
    if year is None:
        files = sorted((DATA_DIR / "matches").glob("afcon-matches-*.csv"))
        dfs = [pd.read_csv(f) for f in files]
        df = pd.concat(dfs, ignore_index=True)
    else:
        filepath = DATA_DIR / "matches" / f"afcon-matches-{year}.csv"
        df = pd.read_csv(filepath)
    return df

def load_players(year=None):
    """Load player data for a given year or all years."""
    if year is None:
        files = sorted((DATA_DIR / "Players").glob("afcon-players-*.csv"))
        dfs = [pd.read_csv(f) for f in files]
        df = pd.concat(dfs, ignore_index=True)
    else:
        filepath = DATA_DIR / "Players" / f"afcon-players-{year}.csv"
        df = pd.read_csv(filepath)
    return df

def load_teams(year=None):
    """Load team data for a given year or all years."""
    files_to_load = []
    if year is None:
        for pattern in ["afcon-teams-*.csv", "afcon-teams2-*.csv"]:
            files_to_load.extend(sorted((DATA_DIR / "Teams").glob(pattern)))
        unique_files = list(set(files_to_load))
        unique_files.sort(key=lambda x: x.name)
        dfs = [pd.read_csv(f) for f in unique_files if f.stat().st_size > 100]
        df = pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
    else:
        filepath = DATA_DIR / "Teams" / f"afcon-teams-{year}.csv"
        if filepath.exists():
            df = pd.read_csv(filepath)
        else:
            filepath = DATA_DIR / "Teams" / f"afcon-teams2-{year}.csv"
            df = pd.read_csv(filepath) if filepath.exists() else pd.DataFrame()
    return df

def load_league(year=None):
    """Load league/tournament data."""
    if year is None:
        files = sorted((DATA_DIR / "League").glob("afcon-league-*.csv"))
        dfs = [pd.read_csv(f) for f in files]
        df = pd.concat(dfs, ignore_index=True)
    else:
        filepath = DATA_DIR / "League" / f"afcon-league-{year}.csv"
        df = pd.read_csv(filepath)
    return df
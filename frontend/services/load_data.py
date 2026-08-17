import pandas as pd
import streamlit as st
import os
DATA_PATH = "data/"


@st.cache_data
def load_teams_2526_2627_venues() -> pd.DataFrame:
    """
    Load teams and venues dataset of 5 popular leagues.

    Reads the CSV file containing stadium and venue information
    and returns it as a pandas DataFrame.

    Returns:
        pd.DataFrame: Venues dataset.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        RuntimeError: If the file cannot be read.
    """

    file_path = DATA_PATH + "all_teams_2526_2627_venues_fotmob.csv"

    # 🔹 Validate file existence
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Teams and venues 2025-26/2026-27 file not found: {file_path}")

    try:
        return pd.read_csv(file_path)

    except Exception as e:
        raise RuntimeError(f"Failed to load Teams and venues 2025-26/2026-27 dataset: {e}")

@st.cache_data
def load_all_matches_2526_whoscored() -> pd.DataFrame:
    """
    Load all matches dataset of 5 popular leagues in 2025-2026.

    Reads the CSV file containing stadium and venue information
    and returns it as a pandas DataFrame.

    Returns:
        pd.DataFrame: Venues dataset.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        RuntimeError: If the file cannot be read.
    """

    file_path = DATA_PATH + "all_matches_2526_whoscored.csv"

    # 🔹 Validate file existence
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"All matches dataset 2025-26 whoscored file not found: {file_path}")

    try:
        return pd.read_csv(file_path)

    except Exception as e:
        raise RuntimeError(f"Failed to load All matches dataset 2025-26 whoscored: {e}")

@st.cache_data
def load_all_matches_2627_whoscored() -> pd.DataFrame:
    """
    Load all matches dataset of 5 popular leagues in 2026-2027.

    Reads the CSV file containing stadium and venue information
    and returns it as a pandas DataFrame.

    Returns:
        pd.DataFrame: Venues dataset.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        RuntimeError: If the file cannot be read.
    """

    file_path = DATA_PATH + "all_matches_2627_whoscored.csv"

    # 🔹 Validate file existence
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"All matches dataset 2026-27 whoscored file not found: {file_path}")

    try:
        return pd.read_csv(file_path)

    except Exception as e:
        raise RuntimeError(f"Failed to load All matches dataset 2026-27 whoscored: {e}")
        
@st.cache_data
def load_all_matches_2526_fotmob() -> pd.DataFrame:
    """
    Load all matches dataset of 5 popular leagues in 2025-2026.

    Reads the CSV file containing stadium and venue information
    and returns it as a pandas DataFrame.

    Returns:
        pd.DataFrame: Venues dataset.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        RuntimeError: If the file cannot be read.
    """

    file_path = DATA_PATH + "all_matches_2526_fotmob.csv"

    # 🔹 Validate file existence
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"All matches dataset 2025-26 fotmob file not found: {file_path}")

    try:
        return pd.read_csv(file_path)

    except Exception as e:
        raise RuntimeError(f"Failed to load All matches dataset 2025-26 fotmob: {e}")
        
@st.cache_data
def load_all_matches_2627_fotmob() -> pd.DataFrame:
    """
    Load all matches dataset of 5 popular leagues in 2026-2027.

    Reads the CSV file containing stadium and venue information
    and returns it as a pandas DataFrame.

    Returns:
        pd.DataFrame: Venues dataset.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        RuntimeError: If the file cannot be read.
    """

    file_path = DATA_PATH + "all_matches_2627_fotmob.csv"

    # 🔹 Validate file existence
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"All matches dataset 2026-27 fotmob file not found: {file_path}")

    try:
        return pd.read_csv(file_path)

    except Exception as e:
        raise RuntimeError(f"Failed to load All matches dataset 2026-27 fotmob: {e}")


@st.cache_data
def liga_standings_tracker_raw_2526() -> pd.DataFrame:
    """
    Load Liga standings tracker raw dataset of 5 popular leagues.

    Reads the CSV file containing stadium and venue information
    and returns it as a pandas DataFrame.

    Returns:
        pd.DataFrame: Venues dataset.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        RuntimeError: If the file cannot be read.
    """

    file_path = DATA_PATH + "liga_standings_tracker_raw.csv"

    # 🔹 Validate file existence
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Liga standings tracker raw 2025-26 file not found: {file_path}")

    try:
        return pd.read_csv(file_path)

    except Exception as e:
        raise RuntimeError(f"Failed to load Liga standings tracker raw 2025-26 dataset: {e}")
                               
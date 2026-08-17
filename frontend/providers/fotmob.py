import pandas as pd
from selenium import webdriver
import numpy as np
from bs4 import BeautifulSoup
import time
import requests
from tqdm import tqdm
import streamlit as st

from frontend.utils.constants import *

def build_team_logo(ccode):

    if pd.isna(ccode):
        return None

    ccode = str(ccode).strip()

    # Si son letras (ESP, CZE, ARG...)
    if ccode.isalpha():
        return (f"https://images.fotmob.com/image_resources/logo/teamlogo/{ccode.lower()}.png")

    # Si es un id numérico de club
    return (f"https://images.fotmob.com/image_resources/logo/teamlogo/{ccode}.png")

@st.cache_data
def extract_all_players_fotmob(df_all_teams_league_venues_photo):
    # Obtener dataframe de equipos
    all_players = []

    for _, row in tqdm(df_all_teams_league_venues_photo.iterrows(), total=len(df_all_teams_league_venues_photo), desc="Descargando plantillas"):

        team_id = row["id_team_fotmob"]

        # Cambia "name" por el nombre real de la columna de equipo si es distinto
        team_name = row.get("name_team_fotmob", None)

        try:
            response = requests.get( f"https://www.fotmob.com/api/data/teams?id={team_id}&ccode3=ESP", timeout=10)
            response.raise_for_status()

            data = response.json()

            # Saltar equipos sin plantilla
            if (
                "squad" not in data
                or data["squad"] is None
                or "squad" not in data["squad"]
            ):
                continue

            # Secciones de la plantilla (Porteros, Defensas, etc.)
            squad_df = pd.json_normalize(data["squad"]["squad"])
            if squad_df.empty:
                continue

            squad_df = squad_df.explode("members").reset_index(drop=True)

            # Información de jugadores
            players_df = pd.json_normalize(squad_df["members"])

            # Unir posición/grupo con datos del jugador
            team_players = pd.concat( [squad_df[["title"]], players_df], axis=1)

            # Añadir información del equipo
            team_players["team_id"] = team_id
            team_players["team_name"] = team_name

            all_players.append(team_players)

        except Exception as e:
            print(f"❌ Error en equipo {team_id}: {e}")

    # Unir todos los jugadores
    final_df = pd.concat(all_players, ignore_index=True)

    # Eliminar columnas innecesarias si existen
    final_df = final_df.drop( columns=[ "title", "role.key", "injury","excludeFromRanking"], errors="ignore")
    final_df = final_df.dropna(subset=["id"])
    # URL de la foto del jugador
    final_df["member_photo"] = "https://images.fotmob.com/image_resources/playerimages/" + final_df["id"].astype(int).astype(str)+ ".png"
    final_df["team_logo"] = final_df["ccode"].apply(build_team_logo)
    final_df["id"] = final_df["id"].astype(float).astype(int).astype(str)

    # Opcional: reordenar columnas principales
    cols_first = [ "team_id", "team_name","id","name","positionId","shirtNumber","member_photo"]

    existing_cols = [c for c in cols_first if c in final_df.columns]
    remaining_cols = [c for c in final_df.columns if c not in existing_cols]

    final_df = final_df[existing_cols + remaining_cols]

    print(f"✅ Total jugadores: {len(final_df):,}")
    print(f"✅ Total equipos: {final_df['team_id'].nunique():,}")
    return final_df

#----------------------------STANDINGS--------------------------------------------------------------

@staticmethod
def emoji_from_color(color: str) -> str:
    return {
        "#2AD572": "🔵",  # Champions
        "#0046A7": "🟢",  # Europa League
        "#02CCF0": "🟣",  # Conference
        "#FF4646": "🔴",  # Descenso
    }.get(color, "⚪")   # Other colors

@staticmethod
def format_diff_xg(value):
    if value > 0:
        return f"<span style='color:green;'>+{float(value)}</span>"
    elif value < 0:
        return f"<span style='color:red;'>{float(value)}</span>"
    else:
        return f"<span style='color:gray;'>0</span>"

@staticmethod
def format_diff_xga(value):
    if value > 0:
        return f"<span style='color:red;'>+{float(value)}</span>"
    elif value < 0:
        return f"<span style='color:green;'>{float(value)}</span>"
    else:
        return f"<span style='color:gray;'>0</span>"

@staticmethod
def format_diff_xpts(value):
    if value > 0:
        return f"<span style='color:green;'>+{float(value)}</span>"
    elif value < 0:
        return f"<span style='color:red;'>{float(value)}</span>"
    else:
        return f"<span style='color:gray;'>0</span>"

@staticmethod
def format_pos_diff(diff):
    if diff > 0:
        return f"<span style='color:red;'>+{int(diff)} ▼</span>"
    elif diff < 0:
        return f"<span style='color:green;'>{int(diff)} ▲</span>"
    else:
        return f"<span style='color:gray;'>0</span>"

def obtener_tabla(data, color_map, tipo="all"):
    

    df = pd.DataFrame(data["table"][0]["data"]["table"][tipo])

    df[["goals_for", "goals_against"]] = df["scoresStr"].str.split("-", expand=True)
    df["competition"] = df["qualColor"].map(lambda x: color_map.get(x, {}).get("title"))
    df["team_logo"] = (
        "https://images.fotmob.com/image_resources/logo/teamlogo/"
        + df["id"].astype(str)
        + ".png"
    )
    df= df.drop(columns=["scoresStr","pageUrl", "deduction", "ongoing", "goalsScored"], errors="ignore")
    return df

def extract_info_opponent(data):

    next_opponent = data["table"][0].get("nextOpponent")

    if not next_opponent:
        return pd.DataFrame()

    df = pd.DataFrame([
        {
            "id": int(team_id),
            "opponent_id": info[0],
            "opponent_name": info[4]["name"],
            "kickoff": info[5],
        }
        for team_id, info in next_opponent.items()
    ])

    df["kickoff"] = pd.to_datetime(df["kickoff"], utc=True)
    df["kickoff"] = df["kickoff"].dt.tz_convert("Europe/Madrid")

    df["match_date"] = df["kickoff"].dt.date
    df["match_time"] = df["kickoff"].dt.strftime("%H:%M")
    df["team_logo_url_opponent"] = "https://images.fotmob.com/image_resources/logo/teamlogo/" + df["opponent_id"].astype(str) + ".png"
    

    return df.drop(columns=["kickoff"])

def extract_data_json_standings(temporada,league):
    BASE_URL = "https://www.fotmob.com/api/data/leagues"

    ligas = {
        "Premier League": {"id": 47, "pais": "ENG"},
        "LaLiga": {"id": 87, "pais": "ESP"},
        "Serie A": {"id": 55, "pais": "ITA"},
        "Bundesliga": {"id": 54, "pais": "GER"},
        "Ligue 1": {"id": 53, "pais": "FRA"},
    }

    id_liga= ligas[league]['id']

    params = {"id": id_liga, "ccode3": "ESP", "season": temporada}
    r = requests.get(BASE_URL, params=params)
    r.raise_for_status()
    data = r.json()

    legend= pd.DataFrame(data['table'][0]['data']['legend'])
    color_map = {item["color"]: {  "title": item["title"]} for item in legend.to_dict("records")}
    return data, color_map

#----------------------------TEAM OF THE WEEKS--------------------------------------------------------------
@st.cache_data
def obtener_totw_jornada(id_liga, round_id, season="2025/2026", mapa_equipos=None):
    """Descarga el Equipo de la Semana de UNA jornada concreta."""
    params = {"leagueId": id_liga, "roundId": round_id, "season": season}
    r = requests.get(TOTW_URL, params=params)
    if r.status_code != 200:
        return None

    data = r.json()
    if not isinstance(data, list) or not data:
        return None
    filas = []
    for jugador in data:
        nombre = jugador.get("name", {}) or {}
        rating = jugador.get("rating", {}) or {}
        layout = jugador.get("verticalLayout", {}) or {}
        team_id = jugador.get("teamId")
        is_top = jugador.get("isTopPlayer", {}) or {}

        filas.append({
            "player_id": jugador.get("id"),
            "player": nombre.get("fullName"),
            "rating": rating.get("num"),
            "rating.bgcolor": rating.get("bgcolor"),
            "teamId": team_id,
            "team": (mapa_equipos or {}).get(team_id),
            "pos_x": layout.get("x"),
            "pos_y": layout.get("y"),
            "matchId": jugador.get("matchId"),
            "isTopPlayer": is_top.get("isTopPlayer"),
            "isTots": jugador.get("isTots"),
            "matchweek": round_id,
        })

    df = pd.DataFrame(filas)
    df = df.drop(columns="isTots", errors="ignore")
    df["season"] = season
    return df

@st.cache_data
def mapa_equipos_liga(id_liga, season="2025/2026", pais="ESP"):
    """
    Usa la tabla de clasificación (que ya sabemos leer bien) para
    construir un diccionario {teamId: nombre_equipo}.
    """
    params = {"id": id_liga, "ccode3": pais, "season": season}
    r = requests.get("https://www.fotmob.com/api/data/leagues", params=params)
    r.raise_for_status()
    data = r.json()

    tablas = data.get("table", [])
    for bloque in tablas:
        tabla_obj = bloque.get("data", {}).get("table", {})
        filas_all = tabla_obj.get("all")
        if filas_all:
            return {f["id"]: f["name"] for f in filas_all if "id" in f and "name" in f}
    return {}

@st.cache_data
def obtener_totw_temporada(nombre_liga, id_liga, num_rondas, season="2025/2026", pais="ESP", pausa=0.3, debug=False):
    """
    Descarga el Equipo de la Semana de TODAS las jornadas de la temporada
    para una liga, y lo devuelve como un único DataFrame.
    """
    mapa_equipos = mapa_equipos_liga(id_liga, season, pais)

    dfs = []
    rondas = list(range(1, num_rondas + 1)) + ["TOTS"]

    for ronda in rondas:
        df_ronda = obtener_totw_jornada(id_liga, ronda, season, mapa_equipos)
        df_ronda["matchweek"] = "Team of the Season"if ronda == "TOTS" else ronda
        if df_ronda is not None:
            df_ronda["league"] = nombre_liga
            df_ronda['url_logo_team'] =  "https://images.fotmob.com/image_resources/logo/teamlogo/"+ df_ronda['teamId'].astype(str) + ".png"
            df_ronda["member_photo"] = "https://images.fotmob.com/image_resources/playerimages/" + df_ronda["player_id"].astype(int).astype(str)+ ".png"
            dfs.append(df_ronda)
            if debug:
                print(f"  ✔ {nombre_liga} jornada {ronda}: {len(df_ronda)} jugadores")
        else:
            if debug:
                print(f"  — {nombre_liga} jornada {ronda}: sin datos (aún no jugada o no disponible)")
        time.sleep(pausa)  # para no machacar la API con requests seguidos

    if not dfs:
        return pd.DataFrame()

    return pd.concat(dfs, ignore_index=True)

@st.cache_data
def totw_global_temporada(df_totw_temporada):
    """
    A partir del DataFrame de todas las jornadas de una liga, calcula
    el 'global' de temporada: cuántas veces ha entrado cada jugador
    en el Equipo de la Semana, con su rating medio.
    """
    if df_totw_temporada.empty:
        return pd.DataFrame()

    resumen = (
        df_totw_temporada
        .assign(rating=pd.to_numeric(df_totw_temporada["rating"], errors="coerce"))
        .groupby(["player_id", "player", "team", "league"], as_index=False)
        .agg(veces_en_totw=("matchweek", "count"), rating_medio=("rating", "mean"))
        .sort_values(["veces_en_totw", "rating_medio"], ascending=[False, False])
        .reset_index(drop=True)
    )
    return resumen


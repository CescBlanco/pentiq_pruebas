from supabase_bbdd.database import supabase
import streamlit as st

def insert_teams_venues_2526_2627(teams):
    response = (
        supabase
        .table("teams_venues_2526_2627")
        .upsert(
            teams,
            on_conflict="id_team_fotmob,season"
        )
        .execute()
    )

    return response


@st.cache_data()
def get_all_teams_venues_2526_2627():

    response = (
        supabase
        .table("teams_venues_2526_2627")
        .select("*")
        .execute()
    )

    return response.data


@st.cache_data()
def check_teams_venues_2526_2627_exists(season, leagues):

    response = (
        supabase
        .table("teams_venues_2526_2627")
        .select("id_team_fotmob")
        .eq("season", season)
        .in_("name_league_fotmob", leagues)
        .execute()
    )

    return len(response.data) > 0

def insert_matches_whoscored202526(matches):

    response = (
        supabase
        .table("matches_whoscored_202526")
        .upsert(
            matches,
            on_conflict="match_id"
        )
        .execute()
    )

    return response

@st.cache_data()
def get_all_matches_whoscored202526():

    response = (
        supabase
        .table("matches_whoscored_202526")
        .select("*")
        .execute()
    )

    return response.data

@st.cache_data()
def check_matches_exists202526(season, leagues):

    response = (
        supabase
        .table("matches_whoscored_202526")
        .select("match_id")
        .eq("season", season)
        .in_("league_name", leagues)
        .execute()
    )

    return len(response.data) > 0


def insert_matches_whoscored202627(matches):

    response = (
        supabase
        .table("matches_whoscored_202627")
        .upsert(
            matches,
            on_conflict="match_id"
        )
        .execute()
    )

    return response

@st.cache_data()
def get_all_matches_whoscored202627():

    response = (
        supabase
        .table("matches_whoscored_202627")
        .select("*")
        .execute()
    )

    return response.data

@st.cache_data()
def check_matches_exists202627(season, leagues):

    response = (
        supabase
        .table("matches_whoscored_202627")
        .select("match_id")
        .eq("season", season)
        .in_("league_name", leagues)
        .execute()
    )

    return len(response.data) > 0


def insert_matches_fotmob202526(matches):

    response = (
        supabase
        .table("matches_fotmob_202526")
        .upsert(
            matches,
            on_conflict="match_id"
        )
        .execute()
    )

    return response

@st.cache_data()
def get_all_matches_fotmob202526():

    response = (
        supabase
        .table("matches_fotmob_202526")
        .select("*")
        .execute()
    )

    return response.data

@st.cache_data()
def check_fotmob_matches_exists202526(season, leagues):

    response = (
        supabase
        .table("matches_fotmob_202526")
        .select("match_id")
        .eq("season", season)
        .in_("league_name", leagues)
        .execute()
    )

    return len(response.data) > 0


def insert_matches_fotmob202627(matches):

    response = (
        supabase
        .table("matches_fotmob_202627")
        .upsert(
            matches,
            on_conflict="match_id"
        )
        .execute()
    )

    return response

@st.cache_data()
def get_all_matches_fotmob202627():

    response = (
        supabase
        .table("matches_fotmob_202627")
        .select("*")
        .execute()
    )

    return response.data

@st.cache_data()
def check_fotmob_matches_exists202627(season, leagues):

    response = (
        supabase
        .table("matches_fotmob_202627")
        .select("match_id")
        .eq("season", season)
        .in_("league_name", leagues)
        .execute()
    )

    return len(response.data) > 0


#--------------------------------- TABLE STANDING TRACKER----------------------------------
def insert_standings_tracker_2526(data):
    response = (
        supabase
        .table("liga_standings_tracker_raw_2526")
        .upsert(
            data,
            on_conflict="matchweek,team,league,season"
        )
        .execute()
    )

    return response


@st.cache_data()
def get_standings_tracker_2526():

    all_data = []
    start = 0
    batch_size = 1000

    while True:

        response = (
            supabase
            .table("liga_standings_tracker_raw_2526")
            .select("*")
            .range(start, start + batch_size - 1)
            .execute()
        )

        data = response.data

        if not data:
            break

        all_data.extend(data)

        # Si devuelve menos registros que el tamaño del bloque,
        # significa que ya hemos llegado al final
        if len(data) < batch_size:
            break

        start += batch_size

    print("Total registros recuperados:", len(all_data))

    return all_data

@st.cache_data()
def check_standings_tracker_exists_2526(season, league):
    response = (
        supabase
        .table("liga_standings_tracker_raw_2526")
        .select("id")
        .eq("league", league)
        .eq("season", season)
        .limit(1)
        .execute()
    )

    return len(response.data) > 0
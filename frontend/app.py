import streamlit as st
from streamlit_extras.avatar import *
from streamlit_card import card
from st_clickable_images import clickable_images

from utils.constants import *
from utils.config_app import *
from frontend.services.load_data import *
from frontend.providers.fotmob import *
from frontend.services import *
from frontend.supabase_bbdd.functions import *
from frontend.supabase_bbdd.bbdd_matches import *

from frontend.pages_buckup.teams import *
from frontend.pages_buckup.team_roster import render_team_roster
from frontend.pages_buckup.venues import *
from frontend.pages_buckup.standings import *
from frontend.pages_buckup.calendar import *
from frontend.pages_buckup.results import *

from datetime import time
import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch, Sbopen, FontManager, inset_image
from mplsoccer import Pitch
from matplotlib import patheffects
import matplotlib.patheffects as path_effects
background_color = '#0C0D0E'
text_color = 'white'
line_color = 'white'


st.set_page_config( page_title="PENTIQ",page_icon="data/logo_photo_pentiq.png", layout="wide")

# -----------------------------
# USUARIO
# -----------------------------

if "usuario" not in st.session_state:
    st.session_state.usuario = {
        "nombre": "Cesc",
        "apellido": "Blanco",
        "pais": "España"
    }


# -----------------------------
# ESTADOS DE LA APP
# -----------------------------

if "liga" not in st.session_state:
    st.session_state.liga = None

if "temporada" not in st.session_state:
    st.session_state.temporada = "2025/2026"

if "pagina" not in st.session_state:
    st.session_state.pagina = "⚽ Results"

# -----------------------------
# INITIAL SELECTION LEAGUE
# -----------------------------
markdown_initial_selection_league()

# -----------------------------
# PRINCIPAL APP
# -----------------------------
pagina = mostrar_sidebar()

if st.session_state.liga is None:
    seleccionar_liga()

else:
    liga = COMPETICIONES[st.session_state.liga]

    col1, col2 = st.columns([1,5])

    with col1:
        st.markdown(
                f"""
                <div style="
                    display:flex;
                    justify-content:center;
                    align-items:center;
                    background-color:#938e8e;
                    border-radius:12px;
                    padding:12px;
                    width:120px;
                    margin:auto;
                ">
                    <img src="{liga['logo']}" width="90">
                </div>
                """,
                unsafe_allow_html=True
            )

    with col2:
        st.title(liga["nombre"].upper())
        st.caption(f"Season {st.session_state.temporada}")

    st.divider()


    # Aquí irán tus páginas
    if pagina == "⚽ Teams":
       
       exists = check_teams_venues_2526_2627_exists(st.session_state.temporada, [liga["nombre"]])
       if exists: 
           df_teams= pd.DataFrame(get_all_teams_venues_2526_2627())

       else:
            df_final_teams= load_teams_2526_2627_venues()
            df_final_teams = df_final_teams.rename(
                        columns={
                            "Surface": "surface",
                            "Capacity": "capacity",
                            "Opened": "opened"
                        }
                    )
                            
            insert_teams_venues_2526_2627(df_final_teams.to_dict(orient="records"))
            df_teams= pd.DataFrame(get_all_teams_venues_2526_2627())

       teams_league=df_teams[df_teams['name_league_fotmob']==liga["nombre"]].reset_index(drop=True)
       teams_league_tempo=teams_league[teams_league['season']==st.session_state.temporada].reset_index(drop=True)
      
       render_teams(teams_league_tempo)

    elif pagina == "👥 Plantillas":

        st.subheader("Plantillas")

        exists = check_teams_venues_2526_2627_exists(st.session_state.temporada, [liga["nombre"]])
        if exists: 
            df_teams= pd.DataFrame(get_all_teams_venues_2526_2627())

        else:
            df_final_teams= load_teams_2526_2627_venues()
            df_final_teams = df_final_teams.rename(
                        columns={
                            "Surface": "surface",
                            "Capacity": "capacity",
                            "Opened": "opened"
                        }
                    )
                            
            insert_teams_venues_2526_2627(df_final_teams.to_dict(orient="records"))
            df_teams= pd.DataFrame(get_all_teams_venues_2526_2627())

        teams_league=df_teams[df_teams['name_league_fotmob']==liga["nombre"]].reset_index(drop=True)
        teams_league=teams_league[teams_league['season']==st.session_state.temporada].reset_index(drop=True)

        df_players = extract_all_players_fotmob(teams_league)

        selected = st.selectbox( "Select Team",sorted(teams_league["name_team_fotmob"].dropna().unique()))
        players_team = df_players[df_players["team_name"] == selected]
        st.dataframe(players_team)

        render_team_roster(players_team)

    elif pagina == "🏆 Standings":
        

         # =========================
        # STANDINGS SECTION
        # =========================
        option = st.segmented_control('\n\n',   ['🏆 Standings', '📈 Ranking trajectory','⭐ Team of the week'], default= '🏆 Standings')

        if option == "🏆 Standings":

            render_standings(st.session_state.temporada, liga['nombre'])
            
        elif option == "📈 Ranking trajectory":

            if st.session_state.temporada == '2025/2026':

                exists = check_standings_tracker_exists_2526(st.session_state.temporada, [liga["nombre"]])
                if exists:
                    df_standings_tracker= pd.DataFrame(get_standings_tracker_2526())
                    df_standings_tracker_league=df_standings_tracker[df_standings_tracker['league']==liga["nombre"]].reset_index(drop=True)

                else:
                    df_standings_tracker= liga_standings_tracker_raw_2526()
                    insert_standings_tracker_2526(df_standings_tracker.to_dict(orient="records"))
                    df_standings_tracker= pd.DataFrame(get_standings_tracker_2526())
                    df_standings_tracker_league=df_standings_tracker[df_standings_tracker['league']==liga["nombre"]].reset_index(drop=True)
                
                render_ranking_trajectory(df_standings_tracker_league)

            if st.session_state.temporada == '2026/2027':
                st.info('No data available yet. Data will appear once the league starts.')

        elif option == "⭐ Team of the week":
        
            render_team_of_week(st.session_state.temporada, liga['nombre'])


    elif pagina == "📅 Match schedule":
        st.subheader(f"📅 {liga['nombre']} Calendar") 

        if st.session_state.temporada == '2025/2026':
                
            exists = check_teams_venues_2526_2627_exists(st.session_state.temporada, [liga["nombre"]])
                    
            if exists: 
    
                df_teams= pd.DataFrame(get_all_teams_venues_2526_2627())
    
            else:
                
                df_final_teams= load_teams_2526_2627_venues()
    
                df_final_teams = df_final_teams.rename(
                            columns={
                                "Surface": "surface",
                                "Capacity": "capacity",
                                "Opened": "opened"
                            }
                        )
                                
    
                insert_teams_venues_2526_2627(df_final_teams.to_dict(orient="records"))
                df_teams= pd.DataFrame(get_all_teams_venues_2526_2627())       

            matches_fotmob= pd.DataFrame(get_all_matches_fotmob202526())
            all_matches_league_fotmob=matches_fotmob[matches_fotmob['league_name']==liga["nombre"]].reset_index(drop=True)

            cols_to_add = [
                "id_team_fotmob",
                "name_venue",
                "city_venue",
                "capacity",
                "url_photo_stadium"

            ]   
                    
            calendar_df = all_matches_league_fotmob.merge(
                df_teams[cols_to_add],
                left_on="home_team_id",
                right_on="id_team_fotmob",
                how="left"
            ).drop(columns="id_team_fotmob")
            calendar_df = calendar_df.drop_duplicates(keep="first").reset_index(drop=True)
    


        elif st.session_state.temporada == '2026/2027':
                
            st.info('Updating match data as games are played.')

            exists = check_teams_venues_2526_2627_exists(st.session_state.temporada, [liga["nombre"]])
                                
            if exists: 
    
                df_teams= pd.DataFrame(get_all_teams_venues_2526_2627())
    
            else:
                
                df_final_teams= load_teams_2526_2627_venues()
    
                df_final_teams = df_final_teams.rename(
                            columns={
                                "Surface": "surface",
                                "Capacity": "capacity",
                                "Opened": "opened"
                            }
                        )
                                
    
                insert_teams_venues_2526_2627(df_final_teams.to_dict(orient="records"))
                df_teams= pd.DataFrame(get_all_teams_venues_2526_2627())    

            matches_fotmob= pd.DataFrame(get_all_matches_fotmob202627())
            all_matches_league_fotmob=matches_fotmob[matches_fotmob['league_name']==liga["nombre"]].reset_index(drop=True)
            cols_to_add = [
                "id_team_fotmob",
                "name_venue",
                "city_venue",
                "capacity",
                "url_photo_stadium"

            ]
            all_matches_league_fotmob["home_team_id"] = ( all_matches_league_fotmob["home_team_id"].astype(str) )

            df_teams["id_team_fotmob"] = (df_teams["id_team_fotmob"].astype(str))
           
            calendar_df = all_matches_league_fotmob.merge(
                df_teams[cols_to_add],
                left_on="home_team_id",
                right_on="id_team_fotmob",
                how="left"
            ).drop(columns="id_team_fotmob")
            calendar_df = calendar_df.drop_duplicates(keep="first").reset_index(drop=True)

        render_calendar(calendar_df)
        
        st.divider()

        render_explore_matches(calendar_df)

    elif pagina == "⚽ Results":
        st.subheader("Results")

        if st.session_state.temporada == '2025/2026':
            exists = check_matches_exists202526( st.session_state.temporada,  liga["nombre"])
            if exists:

                # Ya están en la BD
                matches = get_all_matches_whoscored202526()

            else:

                # Primera carga
                all_matches_whoscored = load_all_matches_2526_whoscored()
                all_matches_whoscored = all_matches_whoscored.rename(
                                columns={
                                    "regionId": "region_id",
                                    "tournamentId": "tournament_id",
                                    "seasonId": "season_id",
                                    "stageId": "stage_id",
                                    "leagueName": "league_name",
                                    "match_id": "match_id",
                                    "match_url": "match_url",
                                    "calendar_month": "calendar_month",
                                    "homeTeamName": "home_team_name",
                                    "awayTeamName": "away_team_name",
                                    "homeTeamId": "home_team_id",
                                    "awayTeamId": "away_team_id",
                                    "homeScore": "home_score",
                                    "awayScore": "away_score",
                                    "match_date": "match_date",
                                    "homeLogo": "home_logo",
                                    "awayLogo": "away_logo",
                                    "matchweek_id": "matchweek_id",
                                    "matchround": "matchround"
                                }
                            )
                
                
                insert_matches_whoscored202526(all_matches_whoscored.to_dict(orient="records"))
                matches = pd.DataFrame(get_all_matches_whoscored202526())

            matches["league_name"] = matches["league_name"].replace(MAPPING_NAMES_LEAGUE_WHOSCORED_TO_FOTMOB)
            matches["season"] = matches["season"].str.replace("-", "/", regex=False)
            all_matches_league_whoscored=matches[matches['league_name']==liga["nombre"]].reset_index(drop=True)
            
    
            
            exists_fotmob = check_fotmob_matches_exists202526( st.session_state.temporada,  liga["nombre"])
            if exists_fotmob:

                # Ya están en la BD
                matches_fotmob = get_all_matches_fotmob202526()

            else:

                df_all_matches_fotmob= load_all_matches_2526_fotmob()
                matches_fotmob = df_all_matches_fotmob.rename(
                        columns={
                            "round": "round",
                            "pageUrl": "page_url",
                            "id": "match_id",
    
                            "home.name": "home_team_name",
                            "home.id": "home_team_id",
    
                            "away.name": "away_team_name",
                            "away.id": "away_team_id",
    
                            "status.finished": "finished",
                            "status.started": "started",
                            "status.cancelled": "cancelled",
                            "status.awarded": "awarded",
    
                            "status.scoreStr": "score_str",
    
                            "status.reason.short": "reason_short",
                            "status.reason.long": "reason_long",
                            "status.reason.longKey": "reason_long_key",
    
                            "id_league_fotmob": "league_id",
                            "name_league_fotmob": "league_name",
    
                            "country_code_fotmob": "country_code",
    
                            "logo_team_home": "home_logo",
                            "logo_team_away": "away_logo"
                        }
                    )

                insert_matches_fotmob202526(matches_fotmob.to_dict(orient="records"))
                matches_fotmob = pd.DataFrame(get_all_matches_fotmob202526())

            all_matches_league_fotmob=matches_fotmob[matches_fotmob['league_name']==liga["nombre"]].reset_index(drop=True)

        
        elif st.session_state.temporada == '2026/2027':
        
            st.info('Updating match data as games are played.')
            exists = check_matches_exists202627( st.session_state.temporada,  liga["nombre"])
            if exists:

                # Ya están en la BD
                matches = get_all_matches_whoscored202627()

            else:

                # Primera carga
                all_matches_whoscored = load_all_matches_2627_whoscored()
                all_matches_whoscored = all_matches_whoscored.rename(
                                columns={
                                    "regionId": "region_id",
                                    "tournamentId": "tournament_id",
                                    "seasonId": "season_id",
                                    "stageId": "stage_id",
                                    "leagueName": "league_name",
                                    "match_id": "match_id",
                                    "match_url": "match_url",
                                    "calendar_month": "calendar_month",
                                    "homeTeamName": "home_team_name",
                                    "awayTeamName": "away_team_name",
                                    "homeTeamId": "home_team_id",
                                    "awayTeamId": "away_team_id",
                                    "homeScore": "home_score",
                                    "awayScore": "away_score",
                                    "match_date": "match_date",
                                    "homeLogo": "home_logo",
                                    "awayLogo": "away_logo",
                                    "matchweek_id": "matchweek_id",
                                    "matchround": "matchround"
                                }
                            )
                all_matches_whoscored["home_score"] = (
                    pd.to_numeric(all_matches_whoscored["home_score"], errors="coerce")
                    .astype("Int64")
                )

                all_matches_whoscored["away_score"] = (
                    pd.to_numeric(all_matches_whoscored["away_score"], errors="coerce")
                    .astype("Int64")
                )
                all_matches_whoscored = all_matches_whoscored.replace({np.nan: None})
                insert_matches_whoscored202627(all_matches_whoscored.to_dict(orient="records"))
                matches = pd.DataFrame(get_all_matches_whoscored202627())

            matches["league_name"] = matches["league_name"].replace(MAPPING_NAMES_LEAGUE_WHOSCORED_TO_FOTMOB)
            matches["season"] = matches["season"].str.replace("-", "/", regex=False)
            all_matches_league_whoscored=matches[matches['league_name']==liga["nombre"]].reset_index(drop=True)


            exists_fotmob = check_fotmob_matches_exists202627( st.session_state.temporada,  liga["nombre"])
            if exists_fotmob:

                    # Ya están en la BD
                matches_fotmob = get_all_matches_fotmob202627()
    
            else:
                df_all_matches_fotmob= load_all_matches_2627_fotmob()   

                matches_fotmob = df_all_matches_fotmob.rename(
                        columns={
                            "round": "round",
                            "pageUrl": "page_url",
                            "id": "match_id",

                            "home.name": "home_team_name",
                            "home.id": "home_team_id",

                            "away.name": "away_team_name",
                            "away.id": "away_team_id",

                            "status.finished": "finished",
                            "status.started": "started",
                            "status.cancelled": "cancelled",
                            "status.awarded": "awarded",

                            "status.scoreStr": "score_str",

                            "status.reason.short": "reason_short",
                            "status.reason.long": "reason_long",
                            "status.reason.longKey": "reason_long_key",

                            "id_league_fotmob": "league_id",
                            "name_league_fotmob": "league_name",

                            "country_code_fotmob": "country_code",

                            "logo_team_home": "home_logo",
                            "logo_team_away": "away_logo",
                        }
                    )
                
                insert_matches_fotmob202627(clean_for_supabase(matches_fotmob))
                matches_fotmob = pd.DataFrame(get_all_matches_fotmob202627())
            all_matches_league_fotmob=matches_fotmob[matches_fotmob['league_name']==liga["nombre"]].reset_index(drop=True)

        col0, col1 = st.columns([1,1])
        

        

        with st.container():
            # ---------------------------
            # Stage filter
            # ---------------------------
            with col0:
                from zoneinfo import ZoneInfo

                hoy = pd.Timestamp.now(tz=ZoneInfo("Europe/Madrid")).normalize().tz_localize(None)
                stages = sorted(all_matches_league_fotmob['round'].dropna().unique().tolist())
                if not stages:
                    raise ValueError("No stages available in dataframe")
                
                 # Buscar stage que contiene la fecha de hoy
                stage_por_defecto = stages[0]

                for stage in stages:
                    fechas_stage = pd.to_datetime(
                        all_matches_league_fotmob.loc[all_matches_league_fotmob["round"] == stage, "match_date"]
                    ).dt.normalize()
                    
                    if hoy in fechas_stage.values:
                        stage_por_defecto = stage
                        break

                indice_stage = stages.index(stage_por_defecto)
                
                stage_selected = st.selectbox( "🏆 Select matchweek",stages, index=indice_stage)
                df_filtered_stage_selected = all_matches_league_fotmob[all_matches_league_fotmob["round"] == stage_selected]

            # NOTE:
            # The current implementation stores the selected stage
            # but does not directly filter the dataframe using it.

            id_stage= df_filtered_stage_selected["round"].iloc[0]
            
            
            # ---------------------------
            # Date filter
            # --------------------------- 
            fechas = sorted(df_filtered_stage_selected['match_date'].dropna().unique().tolist())
            fechas_formateadas = [formatear_fecha_segura(f) for f in fechas]       

            with col1:
                fecha_elegida = None
                if len(fechas) > 0:
                    
                    indice_hoy = min( range(len(fechas)), key=lambda i: abs(pd.Timestamp(fechas[i]).normalize() - hoy))
                    fecha_label = st.selectbox("📆 Select date", fechas_formateadas, index=indice_hoy)

                    idx = fechas_formateadas.index(fecha_label)
                    fecha_elegida = fechas[idx]
                
            # ---------------------------
            # Final filtering
            # ---------------------------
            partidos = df_filtered_stage_selected.copy()

            if fecha_elegida:
                partidos = partidos[partidos["match_date"] == fecha_elegida]

            partidos["match_datetime_sort"] = pd.to_datetime(
                partidos["match_date"].astype(str) + " " + partidos["match_time"].astype(str),
                errors="coerce"
            )

            partidos = partidos.sort_values("match_datetime_sort", ascending=True).reset_index(drop=True)
            # Display filter summary
            if not partidos.empty:
                st.markdown(f"""
                    <h3 style='margin-top: 1em; color: #999;'>
                        ⚽ Matchweek: <span style='color:white;'>{id_stage}</span>
                        {f", Matches from <span style='color:white;'>{formatear_fecha_segura(fecha_elegida)}</span>" if fecha_elegida else ""}
                    </h3>
                """, unsafe_allow_html=True)
            # ------------------------------------
            # Autoabrir si solo hay 1 partido jugado
            # ------------------------------------
            partidos_finalizados = partidos[ partidos["finished"] == True]

            if len(partidos_finalizados) == 1:

                url_unica = partidos_finalizados.iloc[0]["page_url"]

                if  st.session_state.get("partido_mostrado") != url_unica:
                    st.session_state["partido_mostrado"] = url_unica

            elif len(partidos_finalizados) > 1:

                partido_actual = st.session_state.get("partido_mostrado")

                if ( partido_actual is not None and partido_actual not in partidos["page_url"].values):
                    st.session_state.pop("partido_mostrado", None )     
           
            for _, row in partidos.iterrows():
                with st.container():

                    

                    # ---------------------------
                    # Match time formatting
                    # ---------------------------
                    hora = row.get("match_time")

                    if isinstance(hora, time):
                        hora_str = hora.strftime("%H:%M")
                    elif isinstance(hora, str):
                        hora_str = hora[:5] if len(hora) >= 5 else hora
                    else:
                        hora_str = "-"

                    # ---------------------------
                    # Match status
                    # ---------------------------
                    if row.get("finished"):
                        estado = f"✅ Completed ({hora_str})"
                    else:
                        estado = f"🕒 Scheduled ({hora_str})"
                    
                    # ---------------------------
                    # Match score
                    # ---------------------------
                    score = row.get("score_str")

                    if row.get("finished") == True:
                        resultado = score
                    else:
                        resultado = "vs"
                            
                    
                    home_team = row.get('home_team_name', '')
                    away_team = row.get('away_team_name', '')
                    homeTeamPhoto = row.get('home_logo', '')
                    awayTeamPhoto = row.get('away_logo', '')
                    partido_url = row.get('page_url', '')
                    clave = f"ver_{partido_url}"

                    # Layout:
                    # Left -> Match card
                    # Right -> Details button
                    col1, col2 = st.columns([0.70, 0.35])

                    with col1:
                        partido_abierto = (
                            st.session_state.get("partido_mostrado")
                            == partido_url
                        )

                        card_border = (
                            "2px solid #4CAF50"
                            if partido_abierto
                            else "1px solid #e0e0e0"
                        )

                        card_shadow = (
                            "0 0 12px rgba(76,175,80,0.25)"
                            if partido_abierto
                            else "2px 2px 8px rgba(0,0,0,0.05)"
                        )

                        card_background = (
                            "rgba(76,175,80,0.05)"
                            if partido_abierto
                            else "transparent"
                        )

                        partido_html = f"""
                        <div style="
                                border: {card_border};
                                border-radius: 15px;
                                padding: 1.5em;
                                margin-bottom: 1em;
                                background-color: {card_background};
                                box-shadow: {card_shadow};
                            ">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div style="font-size: 14px; color: #999;">{estado}</div>
                                <div style="text-align: center; flex: 1;">
                                    <img src="{homeTeamPhoto}" width="50" style="vertical-align: middle;">
                                    <strong style="margin: 0 1em; font-size: 18px;">{home_team}</strong>
                                    <span style="font-size: 16px; font-weight: bold; color: #999;">{resultado}</span>
                                    <strong style="margin: 0 1em; font-size: 18px;">{away_team}</strong>
                                    <img src="{awayTeamPhoto}" width="50" style="vertical-align: middle;">
                                </div>
                            </div>
                        </div>
                        """
                        st.markdown(partido_html, unsafe_allow_html=True)

                    with col2:

                        status = row.get("finished")
                        partido_jugado = status == True
                        # Match details are only available once a winner field exists.

                        if partido_jugado:

                            varios_partidos = len(partidos_finalizados) > 1

                            partido_abierto = st.session_state.get("partido_mostrado")== partido_url
                        
                            if varios_partidos:

                                if partido_abierto:

                                    if st.button(  "❌ Hide details", key=f"hide_{clave}"):

                                        st.session_state.pop("partido_mostrado",None) 
                                        st.rerun()

                                else:
                                    if st.button("🔍 View match details", key=clave):

                                        st.session_state[ "partido_mostrado"] = partido_url
                                        st.rerun()

                            else:

                                pass

                        else:

                            st.markdown(
                                """
                                <span style="color:gray">
                                    Details are not yet available.
                                </span>
                                """,
                                unsafe_allow_html=True
                            )

            if st.session_state.get("partido_mostrado"):
                partido_filtrado = partidos[partidos["page_url"] == st.session_state["partido_mostrado"]].reset_index(drop=True)
                if partido_filtrado.empty:
                    st.session_state.pop("partido_mostrado", None)
                    #st.warning("This match is not visible with the selected filters. Try changing stage, group or date.")
                    st.stop()

                else:
                    partido_detalle = partido_filtrado.iloc[0]

                    selected_home_team = partido_detalle["home_team_name"]
                    selected_away_team = partido_detalle["away_team_name"]

                    url_match_fotmob= partido_filtrado['page_url'].values[0]
                    estado = partido_filtrado['reason_short'][0]
                    if estado == 'FT':
                        texto_estado = "(FT)"
                    else:
                        texto_estado = "No data available"

                    round_fotmob = int(partido_filtrado['round'][0])
                    df= all_matches_league_whoscored[(all_matches_league_whoscored["home_team_name"]== selected_home_team)& (all_matches_league_whoscored["away_team_name"] == selected_away_team)]
                    url_match_whoscored = df['match_url'].values[0]
                    st.write(url_match_fotmob)
                    st.write(url_match_whoscored)

                    #-------------------------------------------------------------------------------------------
                    #Prepare data json match fotmob
                    data_match_fotmob= prepare_data_fotmob(url_match_fotmob)        
                    df_info_teams_fotmob, df_players_fotmob = process_fotmob_match(data_match_fotmob)
                    st.dataframe(df_info_teams_fotmob)
                    st.dataframe(df_players_fotmob)
                    
                    (df_shots_fotmob, df_weather, df_referee, df_stadium,
                         player_of_the_match, role_potm, colors_team) = extract_df_variables_general_info_match(data_match_fotmob)

                    principal_color_home= colors_team['home.color'].values[0]
                    principal_color_away= colors_team['away.color'].values[0]
                    st.write(principal_color_home)
                    st.write(principal_color_away)

                    #DICCIONARIO DE COLORES DE LOS EQUIPOS POR SI QUIERO OBTENERLOS
                    dict_colors_match_fotmob= data_match_fotmob['general']['teamColors']
                    st.write(dict_colors_match_fotmob)
                    color_home= data_match_fotmob['general']['teamColors']['darkMode']['home']
                    color_away= data_match_fotmob['general']['teamColors']['darkMode']['away']
                    
                    ( home_team, away_team,home_logo, away_logo, home_score, away_score, rating_home, rating_away,coach_home, coach_away, 
                                formation_home, formation_away, av_age_home, av_age_away)  = extract_variables_team_info_details(df_info_teams_fotmob) 

                    #-------------------------------------------------------------------------------------------
                    #Prepare data json match whoscored
                    data_match_whoscored = prepare_data_whoscored(url_match_whoscored)
                    matchdict = data_match_whoscored['matchdict']

                    teams_dict_id_name_whoscored = {matchdict['home']['teamId']: matchdict['home']['name'],
                        matchdict['away']['teamId']: matchdict['away']['name']}

                    st.write("---") 

                    col1, col_space1, col2, col_space2, col3 = st.columns([2,0.3, 4,0.3, 2])

                    with col1:
                        # =============================================================================
                        # HOME TEAM PANEL
                        # =============================================================================
                        #
                        # Mirrors the home team panel and provides:
                        #
                        # - Team information
                        # - Squad selection
                        # - Starting XI
                        # - Bench players
                        # - Substitution activity
                        principal_card_team(home_logo,coach_home, formation_home, av_age_home, rating_home )    

                        st.write('')
                        initial_formation_home = st.segmented_control(" ", ["Starting XI", "Bench"], default="Starting XI", key="home_squad_selector")     
                        
                        if initial_formation_home == "Starting XI":
                            
                            fig1, ax = plot_formation_team( df=df_players_fotmob, team_name=home_team, player_of_the_match=player_of_the_match )
                            st.pyplot(fig1, use_container_width=True)

                        else:
                            
                            # ============================================================
                            # BENCH PLAYERS
                            # ============================================================
                            substitutes = get_team_substitutes(df_players_fotmob,home_team)
                            if substitutes.empty:
                                st.warning( f'No substitutes were found for {home_team}.')

                            else:
                                create_cards_substitutions_list(substitutes)

                    with col_space1:
                        st.write('')

                    with col2:
                        # =============================================================================
                        # MATCH CENTER PANEL
                        # =============================================================================
                        #
                        # Core match information and tactical visualizations.
                        #
                        # Includes:
                        #
                        # - Match scoreboard
                        # - Venue information
                        # - Referee
                        # - Player of the Match
                        # - Key events timeline
                        # - Penalty shootout details
                        # - Initial formations
                        # color_home= "red"
                        # color_away= "blue"
                    
                        
                        card_match_overview(home_team,away_team,home_score, away_score, color_home, color_away ,texto_estado)
                        st.write('')

                        card_match_basic_info(df_stadium,df_referee, player_of_the_match, role_potm)

                    with col_space2:
                        st.write('')

                    with col3:

                        # =============================================================================
                        # AWAY TEAM PANEL
                        # =============================================================================
                        #
                        # Mirrors the home team panel and provides:
                        #
                        # - Team information
                        # - Squad selection
                        # - Starting XI
                        # - Bench players
                        # - Substitution activity

                        principal_card_team(away_logo,coach_away, formation_away, av_age_away,  rating_away)    
                        
                        
                        st.write('')
                        alineacion_away = st.segmented_control( " ", ["Starting XI", "Bench"], default="Starting XI",key="away_squad_selector")  

                        if alineacion_away == "Starting XI":
                            fig2, ax = plot_formation_team(df=df_players_fotmob,team_name=away_team,player_of_the_match=player_of_the_match)

                            st.pyplot( fig2, use_container_width=True)

                        else:
                            # ============================================================
                            # BENCH PLAYERS
                            # ============================================================
                            substitutes = get_team_substitutes(df_players_fotmob,away_team)
                            if substitutes.empty:
                                st.warning( f'No substitutes were found for {away_team}.')

                            else: 
                                create_cards_substitutions_list(substitutes)

                    option = st.segmented_control('Analysis type:\n\n', 
                                    ['Team Analysis', 'Player of the Match'], default='Team Analysis')

                    

                    def prepare_df_events( matchdict: dict, teams_dict_id_name: dict) -> pd.DataFrame:
                        """
                        Convert raw WhoScored match events into a structured DataFrame.

                        This function normalizes nested event attributes and enriches
                        events with team names.

                        Args:
                            matchdict (dict): Match data dictionary obtained from
                                WhoScored match center.
                            teams_dict_id_name (dict): Mapping between team identifiers
                                and team names.

                        Returns:
                            pd.DataFrame:
                                Processed events DataFrame.

                        Raises:
                            TypeError: If inputs have invalid types.
                            KeyError: If required keys are missing.
                        """

                        # 🔹 Validate input types
                        if not isinstance(matchdict, dict):
                            raise TypeError("matchdict must be a dictionary")

                        if not isinstance(teams_dict_id_name, dict):
                            raise TypeError(
                                "teams_dict_id_name must be a dictionary"
                            )

                        if "events" not in matchdict:
                            raise KeyError("events key not found in matchdict")

                        # 🔹 Create events DataFrame
                        events_df = pd.DataFrame(matchdict["events"])

                        # 🔹 Map team names
                        events_df["nameTeam"] = events_df["teamId"] .map(teams_dict_id_name)

                        # 🔹 Normalize nested dictionaries
                        events_df["type"] = events_df["type"].apply(lambda x:x["displayName"] if isinstance(x, dict) else None)

                        events_df["outcomeType"] = events_df["outcomeType"].apply( lambda x: x["displayName"] if isinstance(x, dict) else None)

                        events_df["period"] = events_df["period"].apply( lambda x: x["displayName"] if isinstance(x, dict) else None)

                        return events_df

                    # df_events = prepare_df_events(matchdict, teams_dict_id_name_whoscored)
                    #st.dataframe(df_events)




        

    elif pagina == "📊 Estadísticas":
        st.subheader("Estadísticas")

    elif pagina == "🔄 Transferencias":
        st.subheader("Transferencias")

    elif pagina == "🏟️ Venues":

        st.subheader(f"🏟️ Stadiums")

        exists = check_teams_venues_2526_2627_exists(st.session_state.temporada, [liga["nombre"]])
                
        if exists: 

            df_teams= pd.DataFrame(get_all_teams_venues_2526_2627())

        else:
            
            df_final_teams= load_teams_2526_2627_venues()

            df_final_teams = df_final_teams.rename(
                        columns={
                            "Surface": "surface",
                            "Capacity": "capacity",
                            "Opened": "opened"
                        }
                    )
                            

            insert_teams_venues_2526_2627(df_final_teams.to_dict(orient="records"))
            df_teams= pd.DataFrame(get_all_teams_venues_2526_2627())
        
        teams_league=df_teams[df_teams['name_league_fotmob']==liga["nombre"]].reset_index(drop=True)
        teams_league_tempo=teams_league[teams_league['season']==st.session_state.temporada].reset_index(drop=True)

        render_venues(teams_league_tempo)


        
        

        



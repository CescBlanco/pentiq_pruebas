import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime

from frontend.services.load_data import *
from frontend.supabase_bbdd.bbdd_matches import *


import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch, Sbopen, FontManager, inset_image
from mplsoccer import Pitch
from matplotlib import patheffects
import matplotlib.patheffects as path_effects
background_color = '#0C0D0E'
text_color = 'white'
line_color = 'white'


#Extract json data from fotmob match url and save to supabase cache if not exists
def prepare_data_fotmob(url_match_fotmob):
    id_match_fotmob = extract_match_id_fotmob(url_match_fotmob)

    data_match_fotmob = load_match_cache(source="fotmob", match_id=id_match_fotmob)
    if data_match_fotmob is None: 
        with st.spinner("🟡 No cache in matches fotmob. Scraping match data..."):
            data_match_fotmob = asyncio.run(fetch_match_json(url_match_fotmob))
            save_match_cache( source="fotmob",match_id=id_match_fotmob, data=data_match_fotmob)

    return data_match_fotmob

def clean_for_supabase(df):
    df = df.copy()

    def clean_value(value):
        # NaN / NaT
        if pd.isna(value):
            return None

        # Infinity / -Infinity
        if isinstance(value, (float, np.floating)):
            if not np.isfinite(value):
                return None

        # numpy integers/floats -> tipos Python normales
        if isinstance(value, np.integer):
            return int(value)

        if isinstance(value, np.floating):
            return float(value)

        if isinstance(value, np.bool_):
            return bool(value)

        return value

    return [
        {
            column: clean_value(value)
            for column, value in row.items()
        }
        for row in df.to_dict(orient="records")
    ]

#Extract json data from whoscored match url and save to supabase cache if not exists
def prepare_data_whoscored(url_match_whoscored):
    id_match_whoscored = extract_match_id(url_match_whoscored)

    data_match_whoscored = load_match_cache(source="whoscored", match_id=id_match_whoscored )
    if data_match_whoscored is None: 
        with st.spinner("🟡 No cache in matches whoscored. Scraping match data..."):
            formation_mappings, event_types_json, matchdict, players_dict = extract_match_dict_url(url_match_whoscored)
        
            data_match_whoscored = {
                "formation_mappings": formation_mappings,
                "event_types_json": event_types_json,
                "matchdict": matchdict,
                "players_dict": players_dict
            }
            save_match_cache( source="whoscored",match_id=id_match_whoscored, data=data_match_whoscored)
    return data_match_whoscored

def formatear_fecha_segura(f):
    try:
        fecha_obj = datetime.strptime(f, "%Y-%m-%d")
        return fecha_obj.strftime("%d/%m/%Y")
    except Exception as e:
        st.write("Error:", e)
        return f
            
def process_fotmob_match(data_match_fotmob):

    # ==========================================================
    # 1. Información de los equipos
    # ==========================================================

    def get_team_info(team):
        coach = team.get('coach', {})

        return {
            'coach_name': coach.get('name'),
            'coach_id': coach.get('id'),
            'coach_age': coach.get('age'),
            'coach_countryCode': coach.get('countryCode'),
            'rating': team.get('rating'),
            'formation': team.get('formation'),
            'averageStarterAge': team.get('averageStarterAge'),
            'totalStarterMarketValue': team.get('totalStarterMarketValue')
        }

    # DataFrame inicial de equipos
    df_info_teams = pd.DataFrame(data_match_fotmob['header']['teams'] )

    # Información de las alineaciones
    home_team = data_match_fotmob['content']['lineup']['homeTeam']
    away_team = data_match_fotmob['content']['lineup']['awayTeam']

    # Extraemos información de ambos equipos
    for team in [home_team, away_team]:

        team_info = get_team_info(team)

        for column, value in team_info.items():
            df_info_teams.loc[
                df_info_teams['id'] == team['id'],
                column
            ] = value


    # ==========================================================
    # 2. Información de los jugadores
    # ==========================================================

    def extract_players(team_data, team_type):

        # Copiamos para no modificar el JSON original
        starters = team_data.get('starters', []).copy()
        subs = team_data.get('subs', []).copy()

        # Tipo de jugador
        for player in starters:
            player['player_type'] = 'starter'

        for player in subs:
            player['player_type'] = 'sub'

        # Unimos titulares y suplentes
        players = starters + subs

        # DataFrame
        df = pd.json_normalize(players)

        # Información del equipo
        df['team'] = team_type
        df['team_id'] = team_data.get('id')
        df['team_name'] = team_data.get('name')
        df['playerImage'] = ('https://images.fotmob.com/image_resources/playerimages/'+ df['id'].astype(str)+ '.png')

        return df


    # Extraemos jugadores
    df_home_players = extract_players(home_team, 'home')
    df_away_players = extract_players(away_team, 'away')

    # Unimos home + away
    df_players = pd.concat([df_home_players, df_away_players], ignore_index=True )

    # ==========================================================
    # 3. Información de los capitanes
    # ==========================================================

    df_captains = df_players[ df_players['isCaptain'] == True][['team_id', 'id', 'name']].copy()

    # Renombramos columnas
    df_captains = df_captains.rename(
            columns={
                        'team_id': 'id',
                        'id': 'captain_id',
                        'name': 'captain_name'
                    }
                )

    # Añadimos capitán a la información de los equipos
    df_info_teams = df_info_teams.merge( df_captains, on='id', how='left')

    return df_info_teams, df_players


def extract_df_variables_general_info_match(data_match_fotmob):

    df_shots_fotmob= pd.DataFrame(data_match_fotmob['content']['shotmap']['shots'])
    st.dataframe(df_shots_fotmob)

    df_weather= pd.json_normalize(data_match_fotmob['content']['weather'])
    df_referee= pd.json_normalize(data_match_fotmob['content']['matchFacts']['infoBox']['Referee'])              

    df_stadium= pd.json_normalize(data_match_fotmob['content']['matchFacts']['infoBox']['Stadium'])
    attendance = data_match_fotmob['content']['matchFacts']['infoBox']['Attendance']
    df_stadium['Attendance'] = attendance

    colors_team= pd.json_normalize(data_match_fotmob['content']['matchFacts']["playerOfTheMatch"]['teamData'])
    player_of_the_match= data_match_fotmob['content']['matchFacts']["playerOfTheMatch"]['name']['fullName']
    role_potm= data_match_fotmob['content']['matchFacts']["playerOfTheMatch"]['role']

    return df_shots_fotmob, df_weather, df_referee, df_stadium, player_of_the_match, role_potm, colors_team


def extract_variables_team_info_details( team_info: pd.DataFrame) -> tuple:
    """
    Extract key match and team information from a team details DataFrame.

    This function retrieves the most relevant match variables for both
    home and away teams, including scores, managers, formations,
    average age, and captain identifiers.

    Args:
        team_info (pd.DataFrame): Team information dataset containing
            match metadata.

    Returns:
        tuple:
            (
                home_team,
                away_team,
                home_score,
                away_score,
                manager_name_home,
                manager_name_away,
                initial_formation_home,
                initial_formation_away,
                average_age_home,
                average_age_away,
            )

    Raises:
        TypeError: If team_info is not a DataFrame.
        KeyError: If required columns are missing.
        IndexError: If expected rows are unavailable.
    """

    # 🔹 Extract team names
    home_team = team_info["name"].values[0]
    away_team = team_info["name"].values[1]

    # 🔹 Extract team logos
    home_logo = team_info["imageUrl"].values[0]
    away_logo = team_info["imageUrl"].values[1]

    # 🔹 Full-time scores
    home_score = team_info["score"].values[0]
    away_score = team_info["score"].values[1]

    # 🔹 Managers
    coach_home = team_info["coach_name"].values[0]
    coach_away = team_info["coach_name"].values[1]

    # 🔹 Initial formations
    formation_home = team_info["formation"].values[0]
    formation_away = team_info["formation"].values[1]

    # 🔹 Average squad age
    av_age_home = team_info["averageStarterAge"].values[0]
    av_age_away = team_info["averageStarterAge"].values[1]

    #Global ratings
    rating_home = team_info["rating"].values[0]
    rating_away = team_info["rating"].values[1]

    return ( home_team, away_team,home_logo, away_logo, home_score, away_score, rating_home, rating_away, coach_home, coach_away, 
            formation_home, formation_away, av_age_home, av_age_away)


#--------------------------------------------UX APP----------------------------------------------
def principal_card_team( team_photo: str, manager_name: str, initial_formation: str, average_age: float | int, rating: float | int) -> None:       
    """
    Render the main team information card.

    This component displays:
    - Team image
    - Manager name
    - Initial formation
    - Average squad age
    - Ratinf

    Args:
        team_photo (str): Team logo or image URL.
        manager_name (str): Team manager name.
        initial_formation (str): Starting formation.
        average_age (float | int): Average squad age.
        rating (float | int): Average rating players.

    Returns:
        None
    """

    # 🔹 Team image
    st.markdown(f"""
                <div style='text-align:center;'>
                    <img src='{team_photo}' width='90'><br>
                </div>
            """, unsafe_allow_html=True)
    
    st.write('')

    # 🔹 Team details
    st.markdown(
            f"""
            <p style='text-align:center; font-size:13px; margin:0; line-height:1.4;'>
                Manager: {manager_name}<br>
                Initial formation: {initial_formation} (Avg. age: {average_age})<br>
                Rating: {rating} 
            </p>
            """,
            unsafe_allow_html=True
        )

def card_match_overview( home_team: str, away_team: str, home_score: int | float, away_score: int | float, color_home: str, color_away: str, match_status_text: str) -> None:
    """
    Render the main match overview card.

    This component displays:
    - Home and away team names
    - Match score
    - Custom team colors
    - Match status text

    Args:
        home_team (str): Home team name.
        away_team (str): Away team name.
        home_score (int | float): Home team score.
        away_score (int | float): Away team score.
        color_home (str): Home team display color.
        color_away (str): Away team display color.
        match_status_text (str): Additional match status text.

    Returns:
        None
    """
    st.markdown("""
            <div style='display: flex; justify-content: center; align-items: center; font-size: 28px; font-weight: bold;'>
                <span style='color:{color_home}; margin-right: 15px;'>{home_team}</span>
                <span style='color:white;'>{homeScore} : {awayScore}</span>
                <span style='color:{color_away}; margin-left: 15px;'>{away_team}</span>

            </div>
                <div style='display: flex; justify-content: center; align-items: center; color:#white; font-size:16px;'>
                    {texto_estado}
                </div>
            </div>
        """.format( home_team=home_team, away_team=away_team,
                    homeScore=home_score, awayScore=away_score,
                    color_home=color_home, color_away=color_away, 
                    texto_estado=match_status_text), unsafe_allow_html=True)

def card_match_basic_info(df_stadium,df_referee, player_of_the_match, role_potm):
    st.markdown(
        f"""
        <p style='text-align:center; font-size:15px; margin:0.5; line-height:1.6;'>
            Location: {df_stadium['name'].values[0]} ({df_stadium['city'].values[0]}/{df_stadium['country'].values[0]})<br>
            Capacity: {df_stadium['capacity'].values[0]} (Attendance: {df_stadium['Attendance'].values[0]})<br>
            Referee: {df_referee['text'].values[0] }<br>
            ⭐ Match: {player_of_the_match} ({role_potm})
        </p>
        """,
        unsafe_allow_html=True
    )

#------------------------------------XI FORMATION------------------------------------------------

path_eff = [path_effects.Stroke(linewidth=1.5, foreground=line_color), 
                            path_effects.Normal()]

                            
def get_team_formation(df, team_name):

    lineup = df[
        (df['team_name'] == team_name) &
        (df['player_type'] == 'starter')
    ].copy()

    # Nos quedamos únicamente con jugadores
    # que tengan coordenadas de formación
    lineup = lineup.dropna(
        subset=[
            'verticalLayout.x',
            'verticalLayout.y'
        ]
    ).copy()

    # Aseguramos que sean numéricas
    lineup['verticalLayout.x'] = pd.to_numeric(
        lineup['verticalLayout.x'],
        errors='coerce'
    )

    lineup['verticalLayout.y'] = pd.to_numeric(
        lineup['verticalLayout.y'],
        errors='coerce'
    )

    lineup = lineup.dropna(
        subset=[
            'verticalLayout.x',
            'verticalLayout.y'
        ]
    )

    return lineup



import requests
from PIL import Image
from io import BytesIO

def load_player_image(url):

    try:

        response = requests.get(
            url,
            timeout=5
        )

        response.raise_for_status()

        image = Image.open(
            BytesIO(response.content)
        ).convert('RGBA')

        return image

    except Exception:
        return None

def get_rating_color(rating):

    if pd.isna(rating):
        return '#808080'

    rating = float(rating)

    if rating < 5.0:
        return "#F13722"      # rojo

    elif rating < 7.0:
        return '#F39C12'      # naranja

    elif rating < 9.0:
        return '#2ECC71'      # verde

    else:
        return '#00B4D8'      # azul/cian

def draw_player_rating(
    pitch,
    ax,
    x,
    y,
    rating,
    is_motm=False
):

    if pd.isna(rating):
        return

    rating = float(rating)

    # =============================
    # COLOR DEL RATING
    # =============================

    color = get_rating_color(rating)

    # =============================
    # ESTRELLA SI ES MOTM
    # =============================

    prefix = '★ ' if is_motm else ''

    # =============================
    # RATING
    # =============================

    pitch.annotate(
        f'{prefix}{rating:.1f}',
        xy=(x, y),
        ax=ax,
        color='black',
        fontsize=8,
        fontweight='bold',
        ha='center',
        va='center',
        bbox=dict(
            boxstyle='round,pad=0.35',
            facecolor=color,
            edgecolor='white',
            linewidth=0.8,
            alpha=0.95
        ),
        zorder=10
    )
def plot_formation_team(
    df,
    team_name,
    player_of_the_match=None,
    ax=None
):

    # ==========================================
    # OBTENER XI
    # ==========================================

    lineup = get_team_formation(
        df,
        team_name
    )

    if lineup.empty:
        raise ValueError(
            f"No hay titulares con coordenadas para {team_name}"
        )

    # ==========================================
    # COORDENADAS FOTMOB -> MPLSOCCER
    # ==========================================

    # PROFUNDIDAD
    #
    # FotMob:
    # y = 0.10  -> portero
    # y = 0.29  -> defensa
    # y = 0.48  -> centrocampista
    # y = 0.68  -> extremo
    # y = 0.87  -> delantero
    #
    # En VerticalPitch queremos:
    # portero abajo
    # delanteros arriba
    #
    # ==========================================
    # COORDENADAS FOTMOB -> MPLSOCCER
    # ==========================================

    # PROFUNDIDAD
    # Portero abajo
    # Delanteros arriba

    lineup['pitch_x'] = (
        lineup['verticalLayout.y'] * 120
    )

    # ANCHURA
    # Invertimos izquierda/derecha
    # porque FotMob viene al revés para nuestra visualización

    lineup['pitch_y'] = (
        (1 - lineup['verticalLayout.x']) * 80
    )

    # ==========================================
    # FIGURA
    # ==========================================

    if ax is None:

        fig, ax = plt.subplots(
            figsize=(6, 10)
        )

    else:

        fig = ax.figure

    fig.patch.set_alpha(0)

    # ==========================================
    # CAMPO
    # ==========================================

    pitch = VerticalPitch(
        pitch_type='statsbomb',
        pitch_color=background_color,
        line_color='white',
        linewidth=2
    )

    pitch.draw(ax=ax)

    ax.set_facecolor('none')

    # ==========================================
    # MOTM
    # ==========================================

    if player_of_the_match is not None:

        motm = lineup[
            lineup['name'] == player_of_the_match
        ].copy()

    else:

        motm = lineup.iloc[0:0].copy()

    # Jugadores normales
    normal_players = lineup[
        ~lineup['name'].isin(
            motm['name']
        )
    ].copy()

    
    # ==========================================
    # NOMBRES + DORSALES
    # ==========================================

    for _, row in normal_players.iterrows():

        x = row['pitch_x']
        y = row['pitch_y']

        image = load_player_image(
            row['playerImage']
        )

        if image is not None:

            pitch.inset_image(
                x,
                y,
                image,
                width=12,
                ax=ax,
                zorder=4
            )
        

        # -----------------------------
        # # DORSAL + NOMBRE
        # -----------------------------

        if pd.notna(row['shirtNumber']):

            try:
                shirt = str(int(row['shirtNumber']))
            except:
                shirt = str(row['shirtNumber'])

        else:
            shirt = ''

        player_label = f'{shirt} {row["lastName"]}'.strip()

        pitch.annotate(
            player_label,
            xy=(x - 8, y),
            ax=ax,
            color=text_color,
            fontsize=7,
            ha='center',
            va='center',
            bbox=dict(
                facecolor="#6D6D6D",
                edgecolor='none',
                alpha=0.1,
                pad=0.3
            ),
            zorder=5
        )
        # ======================================
        # RATING
        # ======================================

        draw_player_rating(
            pitch=pitch,
            ax=ax,
            x=x + 5,
            y=y+5,
            rating=row['performance.rating'],
            is_motm=False
        )
    # ==========================================
    # MOTM
    # ==========================================

    if not motm.empty:

        row = motm.iloc[0]

        x = row['pitch_x']
        y = row['pitch_y']

        image = load_player_image(
            row['playerImage']
        )

        if image is not None:

            pitch.inset_image(
                x,
                y,
                image,
                width=12,
                ax=ax,
                zorder=4
            )


        # ======================================
        # DORSAL + NOMBRE
        # ======================================

        if pd.notna(row['shirtNumber']):

            try:
                shirt = str(int(row['shirtNumber']))
            except:
                shirt = str(row['shirtNumber'])

        else:
            shirt = ''

        player_label = f'{shirt} {row["lastName"]}'.strip()

        pitch.annotate(
            player_label,
            xy=(x - 8, y),
            ax=ax,
            color=text_color,
            fontsize=7,
            ha='center',
            va='center',
            bbox=dict(
                facecolor='#1A1A1A',
                edgecolor='none',
                alpha=0.7,
                pad=0.3
            ),
            zorder=7
        )

        draw_player_rating(
            pitch=pitch,
            ax=ax,
            x=x + 5,
            y=y+5,
            rating=row['performance.rating'],
            is_motm=True
        )

    
    return fig, ax

#------------------------------------SUBS------------------------------------------------
import html
import json
import ast
import pandas as pd

def get_team_substitutes(df, team_name):

    substitutes = df[
        (df['team_name'] == team_name) &
        (df['player_type'] == 'sub')
    ].copy()

    return substitutes

# ============================================================
# PARSEAR substitutionEvents
# ============================================================

def parse_substitution_events(value):

    # --------------------------------------------------------
    # SIN DATOS
    # --------------------------------------------------------

    if value is None:
        return []

    try:

        if pd.isna(value):
            return []

    except Exception:
        pass


    # --------------------------------------------------------
    # YA ES LISTA
    # --------------------------------------------------------

    if isinstance(value, list):

        return value


    # --------------------------------------------------------
    # YA ES DICT
    # --------------------------------------------------------

    if isinstance(value, dict):

        return [value]


    # --------------------------------------------------------
    # STRING
    # --------------------------------------------------------

    if isinstance(value, str):

        value = value.strip()

        if not value:
            return []


        # Intentar JSON

        try:

            parsed = json.loads(value)

            if isinstance(parsed, list):
                return parsed

            if isinstance(parsed, dict):
                return [parsed]

        except Exception:
            pass


        # Intentar literal Python

        try:

            parsed = ast.literal_eval(value)

            if isinstance(parsed, list):
                return parsed

            if isinstance(parsed, dict):
                return [parsed]

        except Exception:
            pass


    return []


# ============================================================
# OBTENER INFORMACIÓN DE SUSTITUCIÓN
# ============================================================

def get_substitution_info(row):

    value = row.get(
        'performance.substitutionEvents',
        None
    )

    events = parse_substitution_events(value)


    # --------------------------------------------------------
    # BUSCAR subIn
    # --------------------------------------------------------

    for event in events:

        if not isinstance(event, dict):
            continue


        if event.get('type') != 'subIn':
            continue


        # ----------------------------------------------------
        # MINUTO
        # ----------------------------------------------------

        minute = event.get(
            'time',
            None
        )

        if minute is not None:

            try:

                minute = int(
                    float(minute)
                )

            except Exception:

                minute = None


        # ----------------------------------------------------
        # DEVOLVER INFORMACIÓN
        # ----------------------------------------------------

        return {
            'played': True,
            'minute': minute,
            'reason': event.get(
                'reason',
                None
            )
        }


    # --------------------------------------------------------
    # NO ENCONTRADO
    # --------------------------------------------------------

    return {
        'played': False,
        'minute': None,
        'reason': None
    }


# ============================================================
# TARJETA DE SUPLENTE
# ============================================================

def render_substitute_card(row):


    # ========================================================
    # NOMBRE
    # ========================================================

    name = row.get(
        'name',
        ''
    )

    if pd.isna(name):
        name = ''

    name = html.escape(
        str(name)
    )


    # ========================================================
    # DORSAL
    # ========================================================

    shirt = row.get(
        'shirtNumber',
        ''
    )

    if pd.isna(shirt):

        shirt = ''

    else:

        try:

            shirt = str(
                int(
                    float(shirt)
                )
            )

        except Exception:

            shirt = str(shirt)

    shirt = html.escape(
        shirt
    )


    # ========================================================
    # FOTO
    # ========================================================

    image_url = row.get(
        'playerImage',
        ''
    )

    if pd.isna(image_url):
        image_url = ''

    image_url = str(
        image_url
    ).strip()


    # ========================================================
    # RATING
    # ========================================================

    rating = row.get(
        'performance.rating',
        None
    )


    if pd.notna(rating):

        try:

            rating_value = float(
                rating
            )

            rating_color = get_rating_color(
                rating_value
            )

            rating_html = f'''
                <span
                    class="sub-rating"
                    style="background:{rating_color};"
                >
                    {rating_value:.1f}
                </span>
            '''

        except Exception:

            rating_html = '''
                <span class="sub-rating empty">
                    —
                </span>
            '''

    else:

        rating_html = '''
            <span class="sub-rating empty">
                —
            </span>
        '''


    # ========================================================
    # SUSTITUCIÓN
    # ========================================================

    substitution = get_substitution_info(row)
    played = substitution['played']
    minute = substitution['minute']
    reason = substitution['reason']


    # ========================================================
    # JUGÓ
    # ========================================================

    if played:

        status_class = 'played'
        status_icon = '↗'

        if minute is not None:
            status_text = f"Came on {minute}'"
        else:
            status_text = 'Jugó'


    # ========================================================
    # NO JUGÓ
    # ========================================================

    else:
        status_class = 'unused'
        status_icon = '—'
        status_text = 'Unused'


    # ========================================================
    # FOTO
    # ========================================================

    if image_url:

        image_html = f'''
            <img
                src="{html.escape(
                    image_url,
                    quote=True
                )}"
                class="sub-image"
                loading="lazy"
            >
        '''

    else:

        image_html = '''
            <div class="sub-image-placeholder">
                👤
            </div>
        '''

    return f'''
        <div class="sub-card {status_class}">

            <div class="sub-photo">

                {image_html}

            </div>


            <div class="sub-content">

                <div class="sub-player-line">

                    <span class="sub-number">
                        {shirt}
                    </span>

                    <span
                        class="sub-name"
                        title="{name}"
                    >
                        {name}
                    </span>

                </div>


                <div class="sub-bottom">

                    <span class="sub-status">

                        <span class="sub-status-icon">
                            {status_icon}
                        </span>

                        {status_text}

                    </span>

                    {rating_html}

                </div>

            </div>

        </div>
    '''

def create_cards_substitutions_list(substitutes):
    # ========================================================
    # CREAR TARJETAS
    # ========================================================

    cards = []

    for _, row in substitutes.iterrows():
        cards.append( render_substitute_card(row))

    cards_html = ''.join( cards )


    # ========================================================
    # HTML + CSS
    # ========================================================

    substitutes_html = f'''
    <style>

        /* ====================================================
        CONTENEDOR
        ==================================================== */

        .substitutes-wrapper {{

            width: 100%;

            margin-top: 6px;

            box-sizing: border-box;

        }}


        /* ====================================================
        GRID
        ==================================================== */

        .substitutes-grid {{

            display: grid;

            grid-template-columns:
                repeat(2, minmax(0, 1fr));

            gap: 8px;

            width: 100%;

            box-sizing: border-box;

        }}


        /* ====================================================
        TARJETA
        ==================================================== */

        .sub-card {{

            display: flex;

            align-items: center;

            min-width: 0;

            height: 62px;

            padding: 6px 8px;

            gap: 8px;

            box-sizing: border-box;

            border-radius: 10px;

            background: #181a20;

            border:
                1px solid
                rgba(255,255,255,0.07);

            overflow: hidden;

            transition:
                transform 0.18s ease,
                border-color 0.18s ease,
                background 0.18s ease,
                opacity 0.18s ease;

        }}


        /* ====================================================
        JUGÓ
        ==================================================== */

        .sub-card.played {{

            border-color:
                rgba(46,204,113,0.38);

            background:
                linear-gradient(
                    135deg,
                    rgba(46,204,113,0.12),
                    rgba(24,26,32,0.98)
                );

        }}


        /* ====================================================
        NO JUGÓ
        ==================================================== */

        .sub-card.unused {{

            opacity: 0.70;

        }}


        /* ====================================================
        HOVER
        ==================================================== */

        .sub-card:hover {{

            transform:
                translateY(-2px);

            border-color:
                rgba(255,255,255,0.22);

        }}


        .sub-card.unused:hover {{

            opacity: 0.85;

        }}


        /* ====================================================
        FOTO
        ==================================================== */

        .sub-photo {{

            width: 45px;

            height: 50px;

            min-width: 45px;

            display: flex;

            align-items: flex-end;

            justify-content: center;

            overflow: hidden;

            border-radius: 7px;

            background:
                radial-gradient(
                    circle at 50% 100%,
                    rgba(255,255,255,0.08),
                    transparent 70%
                );

        }}


        .sub-image {{

            width: 48px;

            height: 48px;

            object-fit: contain;

            display: block;

        }}


        .sub-image-placeholder {{

            width: 38px;

            height: 38px;

            border-radius: 50%;

            background: #30343c;

            display: flex;

            align-items: center;

            justify-content: center;

            font-size: 17px;

        }}


        /* ====================================================
        CONTENIDO
        ==================================================== */

        .sub-content {{

            flex: 1;

            min-width: 0;

            height: 100%;

            display: flex;

            flex-direction: column;

            justify-content: center;

        }}


        /* ====================================================
        NOMBRE
        ==================================================== */

        .sub-player-line {{

            display: flex;

            align-items: center;

            gap: 5px;

            min-width: 0;

        }}


        .sub-number {{

            color: #777d87;

            font-size: 9px;

            font-weight: 800;

            flex-shrink: 0;

        }}


        .sub-name {{

            color: #ffffff;

            font-size: 11px;

            font-weight: 700;

            white-space: nowrap;

            overflow: hidden;

            text-overflow: ellipsis;

            min-width: 0;

        }}


        /* ====================================================
        PARTE INFERIOR
        ==================================================== */

        .sub-bottom {{

            display: flex;

            align-items: center;

            justify-content: space-between;

            gap: 5px;

            margin-top: 4px;

            min-width: 0;

        }}


        .sub-status {{

            color: #858b95;

            font-size: 8px;

            font-weight: 600;

            white-space: nowrap;

            overflow: hidden;

            text-overflow: ellipsis;

        }}


        .sub-status-icon {{

            margin-right: 2px;

        }}


        /* ====================================================
        RATING
        ==================================================== */

        .sub-rating {{

            display: inline-flex;

            align-items: center;

            justify-content: center;

            min-width: 24px;

            height: 19px;

            padding: 0 4px;

            border-radius: 5px;

            color: #111318;

            font-size: 9px;

            font-weight: 900;

            flex-shrink: 0;

        }}


        .sub-rating.empty {{

            background: #363a42 !important;

            color: #858b95;

        }}


        /* ====================================================
        TABLET
        ==================================================== */

        @media (max-width: 1000px) {{

            .substitutes-grid {{

                grid-template-columns:
                    repeat(3, minmax(0, 1fr));

                gap: 7px;

            }}

        }}


        /* ====================================================
        TABLET PEQUEÑA
        ==================================================== */

        @media (max-width: 700px) {{

            .substitutes-grid {{

                grid-template-columns:
                    repeat(2, minmax(0, 1fr));

            }}


            .sub-card {{

                height: 58px;

                padding: 5px 7px;

            }}


            .sub-photo {{

                width: 40px;

                height: 46px;

                min-width: 40px;

            }}


            .sub-image {{

                width: 44px;

                height: 44px;

            }}


            .sub-name {{

                font-size: 10px;

            }}

        }}


        /* ====================================================
        MOVIL
        ==================================================== */

        @media (max-width: 500px) {{

            .substitutes-grid {{

                grid-template-columns:
                    repeat(2, minmax(0, 1fr));

                gap: 6px;

            }}


            .sub-card {{

                height: 54px;

                padding: 4px 6px;

                gap: 6px;

                border-radius: 8px;

            }}


            .sub-photo {{

                width: 36px;

                height: 43px;

                min-width: 36px;

            }}


            .sub-image {{

                width: 40px;

                height: 40px;

            }}


            .sub-name {{

                font-size: 9px;

            }}


            .sub-number {{

                font-size: 9px;

            }}


            .sub-status {{

                font-size: 8px;

            }}


            .sub-rating {{

                min-width: 22px;

                height: 18px;

                font-size: 9px;

            }}

        }}

    </style>


    <div class="substitutes-wrapper">

        <div class="substitutes-grid">

            {cards_html}

        </div>

    </div>
    '''


    # ========================================================
    # RENDER
    # ========================================================

    st.html(
        substitutes_html
    )

















# def extract_formation_data_fotmob(df, team_name, team_side):
                            
    #     lineup = df[
    #         (df['team_name'] == team_name) &
    #         (df['player_type'] == 'starter')
    #     ].copy()

    #     # Eliminar jugadores que no tengan coordenadas
    #     lineup = lineup.dropna(
    #         subset=['verticalLayout.x', 'verticalLayout.y']
    #     ).copy()

    #     # ==========================================
    #     # FOTMOB -> STATSBOMB / MPLSOCCER
    #     # ==========================================

    #     # FotMob:
    #     # x = anchura del campo (0 -> 1)
    #     # y = longitud del campo (0 -> 1)

    #     # Coordenada vertical del campo
    #     lineup['pitch_y'] = lineup['verticalLayout.x'] * 80

    #     # Cada equipo ocupa una mitad del campo
    #     if team_side == 'home':
    #         lineup['pitch_x'] = lineup['verticalLayout.y'] * 60

    #         # Invertimos el eje lateral
    #         lineup['pitch_y'] = (
    #             (1 - lineup['verticalLayout.x']) * 80
    #         )

    #     elif team_side == 'away':
    #         lineup['pitch_x'] = 120 - (lineup['verticalLayout.y'] * 60)

    #     lineup['team'] = team_name
    #     lineup['team_side'] = team_side

    #     return lineup
    
    # def plot_initial_formation_fotmob(
    #     df,
    #     home_team,
    #     away_team,
    #     color_home,
    #     color_away,
    #     nombre_jugador_partido=None,
    #     ax=None
    # ):

    #     pitch = Pitch(
    #         pitch_type='statsbomb',
    #         pitch_color=background_color,
    #         line_color='white',
    #         linewidth=2
    #     )

    #     # ==========================================
    #     # FIGURA
    #     # ==========================================

    #     if ax is None:

    #         fig, ax = plt.subplots(figsize=(10, 7))

    #     else:

    #         fig = ax.figure

    #         ax.set_title(
    #             "INITIAL FORMATIONS",
    #             color='white',
    #             fontsize=25,
    #             fontweight='bold',
    #             path_effects=path_eff
    #         )

    #     pitch.draw(ax=ax)

    #     fig.set_facecolor('none')
    #     ax.set_facecolor('none')

    #     # ==========================================
    #     # FORMACIONES
    #     # ==========================================

    #     lineup_home = extract_formation_data_fotmob(
    #         df,
    #         home_team,
    #         'home'
    #     )

    #     lineup_away = extract_formation_data_fotmob(
    #         df,
    #         away_team,
    #         'away'
    #     )

    #     # ==========================================
    #     # HOME
    #     # ==========================================

    #     motm_home = lineup_home[
    #         lineup_home['name'] == nombre_jugador_partido
    #     ]

    #     normal_home = lineup_home[
    #         lineup_home['name'] != nombre_jugador_partido
    #     ]

    #     # Jugadores normales
    #     pitch.scatter(
    #         normal_home['pitch_x'],
    #         normal_home['pitch_y'],
    #         s=950,
    #         color=color_home,
    #         edgecolors='white',
    #         linewidth=2,
    #         ax=ax,
    #         zorder=3
    #     )

    #     # MOTM
    #     if not motm_home.empty:

    #         row = motm_home.iloc[0]

    #         x = row['pitch_x']
    #         y = row['pitch_y']
    #         jersey = row['shirtNumber']

    #         pitch.scatter(
    #             x,
    #             y,
    #             s=2000,
    #             color='gold',
    #             marker='*',
    #             edgecolors='white',
    #             linewidth=2,
    #             ax=ax,
    #             zorder=4
    #         )

    #         ax.text(
    #             x,
    #             y,
    #             str(jersey),
    #             color='black',
    #             fontsize=12,
    #             fontweight='bold',
    #             ha='center',
    #             va='center',
    #             zorder=5
    #         )

    #         ax.text(
    #             x,
    #             y + 6,
    #             row['name'],
    #             color=text_color,
    #             fontsize=7,
    #             ha='center',
    #             va='center',
    #             bbox=dict(
    #                 facecolor='#1A1A1A',
    #                 edgecolor='none',
    #                 alpha=0.6,
    #                 pad=0.3
    #             ),
    #             zorder=5
    #         )

    #     # Nombres + dorsales
    #     for _, row in normal_home.iterrows():

    #         ax.text(
    #             row['pitch_x'],
    #             row['pitch_y'],
    #             str(row['shirtNumber']),
    #             color='black',
    #             fontsize=12,
    #             fontweight='bold',
    #             ha='center',
    #             va='center',
    #             zorder=4
    #         )

    #         ax.text(
    #             row['pitch_x'],
    #             row['pitch_y'] + 6,
    #             row['name'],
    #             color=text_color,
    #             fontsize=7,
    #             ha='center',
    #             va='center',
    #             bbox=dict(
    #                 facecolor='#1A1A1A',
    #                 edgecolor='none',
    #                 alpha=0.6,
    #                 pad=0.3
    #             ),
    #             zorder=4
    #         )

    #     # ==========================================
    #     # AWAY
    #     # ==========================================

    #     motm_away = lineup_away[
    #         lineup_away['name'] == nombre_jugador_partido
    #     ]

    #     normal_away = lineup_away[
    #         lineup_away['name'] != nombre_jugador_partido
    #     ]

    #     # Jugadores normales
    #     pitch.scatter(
    #         normal_away['pitch_x'],
    #         normal_away['pitch_y'],
    #         s=950,
    #         color=color_away,
    #         edgecolors='white',
    #         linewidth=2,
    #         ax=ax,
    #         zorder=3
    #     )

    #     # MOTM
    #     if not motm_away.empty:

    #         row = motm_away.iloc[0]

    #         x = row['pitch_x']
    #         y = row['pitch_y']
    #         jersey = row['shirtNumber']

    #         pitch.scatter(
    #             x,
    #             y,
    #             s=2000,
    #             color='gold',
    #             marker='*',
    #             edgecolors='white',
    #             linewidth=2,
    #             ax=ax,
    #             zorder=4
    #         )

    #         ax.text(
    #             x,
    #             y,
    #             str(jersey),
    #             color='black',
    #             fontsize=12,
    #             fontweight='bold',
    #             ha='center',
    #             va='center',
    #             zorder=5
    #         )

    #         ax.text(
    #             x,
    #             y + 6,
    #             row['name'],
    #             color=text_color,
    #             fontsize=7,
    #             ha='center',
    #             va='center',
    #             bbox=dict(
    #                 facecolor='#1A1A1A',
    #                 edgecolor='none',
    #                 alpha=0.6,
    #                 pad=0.3
    #             ),
    #             zorder=5
    #         )

    #     # Nombres + dorsales AWAY
    #     for _, row in normal_away.iterrows():

    #         ax.text(
    #             row['pitch_x'],
    #             row['pitch_y'],
    #             str(row['shirtNumber']),
    #             color='black',
    #             fontsize=12,
    #             fontweight='bold',
    #             ha='center',
    #             va='center',
    #             zorder=4
    #         )

    #         ax.text(
    #             row['pitch_x'],
    #             row['pitch_y'] + 6,
    #             row['name'],
    #             color=text_color,
    #             fontsize=7,
    #             ha='center',
    #             va='center',
    #             bbox=dict(
    #                 facecolor='#1A1A1A',
    #                 edgecolor='none',
    #                 alpha=0.6,
    #                 pad=0.3
    #             ),
    #             zorder=4
    #         )

    #     return fig, ax

    # fig, ax = plot_initial_formation_fotmob(
    #     df_players_fotmob,
    #     home_team=home_team,
    #     away_team=away_team,
    #     color_home=color_home,
    #     color_away=color_away,
    #     nombre_jugador_partido=player_of_the_match
    # )
    # st.pyplot(fig)
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from mplsoccer import Bumpy
import highlight_text 

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from frontend.providers.fotmob import *


def create_plot_xg_standings(tabla_df: pd.DataFrame) -> None:
    if tabla_df is None or tabla_df.empty:
        st.info(f"No hay datos suficientes para mostrar la clasificación xG para la temporada {st.session_state.temporada}.")

    else:
        tabla_df = round(tabla_df, 1)
        df = tabla_df.copy()

        # =========================
        # HEADER
        # =========================
        c0, c1, c2, c3, c4, c5, c6, c7 , c8= st.columns([0.2, 0.5, 1,  1, 5, 2, 2, 2, 2])

        with c0:
            st.write("")

        with c1:
            st.markdown("<b>#</b>", unsafe_allow_html=True)

        with c3:
            st.markdown("<b></b>", unsafe_allow_html=True)

        with c4:
            st.markdown("<b>Team</b>", unsafe_allow_html=True)

        with c5:
            st.markdown("<b>PJ</b>", unsafe_allow_html=True)

        with c6:
            st.markdown("<b>xG</b>", unsafe_allow_html=True)

        with c7:
            st.markdown("<b>xGA</b>", unsafe_allow_html=True)

        with c8:
            st.markdown("<b>xPTS</b>", unsafe_allow_html=True)

        st.markdown("<hr style='margin:4px 0 6px 0;'>", unsafe_allow_html=True)

        for _, row in df.iterrows():

            c0, c1, c2, c3, c4, c5, c6, c7 , c8= st.columns([0.2, 0.5, 1,  1, 5, 2, 2, 2, 2])

            # Barra de clasificación
            with c0:
                st.markdown(
                    f"""
                    <div style="
                        background:{row['qualColor']};
                        width:6px;
                        height:42px;
                        border-radius:3px;
                        margin:auto;
                    "></div>
                    """,
                    unsafe_allow_html=True,
                )

                with c1:
                    st.markdown(
                        f"""
                        <div style="font-weight:bold;">
                            {row['xPosition']}
                        </div>

                        """,
                        unsafe_allow_html=True,
                    )
                # Posición esperada
                with c2:
                    st.markdown(
                        f"""
                        <div style="font-size:15px;">
                            {format_pos_diff(row['xPositionDiff'])}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with c3:
                    st.image(row["team_logo"], width=35)

                with c4:
                    st.markdown(
                        f"""
                        <div style="font-weight:bold;">
                            {row['name']}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                with c5:
                    st.write(str(row["played"]))

                with c6:
                    st.markdown(
                        f"""
                        <div>{row['xg']}</div>
                        <div style="font-size:14px;">
                            {format_diff_xg(row['xgDiff'])}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                with c7:
                    st.markdown(
                        f"""
                        <div>{row['xgConceded']}</div>
                        <div style="font-size:14px;">
                            {format_diff_xga(row['xgConcededDiff'])}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                with c8:
                    st.markdown(
                        f"""
                        <div>{row['xPoints']}</div>
                        <div style="font-size:14px;">
                            {format_diff_xpts(row['xPointsDiff'])}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

def create_plot_standings(tabla_df: pd.DataFrame) -> None:
    """
    Render a standings table using a custom Streamlit layout.

    This function builds a visually structured league table with:
    - Team rankings
    - Match statistics
    - Goals and points
    - Qualification status

    Args:
        tabla_df (pd.DataFrame): Standings dataset.

    Returns:
        None
    """

    # =========================
    # SHOULD SHOW NEXT OPPONENT?
    # =========================
    show_next_opponent = "team_logo_url_opponent" in tabla_df.columns
    # =========================
    # HEADER COLUMNS
    # =========================
    if show_next_opponent:
        c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11 = st.columns( [1, 1, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2])
    else:
        c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10 = st.columns([1, 1, 4, 2, 2, 2, 2, 2, 2, 2, 2])

    with c1:
        st.write("")

    with c2:
        st.markdown(
            """
            <span style="font-size:14px; font-weight:bold;">
                Team
            </span><br>
            <small style="font-size:12px;">
                (Qualification Status)
            </small>
            """,
            unsafe_allow_html=True
        )

    headers = [
        ("Played Games", c3),
        ("Wins", c4),
        ("Draws", c5),
        ("Losses", c6),
        ("Goals Scored", c7),
        ("Goals Against", c8),
        ("Goal Diff", c9),
        ("Points", c10),
    ]

    if show_next_opponent:
        headers.append(("Next Opponent", c11))


    for label, col in headers:
        with col:
            st.markdown(
                f"<p style='font-size:14px;'>{label}</p>",
                unsafe_allow_html=True
            )

    st.markdown("<hr style='margin:4px 0 6px 0;'>", unsafe_allow_html=True)

    # =========================
    # TABLE ROWS
    # =========================
    for _, row in tabla_df.iterrows():

        if show_next_opponent:
            c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11 = st.columns(
                [1, 1, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2]
            )
        else:
            c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10 = st.columns(
                [1, 1, 5, 2, 2, 2, 2, 2, 2, 2, 2]
            )

        with c0:
            st.markdown(
                f"""
                <div style="
                    background:{row['qualColor']};
                    width:6px;
                    height:42px;
                    border-radius:3px;
                    margin:auto;
                "></div>
                """,
                unsafe_allow_html=True,
            )

        with c1:
            st.image(row["team_logo"], width=40)

        with c2:
            st.markdown(
                f"<div style='font-size:13px; font-weight:bold;'>{row['idx']}. {row['name']}</div>",
                unsafe_allow_html=True
            )

            if pd.notna(row["competition"]):
                st.markdown(
                    f"<div style='font-size:10px; color: var(--text-color-secondary);opacity:0.6;'>{row['competition']}</div>",
                    unsafe_allow_html=True
                )


        # =========================
        # STATS COLUMNS
        # =========================
        with c3:
            st.write(str(row["played"]))

        with c4:
            st.write(str(row["wins"]))

        with c5:
            st.write(str(row["draws"]))

        with c6:
            st.write(str(row["losses"]))

        with c7:
            st.write(str(row["goals_for"]))

        with c8:
            st.write(str(row["goals_against"]))

        with c9:
            st.write(str(row["goalConDiff"]))

        with c10:
            st.write(str(row["pts"]))   

        if show_next_opponent:
            with c11:
                if pd.notna(row["team_logo_url_opponent"]):
                    st.image(row["team_logo_url_opponent"], width=40)

def markdown_legend():
    st.markdown(
        """
        <div style='display: flex; gap: 30px; font-size: 16px;'>
            <div><span style='color: #0066ff;'>●</span> Champions League</div>
            <div><span style='color: #00cc66;'>●</span> Europa League</div>
            <div><span style='color: #cc66ff;'>●</span> Conference League</div>
            <div><span style='color: #ff3333;'>●</span> Descenso</div>
        </div>
        """,
        unsafe_allow_html=True
    )

#---------------------------------------------RANKING TRAJECTORY---------------------------------

def limpieza_df_classjornada(df, mapeo_equipos: dict):

    df_limpieza = df.copy()

    # Reemplazar nombres de equipos
    df_limpieza['team'] = df_limpieza['team'].replace(mapeo_equipos)

    # Pivotar: jornadas como filas y equipos como columnas
    df_pivot = df_limpieza.pivot( index='matchweek', columns='team', values='position')

    # Convertir jornada a número
    df_pivot.index = df_pivot.index.astype(int)

    # Ordenar por jornada
    df_pivot = df_pivot.sort_index()

    return df_pivot

def plot_bumpy_chart(df, highlight_dict, equipos_elegidos=None):
                    
    """
    Genera un Bumpy Chart a partir del DataFrame de posiciones y un diccionario de colores.
    
    Parámetros:
    - df: DataFrame (index=Jornadas, columns=Equipos, values=Posiciones)
    - highlight_dict: diccionario con los colores de cada equipo
    - equipos_elegidos: lista de equipos a visualizar (opcional; si None, se visualizan todos)
    
    Devuelve:
    - fig, ax: figura y eje generados por mplsoccer.Bumpy
    """
    
    # Filtrar solo los equipos seleccionados si se especifica
    if equipos_elegidos is not None:
        equipos_a_plotear = [equipo for equipo in equipos_elegidos if equipo in df.columns]
        df_filtrado = df[equipos_a_plotear]
    else:
        df_filtrado = df

    # Preparar lista de jornadas (x)
    jornadas = df_filtrado.index.tolist()

    # Instanciar Bumpy Chart
    bumpy = Bumpy(
                    scatter_color = '#282828', line_color = '#252525',
                    rotate_xticks=90,
                    ticklabel_size = 15,
                    scatter_primary = 'D',
                    show_right = True,
                    plot_labels = True,
                    alignment_yvalue=.1,
                    alignment_xvalue = .065
                )
    
    # Plotear
    fig, ax = bumpy.plot(
        x_list=jornadas,
        y_list=np.linspace(1,20,20).astype(int),
        values=df_filtrado,
        secondary_alpha=0.5,
        highlight_dict=highlight_dict,
        figsize=(18,18),
        y_label='Position',
        x_label='Matchweek',
        ylim=(-0.1, 22),
        lw=2.5,
    )
    # Fondo transparente:
    fig.patch.set_alpha(0)   # fondo de la figura
    ax.patch.set_alpha(0)    # fondo del eje
    


    # Subtítulo con ejemplo (puedes adaptarlo o quitarlo)
    equipos_highlight = ', '.join([f"<{e}>" for e in equipos_elegidos]) if equipos_elegidos else ''
    highlight_colors = [
        {"color": highlight_dict.get(equipo, 'white')}
        for equipo in (equipos_elegidos if equipos_elegidos else df_filtrado.columns)
    ]

    highlight_text.fig_text(
        x=0.5,
        y=0.875,
        s=f'Comparing: {equipos_highlight}',
        highlight_textprops=highlight_colors,
        fontsize=20,
        color='white',
        ha='center'
    )

    return fig, ax

def render_ranking_trajectory(df_standings_tracker_league):
    
    df_classjornadas_limpio = limpieza_df_classjornada(df_standings_tracker_league, MAPPING_TEAM_NAME_TRANSFERMARKET_TO_FOTMOB)

    equipos_disponibles = df_classjornadas_limpio.columns.difference(["matchweek", "matchweek_num"]).tolist()

    equipos_elegidos = st.multiselect("Select teams to compare:",equipos_disponibles)
    
    if len(equipos_elegidos) < 2:
        st.warning("Select at least 2 teams to compare.")
    else:
        fig, ax = plot_bumpy_chart(df_classjornadas_limpio, HIGHLIGHT_DICT, equipos_elegidos=equipos_elegidos)
        st.pyplot(fig, use_container_width=True)
#---------------------------------------------TEAM OF THE WEEK/SEASON-----------------------------

def titulo_team_of_week(selected_round):

    # Visual title
      st.markdown(
         f"""
         <div style="
            background-color:#1e1e1e;
            padding:20px;
            border-radius:12px;
            border:1px solid #333;
            text-align:center;
            margin-bottom:20px;
         ">
            <h1 style="
                  color:#33c771;
                  margin:0;
                  font-size:32px;
            ">
                  ⭐ Team of the Week
            </h1>

            <p style="
                  color:white;
                  font-size:20px;
                  margin:8px 0 0 0;
            ">
                  Matchweek: {selected_round}
            </p>

         </div>
         """,
         unsafe_allow_html=True
      )

def titulo_team_of_season():

    # Visual title
      st.markdown(
         f"""
         <div style="
            background-color:#1e1e1e;
            padding:20px;
            border-radius:12px;
            border:1px solid #333;
            text-align:center;
            margin-bottom:20px;
         ">
            <h1 style="
                  color:#33c771;
                  margin:0;
                  font-size:32px;
            ">
                  ⭐ Team of the Season 
            </h1>

         </div>
         """,
         unsafe_allow_html=True
      )

def team_of_the_week_plot(df, escala_posicion=100):

    campo_img = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Soccer_field_illustration.svg/1200px-Soccer_field_illustration.svg.png"

    html_jugadores = ""

    for _, row in df.iterrows():
        x = row['pos_x'] * escala_posicion
        y = row['pos_y'] * escala_posicion
        foto = row['member_photo']
        logo = row['url_logo_team']
        nombre = row['player']
        rating = row['rating']
        color_fondo = row['rating.bgcolor']

        html_jugadores += f"""
        <div style="
            position:absolute;
            left:{x}%;
            top:{y}%;
            transform:translate(-50%, -50%);
            text-align:center;
            color:white;
            font-weight:bold;
            font-family:Arial,sans-serif;
        ">

            <div style="position:relative; width:40px; height:40px; margin:auto;">

                <img src="{foto}" width="35" height="35"
                     style="border-radius:50%; border:2px solid white;">

                <img src="{logo}" width="15" height="15"
                     style="
                        position:absolute;
                        bottom:-2px;
                        left:30px;
                        border-radius:50%;
                        background:white;
                        padding:1px;
                     ">

            </div>

            <div style="font-size:10px;  margin-top:8px;">{nombre}</div>

            <div style="
                background:{color_fondo};
                color:white;
                margin-top:6px;
                padding:2px 6px;
                border-radius:8px;
                display:inline-block;
                font-size:11px;
            ">
                {rating}
            </div>

        </div>
        """

    html = f"""
    <div style="
        position:relative;
        width:100%;
        max-width:700px;
        aspect-ratio: 7 / 5;
        margin:auto;
        background-image:url('{campo_img}');
        background-size:contain;
        background-repeat:no-repeat;
        background-position:center;
    ">
        {html_jugadores}
    </div>
    """


    return html

def render_standings(temporada, league):
    data, color_map = extract_data_json_standings(temporada, league)
    
    sections = {
        "🏆 General": "all",
        "🏠 Home": "home",
        "✈️ Away": "away",
        "🔥 Last 5": "form",
        "📊 xG": "xg",
    }
    available_tables = data["table"][0]["data"]["table"]
    sections = {
        label: key
        for label, key in sections.items()
        if key in available_tables
    }

    tabs = st.tabs(list(sections.keys()))

    for tab, (_, table_type) in zip(tabs, sections.items()):
        with tab:
            tabla = obtener_tabla(data, color_map, table_type)
            if tabla.empty:
                st.info(f"No hay datos para la clasificación '{table_type}' en esta temporada.")
                continue

            opponent_df = extract_info_opponent(data)

            if not opponent_df.empty:
                final_tabla = tabla.merge(opponent_df, on="id", how="left")
            else:
                final_tabla = tabla.copy()
                                
            if table_type == "xg":
                with st.expander("ℹ️ ¿Qué es la clasificación xG?"):
                    st.markdown("""
                    La **clasificación xG** (Expected Goals o Goles Esperados) ordena a los equipos según su rendimiento **esperado**, 
                    no únicamente en base a los resultados reales. Se basa en métricas avanzadas que evalúan la calidad de las ocasiones generadas y recibidas.

                    - **xG (Expected Goals):** Goles que un equipo *debería haber marcado* según la calidad de sus ocasiones.
                    - **xGA (Expected Goals Against):** Goles que *debería haber encajado* según las ocasiones concedidas.
                    - **xPTS (Expected Points):** Puntos que *debería tener* según sus xG y xGA.

                    ---
                    - Los **números verdes** indican que un equipo está rindiendo **por encima de lo esperado**.
                    - Los **números rojos** indican que el equipo está **por debajo del rendimiento esperado**.
                    - El número pequeño junto a cada valor muestra la **diferencia entre el rendimiento real y el esperado**.
                    
                    Esta tabla es útil para detectar si un equipo está siendo eficaz o ineficiente en ataque o defensa, más allá del resultado final.
                    """)

                
                with st.container(border=True):
                    create_plot_xg_standings(final_tabla)

            else:
                with st.container(border=True):
                    create_plot_standings(final_tabla)

    st.write("")
    markdown_legend()

def render_team_of_week(temporada, liga):

    if temporada == '2025/2026':
        paises_liga = {
            "Premier League": "ENG",
            "LaLiga": "ESP",
            "Serie A": "ITA",
            "Bundesliga": "GER",
            "Ligue 1": "FRA",
        }

        totw_por_liga = {}
        totw_global_por_liga = {}

        for nombre_liga, info in LIGAS_TOTW.items():
            df_temp = obtener_totw_temporada(
                nombre_liga, info["id"], info["rondas"],
                season=temporada, pais=paises_liga[nombre_liga], debug=True
            )
            totw_por_liga[nombre_liga] = df_temp
            totw_global_por_liga[nombre_liga] = totw_global_temporada(df_temp)

        tow_league= totw_por_liga[liga]

        # Keep only the rounds available in the dataframe
        rounds_available =tow_league["matchweek"].dropna().unique()

        selected_round = st.selectbox( "Select matchweek", rounds_available)

        if selected_round != 'Team of the Season':

            titulo_team_of_week(selected_round)

        else:
            titulo_team_of_season()

        st.write(' ')
        st.write(' ')
        st.write(' ')

        df_week = tow_league[ tow_league["matchweek"] == selected_round ].copy()
        html = team_of_the_week_plot(df_week)
        
        components.html(  html,  height=520,scrolling=True)

    else: 
        st.info('No data available yet. Data will appear once the league starts.')
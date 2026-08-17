import streamlit as st
import pandas as pd


import sys
from pathlib import Path
from st_clickable_images import clickable_images

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

def render_teams(df):

    st.subheader("🌍 Competing Teams")
    st.info("Select a team by tapping its badge.")

    st.markdown(
        """
        <style>
        .team-card {
            text-align: center;
            padding: 2px;
        }

        .team-name {
            text-align: center;
            font-weight: 600;
            margin-top: 3px;
            color: white;
            font-size: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(4)

    for i, row in enumerate(df.to_dict("records")):

        with cols[i % 4]:

            with st.container(border=True):
            
                clicked = clickable_images(
                    [row["logo_team_fotmob"]],
                    titles=[f"View {row['name_team_fotmob']}"],
                    div_style={
                        "display": "flex",
                        "justify-content": "center",
                    },
                    img_style={
                        "width": "140px",
                        "border-radius": "12px",
                        "padding": "12px",
                        "background-color": "#2e2e2e",
                        "box-shadow": "0 2px 8px rgba(0,0,0,0.25)",
                        "transition": "all 0.2s ease-in-out",
                    },
                    key=f"team_{i}",
                )

                st.markdown(
                    f"""
                    <div class="team-card">
                        <div class="team-name">
                            {row['name_team_fotmob'].upper()}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if clicked > -1:
                    st.session_state.selected_team = row["name_team_fotmob"]
                    st.session_state.page = "team_detail"
                    st.rerun()

def render_teams1(df):

    st.subheader("🌍 Competing Teams")
    st.info("Select a team by tapping its badge.")

    # -----------------------------
    # CSS
    # -----------------------------

    st.markdown(
        """
        <style>

        .team-card {
            text-align: center;
            padding: 5px;
        }

        .team-name {
            text-align: center;
            font-weight: 600;
            margin-top: 8px;
            color: white;
            font-size: 20px;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------
    # GRID
    # -----------------------------

    cols = st.columns(4)

    for i, row in enumerate(df.to_dict("records")):

        team_name = row["name_team_fotmob"]
        logo = row["logo_team_fotmob"]

        with cols[i % 4]:

            with st.container(border=True):

                # -----------------------------
                # TEAM LOGO
                # -----------------------------

                st.markdown(
                    """
                    <div class="team-card">
                    """,
                    unsafe_allow_html=True,
                )

                st.image(
                    logo,
                    width=140,
                )

                st.markdown(
                    f"""
                        <div class="team-name">
                            {team_name.upper()}
                        </div>
                    """,
                    unsafe_allow_html=True,
                )

                # -----------------------------
                # BUTTON
                # -----------------------------

                if st.button(
                    "Ver equipo",
                    key=f"team_{i}",
                    use_container_width=True,
                ):

                    st.session_state.selected_team = team_name
                    st.session_state.page = "team_detail"

                    st.rerun()
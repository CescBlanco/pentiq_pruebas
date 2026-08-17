import streamlit as st
import pandas as pd


import sys
from pathlib import Path
from st_clickable_images import clickable_images

from pydeck.data_utils.viewport_helpers import compute_view
import folium
import pandas as pd
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import plotly.express as px

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


# =====================================================
# METRICS
# =====================================================
def stadium_metrics(df):
    
    if df.empty:
        return

    total = len(df)

    avg_capacity = df["capacity"].mean()


    largest = df.loc[df["capacity"].idxmax()]



    newest = df.loc[df["opened"].idxmax()]

    # ------------------------------
    # CSS
    # ------------------------------

    st.markdown(
        """
        <style>

        div[data-testid="stMetricLabel"] {
            font-size: 13px;
        }

        div[data-testid="stMetricValue"] {
            font-size: 26px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )
    
    # -------------------------------
    # INSIGHTS
    # -------------------------------

    st.markdown("")

    with st.container(border=True):

        st.markdown("### 📊 Stadium overview")

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric("🏟️ Total stadiums",total )
            
        with col2:

            st.metric( "👥 Avg capacity",  f"{avg_capacity:,.0f}")

        with col3:
            st.markdown("🏆 **Biggest stadium**")
            
            st.write(largest["name_venue"])

            st.caption(f"{largest['capacity']:,} seats")

        with col4:
            
            st.markdown("🆕 **Newest stadium**")

            st.write(newest["name_venue"])

            st.caption(f"Opened {newest['opened']}")

        with col5:

            st.markdown( "🌱 **Pitch surfaces**" )
            surface_counts = (df["surface"] .value_counts())

            main_surface = (surface_counts.index[0])
            st.write( main_surface)

            st.caption(  f"{surface_counts.iloc[0]} stadiums")

def map_venues_folium(df: pd.DataFrame) -> dict:
    """
    Interactive stadium map using Folium.

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    dict
        Output returned by st_folium().
    """
    st.markdown("## 🌍 Interactive map")

    st.info("Hover over a crest to identify the team.\nClick to open the stadium profile.")

    df = df.copy()

    df["lat_venue"] = pd.to_numeric(df["lat_venue"], errors="coerce")
    df["lon_venue"] = pd.to_numeric(df["lon_venue"], errors="coerce")

    df = df.dropna(subset=["lat_venue", "lon_venue"])

    # ----------------------------------------------------
    # Compute center
    # ----------------------------------------------------

    view_state = compute_view( df[["lon_venue", "lat_venue"]],view_proportion=0.8)

    m = folium.Map(
            location=[view_state.latitude, view_state.longitude],
            zoom_start=view_state.zoom,
            tiles="CartoDB dark_matter",
            control_scale=True,
        )

    # ----------------------------------------------------
    # Cluster
    # ----------------------------------------------------
    cluster = MarkerCluster(disableClusteringAtZoom=5).add_to(m)

    # ----------------------------------------------------
    # Stadiums
    # ----------------------------------------------------

    for _, row in df.iterrows():
        
        popup = folium.Popup(
            f"""
            <div style="width:250px;font-family:Arial">

            <center>

            <img src="{row["logo_team_fotmob"]}" width="70">

            <h4 style="margin-bottom:4px">
            {row["name_venue"]}
            </h4>

            <b>{row["city_venue"]}</b>,
            {row["country_code_fotmob"]}

            <img src="{row['url_photo_stadium']}"
                                width="220"
                                style="border-radius:8px;margin-bottom:8px;">
            </center>

            👥 <b>Capacity:</b> {row["capacity"]}<br>

            🌱 <b>Surface:</b> {row["surface"]}<br>

            📅 <b>Opened:</b> {row["opened"]}

            </div>
            """,
            max_width=300,
        )

        tooltip = f"""
        <b>{row["name_team_fotmob"]}</b>
        """

        icon = folium.CustomIcon( row["logo_team_fotmob"], icon_size=(38, 38),)

        folium.Marker(
                location=[
                    row["lat_venue"],
                    row["lon_venue"]
                ],
                icon=icon,
                tooltip=tooltip,
                popup=popup,
            ).add_to(cluster)

    # ----------------------------------------------------
    # Render
    # ----------------------------------------------------
    output = st_folium(
            m,
            width=None,
            height=700,
            returned_objects=["zoom", "last_clicked"],
        )

    return output

# =====================================================
# RANKING
# =====================================================
def capacity_ranking(teams_league2):

    with st.container(border=True):

        st.markdown("### 🏆 Capacity ranking")


        ranking = (
            teams_league2[
                [
                    "name_team_fotmob",
                    "name_venue",
                    "capacity"
                ]
            ]
            .sort_values(
                "capacity",
                ascending=False
            )
        )

        fig = px.bar(
            ranking,
            x="capacity",
            y="name_team_fotmob",
            orientation="h",
            text="capacity",
            hover_data={
                "name_team_fotmob": False,
                "capacity": True,
                "name_venue": True
            },
            labels={
                "name_venue": "Name Venue",
                "capacity": "Seats",
                "name_team_fotmob": ""
            }
        )


        fig.update_traces(
            texttemplate="%{text:,}",
            textposition="outside"
        )


        fig.update_layout(
            height=600,
            yaxis={
                "categoryorder": "total ascending"
            },
            showlegend=False,
            margin=dict(
                l=20,
                r=40,
                t=20,
                b=20
            )
        )


        st.plotly_chart( fig, use_container_width=True)


def stadium_gallery(df):

    st.markdown("## 📸 Stadium Gallery")


    if "gallery_index" not in st.session_state:

        st.session_state.gallery_index = 0



    selected = st.selectbox(
        "Choose stadium",
        df["name_venue"],
        index=st.session_state.gallery_index
    )


    st.session_state.gallery_index = (
        df.index[
            df["name_venue"] == selected
        ][0]
    )


    row = df.iloc[
        st.session_state.gallery_index
    ]



    col1, col2 = st.columns(
        [1,4]
    )


    with col1:

        st.image(
            row["logo_team_fotmob"],
            width=90
        )


    with col2:

        st.markdown(
            f"""
            ## {row['name_team_fotmob']}

            ### 🏟️ {row['name_venue']}
            """
        )



    st.image(
        row["url_photo_stadium"],
        use_container_width=True
    )



    col1, col2 = st.columns(2)


    with col1:

        if st.button("⬅️ Previous"):

            st.session_state.gallery_index = (
                st.session_state.gallery_index - 1
            ) % len(df)

            st.rerun()



    with col2:

        if st.button("Next ➡️"):

            st.session_state.gallery_index = (
                st.session_state.gallery_index + 1
            ) % len(df)

            st.rerun()



    st.caption(
        f"""
        Stadium 
        {st.session_state.gallery_index + 1}
        /
        {len(df)}
        """
    )


def render_venues(df):

    stadium_metrics(df)
        
    st.divider()

    map_venues_folium(df)
    st.divider()

    capacity_ranking(df)

    st.divider()

    stadium_gallery(df)

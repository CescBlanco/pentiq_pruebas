import streamlit as st
from st_clickable_images import clickable_images

from utils.constants import *

def markdown_initial_selection_league():
    st.markdown("""
        <style>
        div[data-testid="stButton"] > button {
            background-color: #1f1f1f !important;
            color: #eaeaea !important;
            border: 1px solid #333 !important;
            border-radius: 10px !important;
            padding: 0.4rem 1rem !important;
            transition: all 0.2s ease;
        }

        div[data-testid="stButton"] > button:hover {
            background-color: #2a2a2a !important;
            border-color: #555 !important;
        }
        </style>
        """, unsafe_allow_html=True)
    
def seleccionar_liga():

    st.subheader("⚽ Selecciona una competición")
    st.info("Pulsa sobre el logo de la competición para comenzar.")

    cols = st.columns(5)

    for i, (codigo, liga) in enumerate(COMPETICIONES.items()):

        with cols[i % 5]:

            with st.container(border=True):

                st.markdown("""
                <style>
                .league-card {
                    text-align: center;
                    padding: 1px;
                }

                .league-name {
                    text-align: center;
                    font-weight: 600;
                    margin-top: -0.01px;
                    font-size: 18px;
                }
                </style>
                """, unsafe_allow_html=True)

                clicked = clickable_images(
                    [liga["logo"]],
                    titles=[liga["nombre"]],
                    div_style={
                        "display": "flex",
                        "justify-content": "center",
                    },
                    img_style={
                        "width": "120px",
                        "border-radius": "12px",
                        "padding": "10px",
                        "background-color": "#938e8e",
                        "box-shadow": "0 2px 8px rgba(0,0,0,0.25)",
                        "cursor": "pointer",
                        "transition": "all 0.2s ease-in-out",
                    },
                    key=f"league_{codigo}",
                )

                st.markdown(
                    f"""
                    <div class="league-card">
                        <div class="league-name">
                            {liga["nombre"].upper()}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if clicked > -1:
                    st.session_state.liga = codigo
                    st.rerun()

# -----------------------------
# SIDEBAR PRINCIPAL
# -----------------------------

def mostrar_sidebar():

    usuario = st.session_state.usuario

    st.sidebar.image("data/logo_pentiq.png")

    st.sidebar.divider()

    st.sidebar.caption("Profile")

    st.sidebar.write(  f"👤 Welcome: {usuario['nombre']} {usuario['apellido']}")

    st.sidebar.write( f"🌍 {usuario['pais']}")

    st.sidebar.divider()


    # Si ya hay competición seleccionada
    if st.session_state.liga:

        liga_actual = COMPETICIONES[ st.session_state.liga]
        st.sidebar.caption("Selected league")
        st.sidebar.markdown(f"**{liga_actual['nombre']}**")

        st.sidebar.caption("Season")

        temporada = st.sidebar.segmented_control(
            label="Season", options=["2025/2026","2026/2027"],
            default=st.session_state.temporada,
            label_visibility="collapsed"
            )

        if temporada:
            st.session_state.temporada = temporada

        st.sidebar.divider()

        opciones = [
            "⚽ Teams",
            "👥 Plantillas",
            "🏆 Standings",
            "📅 Match schedule",
            "⚽ Results",
            "📊 Estadísticas",
            "🔄 Transferencias",
            "🏟️ Venues"
        ]

        pagina = st.sidebar.radio("Menu", opciones, index=opciones.index("⚽ Results"))


    else:      
        st.sidebar.markdown(
                """
                    ### ⚽ Welcome to PENTIQ

                    No competition selected yet.

                    Select a league to get started.
                    """
            )

        pagina = "Select league"


    if st.sidebar.button("🔄 Change competition"):

        st.session_state.liga = None
        st.rerun()

    return pagina

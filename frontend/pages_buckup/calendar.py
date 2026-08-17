import streamlit as st
from streamlit_calendar import calendar
import pandas as pd



def prepare_matches(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["match_date"] = pd.to_datetime(
        df["match_date"].astype(str) + " " + df["match_time"].astype(str),
        errors="coerce"
    )

    df["date_only"] = df["match_date"].dt.strftime("%Y-%m-%d")

    df["time_display"] = df["match_date"].dt.strftime("%H:%M")
    df = df.astype(object).where(pd.notna(df), None)

    return df

def dataframe_to_events(df: pd.DataFrame):
    events = []

    for _, row in df.iterrows():
        home = row["home_team_name"]
        away = row["away_team_name"]
        score = row["score_str"]

        if row["reason_short"] == "FT":
            title = f"⚽ {home} {score} {away}"
        else:
            title = f"⚽ {home} vs {away}"
        event = {
            "id": str(row["match_id"]),

            "title": title,

            "start": row["match_date"].strftime("%Y-%m-%dT%H:%M:%S"),

            "allDay": False,

            "extendedProps": {
                "match_id": row["match_id"],
                "home_team": row["home_team_name"],
                "away_team": row["away_team_name"],
                "home_team_id": row["home_team_id"],
                "away_team_id": row["away_team_id"],
                "home_team_logo": row["home_logo"],
                "away_team_logo": row["away_logo"],
                "score": row["score_str"],
                "status": row["reason_short"],
                "stadium": row["name_venue"],
                "city": row["city_venue"],
                "capacity": row["capacity"],
                "match_url": row["page_url"],
                "matchweek": row["round"],
            }
        }

        # Color según estado
        if row["reason_short"] == "FT":
            event["backgroundColor"] = "#16a34a"
            event["borderColor"] = "#16a34a"

        else:
            event["backgroundColor"] = "#2563eb"
            event["borderColor"] = "#2563eb"

        events.append(event)

    return events

def show_calendar(events):

    calendar_options = {

        "initialView": "dayGridMonth",
        "firstDay": 1,
        "nowIndicator": True,
        "height": 700,

        "expandRows": True,

        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek"
        },

        "buttonText": {
            "today": "Today"
        },

        "eventDisplay": "block",

        "eventTimeFormat": {
            "hour": "2-digit",
            "minute": "2-digit",
            "hour12": False
        },
        "displayEventTime": True,
        "dayMaxEvents": True,
        "navLinks": True,


    }

    calendar_result = calendar(
        events=events,
        options=calendar_options,
        custom_css="""
        .fc {
            font-family: Inter, sans-serif;
        }

        .fc-toolbar-title {
            font-size: 1.35rem !important;
            font-weight: 700 !important;
        }

        .fc-button {
            border-radius: 8px !important;
            border: none !important;
        }

        .fc-daygrid-day {
            min-height: 110px;
        }

        .fc-event {
            border-radius: 7px !important;
            border: none !important;
            padding: 3px 5px !important;
            cursor: pointer !important;
            font-size: 0.78rem !important;
        }

        .fc-event:hover {
            opacity: 0.85;
            transform: translateY(-1px);
        }

        .fc-day-today {
            background: rgba(37, 99, 235, 0.06) !important;
        }

        @media (max-width: 768px) {

            .fc-toolbar {
                flex-direction: column;
                gap: 10px;
            }

            .fc-toolbar-title {
                font-size: 1.1rem !important;
            }

            .fc-daygrid-day {
                min-height: 75px;
            }

            .fc-event {
                font-size: 0.68rem !important;
                padding: 2px 3px !important;
            }

            .fc-daygrid-event-dot {
                display: none;
            }
        }
        """,
        key="football_calendar"
    )

    return calendar_result

@st.dialog("🏟️ Match Overview")
def show_match_detail(match):

    # --------------------------------------------------
    # Estado
    # --------------------------------------------------

    status = match["reason_short"]

    if status == "FT":
        status_text = "FINISHED"
        status_color = "green"
    else:
        status_text = "UPCOMING"
        status_color = "blue"

    # --------------------------------------------------
    # Fecha
    # --------------------------------------------------

    match_date = match["match_date"]

    date_text = match_date.strftime("%A %d %B %Y")

    # --------------------------------------------------
    # Cabecera
    # --------------------------------------------------

    st.markdown(
        f"### {date_text} (Matchweek {match['round']})" 
    )

    st.caption(
        f"🕐 {match['time_display']} · "
        f":{status_color}[{status_text}]"
    )

    st.divider()

    # --------------------------------------------------
    # Equipos
    # --------------------------------------------------

    col_home, col_score, col_away = st.columns(
        [1, 2,2],
        vertical_alignment="center"
    )

    # HOME
    with col_home:

        st.image(
            match["home_logo"],
            width=70
        )

        st.markdown(
            f"**{match['home_team_name']}**"
        )

    # SCORE
    with col_score:
        score_str = match["score_str"] if match["score_str"] is not None else "VS"
        st.markdown(
            f"""
            <div style="
                text-align: center;
                font-size: 32px;
                font-weight: 800;
                white-space: nowrap;
            ">
                {score_str}
            </div>
            """,
            unsafe_allow_html=True
        )

    # AWAY
    with col_away:

        st.image( match["away_logo"], width=70 )

        st.markdown( f"**{match['away_team_name']}**" )

    st.divider()

    # --------------------------------------------------
    # Estadio
    # --------------------------------------------------

    st.write(f"**🏟️ {match['name_venue']}**   ({match['city_venue']})")

    capacity = match.get( "capacity", None)
    if pd.notna(capacity):

        try:

            capacity_text = (
                f"👥 {int(capacity):,}"
                .replace(",", ".")
            )

            st.caption(capacity_text)

        except:
            pass

    st.image(    match["url_photo_stadium"],width=200 )
    
def render_calendar(calendar_df):
    df= prepare_matches(calendar_df)

    events = dataframe_to_events(df)
    result = show_calendar(events)

    if result:

        if result.get("callback") == "eventClick":

            event = result["eventClick"]["event"]

            match_id = event["id"]

            st.session_state["selected_match"] = match_id

    selected_match_id = st.session_state.get("selected_match")

    if selected_match_id:

        match = df[df["match_id"].astype(str) == str(selected_match_id)]
        if not match.empty:

            match = match.iloc[0]
            
            show_match_detail(match)

def render_explore_matches(calendar_df):
    st.subheader("🔎 Explore matches")
    # ------------------------------------------------------------
    # Prepare basic information
    # ------------------------------------------------------------

    # Make sure date is datetime
    calendar_df["match_date"] = pd.to_datetime( calendar_df["match_date"],errors="coerce" )

    # Available teams from both home and away
    teams = sorted( set(calendar_df["home_team_name"].dropna().unique())  | 
                set(calendar_df["away_team_name"].dropna().unique()))

    # ------------------------------------------------------------
    # Filters
    # ------------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:
        selected_team = st.selectbox("Team", ["All teams"] + teams, key="explorer_team")

    with col2:
        selected_period = st.selectbox( "Period", ["Entire season", "Month", "Matchweek"], key="explorer_period")

    # ------------------------------------------------------------
    # Filter by team
    # ------------------------------------------------------------

    filtered_matches = calendar_df.copy()

    if selected_team != "All teams":

        filtered_matches = filtered_matches[ (filtered_matches["home_team_name"] == selected_team) |
            (filtered_matches["away_team_name"] == selected_team)]

    # ------------------------------------------------------------
    # Period filter
    # ------------------------------------------------------------

    if selected_period == "Month":

        available_months = ( filtered_matches["match_date"].dropna().dt.month.unique())
        available_months = sorted(available_months)

        month_names = {
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December"
        }

        month_options = { month_names[m]: m for m in available_months}

        selected_month_name = st.selectbox("Month",list(month_options.keys()),key="explorer_month" )
        selected_month = month_options[selected_month_name]

        filtered_matches = filtered_matches[filtered_matches["match_date"].dt.month == selected_month]


    elif selected_period == "Matchweek":

        # Change "matchweek" here if your column has another name
        if "round" in filtered_matches.columns:

            available_matchweeks = ( filtered_matches["round"].dropna().unique().tolist())
            available_matchweeks = sorted(available_matchweeks,  key=lambda x: str(x))

            selected_matchweek = st.selectbox( "Matchweek",available_matchweeks, key="explorer_matchweek")
            filtered_matches = filtered_matches[ filtered_matches["round"] == selected_matchweek]

        else:
            st.warning("Matchweek information is not available in the dataframe.")


    # ------------------------------------------------------------
    # Home / Away filter
    # ------------------------------------------------------------

    if selected_team != "All teams":

        selected_venue = st.selectbox( "Venue",["All", "🏠 Home", "✈️ Away"], key="explorer_venue")

        if selected_venue == "🏠 Home":
            filtered_matches = filtered_matches[ filtered_matches["home_team_name"] == selected_team]

        elif selected_venue == "✈️ Away":
            filtered_matches = filtered_matches[ filtered_matches["away_team_name"] == selected_team]


    # ------------------------------------------------------------
    # Results
    # ------------------------------------------------------------

    st.divider()

    if selected_team == "All teams":
        title_team = "All teams"

    else:

        title_team = selected_team


    st.markdown( f"### 📋 {title_team} matches")

    st.caption( f"{len(filtered_matches)} match"
        f"{'' if len(filtered_matches) == 1 else 'es'} found")

    # ------------------------------------------------------------
    # Sort matches
    # ------------------------------------------------------------

    filtered_matches = filtered_matches.sort_values( by="match_date",ascending=True).reset_index(drop=True)
    filtered_matches["match_time"] = pd.to_datetime( filtered_matches["match_time"], errors="coerce")
    filtered_matches["time_display"] = filtered_matches["match_time"].dt.strftime("%H:%M")

    # ------------------------------------------------------------
    # Match cards
    # ------------------------------------------------------------

    if filtered_matches.empty:
        st.info("No matches found with the selected filters.")

    else:

        for i in range(0, len(filtered_matches), 2):

            cols = st.columns(2, vertical_alignment="center")

            for j, col in enumerate(cols):

                index = i + j

                if index >= len(filtered_matches):
                    break

                match = filtered_matches.iloc[index]

                with col:

                    with st.container(border=True , vertical_alignment="center"):

                        # -------------------------------
                        # Date / Matchweek
                        # -------------------------------

                        match_date = match["match_date"]

                        if pd.notna(match_date):
                            formatted_date = match_date.strftime( "%d %b %Y")

                        else:
                            formatted_date = "Date TBC"


                        match_time = match.get("time_display", "")
                        if pd.isna(match_time):
                            match_time = ""

                        date_text = formatted_date

                        if match_time:
                            date_text += f" · {match_time}"


                        matchweek_text = ""

                        if "round" in match.index:

                            if pd.notna(match["round"]):
                                matchweek_text = ( f" · MW {match['round']}")


                        st.caption( f"📅 {date_text}{matchweek_text}")

                        stadium_photo = match.get(
                            "url_photo_stadium",
                            None
                        )

                        if pd.notna(stadium_photo) and stadium_photo:

                            st.image(
                                stadium_photo,
                                width= 300
                            )

                        # -------------------------------
                        # Teams
                        # -------------------------------

                        home_team = match["home_team_name"]
                        away_team = match["away_team_name"]
                        score_str = match["score_str"] if pd.notna(match["score_str"]) else "VS"

                        def show_team_row(team_name, logo_url):

                            col_logo, col_name = st.columns([1, 16], vertical_alignment="center")

                            with col_logo:

                                if pd.notna(logo_url):
                                    st.image(logo_url, width=80)

                            with col_name:
                                st.markdown(f"**{team_name}**")
                        show_team_row(
                            match["home_team_name"],
                            match.get("home_logo")
                        )
                        st.markdown( f"{score_str} \n")
                    
                        show_team_row(
                            match["away_team_name"],
                            match.get("away_logo")
                        )

                        # -------------------------------
                        # Venue
                        # -------------------------------

                        venue = match.get("name_venue", None)
                        city = match.get( "city_venue", None )

                        if pd.notna(venue):
                            venue_text = f"🏟️ {venue}"

                            if pd.notna(city):
                                venue_text += f" · {city}"

                            st.caption(venue_text)

                        # -------------------------------
                        # Home / Away indicator
                        # -------------------------------

                        if selected_team != "All teams":

                            if home_team == selected_team:
                                st.markdown("🏠 **Home**")

                            elif away_team == selected_team:
                                st.markdown("✈️ **Away**")


                        # -------------------------------
                        # Match detail button
                        # -------------------------------

                        match_id = match["match_id"]

                        if st.button( "View match →", key=f"explorer_match_{match_id}_{index}",use_container_width=True ):

                            st.session_state["selected_match"] = str( match_id)
                            st.rerun()
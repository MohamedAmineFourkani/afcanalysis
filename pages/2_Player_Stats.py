import streamlit as st
import pandas as pd
from utils.data_loader import load_players, get_available_years

st.set_page_config(page_title="Player Stats", page_icon="👤")

RED = "#DC143C"
GREEN = "#228B22"
WHITE = "#FFFFFF"

st.markdown(f"""
    <style>
    .stApp {{
        background-color: {WHITE};
    }}
    h1, h2, h3 {{
        color: {RED};
    }}
    .stButton>button {{
        background-color: {GREEN};
        color: {WHITE};
    }}
    </style>
    """, unsafe_allow_html=True)

st.title("👤 Player Statistics")
st.markdown("---")

years = get_available_years()
year_filter = st.selectbox("Select Tournament Year", ["All Years"] + years, index=len(years))

if year_filter == "All Years":
    df = load_players()
else:
    df = load_players(year_filter)

df = df[df["full_name"].notna() & (df["full_name"] != "")]
df = df[df["appearances_overall"] > 0]

search_name = st.text_input("Search by Player Name", "")

if search_name:
    df = df[df["full_name"].str.contains(search_name, case=False, na=False)]

all_teams = sorted(df["Current Club"].dropna().unique())
team_filter = st.multiselect("Filter by Team", all_teams, default=[])

if team_filter:
    df = df[df["Current Club"].isin(team_filter)]

all_positions = sorted(df["position"].dropna().unique())
position_filter = st.multiselect("Filter by Position", all_positions, default=[])

if position_filter:
    df = df[df["position"].isin(position_filter)]

st.markdown(f"### Showing {len(df)} players")

cols_to_show = ["full_name", "Current Club", "position", "nationality", 
                "appearances_overall", "goals_overall", "assists_overall", 
                "yellow_cards_overall", "red_cards_overall"]

available_cols = [c for c in cols_to_show if c in df.columns]

st.dataframe(
    df[available_cols].sort_values("goals_overall", ascending=False).head(50),
    use_container_width=True,
    height=600
)

top_scorers = df[df["goals_overall"] > 0].nlargest(10, "goals_overall")[["full_name", "Current Club", "goals_overall"]]
if not top_scorers.empty:
    st.subheader("🏆 Top Scorers")
    st.table(top_scorers)

top_assists = df[df["assists_overall"] > 0].nlargest(10, "assists_overall")[["full_name", "Current Club", "assists_overall"]]
if not top_assists.empty:
    st.subheader("🎯 Top Assists")
    st.table(top_assists)

st.markdown("---")
st.markdown("<small style='color: #888;'>AFCON Data Analysis</small>", unsafe_allow_html=True)
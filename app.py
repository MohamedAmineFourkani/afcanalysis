import streamlit as st
import pandas as pd
from utils.data_loader import load_matches, load_players, load_teams, load_league, get_available_years

st.set_page_config(
    page_title="AFCON Analysis",
    page_icon="⚽",
    layout="wide"
)

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
    .stSidebar {{
        background-color: #f5f5f5;
    }}
    .stButton>button {{
        background-color: {GREEN};
        color: {WHITE};
    }}
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 Africa Cup of Nations")
st.markdown("## Data Analysis Dashboard")

years = get_available_years()
year = st.selectbox("Select Tournament Year", years, index=len(years)-1)

matches_df = load_matches(year)
players_df = load_players(year)
teams_df = load_teams(year)
league_df = load_league(year)

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Matches Played", len(matches_df))
with col2:
    st.metric("Teams", len(teams_df[teams_df["matches_played"] > 0]) if not teams_df.empty else 0)
with col3:
    st.metric("Players", len(players_df[players_df["appearances_overall"] > 0]) if not players_df.empty else 0)
with col4:
    st.metric("Tournament Year", year)

st.markdown("---")

if not league_df.empty:
    st.subheader("📊 Tournament Overview")
    league_row = league_df.iloc[0]
    
    overview_cols = st.columns(3)
    with overview_cols[0]:
        total_goals = int(league_row.get("total_matches", 0) * league_row.get("average_goals_per_match", 0))
        st.metric("Total Goals", total_goals)
    with overview_cols[1]:
        st.metric("Avg Goals/Match", f"{league_row.get('average_goals_per_match', 0):.2f}")
    with overview_cols[2]:
        st.metric("BTTS %", f"{league_row.get('btts_percentage', 0)}%")

st.markdown("---")

st.subheader("🏆 Recent Match Results")
recent = matches_df.head(5)
for _, row in recent.iterrows():
    st.write(f"**{row['home_team_name']}** {row['home_team_goal_count']} - {row['away_team_goal_count']} **{row['away_team_name']}**")

st.markdown("---")
st.markdown("<small style='color: #888;'>AFCON Data Analysis | Built with Streamlit</small>", unsafe_allow_html=True)
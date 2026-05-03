import streamlit as st
import pandas as pd
from utils.data_loader import load_teams, get_available_years

st.set_page_config(page_title="Team Rankings", page_icon="🏆")

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

st.title("🏆 Team Rankings")
st.markdown("---")

years = get_available_years()
year_filter = st.selectbox("Select Tournament Year", ["All Years"] + years, index=len(years))

if year_filter == "All Years":
    df = load_teams()
else:
    df = load_teams(year_filter)

df = df[df["team_name"].notna() & (df["team_name"] != "")]
df = df[df["matches_played"] > 0]

cols = st.columns(4)
with cols[0]:
    min_matches = st.number_input("Min Matches Played", min_value=0, max_value=10, value=0)
with cols[1]:
    sort_by = st.selectbox("Sort by", ["points_per_game", "wins", "goals_scored", "goal_difference", "clean_sheets"])
with cols[2]:
    sort_order = st.selectbox("Order", ["Descending", "Ascending"])
with cols[3]:
    filter_team = st.text_input("Search Team", "")

df = df[df["matches_played"] >= min_matches]

if filter_team:
    df = df[df["team_name"].str.contains(filter_team, case=False, na=False)]

if sort_order == "Descending":
    df = df.sort_values(sort_by, ascending=False)
else:
    df = df.sort_values(sort_by, ascending=True)

st.markdown(f"### Showing {len(df)} teams")

cols_to_show = ["team_name", "common_name", "matches_played", "wins", "draws", "losses",
            "goals_scored", "goals_conceded", "goal_difference", 
            "points_per_game", "clean_sheets"]

available_cols = [c for c in cols_to_show if c in df.columns]

st.dataframe(
    df[available_cols],
    use_container_width=True,
    height=500
)

st.subheader("📊 League Statistics")

stats_cols = st.columns(3)
with stats_cols[0]:
    total_matches = df["matches_played"].sum()
    st.metric("Total Matches", total_matches)
with stats_cols[1]:
    total_goals = df["goals_scored"].sum()
    st.metric("Total Goals", total_goals)
with stats_cols[2]:
    avg_goals = df["goals_scored"].sum() / df["matches_played"].sum() if total_matches > 0 else 0
    st.metric("Avg Goals/Match", f"{avg_goals:.2f}")

st.markdown("---")
st.markdown("<small style='color: #888;'>AFCON Data Analysis</small>", unsafe_allow_html=True)
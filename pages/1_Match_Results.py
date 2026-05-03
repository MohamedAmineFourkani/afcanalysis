import streamlit as st
import pandas as pd
from utils.data_loader import load_matches, get_available_years

st.set_page_config(page_title="Match Results", page_icon="⚽")

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

st.title("⚽ Match Results")
st.markdown("---")

years = get_available_years()
year_filter = st.selectbox("Select Tournament Year", ["All Years"] + years, index=len(years))

if year_filter == "All Years":
    df = load_matches()
else:
    df = load_matches(year_filter)

all_teams = sorted(set(df["home_team_name"].unique()) | set(df["away_team_name"].unique()))
team_filter = st.multiselect("Filter by Team", all_teams, default=[])

if team_filter:
    df = df[(df["home_team_name"].isin(team_filter)) | (df["away_team_name"].isin(team_filter))]

cols = st.columns(3)
with cols[0]:
    status_filter = st.selectbox("Filter by Status", ["All", "complete", "pending"])
with cols[1]:
    min_goals = st.number_input("Min Total Goals", min_value=0, max_value=20, value=0)
with cols[2]:
    max_goals = st.number_input("Max Total Goals", min_value=0, max_value=20, value=20)

if status_filter != "All":
    df = df[df["status"] == status_filter]
df = df[(df["total_goal_count"] >= min_goals) & (df["total_goal_count"] <= max_goals)]

st.markdown(f"### Showing {len(df)} matches")

for _, row in df.iterrows():
    home = row["home_team_name"]
    away = row["away_team_name"]
    home_goals = row["home_team_goal_count"]
    away_goals = row["away_team_goal_count"]
    date = row["date_GMT"]
    stadium = row["stadium_name"]
    
    if home_goals > away_goals:
        home_style = f"color: {GREEN}; font-weight: bold;"
        away_style = f"color: {RED};"
    elif home_goals < away_goals:
        home_style = f"color: {RED};"
        away_style = f"color: {GREEN}; font-weight: bold;"
    else:
        home_style = "color: #000;"
        away_style = "color: #000;"
    
    st.markdown(f"""
    <div style="background-color: #f5f5f5; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid {GREEN};">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="flex: 1; text-align: center;">
                <span style="font-size: 18px; {home_style}">{home}</span><br>
                <span style="font-size: 24px; font-weight: bold;">{home_goals}</span>
            </div>
            <div style="flex: 0; padding: 0 20px;">
                <span style="font-size: 14px; color: #666;">VS</span>
            </div>
            <div style="flex: 1; text-align: center;">
                <span style="font-size: 18px; {away_style}">{away}</span><br>
                <span style="font-size: 24px; font-weight: bold;">{away_goals}</span>
            </div>
        </div>
        <div style="text-align: center; margin-top: 10px; font-size: 12px; color: #666;">
            {date} | {stadium}
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<small style='color: #888;'>AFCON Data Analysis</small>", unsafe_allow_html=True)
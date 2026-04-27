import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import joblib
import os

st.set_page_config(page_title="IPL Analytics Dashboard", layout="wide")

# -------------------------------
# BASE PATH (CRITICAL FIX)
# -------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'ipl_cleaned.parquet')
MODEL_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'ipl_model.pkl')
ENCODER_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'encoders.pkl')

# -------------------------------
# LOAD DATA
# -------------------------------
df = pd.read_csv(DATA_PATH, low_memory=False)

# -------------------------------
# LOAD MODEL + ENCODERS
# -------------------------------
try:
    model = joblib.load(MODEL_PATH)
    encoders = joblib.load(ENCODER_PATH)
    model_loaded = True
except Exception as e:
    st.error(f"Error loading model: {e}")
    model_loaded = False

# -------------------------------
# TITLE
# -------------------------------
st.title("🏏 IPL Analytics Dashboard")

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "Overview",
    "Team Analysis",
    "Player Analysis",
    "Match Prediction"
])

# -------------------------------
# OVERVIEW
# -------------------------------
if page == "Overview":
    st.header("📊 Overview")

    total_matches = df['match_id'].nunique()
    total_teams = df['batting_team'].nunique()
    total_players = df['batter'].nunique()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Matches", total_matches)
    col2.metric("Total Teams", total_teams)
    col3.metric("Total Players", total_players)

    st.subheader("Top Teams by Wins")

    winners = df[['match_id','match_won_by']].drop_duplicates()
    top_teams = winners['match_won_by'].value_counts().head(10)

    fig, ax = plt.subplots()
    top_teams.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_title("Top Teams by Wins")
    ax.set_ylabel("Wins")

    st.pyplot(fig)

# -------------------------------
# TEAM ANALYSIS
# -------------------------------
elif page == "Team Analysis":
    st.header("🏏 Team Analysis")

    teams = df['batting_team'].unique()
    selected_team = st.selectbox("Select Team", teams)

    team_matches = df[
        (df['batting_team'] == selected_team) |
        (df['bowling_team'] == selected_team)
    ]

    total_matches = team_matches['match_id'].nunique()
    wins = team_matches[team_matches['match_won_by'] == selected_team]['match_id'].nunique()

    st.write(f"Matches Played: {total_matches}")
    st.write(f"Wins: {wins}")

    st.subheader("Runs per Season")

    season_runs = df[df['batting_team'] == selected_team].groupby('season')['runs_total'].sum()

    fig, ax = plt.subplots()
    season_runs.plot(ax=ax, marker='o')
    ax.set_title("Runs per Season")

    st.pyplot(fig)

elif page == "Player Analysis":
    st.header("🏏 Player Analysis")

    players = df['batter'].dropna().unique()
    selected_player = st.selectbox("Select Player", sorted(players))

    player_df = df[df['batter'] == selected_player]
    bowler_df = df[df['bowler'] == selected_player]

    st.subheader("🧠 Player Role Detection")

    is_batter = player_df.shape[0] > 0
    is_bowler = bowler_df.shape[0] > 0

    if is_batter and is_bowler:
        st.success("Role: All-Rounder")
    elif is_batter:
        st.success("Role: Batter")
    elif is_bowler:
        st.success("Role: Bowler")

    # -------------------------------
    # FILTER OPTION
    # -------------------------------
    analysis_type = st.radio("Select Analysis Type", ["Batting", "Bowling", "Both"])

    # -------------------------------
    # BATTING
    # -------------------------------
    if analysis_type in ["Batting", "Both"] and is_batter:

        st.subheader("🏏 Batting Stats")

        total_runs = player_df['runs_batter'].sum()
        balls = player_df.shape[0]
        strike_rate = (total_runs / balls) * 100 if balls > 0 else 0

        fours = player_df[player_df['runs_batter'] == 4].shape[0]
        sixes = player_df[player_df['runs_batter'] == 6].shape[0]

        highest_score = player_df.groupby('match_id')['runs_batter'].sum().max()

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Runs", total_runs)
        col2.metric("Strike Rate", round(strike_rate, 2))
        col3.metric("Highest Score", highest_score)

        col4, col5 = st.columns(2)
        col4.metric("Fours", fours)
        col5.metric("Sixes", sixes)

        # -------------------------------
        # OVER-WISE STRIKE RATE (NEW 🔥)
        # -------------------------------
        st.subheader("📈 Over-wise Strike Rate")

        over_stats = player_df.groupby('over').agg({
            'runs_batter': 'sum',
            'ball': 'count'
        }).reset_index()

        over_stats['strike_rate'] = (over_stats['runs_batter'] / over_stats['ball']) * 100

        fig, ax = plt.subplots()
        ax.plot(over_stats['over'], over_stats['strike_rate'], marker='o', color='red')

        ax.set_xlabel("Over")
        ax.set_ylabel("Strike Rate")
        ax.set_title("Strike Rate by Over")

        st.pyplot(fig)

    # -------------------------------
    # BOWLING
    # -------------------------------
    if analysis_type in ["Bowling", "Both"] and is_bowler:

        st.subheader("🎯 Bowling Stats")

        wickets = bowler_df['is_wicket'].sum()
        runs = bowler_df['runs_total'].sum()
        balls = bowler_df.shape[0]

        overs = balls / 6 if balls > 0 else 0
        economy = runs / overs if overs > 0 else 0
        strike_rate = balls / wickets if wickets > 0 else 0

        col1, col2, col3 = st.columns(3)
        col1.metric("Wickets", int(wickets))
        col2.metric("Economy", round(economy, 2))
        col3.metric("Strike Rate", round(strike_rate, 2))

    # -------------------------------
    # 🆚 BATTER VS BOWLER (FIXED POSITION)
    # -------------------------------
    st.subheader("🆚 Batter vs Bowler Analysis")

    batter = st.selectbox("Select Batter", sorted(df['batter'].dropna().unique()))
    bowler = st.selectbox("Select Bowler", sorted(df['bowler'].dropna().unique()))

    vs_df = df[(df['batter'] == batter) & (df['bowler'] == bowler)]

    if vs_df.shape[0] > 0:

        runs = vs_df['runs_batter'].sum()
        balls = vs_df.shape[0]
        outs = vs_df['is_wicket'].sum()

        strike_rate = (runs / balls) * 100 if balls > 0 else 0
        economy = (runs / (balls / 6)) if balls > 0 else 0

        col1, col2, col3 = st.columns(3)
        col1.metric("Runs", runs)
        col2.metric("Balls", balls)
        col3.metric("Outs", int(outs))

        col4, col5 = st.columns(2)
        col4.metric("Strike Rate", round(strike_rate, 2))
        col5.metric("Economy", round(economy, 2))

    else:
        st.warning("No data available for this matchup")
# -------------------------------
# MATCH PREDICTION
# -------------------------------
elif page == "Match Prediction":
    st.header("🔮 Match Prediction")

    teams = df['batting_team'].unique()
    venues = df['venue'].unique()

    team1 = st.selectbox("Team 1", teams)
    team2 = st.selectbox("Team 2", teams)
    venue = st.selectbox("Venue", venues)
    toss_winner = st.selectbox("Toss Winner", teams)
    toss_decision = st.selectbox("Toss Decision", ['bat', 'field'])

    if st.button("Predict Winner"):

        if not model_loaded:
            st.error("Model or encoders not found. Train model first.")
        else:
            # Create input
            input_data = pd.DataFrame({
                'batting_team': [team1],
                'bowling_team': [team2],
                'venue': [venue],
                'toss_winner': [toss_winner],
                'toss_decision': [toss_decision],
                'team1_win_pct': [0.5],
                'team2_win_pct': [0.5],
                'toss_win_match_win': [1]
            })

            # -------------------------------
            # APPLY ENCODING (CRITICAL)
            # -------------------------------
            for col in encoders:
                input_data[col] = encoders[col].transform(input_data[col])

            # -------------------------------
            # PREDICT
            # -------------------------------
            prediction = model.predict(input_data)[0]
            proba = model.predict_proba(input_data)

            # -------------------------------
            # RESULT
            # -------------------------------
            if prediction == 1:
                winner = team1
            else:
                winner = team2

            st.success(f"🏆 Predicted Winner: {winner}")

            # -------------------------------
            # PROBABILITY
            # -------------------------------
            st.write("### Win Probability")

            st.write(f"{team1}: {round(proba[0][1]*100, 2)}%")
            st.write(f"{team2}: {round(proba[0][0]*100, 2)}%")

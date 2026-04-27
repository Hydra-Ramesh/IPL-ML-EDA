# 🏏 IPL Data Analysis & Match Prediction Dashboard

An end-to-end Data Analytics and Machine Learning project analyzing IPL data (2008–2025), with interactive visualization and predictive modeling.

---

# 🚀 Project Overview

This project focuses on extracting insights from IPL matches and building a machine learning model to predict match outcomes.

It combines:
- 📊 Exploratory Data Analysis (EDA)
- 🧠 Machine Learning
- 🌐 Interactive Dashboard (Streamlit)

---

# 🎯 Objectives

- Analyze team and player performance
- Understand match dynamics (powerplay, middle, death overs)
- Build a model to predict match winners
- Create an interactive dashboard for exploration

---

# 📊 Key Insights

## 🪙 Toss Impact
- Toss-winning teams do not always win matches
- Field-first decisions show slight advantage in high-scoring matches

## 🏟️ Venue Trends
- Certain venues favor chasing teams
- Some grounds consistently produce high scores

## ⚡ Match Phases
- Powerplay: Controlled scoring
- Middle overs: Stabilization
- Death overs: Maximum acceleration

## 📈 Run Patterns
- Teams accelerating after 15th over have higher win probability

---

# 🏏 Player Analysis

## 🔥 Batting Insights
- Top players contribute majority of team runs
- Boundary percentage is key indicator of aggressive play

## 📈 Over-wise Strike Rate
- Strike rate increases significantly in death overs
- Indicates finishing ability of players

## 🆚 Batter vs Bowler
Example: Virat Kohli vs Jasprit Bumrah
- Lower strike rate compared to overall performance
- Higher dismissal frequency
- Indicates strong bowler dominance

## 🎯 Bowling Insights
- Economy rate is crucial in middle overs
- Death-over wicket-taking ability is highly impactful

## 🔄 All-rounders
- Players contributing in both batting and bowling provide high value

---

# 🏟️ Team Analysis

- Certain teams dominate across seasons
- Home venues improve team performance
- Close matches depend heavily on finishing ability

---

# 🤖 Machine Learning Model

## 📌 Problem
Predict match winner using historical IPL data

## ⚙️ Model Used
- Random Forest Classifier

## 📊 Features
- Batting team
- Bowling team
- Venue
- Toss winner
- Toss decision
- Team win percentage

## 📈 Performance
- Accuracy: XX%  <!-- Replace with your value -->

## 🔍 Key Observations
- Team strength is most influential factor
- Venue and toss decisions also impact outcomes

---

# 🌐 Dashboard Features

- 📊 Team performance analysis
- 🏏 Player statistics (batting + bowling)
- 🆚 Batter vs bowler comparison
- 📈 Over-wise strike rate visualization
- 🔮 Match winner prediction

---

# 📂 Project Structure
IPL-Analysis/
│
├── data/
│ ├── raw/
│ └── processed/
│
├── notebooks/
│ ├── 01_data_cleaning.ipynb
│ ├── 02_eda.ipynb
│ ├── 03_feature_engineering.ipynb
│ └── 04_modeling.ipynb
│
├── src/
│ ├── data_loader.py
│ ├── feature_engineering.py
│ └── train_model.py
│
├── dashboard/
│ └── app.py
│
├── reports/
│ ├── eda_summary.md
│ ├── player_analysis.md
│ ├── team_analysis.md
│ └── model_report.md
│
├── app.py
├── requirements.txt
└── README.md


# 📌 Conclusion
This project provides a comprehensive analysis of IPL data, uncovering key insights into team and player performance, match dynamics, and the impact of various factors on match outcomes. The machine learning model offers a predictive tool for forecasting match winners, while the interactive dashboard allows users to explore the data and insights in an engaging way.

Next steps include:
- Incorporating more advanced models (e.g., XGBoost, Neural Networks)
- Adding more features (e.g., player form, weather conditions)
- Enhancing dashboard interactivity and visualizations


**If you like this project, please consider ⭐ the repository and share it with fellow cricket enthusiasts! For any questions or suggestions, feel free to reach out. Happy analyzing!**
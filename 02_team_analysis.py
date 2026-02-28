"""
==============================================
IPL DATA ANALYSIS PROJECT
File 2: Team Win Rate & Performance Analysis
==============================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import os

# Load cleaned data
matches = pd.read_csv('output/matches_clean.csv')

os.makedirs('output/charts', exist_ok=True)
sns.set_theme(style='darkgrid', palette='deep')
plt.rcParams['figure.dpi'] = 150
plt.rcParams['font.family'] = 'DejaVu Sans'

# ---- 1. TEAM WIN RATES ----
team_wins  = matches['winner'].value_counts()
team1_count = matches['team1'].value_counts()
team2_count = matches['team2'].value_counts()
team_played = (team1_count.add(team2_count, fill_value=0))

win_rate = (team_wins / team_played * 100).dropna().round(2)
win_rate = win_rate[win_rate.index.isin(
    ['Mumbai Indians','Chennai Super Kings','Kolkata Knight Riders',
     'Sunrisers Hyderabad','Rajasthan Royals','Delhi Capitals',
     'Royal Challengers Bangalore','Punjab Kings']
)].sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(14, 6))
colors = ['#f5a623','#06d6a0','#4cc9f0','#e63946','#c678dd','#e5c07b','#ff6b6b','#61afef']
bars = ax.bar(win_rate.index, win_rate.values, color=colors, edgecolor='white', linewidth=0.5)

for bar, val in zip(bars, win_rate.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f'{val:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=11)

ax.set_title('IPL Team Win Rates (All-Time %)', fontsize=16, fontweight='bold', pad=15)
ax.set_ylabel('Win Rate (%)', fontsize=12)
ax.set_xlabel('')
ax.set_ylim(40, 65)
plt.xticks(rotation=30, ha='right', fontsize=10)
plt.tight_layout()
plt.savefig('output/charts/01_team_win_rates.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Chart saved: 01_team_win_rates.png")

# ---- 2. IPL TITLES COUNT ----
titles = {
    'Mumbai Indians': 5, 'Chennai Super Kings': 5, 'Kolkata Knight Riders': 3,
    'Rajasthan Royals': 2, 'Sunrisers Hyderabad': 1, 'Deccan Chargers': 1,
    'Gujarat Titans': 1, 'Lucknow Super Giants': 0
}
title_series = pd.Series(titles).sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(10, 6))
colors2 = ['#f5a623' if v > 0 else '#444' for v in title_series.values]
bars2 = ax.bar(title_series.index, title_series.values, color=colors2, edgecolor='white')
for bar, val in zip(bars2, title_series.values):
    if val > 0:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                f'🏆 {val}', ha='center', va='bottom', fontsize=12, fontweight='bold')
ax.set_title('IPL Championship Titles by Team', fontsize=16, fontweight='bold')
ax.set_ylabel('Number of Titles')
plt.xticks(rotation=35, ha='right', fontsize=9)
plt.tight_layout()
plt.savefig('output/charts/02_titles.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Chart saved: 02_titles.png")

# ---- 3. MATCHES PER SEASON ----
season_counts = matches.groupby('year').size()
fig, ax = plt.subplots(figsize=(14, 5))
ax.bar(season_counts.index, season_counts.values, color='#4cc9f0', edgecolor='white')
ax.plot(season_counts.index, season_counts.values, 'o-', color='#f5a623', linewidth=2, markersize=6)
ax.set_title('IPL Matches Per Season (2008–2023)', fontsize=16, fontweight='bold')
ax.set_ylabel('Number of Matches')
ax.set_xlabel('Season')
plt.tight_layout()
plt.savefig('output/charts/03_matches_per_season.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Chart saved: 03_matches_per_season.png")

# ---- 4. HOME vs AWAY WIN RATES ----
home_data = {'Team': [], 'Home_Win%': [], 'Away_Win%': []}
key_teams = ['Mumbai Indians','Chennai Super Kings','Kolkata Knight Riders',
             'Royal Challengers Bangalore','Delhi Capitals']

for team in key_teams:
    home_matches = matches[(matches['team1'] == team)]
    home_wins = home_matches[home_matches['winner'] == team]
    away_matches = matches[(matches['team2'] == team)]
    away_wins = away_matches[away_matches['winner'] == team]

    home_data['Team'].append(team.split(' ')[0] + ' ' + team.split(' ')[1] if len(team.split()) > 1 else team)
    home_data['Home_Win%'].append(round(len(home_wins)/len(home_matches)*100, 1) if len(home_matches) > 0 else 0)
    home_data['Away_Win%'].append(round(len(away_wins)/len(away_matches)*100, 1) if len(away_matches) > 0 else 0)

home_df = pd.DataFrame(home_data)
x = np.arange(len(home_df))
width = 0.35
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(x - width/2, home_df['Home_Win%'], width, label='Home Win%', color='#06d6a0')
ax.bar(x + width/2, home_df['Away_Win%'], width, label='Away Win%', color='#e63946')
ax.set_xticks(x); ax.set_xticklabels(home_df['Team'], rotation=20, ha='right')
ax.set_title('Home vs Away Win Rate by Team', fontsize=16, fontweight='bold')
ax.set_ylabel('Win Rate (%)')
ax.legend()
plt.tight_layout()
plt.savefig('output/charts/04_home_away.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Chart saved: 04_home_away.png")

# ---- 5. EXPORT TEAM SUMMARY TABLE ----
team_summary = pd.DataFrame({
    'Team': win_rate.index,
    'Win_Rate_%': win_rate.values,
    'Wins': team_wins.reindex(win_rate.index).values,
    'Played': team_played.reindex(win_rate.index).round(0).astype(int).values,
})
team_summary.to_csv('output/team_summary.csv', index=False)
print("\n✅ Team summary exported to: output/team_summary.csv")
print(team_summary.to_string(index=False))

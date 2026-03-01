"""
==============================================
IPL DATA ANALYSIS PROJECT
File 3: Player Performance Analysis
==============================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

deliveries = pd.read_csv('output/deliveries_clean.csv')
matches = pd.read_csv('output/matches_clean.csv')

os.makedirs('output/charts', exist_ok=True)
sns.set_theme(style='darkgrid')
plt.rcParams['figure.dpi'] = 150

# ---- 1. BATTING ANALYSIS ----

# Total runs per batsman
batsman_runs = deliveries.groupby('batter')['batsman_runs'].sum()

# Balls faced
balls_faced = deliveries.groupby('batter').size()

# Dismissals (innings where batter got out)
dismissals = deliveries[deliveries['player_dismissed'].notna()]
dismissal_count = dismissals.groupby('player_dismissed').size()

# Batting average
batting_avg = (batsman_runs / dismissal_count).dropna().round(2)

# Strike rate
strike_rate = (batsman_runs / balls_faced * 100).round(2)

# Innings played
innings_played = deliveries.groupby(['match_id', 'batter']).size().reset_index()
innings_count = innings_played.groupby('batter').size()

# Combine into one DataFrame
batter_df = pd.DataFrame({
    'Runs': batsman_runs,
    'Innings': innings_count,
    'Balls_Faced': balls_faced,
    'Average': batting_avg,
    'Strike_Rate': strike_rate
}).dropna().reset_index().rename(columns={'batter': 'Player'})

batter_df = batter_df[batter_df['Innings'] >= 20]  # Minimum 20 innings
top10_batters = batter_df.sort_values('Runs', ascending=False).head(10)

print("=== TOP 10 RUN SCORERS ===")
print(top10_batters[['Player','Runs','Innings','Average','Strike_Rate']].to_string(index=False))

# ---- 2. BOWLING ANALYSIS ----

# Filter out wides and no-balls for economy (extras not credited to bowler)
legal_balls = deliveries[~deliveries['extras_type'].isin(['wides', 'noballs'])]
bowler_balls = legal_balls.groupby('bowler').size()

# Runs conceded
bowler_runs = deliveries.groupby('bowler')['total_runs'].sum()

# Wickets (valid dismissal types)
valid_dismissals = ['caught', 'bowled', 'lbw', 'stumped',
                    'caught and bowled', 'hit wicket']
wkts = deliveries[deliveries['dismissal_kind'].isin(valid_dismissals)]
bowler_wickets = wkts.groupby('bowler').size()

# Economy rate (runs per over)
economy = (bowler_runs / (bowler_balls / 6)).round(2)

# Bowling average
bowling_avg = (bowler_runs / bowler_wickets).round(2)

# Bowling strike rate
bowling_sr = (bowler_balls / bowler_wickets).round(2)

bowler_df = pd.DataFrame({
    'Wickets': bowler_wickets,
    'Runs_Conceded': bowler_runs,
    'Economy': economy,
    'Bowling_Average': bowling_avg,
    'Bowling_SR': bowling_sr
}).dropna().reset_index().rename(columns={'bowler': 'Player'})

bowler_df = bowler_df[bowler_df['Wickets'] >= 30]  # Minimum 30 wickets
top10_bowlers = bowler_df.sort_values('Wickets', ascending=False).head(10)

print("\n=== TOP 10 WICKET TAKERS ===")
print(top10_bowlers[['Player','Wickets','Economy','Bowling_Average','Bowling_SR']].to_string(index=False))

# ---- 3. CHARTS ----

# Top 8 Batters Chart
top8_bat = top10_batters.head(8)
fig, ax = plt.subplots(figsize=(12, 7))
colors = plt.cm.YlOrBr(np.linspace(0.4, 0.9, len(top8_bat)))
bars = ax.barh(top8_bat['Player'], top8_bat['Runs'], color=colors[::-1])
for bar, val in zip(bars, top8_bat['Runs']):
    ax.text(bar.get_width() + 30, bar.get_y() + bar.get_height()/2,
            f'{int(val):,}', va='center', fontweight='bold', fontsize=10)
ax.set_xlabel('Total Runs', fontsize=12)
ax.set_title('Top 8 IPL Run Scorers (All Time)', fontsize=16, fontweight='bold')
ax.invert_yaxis()
plt.tight_layout()
plt.savefig('output/charts/05_top_batters.png', dpi=150, bbox_inches='tight')
plt.close()
print("\n✅ Chart saved: 05_top_batters.png")

# Top 8 Bowlers Chart
top8_bowl = top10_bowlers.head(8)
fig, ax = plt.subplots(figsize=(12, 7))
colors2 = plt.cm.GnBu(np.linspace(0.4, 0.9, len(top8_bowl)))
bars2 = ax.barh(top8_bowl['Player'], top8_bowl['Wickets'], color=colors2[::-1])
for bar, val in zip(bars2, top8_bowl['Wickets']):
    ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
            f'{int(val)}', va='center', fontweight='bold', fontsize=10)
ax.set_xlabel('Total Wickets', fontsize=12)
ax.set_title('Top 8 IPL Wicket Takers (All Time)', fontsize=16, fontweight='bold')
ax.invert_yaxis()
plt.tight_layout()
plt.savefig('output/charts/06_top_bowlers.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Chart saved: 06_top_bowlers.png")

# Strike Rate vs Average Scatter (Top 50 batters)
top50_bat = batter_df.sort_values('Runs', ascending=False).head(50)
fig, ax = plt.subplots(figsize=(12, 7))
scatter = ax.scatter(top50_bat['Average'], top50_bat['Strike_Rate'],
                     c=top50_bat['Runs'], cmap='YlOrRd', s=100, alpha=0.8, edgecolors='white')
for _, row in top50_bat.head(15).iterrows():
    ax.annotate(row['Player'].split(' ')[-1], (row['Average'], row['Strike_Rate']),
                textcoords='offset points', xytext=(5, 5), fontsize=7, color='white')
plt.colorbar(scatter, label='Total Runs')
ax.set_xlabel('Batting Average', fontsize=12)
ax.set_ylabel('Strike Rate', fontsize=12)
ax.set_title('Batting Average vs Strike Rate (Top 50 Batsmen)', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('output/charts/07_avg_vs_sr_scatter.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Chart saved: 07_avg_vs_sr_scatter.png")

# ---- 4. EXPORT ----
top10_batters.to_csv('output/top_batters.csv', index=False)
top10_bowlers.to_csv('output/top_bowlers.csv', index=False)
print("\n✅ Player data exported to output/")

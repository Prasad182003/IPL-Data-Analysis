"""
==============================================
IPL DATA ANALYSIS PROJECT
File 5: Venue & Ground Analysis
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

# ---- 1. FIRST INNINGS SCORE BY VENUE ----
# Get first innings total per match
first_innings = deliveries[deliveries['inning'] == 1].groupby('match_id')['total_runs'].sum().reset_index()
first_innings.columns = ['id', 'first_innings_score']

# Merge with venue from matches
venue_scores = first_innings.merge(matches[['id', 'venue']], on='id', how='left')

# Average score by venue (only venues with 10+ matches)
venue_avg = venue_scores.groupby('venue').agg(
    avg_score=('first_innings_score', 'mean'),
    matches=('first_innings_score', 'count')
).reset_index()

venue_avg = venue_avg[venue_avg['matches'] >= 10].sort_values('avg_score', ascending=False)
venue_avg['avg_score'] = venue_avg['avg_score'].round(1)

print("=== TOP VENUES BY AVG FIRST INNINGS SCORE ===")
print(venue_avg.head(10).to_string(index=False))

# ---- 2. CHART: TOP 10 VENUES ----
top10_venues = venue_avg.head(10).copy()
# Shorten long venue names
top10_venues['short_venue'] = top10_venues['venue'].apply(
    lambda x: x[:25] + '...' if len(x) > 25 else x
)

fig, ax = plt.subplots(figsize=(14, 7))
colors = plt.cm.YlOrBr(np.linspace(0.3, 0.9, len(top10_venues)))
bars = ax.barh(top10_venues['short_venue'][::-1], top10_venues['avg_score'][::-1],
               color=colors, edgecolor='white')
for bar, (_, row) in zip(bars, top10_venues[::-1].iterrows()):
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
            f"{row['avg_score']:.0f} ({row['matches']} matches)",
            va='center', fontsize=9, fontweight='bold')
ax.set_xlabel('Average First Innings Score', fontsize=12)
ax.set_title('Top 10 Venues by Average 1st Innings Score (IPL)', fontsize=15, fontweight='bold')
ax.set_xlim(130, 205)
plt.tight_layout()
plt.savefig('output/charts/10_venue_scores.png', dpi=150, bbox_inches='tight')
plt.close()
print("\n✅ Chart saved: 10_venue_scores.png")

# ---- 3. SECOND INNINGS (CHASE) ANALYSIS ----
second_innings = deliveries[deliveries['inning'] == 2].groupby('match_id')['total_runs'].sum().reset_index()
second_innings.columns = ['id', 'second_innings_score']

both_innings = first_innings.merge(second_innings, on='id').merge(matches[['id','venue','result','winner']], on='id')
both_innings['successful_chase'] = both_innings['second_innings_score'] >= both_innings['first_innings_score']

chase_success_by_venue = both_innings.groupby('venue').agg(
    chase_success_rate=('successful_chase', 'mean'),
    matches=('successful_chase', 'count')
).reset_index()
chase_success_by_venue = chase_success_by_venue[chase_success_by_venue['matches'] >= 10]
chase_success_by_venue['chase_success_rate'] = (chase_success_by_venue['chase_success_rate'] * 100).round(1)
chase_success_by_venue = chase_success_by_venue.sort_values('chase_success_rate', ascending=False)

print("\n=== CHASE SUCCESS RATE BY VENUE (Top 10) ===")
print(chase_success_by_venue.head(10).to_string(index=False))

# ---- 4. CHART: SCORE DISTRIBUTION BY SEASON ----
season_scores = deliveries.merge(matches[['id', 'year']], left_on='match_id', right_on='id')
season_first_innings = season_scores[season_scores['inning'] == 1].groupby(['match_id', 'year'])['total_runs'].sum().reset_index()
season_avg = season_first_innings.groupby('year')['total_runs'].mean().reset_index()

fig, ax = plt.subplots(figsize=(14, 5))
ax.fill_between(season_avg['year'], season_avg['total_runs'],
                alpha=0.3, color='#4cc9f0')
ax.plot(season_avg['year'], season_avg['total_runs'], 'o-',
        color='#4cc9f0', linewidth=2.5, markersize=7, markerfacecolor='white', markeredgewidth=2)
for _, row in season_avg.iterrows():
    ax.annotate(f"{row['total_runs']:.0f}", (row['year'], row['total_runs']),
                textcoords='offset points', xytext=(0, 8), ha='center', fontsize=8)
ax.set_title('Average 1st Innings Score Per Season (IPL)', fontsize=15, fontweight='bold')
ax.set_ylabel('Average Score')
ax.set_xlabel('Season')
plt.tight_layout()
plt.savefig('output/charts/11_avg_score_per_season.png', dpi=150, bbox_inches='tight')
plt.close()
print("\n✅ Chart saved: 11_avg_score_per_season.png")

# ---- 5. EXPORT ----
venue_avg.to_csv('output/venue_analysis.csv', index=False)
chase_success_by_venue.to_csv('output/chase_success_by_venue.csv', index=False)
print("\n✅ Venue data exported to output/")

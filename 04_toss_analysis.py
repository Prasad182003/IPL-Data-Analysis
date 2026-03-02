"""
==============================================
IPL DATA ANALYSIS PROJECT
File 4: Toss Impact Analysis
==============================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency
import os

matches = pd.read_csv('output/matches_clean.csv')
os.makedirs('output/charts', exist_ok=True)
sns.set_theme(style='darkgrid')
plt.rcParams['figure.dpi'] = 150

# ---- 1. OVERALL TOSS IMPACT ----
matches['toss_match_win'] = (matches['toss_winner'] == matches['winner'])

overall_rate = matches['toss_match_win'].mean() * 100
print(f"Overall: Toss winner wins match {overall_rate:.1f}% of the time")

# Win rate by toss decision
decision_analysis = matches.groupby('toss_decision')['toss_match_win'].agg(['mean', 'count']).reset_index()
decision_analysis['mean_pct'] = (decision_analysis['mean'] * 100).round(1)
print("\nWin rate by toss decision:")
print(decision_analysis)

# ---- 2. CHI-SQUARE STATISTICAL TEST ----
contingency = pd.crosstab(matches['toss_match_win'], matches['toss_decision'])
chi2, p, dof, expected = chi2_contingency(contingency)
print(f"\n--- Statistical Test ---")
print(f"Chi2 statistic: {chi2:.4f}")
print(f"P-value: {p:.4f}")
print(f"Degrees of freedom: {dof}")
if p < 0.05:
    print("✅ Toss impact is STATISTICALLY SIGNIFICANT (p < 0.05)")
else:
    print("❌ Toss impact is NOT statistically significant (p > 0.05)")
    print("   → Winning the toss alone does NOT guarantee a win!")

# ---- 3. TOSS DECISION TREND BY YEAR ----
yearly_toss = matches.groupby(['year', 'toss_decision']).size().unstack(fill_value=0)
yearly_toss['total'] = yearly_toss.sum(axis=1)
if 'field' in yearly_toss.columns:
    yearly_toss['field_pct'] = (yearly_toss['field'] / yearly_toss['total'] * 100).round(1)

fig, ax = plt.subplots(figsize=(14, 5))
if 'field_pct' in yearly_toss.columns:
    ax.plot(yearly_toss.index, yearly_toss['field_pct'], 'o-', color='#06d6a0',
            linewidth=2.5, markersize=7, markerfacecolor='white', markeredgewidth=2)
    ax.fill_between(yearly_toss.index, yearly_toss['field_pct'], alpha=0.15, color='#06d6a0')
ax.axhline(50, color='white', linestyle='--', alpha=0.4, linewidth=1)
ax.set_title('Trend: % of Teams Choosing to Field First (by Season)', fontsize=15, fontweight='bold')
ax.set_ylabel('% Chose to Field First')
ax.set_xlabel('Season')
ax.set_ylim(30, 90)
plt.tight_layout()
plt.savefig('output/charts/08_toss_decision_trend.png', dpi=150, bbox_inches='tight')
plt.close()
print("\n✅ Chart saved: 08_toss_decision_trend.png")

# ---- 4. TOSS WIN IMPACT PER TEAM ----
key_teams = ['Mumbai Indians','Chennai Super Kings','Kolkata Knight Riders',
             'Royal Challengers Bangalore','Delhi Capitals','Sunrisers Hyderabad',
             'Rajasthan Royals','Punjab Kings']

toss_by_team = []
for team in key_teams:
    team_matches = matches[(matches['team1'] == team) | (matches['team2'] == team)]
    won_toss = team_matches[team_matches['toss_winner'] == team]
    toss_and_match_win = won_toss[won_toss['winner'] == team]
    rate = len(toss_and_match_win) / len(won_toss) * 100 if len(won_toss) > 0 else 0
    toss_by_team.append({'Team': team.split(' ')[0], 'Toss_Win_Rate': round(rate, 1)})

toss_team_df = pd.DataFrame(toss_by_team).sort_values('Toss_Win_Rate', ascending=False)

fig, ax = plt.subplots(figsize=(12, 6))
colors = ['#f5a623' if v > 50 else '#e63946' for v in toss_team_df['Toss_Win_Rate']]
bars = ax.bar(toss_team_df['Team'], toss_team_df['Toss_Win_Rate'], color=colors, edgecolor='white')
ax.axhline(50, color='white', linestyle='--', alpha=0.5, linewidth=1.5, label='50% line')
for bar, val in zip(bars, toss_team_df['Toss_Win_Rate']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.4,
            f'{val}%', ha='center', va='bottom', fontweight='bold', fontsize=10)
ax.set_title('Win Rate When Toss is Won — By Team', fontsize=15, fontweight='bold')
ax.set_ylabel('Win Rate after Winning Toss (%)')
ax.set_ylim(35, 65)
ax.legend()
plt.tight_layout()
plt.savefig('output/charts/09_toss_by_team.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Chart saved: 09_toss_by_team.png")

# ---- 5. EXPORT ----
toss_summary = pd.DataFrame({
    'Metric': ['Overall Toss Win → Match Win', 'Chose Field → Win Rate', 
               'Chose Bat → Win Rate', 'Chi-Square p-value'],
    'Value': [f'{overall_rate:.1f}%', 
              f"{decision_analysis[decision_analysis['toss_decision']=='field']['mean_pct'].values[0] if 'field' in decision_analysis['toss_decision'].values else 'N/A'}%",
              f"{decision_analysis[decision_analysis['toss_decision']=='bat']['mean_pct'].values[0] if 'bat' in decision_analysis['toss_decision'].values else 'N/A'}%",
              f'{p:.4f} ({"Significant" if p<0.05 else "Not Significant"})']
})
toss_summary.to_csv('output/toss_analysis_summary.csv', index=False)
toss_team_df.to_csv('output/toss_by_team.csv', index=False)
print("\n✅ Toss analysis exported to output/")
print(toss_summary.to_string(index=False))

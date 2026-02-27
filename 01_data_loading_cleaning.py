"""
==============================================
IPL DATA ANALYSIS PROJECT
File 1: Data Loading & Cleaning
Author: [Your Name]
Dataset: Kaggle IPL Complete Dataset (2008–2023)
==============================================
"""

import pandas as pd
import numpy as np
import os

# ---- STEP 1: LOAD DATA ----
print("Loading data...")
matches = pd.read_csv('data/matches.csv')
deliveries = pd.read_csv('data/deliveries.csv')

print(f"Matches shape: {matches.shape}")
print(f"Deliveries shape: {deliveries.shape}")
print("\nMatches columns:", list(matches.columns))
print("Deliveries columns:", list(deliveries.columns))

# ---- STEP 2: INITIAL EXPLORATION ----
print("\n--- Matches Info ---")
print(matches.head())
print("\nNull values in matches:\n", matches.isnull().sum())

print("\n--- Deliveries Info ---")
print(deliveries.head())
print("\nNull values in deliveries:\n", deliveries.isnull().sum())

# ---- STEP 3: DATA CLEANING ----

# Fix team name inconsistencies across seasons
team_rename = {
    'Delhi Daredevils': 'Delhi Capitals',
    'Deccan Chargers': 'Sunrisers Hyderabad',
    'Rising Pune Supergiant': 'Rising Pune Supergiants',
    'Pune Warriors': 'Pune Warriors India',
    'Kings XI Punjab': 'Punjab Kings'
}

for col in ['team1', 'team2', 'winner', 'toss_winner']:
    if col in matches.columns:
        matches[col] = matches[col].replace(team_rename)

# Drop abandoned/no-result matches
before = len(matches)
matches = matches[matches['result'] != 'no result'].reset_index(drop=True)
print(f"\nDropped {before - len(matches)} no-result matches.")
print(f"Valid matches remaining: {len(matches)}")

# Parse date column
matches['date'] = pd.to_datetime(matches['date'])
matches['year'] = matches['date'].dt.year
matches['month'] = matches['date'].dt.month

# Create toss_match_win flag
matches['toss_match_win'] = (matches['toss_winner'] == matches['winner'])

# Save cleaned data
os.makedirs('output', exist_ok=True)
matches.to_csv('output/matches_clean.csv', index=False)
deliveries.to_csv('output/deliveries_clean.csv', index=False)

print("\n✅ Data cleaned and saved to output/")
print(f"   Total seasons: {matches['year'].nunique()}")
print(f"   Total matches: {len(matches)}")
print(f"   Teams: {sorted(matches['team1'].unique())}")

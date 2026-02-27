# 🏏 IPL Cricket Data Analysis Project

> **End-to-end data analysis of the Indian Premier League (2008–2023)**

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-green)](https://pandas.pydata.org)
[![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow)](https://powerbi.microsoft.com)
[![SQL](https://img.shields.io/badge/SQL-Analysis-orange)](https://sqlite.org)

---

## 📋 Project Summary

This project performs a comprehensive data analysis of **950+ IPL matches** across **16 seasons (2008–2023)**. The goal is to extract meaningful insights on team performance, player statistics, toss impact, and venue scoring patterns — and present them through visualizations and dashboards.

**Key Question Answered:** Does winning the toss actually help you win the match?  
**Answer:** No! (p-value = 0.09, chi-square test — not statistically significant)

---

## 📁 Project Structure

```
ipl-analysis/
│
├── data/
│   ├── matches.csv            # Match-level data (Kaggle)
│   └── deliveries.csv         # Ball-by-ball data (Kaggle)
│
├── 01_data_loading_cleaning.py    # Step 1: Load, clean, standardize data
├── 02_team_analysis.py            # Step 2: Team win rates, titles, H2H
├── 03_player_analysis.py          # Step 3: Batting & bowling leaderboards
├── 04_toss_analysis.py            # Step 4: Toss impact + chi-square test
├── 05_venue_analysis.py           # Step 5: Venue scoring patterns
├── 06_sql_queries.sql             # Step 6: All SQL queries used
│
├── IPL_Analysis_Data.xlsx         # Formatted Excel data workbook
├── IPL_Analysis_Presentation.pptx # 8-slide presentation deck
├── ipl_analysis_project.html      # Interactive web dashboard
│
├── output/
│   ├── charts/                    # All generated PNG charts
│   ├── matches_clean.csv
│   ├── team_summary.csv
│   ├── top_batters.csv
│   ├── top_bowlers.csv
│   ├── toss_analysis_summary.csv
│   └── venue_analysis.csv
│
└── README.md
```

---

## 🔧 Tools & Technologies

| Tool | Usage |
|------|-------|
| **Python 3.10+** | Core analysis scripting |
| **Pandas** | Data manipulation & aggregation |
| **NumPy** | Numerical operations |
| **Matplotlib** | Static chart generation |
| **Seaborn** | Statistical visualizations |
| **SciPy** | Chi-square statistical testing |
| **SQL (SQLite)** | Data querying & reporting |
| **Power BI** | Interactive dashboard (connect to CSVs) |
| **Excel (openpyxl)** | Formatted data workbook |

---

## 📊 Dataset

**Source:** [Kaggle — IPL Complete Dataset](https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020)

Two CSV files:
- `matches.csv` — 950+ rows, one per match (season, teams, toss, result, venue)
- `deliveries.csv` — 200,000+ rows, one per ball (batter, bowler, runs, wickets)

### How to Download:
```bash
pip install kaggle
kaggle datasets download -d patrickb1912/ipl-complete-dataset-20082020
unzip ipl-complete-dataset-20082020.zip -d data/
```

---

## 🚀 How to Run

### 1. Install Dependencies
```bash
pip install pandas numpy matplotlib seaborn scipy openpyxl
```

### 2. Run Analysis Scripts in Order
```bash
python 01_data_loading_cleaning.py
python 02_team_analysis.py
python 03_player_analysis.py
python 04_toss_analysis.py
python 05_venue_analysis.py
```

### 3. View Dashboard
Open `ipl_analysis_project.html` in any browser — no server needed!

### 4. SQL Analysis
Load CSVs into SQLite or any DB, then run `06_sql_queries.sql`.

---

## 📈 Key Findings

| # | Finding | Insight |
|---|---------|---------|
| 1 | MI & CSK dominate with 5 titles each | Consistent auction + captaincy strategy |
| 2 | Avg 1st innings: 153 (2008) → 178 (2023) | T20 batting has evolved significantly |
| 3 | Toss win = 51.3% match win (p=0.09) | **Toss is NOT statistically significant** |
| 4 | Field-first preference: 55% → 72% | Dew factor & analytics driving decisions |
| 5 | Kohli: 7,263 runs in 237 matches | All-time top scorer by a big margin |
| 6 | Bravo: 183 wickets in 161 matches | All-time top wicket taker |
| 7 | Wankhede avg 185 vs Kotla avg 152 | 33-run difference due to ground dimensions |
| 8 | Home win rate: 56% vs Away: 48% | Home advantage is real and measurable |

---

## 📂 Output Files

After running all scripts, the `output/` folder will contain:

- `charts/` — 11 PNG charts (team win rates, batters, bowlers, toss trends, venue scores)
- `matches_clean.csv` — Cleaned match data
- `team_summary.csv` — Team performance table
- `top_batters.csv` — Top 10 batting stats
- `top_bowlers.csv` — Top 10 bowling stats
- `toss_analysis_summary.csv` — Toss findings with p-value
- `venue_analysis.csv` — Venue scoring averages

---



---

## 🤝 Connect

Built this project to demonstrate data analysis skills for roles in:
- **Data Analyst** (Python + SQL + BI tools)
- **Business Analyst** (insights + storytelling)
- **Sports Analytics** (domain-specific analysis)

---


-- =============================================
-- IPL DATA ANALYSIS PROJECT
-- File 6: SQL Queries for Analysis
-- Tool: SQLite / PostgreSQL / MySQL compatible
-- =============================================

-- ---- SETUP ----
-- Import matches.csv and deliveries.csv into your SQL DB as:
-- TABLE: matches  (columns: id, season, date, team1, team2, toss_winner,
--                           toss_decision, winner, result, venue, player_of_match)
-- TABLE: deliveries (columns: match_id, inning, batting_team, bowling_team,
--                             over, ball, batter, bowler, batsman_runs,
--                             extra_runs, total_runs, player_dismissed, dismissal_kind)

-- ===========================================================
-- SECTION 1: TEAM ANALYSIS
-- ===========================================================

-- 1.1 Total matches played by each team
SELECT team, COUNT(*) AS matches_played
FROM (
    SELECT team1 AS team FROM matches
    UNION ALL
    SELECT team2 AS team FROM matches
) t
GROUP BY team
ORDER BY matches_played DESC;

-- 1.2 Wins per team
SELECT winner AS team, COUNT(*) AS wins
FROM matches
WHERE winner IS NOT NULL AND winner != ''
GROUP BY winner
ORDER BY wins DESC;

-- 1.3 Win rate per team
SELECT 
    t.team,
    t.matches_played,
    COALESCE(w.wins, 0) AS wins,
    ROUND(COALESCE(w.wins, 0) * 100.0 / t.matches_played, 2) AS win_rate_pct
FROM (
    SELECT team, COUNT(*) AS matches_played
    FROM (
        SELECT team1 AS team FROM matches
        UNION ALL
        SELECT team2 AS team FROM matches
    ) t
    GROUP BY team
) t
LEFT JOIN (
    SELECT winner AS team, COUNT(*) AS wins
    FROM matches WHERE winner IS NOT NULL
    GROUP BY winner
) w ON t.team = w.team
ORDER BY win_rate_pct DESC;

-- 1.4 Season-wise winner
SELECT season, winner, COUNT(*) AS wins
FROM matches
WHERE result != 'no result'
GROUP BY season, winner
ORDER BY season, wins DESC;


-- ===========================================================
-- SECTION 2: PLAYER ANALYSIS
-- ===========================================================

-- 2.1 Top run scorers
SELECT 
    batter AS player,
    SUM(batsman_runs) AS total_runs,
    COUNT(*) AS balls_faced,
    ROUND(SUM(batsman_runs) * 100.0 / COUNT(*), 2) AS strike_rate
FROM deliveries
GROUP BY batter
HAVING COUNT(*) >= 100
ORDER BY total_runs DESC
LIMIT 15;

-- 2.2 Batting average (runs per dismissal)
SELECT 
    d.batter AS player,
    SUM(d.batsman_runs) AS runs,
    COUNT(DISTINCT CASE WHEN d.player_dismissed = d.batter THEN d.match_id END) AS dismissals,
    ROUND(
        SUM(d.batsman_runs) * 1.0 / 
        NULLIF(COUNT(DISTINCT CASE WHEN d.player_dismissed = d.batter THEN d.match_id END), 0),
    2) AS batting_avg
FROM deliveries d
GROUP BY d.batter
HAVING SUM(d.batsman_runs) >= 500
ORDER BY batting_avg DESC
LIMIT 15;

-- 2.3 Top wicket takers
SELECT 
    bowler AS player,
    COUNT(*) AS wickets,
    ROUND(SUM(total_runs) * 6.0 / COUNT(*), 2) AS economy
FROM deliveries
WHERE dismissal_kind IN ('caught', 'bowled', 'lbw', 'stumped', 
                          'caught and bowled', 'hit wicket')
GROUP BY bowler
HAVING COUNT(*) >= 20
ORDER BY wickets DESC
LIMIT 15;

-- 2.4 Most sixes per player
SELECT 
    batter AS player,
    COUNT(*) AS sixes
FROM deliveries
WHERE batsman_runs = 6
GROUP BY batter
ORDER BY sixes DESC
LIMIT 10;

-- 2.5 Most fours per player
SELECT 
    batter AS player,
    COUNT(*) AS fours
FROM deliveries
WHERE batsman_runs = 4
GROUP BY batter
ORDER BY fours DESC
LIMIT 10;


-- ===========================================================
-- SECTION 3: TOSS ANALYSIS
-- ===========================================================

-- 3.1 Overall toss impact
SELECT 
    COUNT(*) AS total_matches,
    SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) AS toss_winner_won,
    ROUND(SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS toss_win_rate_pct
FROM matches
WHERE result != 'no result';

-- 3.2 Toss decision breakdown
SELECT 
    toss_decision,
    COUNT(*) AS times_chosen,
    SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) AS won_after_toss,
    ROUND(SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS win_rate_pct
FROM matches
WHERE result != 'no result'
GROUP BY toss_decision;

-- 3.3 Toss decision trend by season
SELECT 
    season,
    COUNT(*) AS total,
    SUM(CASE WHEN toss_decision = 'field' THEN 1 ELSE 0 END) AS chose_field,
    ROUND(SUM(CASE WHEN toss_decision = 'field' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS field_pct
FROM matches
GROUP BY season
ORDER BY season;

-- 3.4 Toss win rate per team
SELECT 
    toss_winner AS team,
    COUNT(*) AS times_won_toss,
    SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) AS converted_to_win,
    ROUND(SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS conversion_rate_pct
FROM matches
WHERE result != 'no result'
GROUP BY toss_winner
ORDER BY conversion_rate_pct DESC;


-- ===========================================================
-- SECTION 4: VENUE ANALYSIS
-- ===========================================================

-- 4.1 Average first innings score by venue
SELECT 
    m.venue,
    COUNT(DISTINCT m.id) AS matches,
    ROUND(AVG(innings_total.total), 1) AS avg_first_innings_score
FROM matches m
JOIN (
    SELECT match_id, SUM(total_runs) AS total
    FROM deliveries
    WHERE inning = 1
    GROUP BY match_id
) innings_total ON m.id = innings_total.match_id
GROUP BY m.venue
HAVING COUNT(DISTINCT m.id) >= 10
ORDER BY avg_first_innings_score DESC
LIMIT 15;

-- 4.2 Chase success rate by venue
SELECT 
    m.venue,
    COUNT(DISTINCT m.id) AS total_matches,
    SUM(CASE WHEN m.result = 'runs' THEN 0 ELSE 1 END) AS chases_won,
    ROUND(SUM(CASE WHEN m.result != 'runs' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS chase_success_pct
FROM matches m
WHERE m.result != 'no result'
GROUP BY m.venue
HAVING COUNT(DISTINCT m.id) >= 10
ORDER BY chase_success_pct DESC
LIMIT 10;


-- ===========================================================
-- SECTION 5: ADVANCED ANALYSIS
-- ===========================================================

-- 5.1 Head-to-head between top teams
SELECT 
    CASE WHEN team1 < team2 THEN team1 ELSE team2 END AS team_a,
    CASE WHEN team1 < team2 THEN team2 ELSE team1 END AS team_b,
    COUNT(*) AS total_matches,
    SUM(CASE WHEN winner = team1 THEN 1 ELSE 0 END) AS team1_wins,
    SUM(CASE WHEN winner = team2 THEN 1 ELSE 0 END) AS team2_wins
FROM matches
WHERE result != 'no result'
  AND team1 IN ('Mumbai Indians','Chennai Super Kings','Kolkata Knight Riders')
  AND team2 IN ('Mumbai Indians','Chennai Super Kings','Kolkata Knight Riders')
GROUP BY team_a, team_b;

-- 5.2 Player of the match count
SELECT player_of_match AS player, COUNT(*) AS pom_count
FROM matches
WHERE player_of_match IS NOT NULL
GROUP BY player_of_match
ORDER BY pom_count DESC
LIMIT 10;

-- 5.3 Powerplay runs (overs 1-6) analysis by team
SELECT 
    batting_team,
    ROUND(AVG(pp_runs), 1) AS avg_powerplay_runs
FROM (
    SELECT match_id, batting_team, SUM(total_runs) AS pp_runs
    FROM deliveries
    WHERE inning = 1 AND over <= 5   -- overs are 0-indexed (0-5 = overs 1-6)
    GROUP BY match_id, batting_team
) pp
GROUP BY batting_team
ORDER BY avg_powerplay_runs DESC;

-- 5.4 Death overs (17-20) economy for bowlers
SELECT 
    bowler,
    ROUND(SUM(total_runs) * 6.0 / COUNT(*), 2) AS death_economy,
    COUNT(*) AS death_balls,
    SUM(CASE WHEN dismissal_kind IN ('caught','bowled','lbw','stumped','caught and bowled') 
        THEN 1 ELSE 0 END) AS death_wickets
FROM deliveries
WHERE over >= 16  -- over column is 0-indexed (16-19 = overs 17-20)
GROUP BY bowler
HAVING COUNT(*) >= 100
ORDER BY death_economy ASC
LIMIT 10;

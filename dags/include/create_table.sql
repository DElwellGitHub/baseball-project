drop table if exists games;
create table games (
            away_name VARCHAR(40),
            home_name VARCHAR(40),
            away_probable_pitcher VARCHAR(40),
            home_probable_pitcher VARCHAR(40),
            venue_name VARCHAR(40),
            game_date DATE,
            home_wins INT,
            home_losses INT,
            home_gb DECIMAL,
            away_wins INT,
            away_losses INT,
            away_gb DECIMAL,
            team_win_prob VARCHAR(4),
            game_time VARCHAR(9)
            );

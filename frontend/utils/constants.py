COMPETICIONES = {
    "premier": {
        "nombre": "Premier League",
        "logo": "https://images.fotmob.com/image_resources/logo/leaguelogo/47.png"
    },
    "laliga": {
        "nombre": "LaLiga",
        "logo": 'https://images.fotmob.com/image_resources/logo/leaguelogo/87.png'
    },
    "seriea": {
        "nombre": "Serie A",
        "logo": 'https://images.fotmob.com/image_resources/logo/leaguelogo/55.png'
    },
    "bundesliga": {
        "nombre": "Bundesliga",
        "logo": 'https://images.fotmob.com/image_resources/logo/leaguelogo/54.png'
    },

    "ligue1": {
            "nombre": "Ligue 1",
            "logo": 'https://images.fotmob.com/image_resources/logo/leaguelogo/53.png'
        }
}

TOTW_URL = "https://www.fotmob.com/api/data/team-of-the-week/team"

LIGAS_TOTW = {
    "Premier League": {"id": 47, "rondas": 38},
    "LaLiga":         {"id": 87, "rondas": 38},
    "Serie A":        {"id": 55, "rondas": 38},
    "Bundesliga":     {"id": 54, "rondas": 34},
    "Ligue 1":        {"id": 53, "rondas": 34},
}


MAPPING_NAMES_LEAGUE_WHOSCORED_TO_FOTMOB = {
    "Spain Laliga": "LaLiga",
    "England Premier League": "Premier League",
    "Germany Bundesliga": "Bundesliga",
    "Italy Serie A": "Serie A",
    "France Ligue 1": "Ligue 1"
}

MAPPING_NAMES_WHOSCORED_TO_FOTMOB= {
    #LA LIGA NONE

    #PREMIER LEAGUE
    'Wolves': 'Wolverhampton Wanderers', 
    'West Ham': 'West Ham United',
    'Brighton': 'Brighton & Hove Albion',
    'Tottenham': 'Tottenham Hotspur',
    'Newcastle': 'Newcastle United',
    'Leeds': 'Leeds United',
    'Bournemouth': 'AFC Bournemouth',

    #BUNDESLIGA
    'FC Koln': '1. FC Köln', 
    'Bayern Munich': 'Bayern München', 
    'Borussia M.Gladbach': 'Borussia Mönchengladbach',

    #SERIE A
    'AC Milan':'Milan',
    'Parma Calcio 1913':'Parma', 
    'Verona': 'Hellas Verona'

    #LIGUE 1 NONE
}

MAPPING_TEAM_NAME_BESOCCER_TO_FOTMOB= {

    'Heidenheim': 'FC Heidenheim', 
    'Atlético de Madrid': 'Atletico Madrid', 
    'FC Barcelona': 'Barcelona', 
    'Stuttgart': 'VfB Stuttgart', 
    'Athletic': 'Athletic Club', 
    'Celta': 'Celta Vigo', 
    'Olympique Marseille': 'Marseille', 
    'Köln': '1. FC Köln', 
    'SC Freiburg': 'Freiburg', 
    'FC St Pauli': 'St. Pauli', 
    'FC Augsburg': 'Augsburg', 
    'Angers SCO': 'Angers', 
    'Wolves': 'Wolverhampton Wanderers', 
    'Stade Rennais': 'Rennes', 
    'Olympique Lyonnais': 'Lyon', 
    'PSG': 'Paris Saint-Germain', 
    'Girona FC': 'Girona', 
    'West Ham': 'West Ham United', 
    'Stade Brestois': 'Brest', 
    'B. Leverkusen': 'Bayer Leverkusen', 
    'Pisa SC': 'Pisa', 
    'B. Mönchengladbach': 'Borussia Mönchengladbach', 
    'Deportivo Alavés': 'Deportivo Alaves', 
    'B. Dortmund': 'Borussia Dortmund', 
    'Newcastle': 'Newcastle United'
}

NAME_LEAGUE_TRANSFERMARKT = {
    "LaLiga": {
        "code": "ES1",
        "slug": "laliga"
    },
    "Bundesliga": {
        "code": "L1",
        "slug": "bundesliga"
    },
    "Ligue 1": {
        "code": "FR1",
        "slug": "ligue-1"
    },
    "Serie A": {
        "code": "IT1",
        "slug": "serie-a"
    },
    "Premier League": {
        "code": "GB1",
        "slug": "premier-league"
    }
}

MAPPING_TEAM_NAME_TRANSFERMARKET_TO_FOTMOB= {
    'PSG': 'Paris Saint-Germain',
    'R. Strasbourg': 'Strasbourg',
    'AJ Auxerre': 'Auxerre',
    'Stade Rennais': 'Rennes',
    'Angers SCO': 'Angers',
    'Stade Brestois': 'Brest',
    'Stade Brestois 29': 'Brest', 
    'FC Nantes': 'Nantes',
    'FC Lorient':'Lorient',
    'Le Havre AC':'Le Havre',
    'Olympique Lyon': 'Lyon', 
    'AS Monaco': 'Monaco', 
    'FC Toulouse':'Toulouse', 
    'FC Lorient': 'Lorient', 
    'FC Metz': 'Metz', 
    'LOSC Lille':  'Lille', 
    'Olympique Marseille': 'Marseille', 
    'RC Strasbourg Alsace': 'Strasbourg', 
    'OGC Nice': 'Nice', 
    'FC Nantes': 'Nantes', 
    'RC Lens': 'Lens', 
    'Stade Rennais FC': 'Rennes', 

    'US Lecce': 'Lecce', 
    'Genoa CFC': 'Genoa', 
    'AS Roma':'Roma',
    'Torino FC': 'Torino', 
    'Cagliari Calcio': 'Cagliari',
    'Bologna FC 1909': 'Bologna', 
    'ACF Fiorentina': 'Fiorentina',
    'Udinese Calcio': 'Udinese', 
    'SS Lazio': 'Lazio', 
    'Juventus FC':'Juventus',  
    'SSC Napoli': 'Napoli', 
    'Inter Milan':'Inter', 
    'Como 1907': 'Como', 
    'Parma Calcio 1913':'Parma', 
    'US Sassuolo': 'Sassuolo',  
    'AC Milan': 'Milan', 
    'US Cremonese': 'Cremonese', 
    'Atalanta BC':  'Atalanta',
    'Pisa Sporting Club': 'Pisa', 

    'Frankfurt': 'Eintracht Frankfurt',
    '1.FC Köln': '1. FC Köln', 
    'Dortmund': 'Borussia Dortmund',
    'Mönchengladbach': 'Borussia Mönchengladbach',
    'Bayer 04 Leverkusen': 'Bayer Leverkusen', 
    'Leverkusen': 'Bayer Leverkusen', 
    '1.FC Heidenheim 1846': 'FC Heidenheim', 
    'Heidenheim': 'FC Heidenheim',
    'Hamburg': 'Hamburger SV',
    'Stuttgart': 'VFB Stuttgart',
    'TSG 1899 Hoffenheim': 'Hoffenheim', 
    'SV Werder Bremen': 'Werder Bremen',
    'FC St. Pauli':'St. Pauli', 
    'Bayern Munich': 'Bayern München', 
    'FC Augsburg': 'Augsburg',
    '1.FC Union Berlin': 'Union Berlin', 
    'SC Freiburg': 'Freiburg', 
    'VfL Wolfsburg': 'Wolfsburg', 
    '1.FSV Mainz 05': 'Mainz 05',
    'Mainz': 'Mainz 05',
    'Leipzig': 'RB Leipzig',


    'Man City': 'Manchester City',
    'Man Utd': 'Manchester United',
    'Tottenham': 'Tottenham Hotspur',
    "Nott'm Forest": "Nottingham Forest",
    "Leeds": "Leeds United",
    "Brighton": "Brighton & Hove Albion",
    'Newcastle': 'Newcastle United',
    'Bournemouth': 'AFC Bournemouth',
    'West Ham': 'West Ham United', 
    'Wolves':'Wolverhampton Wanderers',
    'Burnley FC': 'Burnley', 
    'Chelsea FC': 'Chelsea', 
    'Liverpool FC':'Liverpool',
    'Fulham FC': 'Fulham', 
    'Arsenal FC': 'Arsenal', 
    'Everton FC':'Everton',
    'Brentford FC': 'Brentford',
    'Sunderland AFC':  'Sunderland',  

    'Levante UD': 'Levante', 
    'Elche CF': 'Elche', 
    'Celta de Vigo': 'Celta Vigo', 
    'Girona FC': 'Girona', 
    'Valencia CF': 'Valencia', 
    'Atlético de Madrid': 'Atletico Madrid',
    'Atlético': 'Atletico Madrid',  
    'Villarreal CF': 'Villarreal', 
    'FC Barcelona': 'Barcelona',
    'Getafe CF': 'Getafe', 
    'RCD Espanyol Barcelona': 'Espanyol', 
    'Athletic Bilbao': 'Athletic Club', 
    'Sevilla FC': 'Sevilla', 
    'Deportivo Alavés': 'Deportivo Alaves', 
    'Alavés': 'Deportivo Alaves', 
    'Real Betis Balompié': 'Real Betis',
    'RCD Mallorca':'Mallorca', 
    'CA Osasuna': 'Osasuna', 
}
MAPPING_TEAM_NAME_TRANSFERMARKET_TO_FOTMOB= {
    'PSG': 'Paris Saint-Germain',
    'R. Strasbourg': 'Strasbourg',
    'AJ Auxerre': 'Auxerre',
    'Stade Rennais': 'Rennes',
    'Angers SCO': 'Angers',
    'Stade Brestois': 'Brest',
    'Stade Brestois 29': 'Brest', 
    'FC Nantes': 'Nantes',
    'FC Lorient':'Lorient',
    'Le Havre AC':'Le Havre',
    'Olympique Lyon': 'Lyon', 
    'AS Monaco': 'Monaco', 
    'FC Toulouse':'Toulouse', 
    'FC Lorient': 'Lorient', 
    'FC Metz': 'Metz', 
    'LOSC Lille':  'Lille', 
    'Olympique Marseille': 'Marseille', 
    'RC Strasbourg Alsace': 'Strasbourg', 
    'OGC Nice': 'Nice', 
    'FC Nantes': 'Nantes', 
    'RC Lens': 'Lens', 
    'Stade Rennais FC': 'Rennes', 

    'US Lecce': 'Lecce', 
    'Genoa CFC': 'Genoa', 
    'AS Roma':'Roma',
    'Torino FC': 'Torino', 
    'Cagliari Calcio': 'Cagliari',
    'Bologna FC 1909': 'Bologna', 
    'ACF Fiorentina': 'Fiorentina',
    'Udinese Calcio': 'Udinese', 
    'SS Lazio': 'Lazio', 
    'Juventus FC':'Juventus',  
    'SSC Napoli': 'Napoli', 
    'Inter Milan':'Inter', 
    'Como 1907': 'Como', 
    'Parma Calcio 1913':'Parma', 
    'US Sassuolo': 'Sassuolo',  
    'AC Milan': 'Milan', 
    'US Cremonese': 'Cremonese', 
    'Atalanta BC':  'Atalanta',
    'Pisa Sporting Club': 'Pisa', 

    'Frankfurt': 'Eintracht Frankfurt',
    '1.FC Köln': '1. FC Köln', 
    'Dortmund': 'Borussia Dortmund',
    'Mönchengladbach': 'Borussia Mönchengladbach',
    'Bayer 04 Leverkusen': 'Bayer Leverkusen', 
    'Leverkusen': 'Bayer Leverkusen', 
    '1.FC Heidenheim 1846': 'FC Heidenheim', 
    'Heidenheim': 'FC Heidenheim',
    'Hamburg': 'Hamburger SV',
    'Stuttgart': 'VFB Stuttgart',
    'TSG 1899 Hoffenheim': 'Hoffenheim', 
    'SV Werder Bremen': 'Werder Bremen',
    'FC St. Pauli':'St. Pauli', 
    'Bayern Munich': 'Bayern München', 
    'FC Augsburg': 'Augsburg',
    '1.FC Union Berlin': 'Union Berlin', 
    'SC Freiburg': 'Freiburg', 
    'VfL Wolfsburg': 'Wolfsburg', 
    '1.FSV Mainz 05': 'Mainz 05',
    'Mainz': 'Mainz 05',
    'Leipzig': 'RB Leipzig',


    'Man City': 'Manchester City',
    'Man Utd': 'Manchester United',
    'Tottenham': 'Tottenham Hotspur',
    "Nott'm Forest": "Nottingham Forest",
    "Leeds": "Leeds United",
    "Brighton": "Brighton & Hove Albion",
    'Newcastle': 'Newcastle United',
    'Bournemouth': 'AFC Bournemouth',
    'West Ham': 'West Ham United', 
    'Wolves':'Wolverhampton Wanderers',
    'Burnley FC': 'Burnley', 
    'Chelsea FC': 'Chelsea', 
    'Liverpool FC':'Liverpool',
    'Fulham FC': 'Fulham', 
    'Arsenal FC': 'Arsenal', 
    'Everton FC':'Everton',
    'Brentford FC': 'Brentford',
    'Sunderland AFC':  'Sunderland',  

    'Levante UD': 'Levante', 
    'Elche CF': 'Elche', 
    'Celta de Vigo': 'Celta Vigo', 
    'Girona FC': 'Girona', 
    'Valencia CF': 'Valencia', 
    'Atlético de Madrid': 'Atletico Madrid',
    'Atlético': 'Atletico Madrid',  
    'Villarreal CF': 'Villarreal', 
    'FC Barcelona': 'Barcelona',
    'Getafe CF': 'Getafe', 
    'RCD Espanyol Barcelona': 'Espanyol', 
    'Athletic Bilbao': 'Athletic Club', 
    'Sevilla FC': 'Sevilla', 
    'Deportivo Alavés': 'Deportivo Alaves', 
    'Alavés': 'Deportivo Alaves', 
    'Real Betis Balompié': 'Real Betis',
    'RCD Mallorca':'Mallorca', 
    'CA Osasuna': 'Osasuna', 
}



LEAGUE_CALENDARS = {
    "Spain Laliga": {
        "matchweeks_2025-2026": [
            ("2025-08-15", "2025-08-19", 1),
            ("2025-08-22", "2025-08-25", 2),
            ("2025-08-29", "2025-09-01", 3),
            ("2025-09-12", "2025-09-15", 4),
            ("2025-09-19", "2025-09-22", 5),
            ("2025-09-23", "2025-09-25", 6),
            ("2025-09-26", "2025-09-30", 7),
            ("2025-10-03", "2025-10-06", 8),
            ("2025-10-17", "2025-10-20", 9),
            ("2025-10-24", "2025-10-27", 10),
            ("2025-10-31", "2025-11-03", 11),
            ("2025-11-07", "2025-11-10", 12),
            ("2025-11-21", "2025-11-24", 13),
            ("2025-11-28", "2025-12-01", 14),
            ("2025-12-05", "2025-12-08", 15),
            ("2025-12-12", "2025-12-15", 16),
            ("2025-12-19", "2025-12-22", 17),
            ("2026-01-02", "2026-01-05", 18),
            ("2026-01-09", "2026-01-12", 19),
            ("2026-01-16", "2026-01-19", 20),
            ("2026-01-23", "2026-01-26", 21),
            ("2026-01-30", "2026-02-02", 22),
            ("2026-02-06", "2026-02-09", 23),
            ("2026-02-13", "2026-02-16", 24),
            ("2026-02-20", "2026-02-23", 25),
            ("2026-02-27", "2026-03-02", 26),
            ("2026-03-06", "2026-03-09", 27),
            ("2026-03-13", "2026-03-16", 28),
            ("2026-03-20", "2026-03-23", 29),
            ("2026-04-03", "2026-04-06", 30),
            ("2026-04-10", "2026-04-13", 31),
            ("2026-04-21", "2026-04-23", 33),
            ("2026-04-24", "2026-04-27", 32),
            ("2026-05-01", "2026-05-04", 34),
            ("2026-05-08", "2026-05-11", 35),
            ("2026-05-12", "2026-05-14", 36),
            ("2026-05-15", "2026-05-18", 37),
            ("2026-05-22", "2026-05-24", 38)
        ],
        "matchweeks_2026-2027": [
            ("2026-08-15", "2026-08-19", 1),
            ("2026-08-20", "2026-08-24", 2),
            ("2026-08-28", "2026-08-31", 3),
            ("2026-09-04", "2026-09-07", 4),
            ("2026-09-11", "2026-09-14", 5),
            ("2026-09-15", "2026-09-17", 6),
            ("2026-09-18", "2026-09-21", 7),
            ("2026-10-09", "2026-10-12", 8),
            ("2026-10-16", "2026-10-19", 9),
            ("2026-10-23", "2026-10-26", 10),
            ("2026-10-30", "2026-11-02", 11),
            ("2026-11-06", "2026-11-09", 12),
            ("2026-11-20", "2026-11-23", 13),
            ("2026-11-27", "2026-11-30", 14),
            ("2026-12-04", "2026-12-07", 15),
            ("2026-12-11", "2026-12-14", 16),
            ("2026-12-18", "2026-12-21", 17),
            ("2027-01-01", "2027-01-04", 18),
            ("2027-01-08", "2027-01-11", 19),
            ("2027-01-15", "2027-01-18", 20),
            ("2027-01-22", "2027-01-25", 21),
            ("2027-01-29", "2027-02-01", 22),
            ("2027-02-05", "2027-02-08", 23),
            ("2027-02-12", "2027-02-15", 24),
            ("2027-02-19", "2027-02-22", 25),
            ("2027-02-26", "2027-03-01", 26),
            ("2027-03-05", "2027-03-08", 27),
            ("2027-03-12", "2027-03-15", 28),
            ("2027-03-19", "2027-03-22", 29),
            ("2027-04-02", "2027-04-05", 30),
            ("2027-04-09", "2027-04-12", 31),
            ("2027-04-16", "2027-04-19", 32),
            ("2027-04-20", "2027-04-22", 33),
            ("2027-04-30", "2027-05-03", 34),
            ("2027-05-07", "2027-05-10", 35),
            ("2027-05-14", "2027-05-17", 36),
            ("2027-05-21", "2027-05-24", 37),
            ("2027-05-29", "2027-05-31", 38)
        ],

        
        "exceptions": {
            "1913937": 6,
            "1914066": 19,
            "1914062": 19,
            "1914035": 16,
            "1914092": 23,
        },
    },

    "England Premier League": {
        "matchweeks_2025-2026": [          
            ("2025-08-15", "2025-08-18", 1),
            ("2025-08-22", "2025-08-25", 2),
            ("2025-08-29", "2025-09-01", 3),
            ("2025-09-13", "2025-09-15", 4),
            ("2025-09-20", "2025-09-22", 5),
            ("2025-09-27", "2025-09-29", 6),
            ("2025-10-03", "2025-10-06", 7),
            ("2025-10-18", "2025-10-20", 8),
            ("2025-10-24", "2025-10-27", 9),
            ("2025-11-01", "2025-11-03", 10),
            ("2025-11-08", "2025-11-10", 11),
            ("2025-11-22", "2025-11-24", 12),
            ("2025-11-29", "2025-12-01", 13),
            ("2025-12-02", "2025-12-05", 14),   # Intersemanal
            ("2025-12-06", "2025-12-08", 15),
            ("2025-12-13", "2025-12-15", 16),
            ("2025-12-20", "2025-12-22", 17),
            ("2025-12-26", "2025-12-29", 18),
            ("2025-12-30", "2026-01-01", 19),   # Intersemanal
            ("2026-01-03", "2026-01-05", 20),
            ("2026-01-06", "2026-01-08", 21),
            ("2026-01-17", "2026-01-19", 22),
            ("2026-01-24", "2026-01-26", 23),
            ("2026-01-31", "2026-02-02", 24),
            ("2026-02-06", "2026-02-08", 25),   # Intersemanal
            ("2026-02-10", "2026-02-12", 26),
            ("2026-02-21", "2026-02-23", 27),
            ("2026-02-27", "2026-03-01", 28),   # Intersemanal
            ("2026-03-03", "2026-03-05", 29),
            ("2026-03-14", "2026-03-16", 30),
            ("2026-03-20", "2026-03-23", 31),
            ("2026-04-10", "2026-04-13", 32),
            ("2026-04-18", "2026-04-20", 33),
            ("2026-04-21", "2026-04-27", 34),
            ("2026-05-01", "2026-05-04", 35),
            ("2026-05-09", "2026-05-11", 36),
            ("2026-05-15", "2026-05-19", 37),   # Intersemanal
            ("2026-05-24", "2026-05-25", 38)
        ],
        "matchweeks_2026-2027": [
            ("2026-08-21", "2026-08-24", 1),
            ("2026-08-28", "2026-08-31", 2),
            ("2026-09-04", "2026-09-06", 3),
            ("2026-09-12", "2026-09-14", 4),
            ("2026-09-18", "2026-09-20", 5),
            ("2026-10-09", "2026-10-12", 6),
            ("2026-10-18", "2026-10-19", 7),
            ("2026-10-23", "2026-10-26", 8),
            ("2026-10-30", "2026-11-02", 9),
            ("2026-11-06", "2026-11-09", 10),
            ("2026-11-20", "2026-11-23", 11),
            ("2026-11-27", "2026-11-30", 12),
            ("2026-12-01", "2026-12-03", 13),
            ("2026-12-04", "2026-12-07", 14),
            ("2026-12-11", "2026-12-14", 15),
            ("2026-12-18", "2026-12-21", 16),
            ("2026-12-25", "2026-12-28", 17),
            ("2026-12-29", "2026-12-31", 18),
            ("2027-01-01", "2027-01-04", 19),
            ("2027-01-05", "2027-01-07", 20),
            ("2027-01-15", "2027-01-18", 21),
            ("2027-01-22", "2027-01-25", 22),
            ("2027-01-29", "2027-02-01", 23),
            ("2027-02-05", "2027-02-08", 24),
            ("2027-02-09", "2027-02-11", 25),
            ("2027-02-19", "2027-02-22", 26),
            ("2027-02-26", "2027-03-01", 27),
            ("2027-03-02", "2027-03-04", 28),
            ("2027-03-12", "2027-03-15", 29),
            ("2027-03-19", "2027-03-22", 30),
            ("2027-04-09", "2027-04-12", 31),
            ("2027-04-16", "2027-04-19", 32),
            ("2027-04-23", "2027-04-26", 33),
            ("2027-04-30", "2027-05-03", 34),
            ("2027-05-07", "2027-05-10", 35),
            ("2027-05-14", "2027-05-17", 36),
            ("2027-05-21", "2027-05-24", 37),
            ("2027-05-28", "2027-05-31", 38)
        ],
        "exceptions": {
            "1903466": 31,
            "1903469": 31
           
        },
    },

    "Germany Bundesliga": {
        "matchweeks_2025-2026": [          
            ("2025-08-22", "2025-08-25", 1),
            ("2025-08-29", "2025-09-01", 2),
            ("2025-09-12", "2025-09-15", 3),
            ("2025-09-19", "2025-09-22", 4),
            ("2025-09-26", "2025-09-29", 5),
            ("2025-10-03", "2025-10-06", 6),
            ("2025-10-17", "2025-10-20", 7),
            ("2025-10-24", "2025-10-27", 8),
            ("2025-10-31", "2025-11-03", 9),
            ("2025-11-07", "2025-11-10", 10),
            ("2025-11-21", "2025-11-24", 11),
            ("2025-11-28", "2025-12-01", 12),
            ("2025-12-05", "2025-12-08", 13),
            ("2025-12-12", "2025-12-15", 14),
            ("2025-12-19", "2025-12-22", 15),
            ("2026-01-09", "2026-01-12", 16),
            ("2026-01-13", "2026-01-15", 17),  
            ("2026-01-16", "2026-01-19", 18),
            ("2026-01-23", "2026-01-26", 19),  
            ("2026-01-30", "2026-02-02", 20),
            ("2026-02-06", "2026-02-09", 21),
            ("2026-02-13", "2026-02-16", 22),
            ("2026-02-20", "2026-02-23", 23),
            ("2026-02-27", "2026-03-02", 24),
            ("2026-03-06", "2026-03-09", 25),
            ("2026-03-13", "2026-03-16", 26),
            ("2026-04-20", "2026-04-23", 27),
            ("2026-04-04", "2026-04-06", 28),
            ("2026-04-10", "2026-04-13", 29),
            ("2026-04-17", "2026-04-20", 30),
            ("2026-04-24", "2026-04-27", 31),
            ("2026-05-02", "2026-05-04", 32),
            ("2026-05-08", "2026-05-11", 33),
            ("2026-05-16", "2026-05-17", 34)
        ],
        "matchweeks_2026-2027": [
            ("2026-08-28", "2026-08-30", 1),
            ("2026-09-04", "2026-09-06", 2),
            ("2026-09-12", "2026-09-13", 3),
            ("2026-09-18", "2026-09-20", 4),
            ("2026-10-09", "2026-10-12", 5),
            ("2026-10-16", "2026-10-19", 6),
            ("2026-10-23", "2026-10-26", 7),
            ("2026-10-30", "2026-11-02", 8),
            ("2026-11-06", "2026-11-09", 9),
            ("2026-11-20", "2026-11-23", 10),
            ("2026-11-27", "2026-11-30", 11),
            ("2026-12-04", "2026-12-07", 12),
            ("2026-12-11", "2026-12-14", 13),
            ("2026-12-18", "2026-12-21", 14),
            ("2027-01-08", "2027-01-11", 15),
            ("2027-01-12", "2027-01-14", 16),
            ("2027-01-15", "2027-01-18", 17),
            ("2027-01-22", "2027-01-25", 18),
            ("2027-01-29", "2027-02-01", 19),
            ("2027-02-05", "2027-02-08", 20),
            ("2027-02-12", "2027-02-15", 21),
            ("2027-02-19", "2027-02-22", 22),
            ("2027-02-26", "2027-03-01", 23),
            ("2027-03-02", "2027-03-04", 24),
            ("2027-03-05", "2027-03-08", 25),
            ("2027-03-12", "2027-03-15", 26),
            ("2027-03-19", "2027-03-22", 27),
            ("2027-04-02", "2027-04-05", 28),
            ("2027-04-09", "2027-04-12", 29),
            ("2027-04-16", "2027-04-19", 30),
            ("2027-04-23", "2027-04-26", 31),
            ("2027-05-07", "2027-05-10", 32),
            ("2027-05-14", "2027-05-17", 33),
            ("2027-05-21", "2027-05-24", 34)
        ],
        "exceptions": {
           "1910684": 16,
           "1910688": 16,
           "1910799": 17,
                      
        },
    },

    "Italy Serie A": {
        "matchweeks_2025-2026": [          
            ("2025-08-23", "2025-08-25", 1),
            ("2025-08-29", "2025-09-01", 2),
            ("2025-09-13", "2025-09-15", 3),
            ("2025-09-19", "2025-09-22", 4),
            ("2025-09-27", "2025-09-29", 5),
            ("2025-10-03", "2025-10-06", 6),
            ("2025-10-18", "2025-10-20", 7),
            ("2025-10-24", "2025-10-27", 8),
            ("2025-10-28", "2025-10-30", 9),
            ("2025-11-01", "2025-11-03", 10),
            ("2025-11-07", "2025-11-10", 11),
            ("2025-11-21", "2025-11-24", 12),
            ("2025-11-28", "2025-12-01", 13),
            ("2025-12-06", "2025-12-09", 14),
            ("2025-12-12", "2025-12-15", 15),
            ("2025-12-20", "2025-12-22", 16),
            ("2026-12-27", "2026-12-29", 17),
            ("2026-01-02", "2026-01-04", 18),
            ("2026-01-06", "2026-01-08", 19),
            ("2026-01-10", "2026-01-12", 20),
            ("2026-01-16", "2026-01-19", 21),
            ("2026-01-23", "2026-02-26", 22),
            ("2026-01-30", "2026-02-03", 23),
            ("2026-02-06", "2026-02-09", 24),
            ("2026-02-13", "2026-02-16", 25),
            ("2026-02-20", "2026-02-23", 26),
            ("2026-02-27", "2026-03-02", 27),
            ("2026-03-06", "2026-03-09", 28),
            ("2026-03-13", "2026-03-16", 29),
            ("2026-03-20", "2026-03-23", 30),
            ("2026-04-04", "2026-04-06", 31),
            ("2026-04-10", "2026-04-13", 32),
            ("2026-04-17", "2026-04-20", 33),
            ("2026-04-24", "2026-04-27", 34),
            ("2026-05-01", "2026-05-04", 35),
            ("2026-05-08", "2026-05-11", 36),
            ("2026-05-17", "2026-05-18", 37),  # intersemanal posible
            ("2026-05-22", "2026-05-25", 38)
        ],
        "matchweeks_2026-2027": [          
            ("2026-08-21", "2026-08-24", 1),
            ("2026-08-28", "2026-08-31", 2),
            ("2026-09-04", "2026-09-07", 3),
            ("2026-09-11", "2026-09-14", 4),
            ("2026-09-18", "2026-09-20", 5),
            ("2026-10-09", "2026-10-12", 6),
            ("2026-10-16", "2026-10-19", 7),
            ("2026-10-23", "2026-10-26", 8),
            ("2026-10-27", "2026-10-29", 9),
            ("2026-10-30", "2026-11-02", 10),
            ("2026-11-06", "2026-11-09", 11),
            ("2026-11-20", "2026-11-23", 12),
            ("2026-11-27", "2026-11-30", 13),
            ("2026-12-04", "2026-12-07", 14),
            ("2026-12-11", "2026-12-14", 15),
            ("2026-12-18", "2026-12-21", 16),
            ("2027-01-01", "2027-01-04", 17),
            ("2027-01-05", "2027-01-07", 18),
            ("2027-01-08", "2027-01-11", 19),
            ("2027-01-15", "2027-01-18", 20),
            ("2027-01-22", "2027-01-25", 21),
            ("2027-01-29", "2027-02-01", 22),
            ("2027-02-05", "2027-02-08", 23),
            ("2027-02-12", "2027-02-15", 24),
            ("2027-02-19", "2027-02-22", 25),
            ("2027-02-26", "2027-03-01", 26),
            ("2027-03-05", "2027-03-08", 27),
            ("2027-03-12", "2027-03-15", 28),
            ("2027-03-19", "2027-03-22", 29),
            ("2027-04-02", "2027-04-05", 30),
            ("2027-04-09", "2027-04-12", 31),
            ("2027-04-16", "2027-04-19", 32),
            ("2027-04-23", "2027-04-26", 33),
            ("2027-04-30", "2027-05-03", 34),
            ("2027-05-07", "2027-05-10", 35),
            ("2027-05-14", "2027-05-17", 36),
            ("2027-05-21", "2027-05-24", 37),
            ("2027-05-28", "2027-05-31", 38)
        ],
        "exceptions": {
            "1901309": 16,
            "1901306": 16,
            "1901311": 16,
            "1901303": 16,
            "1901358": 24
 
        },
    },

    "France Ligue 1": {
        "matchweeks_2025-2026": [          
            ("2025-08-15", "2025-08-17", 1),
            ("2025-08-22", "2025-08-24", 2),
            ("2025-08-29", "2025-08-31", 3),
            ("2025-09-12", "2025-09-14", 4),
            ("2025-09-19", "2025-09-22", 5),
            ("2025-09-26", "2025-09-28", 6),
            ("2025-10-03", "2025-10-05", 7),
            ("2025-10-17", "2025-10-19", 8),
            ("2025-10-24", "2025-10-26", 9),
            ("2025-10-29", "2025-10-30", 10),
            ("2025-11-01", "2025-11-03", 11),
            ("2025-11-07", "2025-11-09", 12),
            ("2025-11-21", "2025-11-23", 13),
            ("2025-11-28", "2025-11-30", 14),
            ("2025-12-05", "2025-12-07", 15),
            ("2025-12-12", "2025-12-14", 16),
            ("2026-01-02", "2026-01-04", 17),
            ("2026-01-16", "2026-01-18", 18),
            ("2026-01-23", "2026-01-25", 19),
            ("2026-01-30", "2026-02-01", 20),
            ("2026-02-06", "2026-02-08", 21),
            ("2026-02-13", "2026-02-15", 22),
            ("2026-02-20", "2026-02-22", 23),
            ("2026-02-27", "2026-03-01", 24),
            ("2026-03-06", "2026-03-08", 25),
            ("2026-03-13", "2026-03-15", 26),
            ("2026-03-20", "2026-03-22", 27),
            ("2026-04-03", "2026-04-05", 28),
            ("2026-04-10", "2026-04-12", 29),
            ("2026-04-17", "2026-04-19", 30),
            ("2026-04-24", "2026-04-26", 31),
            ("2026-05-01", "2026-05-03", 32),
            ("2026-05-08", "2026-05-10", 33),
            ("2026-05-17", "2026-05-18", 34),
        ],
        "matchweeks_2026-2027": [
            ("2026-08-21", "2026-08-23", 1),
            ("2026-08-28", "2026-08-30", 2),
            ("2026-09-03", "2026-09-06", 3),
            ("2026-09-10", "2026-09-13", 4),
            ("2026-09-18", "2026-09-20", 5),
            ("2026-10-09", "2026-10-12", 6),
            ("2026-10-16", "2026-10-19", 7),
            ("2026-10-23", "2026-10-26", 8),
            ("2026-10-30", "2026-11-02", 9),
            ("2026-11-06", "2026-11-09", 10),
            ("2026-11-20", "2026-11-23", 11),
            ("2026-11-27", "2026-11-30", 12),
            ("2026-12-04", "2026-12-07", 13),
            ("2026-12-11", "2026-12-14", 14),
            ("2027-01-01", "2027-01-04", 15),
            ("2027-01-15", "2027-01-18", 16),
            ("2027-01-22", "2027-01-25", 17),
            ("2027-01-29", "2027-02-01", 18),
            ("2027-02-05", "2027-02-08", 19),
            ("2027-02-12", "2027-02-15", 20),
            ("2027-02-19", "2027-02-22", 21),
            ("2027-02-26", "2027-03-01", 22),
            ("2027-03-05", "2027-03-08", 23),
            ("2027-03-12", "2027-03-15", 24),
            ("2027-03-19", "2027-03-22", 25),
            ("2027-04-02", "2027-04-05", 26),
            ("2027-04-09", "2027-04-12", 27),
            ("2027-04-16", "2027-04-19", 28),
            ("2027-04-23", "2027-04-26", 29),
            ("2027-04-30", "2027-05-03", 30),
            ("2027-05-07", "2027-05-10", 31),
            ("2027-05-14", "2027-05-17", 32),
            ("2027-05-21", "2027-05-24", 33),
            ("2027-05-28", "2027-05-31", 34)
        ],
        "exceptions": {
            "1911504": 26,
            "1911537": 29,
            "1911538": 29

        },
    },
}

HIGHLIGHT_DICT = {
    #LA LIGA
    'Deportivo Alaves':          '#0066CC',   # azul dominante
    'Athletic Club':             '#EE2523',   # rojo rojiblanco :contentReference[oaicite:0]{index=0}
    'Atletico Madrid':        '#CB3524',# rojo célebre  
    'Barcelona':                '#004D98',   # azul marino ùnico  
    'Real Betis':                '#007A33',   # verde Betis  
    'Celta Vigo':             '#78BE20',   # verde céltico  
    'Espanyol':              '#007FC8',   # azul periquito :contentReference[oaicite:1]{index=1}
    'Getafe':                 '#003C71',   # azul Getafe  
    'Girona':                 '#FF6A00',   # naranja Gironí   
    'Las Palmas':             '#FDB913',   # amarillo claro  
    'Leganés':                '#005BAA',   # azul Leganés  
    'Mallorca':              '#990000',   # granate Mallorca  
    'Osasuna':                '#E31937',   # rojo Osasuna  
    'Rayo Vallecano':            '#D31947',  # rojo franja  
    'Real Madrid':            '#FFFFFF',   # blanco clásico  
    'Real Sociedad':             '#1B4F9C',   # azul txuri-urdin  
    'Sevilla':                '#D70F21',   # rojo sevillista  
    'Valencia':               '#0097D7',   # azul Valencia :contentReference[oaicite:2]{index=2}
    'Real Valladolid':        '#512888',   # violeta Pucela  
    'Villarreal':             '#FFE667',   # amarillo Villarreal 
    'Elche' :                 "#08DF61", 
    'Levante' :               "#EB1596", 
    'Real Oviedo':            "#4088C8",

    #SERIE A
    'Napoli':                 '#009DDC',  # azul Napoli
    'Inter':                  '#003399',  # azul Inter
    'Atalanta':               '#1C1C9C',  # azul oscuro Atalanta
    'Juventus':               '#000000',  # negro Juventus
    'Roma':                   '#8E1111',  # rojo romano
    'Fiorentina':             '#582C83',  # violeta Fiorentina
    'Lazio':                  '#A5CBE3',  # celeste Lazio
    'Milan':                  '#D50000',  # rojo Milan
    'Bolonia':                '#AA1454',  # rojo Bologna
    'Como':                   '#005BAC',  # azul Como
    'Torino':                 '#781F1F',  # granate Torino
    'Udinese':                '#CCCCCC',  # gris Udinese
    'Génova':                 "#020202",  # rojo Genoa
    'Hellas Verona':          '#F4C514',  # amarillo Verona
    'Cagliari':               '#C8102E',  # rojo Cagliari
    'Parma':                  '#FFF200',  # amarillo Parma
    'Lecce':                  '#DC143C',  # rojo Lecce
    'Empoli':                 '#0073CF',  # azul Empoli
    'Venezia':                '#FF7F00',  # naranja Venezia
    'Monza':                  '#E30613',  # rojo Monza
    'Sassuolo':               "#074422",
    'Cremonese':              "#4E2E30",
    'Pisa':                   "#161B33FF",   

    #BUNDESLIGA
    'Bayern Múnich':             '#DC052D',   # rojo Bayern
    'Bayer 04 Leverkusen':       '#E2001A',   # rojo Leverkusen
    'Eintracht Frankfurt':       '#000000',   # negro Frankfurt
    'Borussia Dortmund':         '#FDE100',   # amarillo Dortmund
    'Friburgo':               '#000000',   # negro Freiburg
    'Mainz 05':              '#C60C30',   # rojo Mainz
    'RB Leipzig':                '#FFFFFF',   # blanco Leipzig
    'Werder Bremen':          '#008060',   # verde Bremen
    'VFB Stuttgart':             '#E32219',   # rojo Stuttgart
    'Borussia Mönchengladbach':  '#0A3C02',   # verde oscuro Gladbach
    'Wolfsburgo':            '#65B32E',   # verde Wolfsburg
    'Augsburgo':              '#B5121B',   # rojo Augsburg
    'Union Berlin':           '#E30C1B',   # rojo Union
    'St. Pauli':              '#402E2A',   # marrón St. Pauli
    'Hoffenheim':       '#005BAC',   # azul Hoffenheim
    'FC Heidenheim':        '#DA291C',   # rojo Heidenheim
    'Holstein Kiel':             '#005CA9',   # azul Kiel
    'Bochum':                '#1E4DA1',   # azul Bochum
    "Hamburger SV":               "#F5D2CD",
    '1. FC Köln':                "#FAD5D5",

    #PREMIER LEAGUE
    'Liverpool':             '#C8102E',   # rojo Liverpool
    'Arsenal':               '#EF0107',   # rojo Arsenal
    'Manchester City':          '#6CABDD',   # azul cielo City
    'Chelsea':               '#034694',   # azul Chelsea
    'Newcastle United':         '#241F20',   # negro Newcastle
    'Aston Villa':              '#670E36',   # burdeos Villa
    'Nottingham Forest':        '#DD0000',   # rojo Forest
    'Brighton & Hove Albion':   '#0057B8',   # azul Brighton
    'AFC Bournemouth':          '#DA291C',   # rojo Bournemouth
    'Brentford':             '#E30613',   # rojo Brentford
    'Fulham':                '#000000',   # negro Fulham
    'Crystal Palace':           '#1B458F',   # azul Palace
    'Everton':               '#003399',   # azul Everton
    'West Ham United':          '#7A263A',   # burdeos West Ham
    'Manchester United':        '#DA291C',   # rojo Man. United
    'Wolverhampton Wanderers':  '#FDB913',   # amarillo Wolves
    'Tottenham Hotspur':        '#132257',   # azul Spurs
    'Leicester City':           '#003090',   # azul Leicester
    'Ipswich Town':             '#005BAC',   # azul Ipswich
    'Southampton':           '#D71920',   # rojo Southampton
    "Leeds United":             "#879210",
    'Sunderland':           "#EA898C" ,
    'Burnley':               "#C80E81" ,

    #LIGUE 1
    'Paris Saint-Germain':   '#004170',   # azul PSG
    'Marseille':             '#0093D0',   # celeste Marseille
    'Monaco':                '#FF0000',   # rojo Monaco
    'Nice':                  '#E30B17',   # rojo Nice
    'Lille':                 '#ED1C24',   # rojo Lille
    'Lyon':                  '#001E61',   # azul Lyon
    'Strasbourg':            '#005BAC',   # azul Strasbourg
    'Lens':                  '#FFD800',   # amarillo Lens
    'Brest':                 '#E0001B',   # rojo Brest
    'Toulouse':              '#461D7C',   # púrpura Toulouse
    'Auxerre':               '#0073CF',   # azul Auxerre
    'Rennes FC':             '#E50C0C',   # rojo Rennes
    'Nantes':                '#FFE600',   # amarillo Nantes
    'Angers':                '#000000',   # negro Angers
    'Le Havre':              '#4C6B94',   # azul Le Havre
    'Stade de Reims':        '#D2001A',   # rojo Reims
    'Saint-Étienne':         '#00874B',   # verde Saint-Étienne
    'Montpellier':           '#F47920',   # naranja Montpellier
    'Paris FC':              "#464387", 
    'Lorient':               "#E56205" ,
    'Metz':                  '#C80E81'
}
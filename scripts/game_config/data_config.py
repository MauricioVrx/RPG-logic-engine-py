from scripts.game_config.constants import PROF_NAMES

#====================================================================
# TIME SYSTEM VALUES
#====================================================================
# Time initial date
INIT_YEAR  = 1216
INIT_MONTH = 1
INIT_DAY   = 1
INIT_HOUR  = 8

# Time format
MINUTES_PER_HOUR = 60
HOURS_PER_DAY    = 24

DAYS_PER_MONTH   = 40
MONTHS_PER_YEAR  = 8

DAYS_PER_YEAR    = DAYS_PER_MONTH * MONTHS_PER_YEAR

# Dictionary of the seasons of the year with the corresponding month
SEASONS = {
    1: "spring",
    2: "spring",
    3: "summer",
    4: "summer",
    5: "autumn",
    6: "autumn",
    7: "winter",
    8: "winter",
}

# List of times of day with start times
DAY_PHASES = [
    (5, "dawn"),
    (8, "morning"),
    (12, "afternoon"),
    (18, "sunset"),
    (20, "night"),
    (0, "deep_night")
]


#=========================================================================
# CD DIFFICULT
#=========================================================================
DIFFICULT_BY_PROFICIENCY = dict(zip(PROF_NAMES, [10,15,20,30,40])) 
DIFFICULT_BY_LEVEL       = {0: 14, 1: 15, 2: 16, 3: 18, 4: 19, 5: 20, 6: 22, 7: 23, 8: 24, 9: 26, 10: 27, 11: 28, 12: 30, 13: 31, 14: 32, 15: 34, 16: 35, 17: 36, 18: 38, 19: 39, 20: 40, 21: 42, 22: 44, 23: 46, 24: 48, 25: 50}
DIFFICULT_ADJUSTMENT     = { "Incredibly Easy": -10, "Very Easy": -5, "Easy": -2, "Hard": +2, "Very Hard": +5, "Incredibly Hard": +10 }

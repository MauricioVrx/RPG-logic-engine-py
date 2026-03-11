from scripts.game_system.data_config  import (MINUTES_PER_HOUR, HOURS_PER_DAY, DAYS_PER_MONTH, MONTHS_PER_YEAR, DAYS_PER_YEAR, SEASONS)

class Calendar:
    MINUTES_PER_HOUR = MINUTES_PER_HOUR
    HOURS_PER_DAY    = HOURS_PER_DAY

    DAYS_PER_MONTH   = DAYS_PER_MONTH
    MONTHS_PER_YEAR  = MONTHS_PER_YEAR

    DAYS_PER_YEAR    = DAYS_PER_YEAR
    
    SEASONS          = SEASONS

    @classmethod
    def get_season(cls, month):
        return cls.SEASONS.get(month)
    
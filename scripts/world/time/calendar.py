from scripts.game_system.data_config  import (MINUTES_PER_HOUR, HOURS_PER_DAY, DAYS_PER_MONTH, MONTHS_PER_YEAR, DAYS_PER_YEAR, SEASONS, DAY_PHASES)

class Calendar:
    """
    Static configuration class for time rules.

    Defines constants and helper methods for:
    - Time units
    - Seasons
    - Day phases
    """

    MINUTES_PER_HOUR = MINUTES_PER_HOUR
    HOURS_PER_DAY    = HOURS_PER_DAY

    DAYS_PER_MONTH   = DAYS_PER_MONTH
    MONTHS_PER_YEAR  = MONTHS_PER_YEAR

    DAYS_PER_YEAR    = DAYS_PER_YEAR
    
    SEASONS          = SEASONS

    DAY_PHASES       = DAY_PHASES

    @classmethod
    def get_season(cls, month):
        return cls.SEASONS.get(month)
    
    @classmethod
    def get_day_phase(cls, hour):
        """
        Returns the day phase corresponding to a given hour.

        Returns
        -------
        list
            [hour_start, phase_name, index]
        """
        day_phase = -1
        pos = 0
        for idx in range(len(DAY_PHASES)-1):
            if DAY_PHASES[idx][0] <= hour < DAY_PHASES[idx+1][0]:
                day_phase = DAY_PHASES[idx]
                pos = idx
                break
        if day_phase == -1:
            day_phase = DAY_PHASES[-1]
        day_phase =  list(day_phase) + [pos]
        return day_phase
    
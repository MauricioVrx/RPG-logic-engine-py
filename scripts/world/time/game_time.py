from scripts.world.time.calendar     import Calendar
from scripts.game_config.data_config import INIT_YEAR, INIT_MONTH, INIT_DAY, INIT_HOUR

class GameTime:
    """
    Core time representation of the game.

    Stores time internally as total minutes and provides utilities
    to convert between absolute time and structured date formats.

    Responsibilities
    ----------------
    - Store total elapsed time
    - Convert between minutes and date formats
    - Provide current date and time
    - Calculate elapsed playtime
    """
    def __init__(self, year=INIT_YEAR, month=INIT_MONTH, day=INIT_DAY, hour=INIT_HOUR):
        self.total_minutes = self.to_minutes(year, month, day, hour)
        self.initial_date  = year, month, day, hour, 0


    def to_minutes(self, year, month, day, hour, minutes = 0):
        """
        Convert a date to minutes
        """
        days = (
            year * Calendar.DAYS_PER_YEAR
            + (month - 1) * Calendar.DAYS_PER_MONTH
            + (day - 1)
        )
        return days * 1440 + hour * Calendar.MINUTES_PER_HOUR + minutes
    

    def get_date(self, initial_minutes = 0):
        """
        Converts total minutes into a structured date.

        Returns current or custom time based on provided minutes.

        Returns
        -------
        tuple
            (year, month, day, hour, minute)
        """
        if initial_minutes == 0:
            minutes = self.total_minutes
        else:
            minutes = initial_minutes

        total_days = minutes // (Calendar.MINUTES_PER_HOUR * Calendar.HOURS_PER_DAY)

        hour = (minutes % (Calendar.MINUTES_PER_HOUR * Calendar.HOURS_PER_DAY)) // Calendar.MINUTES_PER_HOUR
        minute = minutes % Calendar.MINUTES_PER_HOUR
        year = total_days // Calendar.DAYS_PER_YEAR

        remaining_days = total_days % Calendar.DAYS_PER_YEAR

        month = (remaining_days // Calendar.DAYS_PER_MONTH) +1 
        day = (remaining_days % Calendar.DAYS_PER_MONTH) +1

        return  year, month, day, hour, minute
    

    def get_season(self, month):
        """
        Get current season by month.
        """
        n_month = month
        if isinstance(n_month, tuple):
            n_month = int(n_month[-4])
        return Calendar.get_season(n_month)


    def get_day_phase(self, phase_type = "name"):
        """
        Get current day phase.
        """
        _ , _, _, hour, _ = self.get_date()
        actual_position = Calendar.get_day_phase(hour)
        if phase_type == "name":
            return actual_position[1]
        elif phase_type == "hour":
            return actual_position[0]
        elif phase_type == "position":
            return actual_position[2]
        else:
            return actual_position
        
    def get_game_time(self):
        """
        Get the total time spent playing the game since it started.
        """
        now_year, now_month, now_day, now_hour, now_minute = self.get_date()
        initial_year, initial_month, initial_day, initial_hour, initial_minute = self.initial_date
        
        initial_minutes = self.to_minutes(initial_year, initial_month, initial_day, initial_hour, initial_minute)
        today_minutes   = self.to_minutes(now_year, now_month, now_day, now_hour, now_minute)
        
        diff_minutes = today_minutes - initial_minutes
        total_days   = diff_minutes // (Calendar.MINUTES_PER_HOUR * Calendar.HOURS_PER_DAY)

        hour   = (diff_minutes % (Calendar.MINUTES_PER_HOUR * Calendar.HOURS_PER_DAY)) // Calendar.MINUTES_PER_HOUR
        minute = diff_minutes % Calendar.MINUTES_PER_HOUR
        year   = total_days // Calendar.DAYS_PER_YEAR

        remaining_days = total_days % Calendar.DAYS_PER_YEAR

        month = (remaining_days // Calendar.DAYS_PER_MONTH)
        day = (remaining_days % Calendar.DAYS_PER_MONTH)

        return  year, month, day, hour, minute

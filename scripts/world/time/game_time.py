from scripts.world.time.calendar     import Calendar
from scripts.game_system.data_config import INIT_YEAR, INIT_MONTH, INIT_DAY, INIT_HOUR

class GameTime:

    def __init__(self, year=INIT_YEAR, month=INIT_MONTH, day=INIT_DAY, hour=INIT_HOUR):
        self.total_minutes = self.to_minutes(year, month, day, hour)

    def to_minutes(self, year, month, day, hour, minutes = 0):
        days = (
            year * Calendar.DAYS_PER_YEAR
            + (month - 1) * Calendar.DAYS_PER_MONTH
            + (day - 1)
        )

        return days * 1440 + hour * Calendar.MINUTES_PER_HOUR + minutes
    

    def get_date(self):
        minutes = self.total_minutes

        total_days = minutes // 1440

        hour = (minutes % 1440) // Calendar.MINUTES_PER_HOUR
        minute = minutes % Calendar.MINUTES_PER_HOUR
        year = total_days // Calendar.DAYS_PER_YEAR

        remaining_days = total_days % Calendar.DAYS_PER_YEAR
        month = (remaining_days // Calendar.DAYS_PER_MONTH) + 1
        day = (remaining_days % Calendar.DAYS_PER_MONTH) + 1

        return  year, month, day, hour, minute
    

    def get_season(self, month):
        n_month = month
        if isinstance(n_month, tuple):
            n_month = int(n_month[3])
        return Calendar.get_season(n_month)


    def get_day_phase(self, hour):
        n_hour = hour
        if isinstance(n_hour, tuple):
            n_hour = int(n_hour[1])
            
        return Calendar.get_day_phase(n_hour)
    
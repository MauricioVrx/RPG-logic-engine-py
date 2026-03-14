from scripts.game_system.data_config import MINUTES_PER_HOUR, HOURS_PER_DAY, DAYS_PER_MONTH, MONTHS_PER_YEAR
from scripts.world.time.calendar import MONTHS_PER_YEAR, DAYS_PER_MONTH, HOURS_PER_DAY, MINUTES_PER_HOUR


class TimeSystem:

    def __init__(self, game_time):
        self.game_time = game_time

    def advance_minutes(self, minutes):
        self.game_time.total_minutes += minutes

    def pass_minutes(self, minutes):
        self.advance_minutes(minutes)

    def pass_hours(self, hours):
        self.pass_minutes(hours * MINUTES_PER_HOUR)

    def pass_days(self, days):
        self.pass_hours(days * HOURS_PER_DAY)

    def pass_months(self, months):
        self.pass_days(months * DAYS_PER_MONTH)

    def pass_years(self, years):
        self.pass_months(years * MONTHS_PER_YEAR)

    def pass_time_next_to(self, years = None, months = None, days = None, hours = None, minutes= None):
        initial_date = self.game_time.get_date()

        time_funcs_list = [self.pass_years, self.pass_months, self.pass_days, self.pass_hours, self.pass_minutes]
        
        pass_to_date    = [years, months, days, hours, minutes]
        print(initial_date)
        print(pass_to_date)
        pass_time = self.get_time_diff(initial_date, pass_to_date)

        for n in range(len(pass_time)):
            time_funcs_list[n](pass_time[n])


    def get_time_diff(self, today, pass_to_date):
        time_range = [MONTHS_PER_YEAR, DAYS_PER_MONTH, HOURS_PER_DAY, MINUTES_PER_HOUR]
        actual_date = today
        to_date     = pass_to_date

        range_list = len(to_date)

        # Last position in lists with diff from today and pass_to_date
        last_position = 0
        for pos in range(range_list):
            if actual_date[pos] != to_date[pos] and to_date[pos] != None:
                last_position = pos
                break

        pass_time_list = [0] # list showing the time difference
        if to_date[0] != None:
            pass_time_list = [to_date[0] - actual_date[0]] # years diff 

        for time in range(1, range_list):

            actual  = actual_date[time]
            to_time = to_date[time]

            if (to_time == None) or (sum(pass_time_list) > 0 and actual == to_time):
                pass_time_list.append(0)
                continue

            if to_time <= actual and last_position >= time:
                n_time = time_range[time-1] - actual + to_time
                if pass_time_list[time-1] > 0:
                    pass_time_list[time-1] -= 1
            else:
                n_time = to_time - actual
            pass_time_list.append(n_time)

        return pass_time_list
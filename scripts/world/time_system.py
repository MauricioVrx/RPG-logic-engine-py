from scripts.game_system.data_config import MINUTES_PER_HOUR, HOURS_PER_DAY, DAYS_PER_MONTH, MONTHS_PER_YEAR, DAY_PHASES

from scripts.system.exceptions import (
    TimeFormatError,
    TimeNamePhaseNotFoundError
)

class TimeSystem:

    def __init__(self, game_time):
        self.game_time = game_time

    # ==============================================================
    # TIME PASS FUNCTIONS
    # ==============================================================

    def advance_minutes(self, minutes):
        """Add minutes to the playing time"""
        self.game_time.total_minutes += minutes

    def pass_minutes(self, minutes):
        """Add minutes to the playing time"""
        self.advance_minutes(minutes)

    def pass_hours(self, hours):
        """Add hours to the playing time"""
        self.pass_minutes(hours * MINUTES_PER_HOUR)

    def pass_days(self, days):
        """Add days to the playing time"""
        self.pass_hours(days * HOURS_PER_DAY)

    def pass_months(self, months):
        """Add months to the playing time"""
        self.pass_days(months * DAYS_PER_MONTH)

    def pass_years(self, years):
        """Add years to the playing time"""
        self.pass_months(years * MONTHS_PER_YEAR)

    def pass_time_next_to(self, years = None, months = None, days = None, hours = None, minutes= None):
        """
        Pass playing time to next coincidence with input time
        """

        initial_date = self.game_time.get_date()

        time_funcs_list = [self.pass_years, self.pass_months, self.pass_days, self.pass_hours, self.pass_minutes]
        
        pass_to_date    = [years, months, days, hours, minutes]

        pass_time = self.get_time_diff(initial_date, pass_to_date)

        for n in range(len(pass_time)):
            time_funcs_list[n](pass_time[n])


    def pass_day_phases(self, n_phases = 1):
        """Pass day phase n times"""
        len_phases_list = len(DAY_PHASES)
        actual = self.get_day_phase()[2]
        to_phase = actual + n_phases

        while to_phase > len_phases_list-1:
            to_phase -= len_phases_list

        hour = DAY_PHASES[to_phase][0]

        return self.pass_time_next_to(hours=hour, minutes= 0)

    def __pass_to_day_phase(self, name):
        for phase in DAY_PHASES:
            if phase[1] == name:
                return phase[0]
        raise TimeNamePhaseNotFoundError(name)

    def pass_to_morning(self):
        """Pass day phase to morning"""
        hour = self.__pass_to_day_phase("morning")
        self.pass_time_next_to(hours=hour, minutes= 0)
         
    def pass_to_sunset(self):
        """Pass day phase to sunset"""
        hour = self.__pass_to_day_phase("sunset")
        self.pass_time_next_to(hours=hour, minutes= 0)

    def pass_to_night(self):
        """Pass day phase to night"""
        hour = self.__pass_to_day_phase("night")
        self.pass_time_next_to(hours=hour, minutes= 0)

    def get_day_phase(self):
        """Get day phase list [hour, name, index]"""
        phase = self.game_time.get_day_phase("all")
        return phase
    

    def get_time_diff(self, today, pass_to_date):
        time_range = [MONTHS_PER_YEAR, DAYS_PER_MONTH, HOURS_PER_DAY, MINUTES_PER_HOUR]
        actual_date = today
        to_date     = pass_to_date

        range_list = len(to_date)

        # Validate time range
        time_error = []
        _ , month, day, hour, minute = pass_to_date

        if minute is not None and (minute < 0 or minute >= MINUTES_PER_HOUR):
            time_error.append("minutes")

        if hour is not None and (hour < 0 or hour >= HOURS_PER_DAY):
            time_error.append("hours")

        if day is not None and (day <= 0 or day > DAYS_PER_MONTH):
            time_error.append("days")

        if month is not None and (month <= 0 or month > MONTHS_PER_YEAR):
            time_error.append("months")

        if time_error:
            raise TimeFormatError(time_error)

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
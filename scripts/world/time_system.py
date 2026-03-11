class TimeSystem:

    def __init__(self, game_time):
        self.game_time = game_time

    def advance_minutes(self, minutes):
        self.game_time.total_minutes += minutes

    def pass_minutes(self, minutes):
        self.advance_minutes(minutes)

    def pass_hours(self, hours):
        self.advance_minutes(hours * 60)

    def pass_days(self, days):
        self.advance_minutes(days * 1440)
from datetime import datetime


class Day:
    def __init__(self):
        self.day = self.set_day()

    def set_day(self):
        today = datetime.now()
        day_index = today.weekday()
        if day_index == 0:
            return "Monday"
        elif day_index == 1:
            return "Tuesday"
        elif day_index == 2:
            return "Wednesday"
        elif day_index == 3:
            return "Thursday"
        elif day_index == 4:
            return "Friday"
        elif day_index == 5:
            return "Saturday"
        elif day_index == 6:
            return "Sunday"
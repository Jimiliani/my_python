class GithubDate:
    def __init__(self, date_):
        self.year = int(date_[0:4])
        self.month = int(date_[5:7])
        self.day = int(date_[8:10])
        self.hour = int(date_[11:13])
        self.minutes = int(date_[14:16])
        self.seconds = int(date_[17:19])

    def get_str(self):
        return str(self.year) + '.' + str(self.month) + '.' + str(self.day) + ' ' + str(self.hour) + ':' + str(
            self.minutes) + ':' + str(self.seconds)

    def __gt__(self, other):
        if self.year > other.year:
            return True
        elif self.year < other.year:
            return False
        elif self.month > other.month:
            return True
        elif self.month < other.month:
            return False
        elif self.day > other.day:
            return True
        elif self.day < other.day:
            return False
        elif self.hour > other.hour:
            return True
        elif self.hour < other.hour:
            return False
        elif self.minutes > other.minutes:
            return True
        elif self.minutes < other.minutes:
            return False
        elif self.seconds > other.seconds:
            return True
        elif self.seconds <= other.seconds:
            return False

    def __it__(self, other):
        if self.year < other.year:
            return True
        elif self.year > other.year:
            return False
        elif self.month < other.month:
            return True
        elif self.month > other.month:
            return False
        elif self.day < other.day:
            return True
        elif self.day > other.day:
            return False
        elif self.hour < other.hour:
            return True
        elif self.hour > other.hour:
            return False
        elif self.minutes < other.minutes:
            return True
        elif self.minutes > other.minutes:
            return False
        elif self.seconds < other.seconds:
            return True
        elif self.seconds >= other.seconds:
            return False

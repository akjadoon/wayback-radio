import datetime

class Dataset:
    def __init__(self, name, base_url: str, earliest_date: datetime.date):
        self.name = name
        self.base_url = base_url
        self.earliest_date = earliest_date
import datetime

class DataSet:
    def __init__(self, name, base_url: str, earliest_date: datetime.date):
        if " " in name:
            raise Exception("DataSet name must not contain spaces")
        self.name = name
        self.base_url = base_url
        self.earliest_date = earliest_date

    def serialize(self):
        return {
            "name": self.name,
            "base_url": self.base_url,
            "earliest_date": datetime.datetime(self.earliest_date.year, self.earliest_date.month, self.earliest_date.day) 
        }
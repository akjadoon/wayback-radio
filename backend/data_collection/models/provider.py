import os
import datetime

from models import DataSet

class Provider:
    def __init__(self):
        pass


class BillboardProvider(Provider):
    def __init__(self):
        self.name = "billboard"
        self.datasets = [
            DataSet("hot100", "https://billboard.com/charts/the-billboard-hot-100", datetime.date(1958, 8, 4))
        ]
        self.cookie_header = os.getenv("BILLBOARD_COOKIE_HEADER")

    def get_dataset(self, dataset_name: str):
        for d in self.datasets:
            if d.name == dataset_name:
                return d
        return None

    def serialize(self):
        return {
            "name": self.name
        }

def get_provider(provider_name: str):
    if provider_name == "billboard":
        return BillboardProvider()
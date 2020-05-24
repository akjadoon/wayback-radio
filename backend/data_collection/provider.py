import os
import datetime

from dataset import Dataset

class Provider:
    def __init__(self):
        pass

class BillboardProvider:
    def __init__(self):
        self.name = "billboard"
        self.datasets = [
            Dataset("hot_100", "https://billboard.com/charts/the-billboard-hot-100", datetime.date(1958, 8, 4))
        ]
        self.cookie_header = os.getenv("BILLBOARD_COOKIE_HEADER")
    
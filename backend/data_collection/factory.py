from fetcher import BillboardFetcher
from parsers import BillboardParser
from models import BillboardProvider
from inserters import ResourceInserter

class Factory:
    def __init__(self):
        self.classes = {
            "billboard": 
                {
                    "provider": BillboardProvider,
                    "fetcher": BillboardFetcher,
                    "parser": BillboardParser,
                    "inserter": ResourceInserter
                }
        }
    def get_provider_cls(self, name):
        return self.classes[name]["provider"]

    def get_fetcher_cls(self, name):
        return self.classes[name]["fetcher"]

    def get_parser_cls(self, name):
        return self.classes[name]["parser"]

    def get_inserter_cls(self, name):
        return self.classes[name]["inserter"]

factory = Factory()
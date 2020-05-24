from fetcher import BillboardFetcher
from provider import BillboardProvider


class Factory:
    def __init__(self):
        self.classes = {
            "billboard": 
                {
                    "fetcher": BillboardFetcher,
                    "provider": BillboardProvider,
                }
        }
    def get_provider_cls(self, name):
        return self.classes[name]["provider"]

    def get_fetcher_cls(self, name):
        return self.classes[name]["fetcher"]

    def get_parser_cls(self, name):
        raise NotImplementedError

    def get_inserter_cls(self, name):
        raise NotImplementedError

factory = Factory()
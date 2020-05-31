import datetime
import regex
import logging

import factory
from models import Provider, DataSet



class FetchedFile:
    file_regex = regex.compile(r"(\w+)_(\w+)_(\d+)_(\d+)")
    @classmethod
    def from_file_name(cls, filename):
        match = cls.file_regex.match(filename)
        if len(match) < 5:
            logging.error(f"Cannot convert {filename} to FetchedFile")
            return None

        try:
            provider = factory.Factory().get_provider_cls(match[1])()
        except:
            logging.error(f"Cannot find provider {match[1]}")
            return None

        dataset = provider.get_dataset(match[2])
        if not dataset:
            logging.error(f"Provider {provider.name} has no dataset {match[2]}")
        try:
            event_date = datetime.datetime.strptime(match[3], "%Y%m%d").date()
            created_at = datetime.datetime.strptime(match[4], "%Y%m%d%H%M%S")
        except:
            logging.error(f"Cannot get timestamps from {filename}")
            return None
        return cls(provider, dataset, event_date, created_at)

    def __init__(self, provider: Provider, dataset: DataSet, event_date: datetime.date, created_at: datetime.datetime, ext: str = "html"):
        if dataset.name not in [
            ds.name for ds in
            provider.datasets
        ]:
            raise Exception(f"Got invalid dataset {dataset.name} for provider {provider.name}")

        self.provider = provider
        self.dataset = dataset
        self.event_date = event_date
        self.created_at = created_at
        self.ext = ext

    @property
    def resource_name(self):
        return self.provider.name + "_" + self.dataset.name
    
    @property
    def name(self):
        return (
            self.provider.name + "_" + self.dataset.name + "_" +
            self.event_date.strftime("%Y%m%d") +
            self.created_at.strftime("_%Y%m%d%H%M%S") +
            "." + self.ext
        )
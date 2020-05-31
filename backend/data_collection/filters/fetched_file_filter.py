import os
import regex
import logging
import datetime
from typing import List

from consts import local_data_path
from models import DataSet, FetchedFile, Provider


class FetchedFileFilter:
    def filter(self, fetched_files: List[FetchedFile], provider: Provider, datasets: List[DataSet], start_date: datetime.date = None) -> List[FetchedFile]:
        return [
            ff for ff in fetched_files
            if ff.provider.name == provider.name 
            and ff.dataset.name in [d.name for d in datasets]
            and (
                (not start_date) or (ff.event_date >= start_date)
            )
        ]
    
    def filter_latest_version_only(self, fetched_files: List[FetchedFile], provider: Provider, datasets: List[DataSet], start_date: datetime.date = None) -> List[FetchedFile]:
        return sorted(self._latest_filter(
            self.filter(
                fetched_files,
                provider,
                datasets,
                start_date=start_date
        )), key=lambda ff: ff.event_date)

    def _latest_filter(self, fetched_files: List[FetchedFile]) -> List[FetchedFile]:
        names = set([ff.resource_name for ff in fetched_files])
        latest = {}
        for ff in fetched_files:
            if ff.name not in latest or latest[ff.resource_name].created_at < ff.created_at:
                latest[ff.resource_name] = ff
        return list(latest.values())

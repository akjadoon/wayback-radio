
import requests
import regex
import datetime
import logging
import os
import datetime
from typing import List

from bs4 import BeautifulSoup

from .fetcher import Fetcher
from models import DataSet, FetchedFile, BillboardProvider
from fileio import fetched_file_io


class BillboardFetcher(Fetcher):
    def __init__(self):
        self.provider = BillboardProvider()

    def fetch(self, dataset_names: List[str] = None, start_date=None):
        datasets = self.provider.datasets
        if dataset_names:
            datasets = [
                d for d in self.provider.datasets
                if d.name in dataset_names
            ]

        if not datasets:
            logging.error(f"Cannot fetch {dataset_names} for billboard")

        for d in datasets:
            dates = self.fetch_chart(d, fetched_file_io.write, start_date=start_date)

    def next_chart_date(self, soup: BeautifulSoup):
        next_week_span_regex = regex.compile("\s*Next Week\s*")
        date_dropdown = soup.find(class_="dropdown__date-selector-inner")
        link_child = date_dropdown.find(string=next_week_span_regex)
        if not link_child or 'href' not in link_child.parent.attrs:
            return None
        return datetime.datetime.strptime(
        link_child.parent['href'].split("/")[-1], "%Y-%m-%d"
        )

    def fetch_chart(self, dataset: DataSet, html_parser_fn, start_date=None):
        dates = []
        cur = dataset.earliest_date
        if start_date:
            cur = start_date
        last_date_reached = False
        while cur:
            dates.append(cur)
            url = f"{dataset.base_url}/{cur.strftime('%Y-%m-%d')}" 
            headers = {
                "cookie": self.provider.cookie_header
            }
            res = requests.get(
                url,
                headers=headers
            )
            fetched_file = FetchedFile(self.provider, dataset, cur, datetime.datetime.now())
            html_parser_fn(fetched_file, res.content)
            soup = BeautifulSoup(res.content, "lxml")
            cur = self.next_chart_date(soup)
        return dates

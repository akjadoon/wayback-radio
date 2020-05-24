
import requests
import regex
import datetime
import logging
import os
import datetime
from typing import List
from bs4 import BeautifulSoup
from .fetcher import Fetcher
from dataset import Dataset
from provider import BillboardProvider
from consts import local_data_path


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
            dates = self.fetch_chart(d, self.save_as_html, start_date=start_date)

    def next_chart_date(self, soup: BeautifulSoup):
        next_week_span_regex = regex.compile("\s*Next Week\s*")
        date_dropdown = soup.find(class_="dropdown__date-selector-inner")
        link_child = date_dropdown.find(string=next_week_span_regex)
        if not link_child or 'href' not in link_child.parent.attrs:
            return None
        return datetime.datetime.strptime(
        link_child.parent['href'].split("/")[-1], "%Y-%m-%d"
        )

    def fetch_chart(self, dataset: Dataset, html_parser_fn, start_date=None):
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
            html_parser_fn(res.content, dataset, cur)
            soup = BeautifulSoup(res.content, "lxml")
            cur = self.next_chart_date(soup)
        return dates

    def save_as_html(self, content: bytes, dataset: Dataset, chart_date: datetime.date):
        if " " in dataset.name:
            raise Exception("chart_name must not contain spaces")
        chart_file_name = (
            self.provider.name + "_" + dataset.name + "_" +
            chart_date.strftime("%Y%m%d") + datetime.datetime.now().strftime("_%Y%m%d") + ".html"
        )
        with open(
                os.path.join(
                    local_data_path,
                    chart_file_name
                ),
            "wb") as htmlFile:
            try:
                htmlFile.write(content)
            except Exception as e:
                logging.error(f"Could not write {chart_file_name}", e)
        logging.info(f"Successfully fetched {chart_file_name}")

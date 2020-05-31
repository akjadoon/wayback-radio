import datetime
import os
import json
import logging
import regex
from typing import List

from bs4 import BeautifulSoup

from consts import local_data_path
from filters import fetched_file_filter
from fileio import fetched_file_io
from models import BillboardChart, BillboardChartItem, BillboardProvider, FetchedFile

from .parser import Parser

class BillboardParser(Parser):
    def __init__(self):
        self.provider = BillboardProvider()

    def parse(self, fetched_files: List[FetchedFile]):
        if not all([ff.provider.name == self.provider.name for ff in fetched_files]):
            logging.error("Got invalid provider for BillboardParser")
            return None

        parsed = []
        for ff in fetched_files:
            obj = self.parse_file(fetched_file_io.read(ff), ff.event_date)
            if obj:
                parsed.append(obj)
        return parsed

    def parse_chart_item(self, soup: BeautifulSoup) -> List[BillboardChartItem]:
        listItem = soup.find('div', class_="chart-list-item__first-row")
        artist = listItem.find('div', class_="chart-list-item__artist").get_text().strip()
        song = listItem.find('div', class_="chart-list-item__title").get_text().strip()
        rank = listItem.find('div', class_="chart-list-item__rank").get_text().strip()

        listItem = soup.find('div', class_="chart-list-item__stats")
        weeks_on_chart = listItem.find('div', class_="chart-list-item__weeks-on-chart").get_text().strip()

        last_week = listItem.find('div', class_="chart-list-item__last-week").get_text().strip()

        two_weeks_ago = None
        song_writers = None
        producers = None
        awards = None
        imprint_promotion_label = None
        riaa = None
        try:
            riaa = soup.find('div', class_="chart-list-item__riaa-heading").get_text().strip()
        except:
            pass

        try:
            two_weeks_ago = listItem.find_all('div', class_="chart-list-item__last-week")[1].get_text().strip()
        except:
            logging.error("Could not find two_weeks_ago field")

        weeks_on_chart = listItem.find('div', class_="chart-list-item__weeks-on-chart").get_text().strip()
        peak_position = listItem.find('div', class_="chart-list-item__weeks-at-one").get_text().strip()

        listItem = soup.find('div', class_="chart-list-item__people_data")
        rxs = {
            "song_writers": r"(?:Songwriter\(s\):)([\s\S]*)",
            "producers": r"(?:Producer\(s\):)([\s\S]*)",
            "imprint_promotion_label": r"(?:Imprint\/Promotion Label:)([\s\S]*)"
        }
        try:
            for cell in listItem.find_all('div', class_="chart-list-item__people_data-cell"):
                song_writer_match = regex.search( r"(?:Songwriter\(s\):)([\s\S]*)", cell.get_text())
                producers_match = regex.search(rxs["producers"], cell.get_text())
                imprint_promotion_label_match = regex.search(rxs["imprint_promotion_label"], cell.get_text())

                if song_writer_match:
                    song_writers = [s.strip() for s in song_writer_match[1].split(",")]
                if  producers_match:
                    producers = [s.strip() for s in producers_match[1].split(",")]
                if  imprint_promotion_label_match:
                    imprint_promotion_label = imprint_promotion_label_match[1].strip()
        except Exception as e:
            logging.error("Could not find field", e)

        return BillboardChartItem(
            artist,
            song,
            int(rank),
            last_week,
            two_weeks_ago,
            peak_position,
            weeks_on_chart,
            riaa, 
            song_writers,
            producers,
            imprint_promotion_label
        )

    def parse_file(self, content: bytes, event_date: datetime.date) -> BillboardChart:
        soup = BeautifulSoup(content, "lxml")
        chartItems = [
            self.parse_chart_item(chartItem)
            for i, chartItem in 
            enumerate(soup.find_all('div', class_="chart-list-item"))

        ]
        return BillboardChart(chartItems, event_date)

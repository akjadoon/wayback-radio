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

        peak_position, weeks_on_chart, last_week, two_weeks_ago = self.parse_stats(soup)

        song_writers, producers, imprint_promotion_label = self.parse_people_data(soup)

        riaa = None
        try:
            riaa = soup.find('div', class_="chart-list-item__riaa-heading").get_text().strip()
        except:
            pass

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
    
    def parse_stats(self, chart_list_item: BeautifulSoup):
        stats = chart_list_item.find('div', class_="chart-list-item__stats")
        if not stats:
            return None, None, None, None

        weeks_on_chart = stats.find('div', class_="chart-list-item__weeks-on-chart").get_text().strip()
        peak_position = stats.find('div', class_="chart-list-item__weeks-at-one").get_text().strip()
        last_week = stats.find('div', class_="chart-list-item__last-week").get_text().strip()
        try:
            two_weeks_ago = stats.find_all('div', class_="chart-list-item__last-week")[1].get_text().strip()
        except:
            logging.error("Could not find two_weeks_ago field")
        return  peak_position, weeks_on_chart, last_week, two_weeks_ago 

    def parse_people_data(self, chart_list_item: BeautifulSoup):
        people_data = chart_list_item.find('div', class_="chart-list-item__people_data")
        if not people_data:
            return None, None, None
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
                return song_writers, producers, imprint_promotion_label
        except Exception as e:
            pass
        return None, None, None

    def correctDuplicateRanks(self, chart_items: List[BillboardChartItem]) -> List[BillboardChartItem]:
        for i in range(len(chart_items) - 1):
            if chart_items[i].rank == chart_items[i + 1].rank:
                chart_items[i + 1].rank += 1
        return chart_items
    
    def parse_file(self, content: bytes, event_date: datetime.date) -> BillboardChart:
        soup = BeautifulSoup(content, "lxml")
        chartItems = self.correctDuplicateRanks([
            self.parse_chart_item(chartItem)
            for i, chartItem in 
            enumerate(soup.find_all('div', class_="chart-list-item"))
        ])
        return BillboardChart(chartItems, event_date)

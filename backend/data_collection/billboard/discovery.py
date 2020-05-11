
import requests
import regex
import datetime
import logging
import os

from bs4 import BeautifulSoup

from consts import billboard_cookie_header, billboard_hot_100_base_url, billboard_hot_100_earliest_date

def next_chart_date(soup: BeautifulSoup):
    next_week_span_regex = regex.compile("\s*Next Week\s*")
    date_dropdown = soup.find(class_="dropdown__date-selector-inner")
    link_child = date_dropdown.find(string=next_week_span_regex)
    if not link_child or 'href' not in link_child.parent.attrs:
        return None
    return datetime.datetime.strptime(
       link_child.parent['href'].split("/")[-1], "%Y-%m-%d"
    )

def fetch_chart(base_url, start_date, html_parser_fn):
    dates = []
    cur = start_date
    last_date_reached = False
    while cur:
        dates.append(cur)
        url = f"{base_url}/{cur.strftime('%Y-%m-%d')}" 
        headers = {
            "cookie": billboard_cookie_header
        }
        res = requests.get(
            url,
            headers=headers
        )
        html_parser_fn(res.content, "billboard_hot_100", cur)
        soup = BeautifulSoup(res.content, "lxml")
        cur = next_chart_date(soup)
    return dates


def fetch_billboard_page(base_url, path) -> bytes:
    url = f"{base_url}{path}"
    headers = {
        "cookie": billboard_cookie_header
    }
    res = requests.get(
        url,
        headers=headers
    )
    return res.content

def parse_billboard_hot_100_page(content: bytes):
    soup = BeautifulSoup(content, "lxml")
    listItem = soup.find('div', class_="chart-list-item__first-row")
    artist = listItem.find('div', class_="chart-list-item__artist").get_text().strip()
    song = listItem.find('div', class_="chart-list-item__title").get_text().strip()
    rank = listItem.find('div', class_="chart-list-item__rank").get_text().strip()
    return {
        "Artist": artist,
        "Song": song,
        "Rank": rank
    }

def save_as_html(content: bytes, chart_name, chart_date: datetime.date):
    if " " in chart_name:
        raise Exception("chart_name must not contain spaces")
    chart_file_name = chart_name + chart_date.strftime("_%Y%m%d") + datetime.datetime.now().strftime("_%Y%m%d") + ".html"
    
    with open(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "data",
                chart_file_name
            ),
        "wb") as htmlFile:
        try:
            htmlFile.write(content)
        except Exception as e:
            logging.error(f"Could not write {chart_file_name}", e)
    logging.info(f"Successfully fetched {chart_file_name}")

if __name__ == "__main__":
    url = "/2020-05-02"
    start_date = datetime.date(2020, 2, 8)
    dates = fetch_chart(billboard_hot_100_base_url, start_date, save_as_html)
    print(dates)
import os
import datetime
import argparse
import json
import logging

from factory import factory
from models import FetchedFile
from filters import fetched_file_filter
from fileio import fetched_file_io

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


argparser = argparse.ArgumentParser(description='Start a data collection task')
argparser.add_argument('-s', '--start-date', type=lambda s: datetime.datetime.strptime(s, "%d,%m,%Y").date(), required=False)
argparser.add_argument('task', type=str, choices=['fetch', 'load'])
argparser.add_argument('provider', type=str)
argparser.add_argument('dataset', type=str)


def main():
    args = argparser.parse_args()
    task, provider_name, dataset_name, start_date = args.task, args.provider, args.dataset, args.start_date
    provider = factory.get_provider_cls(provider_name)()
    if not provider:
        logging.error(f"No provider {provider} found")
        return
    dataset = provider.get_dataset(dataset_name)
    if not dataset:
        logging.error(f"No dataset {dataset_name} found for provider {provider.name}")
        return

    if args.task == "fetch":
        fetcher = factory.get_fetcher_cls(provider_name)()
        fetcher.fetch(dataset_names=[dataset_name], start_date=start_date)
    elif args.task == "load":
        fetched_files = fetched_file_filter.filter_latest_version_only(
            fetched_file_io.all(),
            provider,
            [dataset],
            start_date=start_date
        )
        parser = factory.get_parser_cls(provider_name)()
        parsed = parser.parse(fetched_files)
        print(parsed)
        inserter = factory.get_inserter_cls(provider_name)()
        inserter.bulk_insert([
            (provider, dataset, p)
            for p in parsed
        ])

if __name__ == "__main__":
    main()
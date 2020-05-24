import os
import datetime
import argparse
import json
import logging

from factory import factory

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


argparser = argparse.ArgumentParser(description='Start a data collection task')
argparser.add_argument('-s', '--start-date', type=lambda s: datetime.datetime.strptime(s, "%d,%m,%Y").date(), required=False)
argparser.add_argument('task', type=str, choices=['fetch', 'load'])
argparser.add_argument('provider', type=str)
argparser.add_argument('dataset', type=str)


def main():
    args = argparser.parse_args()
    task, provider_name, dataset_name, start_date = args.task, args.provider, args.dataset, args.start_date
    print(start_date)
    provider = factory.get_provider_cls(provider_name)()
    if not provider:
        logging.error(f"No dataset {dataset} found for provider {name}")
        return

    if args.task == "fetch":
        fetcher = factory.get_fetcher_cls(provider_name)()
        fetcher.fetch(dataset_names=[dataset_name], start_date=start_date)
    elif args.task == "load":
        parser = factory.get_parser_cls(provider_name)()
        parsed = parser.load(datasets=[dataset_name], start_date=start_date)
        inserter = factory.get_inserter_cls(provider_name)()
        inserter.insert(dataset, parsed)

if __name__ == "__main__":
    main()
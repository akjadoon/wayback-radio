import datetime
import logging
from typing import Any, List, Tuple

from models import Provider, DataSet
from db import db 

class ResourceInserter:
    def insert(self, provider: Provider, dataset: DataSet, data) -> bool:
        result = None
        try:
            result = db.datasets.insert_one(
                self.as_insertable(provider, dataset, data)
            )
            logging.info(f"Successfully inserted {dataset.name} for provider {provider.name} for {data.event_date}")
        except Exception as e:
            logging.error(f"Failed to insert dataset {dataset.name} for provider {provider.name} for {data.event_date}", e)
        return result  
    
    def bulk_insert(self, resources: List[Tuple[Provider, DataSet, Any]]):
        result = None
        try:
            result = db.datasets.insert_many(
                [
                    self.as_insertable(provider, dataset, data)
                    for provider, dataset, data in resources
                ]
            )
            logging.info("Successfully bulk inserted charts")
        except Exception as e:
            logging.error(f"Failed to bulk insert charts", e)
        return result

    def as_insertable(self, provider: Provider, dataset: DataSet, data):
        return {   
            "created_at": datetime.datetime.now(),
            "provider": provider.serialize(),
            "dataset": dataset.serialize(),
            "data": data.serialize()
        }
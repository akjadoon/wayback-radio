import datetime

from typing import List

from models import BillboardChartItem

class BillboardChart:
    def __init__(self, chart_items: List[BillboardChartItem], event_date: datetime.date ):
        if len(set([item.rank for item in chart_items])) < len(chart_items):
            raise Exception("Cannot create BillboardChart, ranks of chart_items not unique")
    
        self.items = {
            item.rank: item
            for item in chart_items
        }
        self.event_date = event_date
    
    def serialize(self):
        return {
            "event_date": datetime.datetime(self.event_date.year, self.event_date.month, self.event_date.day),
            "items": {
                str(rank): item.serialize() 
                for rank, item in self.items.items()
            }
        }
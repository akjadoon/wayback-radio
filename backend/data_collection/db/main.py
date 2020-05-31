import os
from pymongo import MongoClient


user = os.getenv("WAYBACK_RADIO_DB_USER")
password = os.getenv("WAYBACK_RADIO_DB_PASSWORD")
cluster = os.getenv("WAYBACK_RADIO_DB_CLUSTER")
client = MongoClient(f"mongodb+srv://{user}:{password}@{cluster}.azure.mongodb.net/test?retryWrites=true&w=majority")
db = client.wayback_radio_db

if __name__ == "__main__":
    print([doc for doc in db.charts.find({})])
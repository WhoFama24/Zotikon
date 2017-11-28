import requests
from time import sleep
from random import randrange
from datetime import datetime, timezone, timedelta

DBNAME = "ZotikonEventTSDB"
DBUSER = "zotikon_writer"
DBUSER_PWD = "write"
DB_URL = "http://192.168.7.2/influxdb/write"
DB_EVENT_NAME = "Event_DatabaseUnitTest"


# Run Performance Test
if __name__ == "__main__":
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    for i in range(150):
        now = datetime.now(timezone.utc)
        data_time = str((now - epoch) // timedelta(microseconds=1))
        body = DB_EVENT_NAME + ",playerId='1' heartRate=" + randrange(35,200) + ",temperature=" + randrange(32,42) + " " + data_time
        requests.post(DB_URL, data=body, params={"db": DBNAME}, headers={"Content-Type": "text/plain"})
        sleep(1/151)        # sleep for 1/151 seconds

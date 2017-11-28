import requests
from time import sleep
from random import randrange
from datetime import datetime, timezone, timedelta

DB_NAME = "ZotikonEventTSDB"
DB_URL = "http://192.168.7.2/influxdb/write"
DB_EVENT_NAME = "Event_DatabaseUnitTest"


# Run Performance Test
if __name__ == "__main__":
    print("\n\nBeginning Database Performance Test")
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    start_time = datetime.now(timezone.utc)
    for i in range(150):
        now = datetime.now(timezone.utc)
        data_time = str((now - epoch) // timedelta(microseconds=1))
        body = DB_EVENT_NAME + ",playerId='1' heartRate=" + randrange(35,200) + ",temperature=" + randrange(32,42) + " " + data_time
        requests.post(DB_URL, data=body, params={"db": DB_NAME}, headers={"Content-Type": "text/plain"})
        print("Wrote data point %u at time " + str(now))
        sleep(1/200)        # sleep for 1/200 seconds
    end_time = datetime.now(timezone.utc)
    test_duration = (end_time - start_time) // timedelta(microseconds=1)

    print("\nDatabase Performance Test Complete")
    print("------------------");
    print("Elapsed Time: %u seconds, %u microseconds", (test_duraction // 1000000), test_duration)

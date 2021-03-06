import json
from datetime import datetime

from cabin.utils.files import *
from cabin.utils.time import *
from dateutil import tz
from flume.QueueDailySummary import queue_daily_summary as qds

SAMPLES_PATH = "tests/QueueDailySummary/samples/"


def test_queue_daily_summary():
    timer_json = load_text(SAMPLES_PATH + "timer.json")
    devices_json = load_text(SAMPLES_PATH + "devices.json")
    nzdt = tz.gettz("Pacific/Auckland")
    expected_start = as_utc(start_of_day(datetime(2020, 10, 19, tzinfo=nzdt)))
    expected_end = as_utc(start_of_day(datetime.now(tz=nzdt)))

    requests = json.loads(qds.main(timer_json, devices_json))
    devices = json.loads(devices_json)
    for i in range(len(requests)):
        req = requests[i]
        assert req["timespan"] == "DAILY"
        assert fromtimestamp(req["startTimestamp"]) == expected_start
        assert fromtimestamp(req["endTimestamp"]) == expected_end
        d = devices[i]
        assert req["device"] == d
        assert req["readPartition"] == f"{d['customerID']}_{d['deviceID']}"
        assert req["writePartition"] == f"{d['customerID']}_{d['deviceID']}_DAILY"

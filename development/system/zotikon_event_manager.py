import requests


class ZotikonEvent:
    """
    This class is used to handle all actions related to a specific event in the Zotikon system.

    Keyword Arguments:
        event_name -- (REQUIRED) -- the name of the event
    """

    influxdb_web_api_query = 'http://localhost:8086/query'
    influxdb_web_api_write = 'http://localhost:8086/write'

    def __init__(self, event_name='DEFAULT_NAME'):
        self.event_name = event_name


    def start_event(self):
        pass

    def end_event(self):
        pass

    def add_measurement(self, player_id, heart_rate_data, temperature_data, timestamp):
        pass

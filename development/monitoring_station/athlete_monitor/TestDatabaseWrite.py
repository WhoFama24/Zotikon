# -*- coding: utf-8 -*-
"""Tutorial on using the InfluxDB client."""

import argparse

from influxdb import InfluxDBClient


def main(host='192.168.7.2', port=8086):
    """Instantiate a connection to the InfluxDB."""
    user = 'debian'
    password = 'temppwd'
    dbname = 'ZotikonEventTSDB'
    dbuser = 'zotikon_writer'
    dbuser_password = 'write'
    json_body = [
        {
            "measurement": "Event_002",
            "tags": {
                "playerId": "1",
            },
            "fields": {
                "heartRate": 50,
                "temperature": 21,
            }
        }
    ]

    client = InfluxDBClient(host, port, user, password, dbname)

    print "Switch user: " + dbuser
    client.switch_user(dbuser, dbuser_password)

    print "Write points: {0}".format(json_body)
    client.write_points(json_body)


def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(
        description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False,
                        default='localhost',
                        help='hostname of InfluxDB http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port of InfluxDB http API')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(host=args.host, port=args.port)

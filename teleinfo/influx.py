from abc import ABC, abstractmethod
import datetime
import logging
import os
import influxdb_client

class TMDB(ABC):

    @abstractmethod
    def push(self,measures):
        pass

class Influx(TMDB):
    def __init__(self,url,org) -> None:
        token = os.environ.get("INFLUXDB_TOKEN",None)
        url = os.environ.get("INFLUXDB_URL",url)
        org = os.environ.get("INFLUXDB_ORG",org)
        self.client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
        self.bucket="teleinfo"
        self.write_api = self.client.write_api(write_options=influxdb_client.client.write_api.SYNCHRONOUS)

    def push(self, measures):
        points = create_points(measures=measures)
        if len(points):
            self.write_api.write(bucket=self.bucket, record=points)



def create_points(measures):
    points = []

    if "timestamp" not in measures:
        logging.warning("exclude measure, missing timestamp")
        return points

    timestamp = measures["timestamp"]
    del measures["timestamp"]


    for measure, value in measures.items():
        point = (
            influxdb_client.Point(measure)
            .tag("host", "raspberry")
            .tag("region", "linky")
            .field("value", value)
            .time(timestamp,write_precision=influxdb_client.WritePrecision.S)
        )
        
        points.append(point)

    return points

import struct
import time
import socketserver
import math
import requests

import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

influxdb_org = "HA5KFU"
influxdb_url = "REDACTED"
influxdb_token = 'REDACTED'
influxdb_bucket = "mosogep"
write_client = influxdb_client.InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org)
write_api = write_client.write_api(write_options=SYNCHRONOUS)


class MosogepDataSaver(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0]
        address = self.client_address[0]
        floor_num = int(address.split('.')[-1])  # last octett of IP is the level number
        timestamp = time.time()
        if len(data) >= 8:
            drier_power, wm_power = struct.unpack('>HH', data[4:8])
#            print(f"{timestamp},{floor_num},{drier_power},{wm_power}")
            point = (
              Point("meres")
              .tag("level", str(floor_num))
              .field("wm_power", wm_power)
              .field("drier_power", drier_power)
            )
            write_api.write(bucket=influxdb_bucket, org=influxdb_org, record=point)


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 1234
    with socketserver.UDPServer((HOST, PORT), MosogepDataSaver) as server:
        server.serve_forever()

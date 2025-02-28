import time
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

influxdb_org = "statusch"
influxdb_url = 'http://127.0.0.1:8086'
influxdb_token = 
influxdb_bucket = "statusch"
write_client = InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org)
write_api = write_client.write_api(write_options=SYNCHRONOUS)



if __name__ == "__main__":
    
    while True:
        time.sleep(1)
        for floor_num in (1,2,3,4):
            # toggle them on-off every 90 seconds
            power = 0 if int(time.time()) % 180 < 90 else 1000
            point = (
                Point("meres")
                .tag("level", str(floor_num))
                .field("wm_power", float(power))
                .field("drier_power", float(power))
            )
            write_api.write(bucket=influxdb_bucket, org=influxdb_org, record=point)



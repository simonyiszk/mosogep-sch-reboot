import struct
import time
import socketserver
import math
import requests
import pickle
from collections import defaultdict

# record data for this many seconds
RECORD_FOR = 60
CURRENT_FLOOR = 0
start_time = 10**10
records = defaultdict(list)

class MosogepDataSaver(socketserver.BaseRequestHandler):
    def update_data(self, floor, wm_power, drier_power, packet, timestamp):
        global start_time
        start_time = min(start_time, timestamp)
        records[floor].append((timestamp, packet))

    def print_data(self):
        print(f"Data collected for {RECORD_FOR} seconds on floor {CURRENT_FLOOR}")
        for floor,vals in records.items():
            print(f"\t{floor}\t-{len(vals)} packets")
        pickle.dump(records, open(f"floor-{CURRENT_FLOOR}.pickle", "wb"))
        exit()

    def handle(self):
        data = self.request[0]
        address = self.client_address[0]
        floor_num = int(address.split('.')[-1])  # last octett of IP is the level number
        timestamp = time.time()
        #print(data)
        if len(data) >= 8:
            drier_power, wm_power = struct.unpack('>HH', data[4:8])
            self.update_data(floor_num, wm_power, drier_power, data, timestamp)
        if timestamp - start_time > RECORD_FOR:
            self.print_data()
            exit()


if __name__ == "__main__":
    HOST, PORT = "", 1234
    CURRENT_FLOOR = int(input("Enter current floor: "))
    print(f"Collecting data for {RECORD_FOR} seconds at floor {CURRENT_FLOOR}")
    with socketserver.UDPServer((HOST, PORT), MosogepDataSaver) as server:
        server.serve_forever()

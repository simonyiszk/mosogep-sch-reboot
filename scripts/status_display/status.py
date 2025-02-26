import struct
import time
import socketserver
import math
import requests

import mosogep_data

last_updated = 0
#ips = set()
values = {}
class MosogepDataSaver(socketserver.BaseRequestHandler):
    def update_data(self, floor, wm_power, drier_power):
        global last_updated
        _, old_cnt, old_wm, old_drier = values.get(floor, ("", 0, 0, 0))
        values[floor] = ("\033[42m",old_cnt + 1, max(old_wm, wm_power), max(old_drier, drier_power))
        if time.time() - last_updated > 3:
            last_updated = time.time()
            self.print_data()
            #ips = set()
            values.clear()
    def print_data(self):
        print("\x1b[2J\033[H")
        #print(" ".join(f"{seen.get(i,0):2}" for i in range(0,32)))
        #print(" ".join((f"\033[42m{i:2}\033[49m" if i in seen else f"\033[41m{i:2}\033[49m") for i in range(0,32)))

        for i in range(0, 10):
            j = i + 10

            col1_default = "\033[41m" if mosogep_data.floor_has_device(i) else "\033[100m"
            col2_default = "\033[41m" if mosogep_data.floor_has_device(j) else "\033[100m"

            col1, cnt1, wm1, drier1 = values.get(i, (col1_default,0,0,0))
            col2, cnt2, wm2, drier2 = values.get(j, (col2_default,0,0,0))

            print(f"{col1}{i:2}\033[49m {cnt1:2} {wm1:5} {drier1:5}         {col2}{j:2}\033[49m {cnt2:2} {wm2:5} {drier2:5}")
        #print(seen)
        #print(list(sorted(list(ips))))
    def handle(self):
        data = self.request[0]
        address = self.client_address[0]
        floor_num = int(address.split('.')[-1])  # last octett of IP is the level number
        timestamp = time.time()
        if len(data) >= 8:
            drier_power, wm_power = struct.unpack('>HH', data[4:8])
            self.update_data(floor_num, wm_power, drier_power)
            #ips.add(address)
        #if not b'Mosogep.sch' in data:
        #print(data)
if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 1234
    with socketserver.UDPServer((HOST, PORT), MosogepDataSaver) as server:
        server.serve_forever()

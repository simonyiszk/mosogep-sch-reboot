import struct
import time
import socketserver
import math


class MosogepDataSaver(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0]
        address = self.client_address[0]
        floor_num = int(address.split('.')[-1])  # last octett of IP is the level number
        timestamp = time.time()
        if len(data) >= 8:
            drier_power, wm_power = struct.unpack('>HH', data[4:8])
            if floor_num == 6:
	            print(f"{timestamp},{floor_num},{drier_power},{wm_power}")


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 1234
    with socketserver.UDPServer((HOST, PORT), MosogepDataSaver) as server:
        server.serve_forever()
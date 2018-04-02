import requests
import datetime

url = "http://10.255.87.100:8000/api/v1/UDPTrafficStat/"
post_args = {"data_list": [
    {"app_id": 2, "byte_sent": 5001, "packets_sent": 100, "packets_receive": 100,
     "drop_packets": 0, "avg_latency": 0.034, "pkt_time": str(datetime.datetime.now())},
    {"app_id": 2, "byte_sent": 5002, "packets_sent": 100, "packets_receive": 100,
     "drop_packets": 0, "avg_latency": 0.034, "pkt_time": str(datetime.datetime.now())},
    {"app_id": 2, "byte_sent": 5003, "packets_sent": 100, "packets_receive": 100,
     "drop_packets": 0, "avg_latency": 0.034, "pkt_time": str(datetime.datetime.now())},
]}
# post_args = [
#     (2, 5001, 100, 100, 0, 0.034, str(datetime.datetime.now())),
#     (2, 5001, 100, 100, 0, 0.034, str(datetime.datetime.now())),
#     (2, 5001, 100, 100, 0, 0.034, str(datetime.datetime.now())),
# ]

# post_args = {"app_id": 2, "byte_sent": 5001, "packets_sent": 100, "packets_receive": 100,
#      "drop_packets": 0, "avg_latency": 0.034, "pkt_time": str(datetime.datetime.now())}

r = requests.post(url,
                  json=post_args)

#
# r = requests.get(url)

print(r.status_code)
print(r.text)

# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
#
#
# import datetime
#
# print(datetime.datetime.now())
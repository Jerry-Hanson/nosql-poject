from utils.ConfigFileReader import ConfigFileReader
from socket import *
import matplotlib.pyplot as plt
import json
import numpy as np

config = ConfigFileReader("config/server_config.yaml")
address = config.info['server_address']
port = config.info['server_port']
buffersize = 1024 * 15

s = socket(AF_INET, SOCK_STREAM)
s.bind((address, port))
# 设置最大连接数
s.listen(config.info['max_connection'])


clientsock, clientaddress = s.accept()
msg = ""
while True:
    buf = clientsock.recv(buffersize).decode('utf-8')
    if buf.endswith("\0"):
        msg += buf[:-1]
        break
    msg += buf

img_array = np.array(json.loads(msg))
plt.imshow(img_array)
plt.axis(False)
plt.show()
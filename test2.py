from socket import *
from utils.ConfigFileReader import ConfigFileReader
import cv2
import numpy as np
import json

img_array = cv2.imread("./images/chat.png")
msg = json.dumps(img_array.tolist())

config = ConfigFileReader('config/client_config.yaml')
address = config.info['server_address']
port = config.info['server_port']
s = socket(AF_INET, SOCK_STREAM)
s.connect((address, port))

msg = msg + "\0"
s.send(msg.encode('utf-8'))
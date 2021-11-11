from socket import *
import yaml

# read config file
config_file_path = "./config.yaml"
with open(config_file_path, 'r', encoding = 'utf-8') as fp:
    config_data = yaml.load(fp, yaml.FullLoader)

address = config_data['address']
port = config_data['port']
bufferSize = config_data['buffersize']
maxConnection = config_data['max_connection']

# create socket
s = socket(AF_INET, SOCK_STREAM)
s.bind((address, port))
s.listen(maxConnection)
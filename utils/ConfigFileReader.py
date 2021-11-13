import yaml



class ConfigFileReader:
    def __init__(self, filePath):
        self.filePath = filePath
        with open(filePath, "r") as fp:
            self.info = yaml.load(fp, yaml.FullLoader)
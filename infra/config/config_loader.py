import configparser


class Config:
    def __init__(self):
        self.cfp = configparser.ConfigParser()
        self.has_read = False

    def read(self, file):
        self.cfp.read(file)
        self.has_read = True

    def get(self, section, key):
        if self.has_read is False:
            raise Exception("config used before read file")
        return self.cfp.get(section, key)


def config_provider(file="config.ini"):
    config = Config()
    config.read(file)
    return config

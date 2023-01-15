from infra.config.config_loader import config_provider
class Container:
    def __init__(self):
        self.config = config_provider()

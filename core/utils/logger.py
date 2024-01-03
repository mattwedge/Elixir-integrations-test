import logging


class Logger:
    """A custom logging implementation

    TODO: figure out why the `print` statements are needed
    """

    def __init__(self, name):
        self.name = name
        self.logger = logging.getLogger(name)

    def debug(self, msg):
        self.logger.debug(msg)
        print(msg)

    def info(self, msg):
        self.logger.info(msg)
        print(msg)

    def warning(self, msg):
        self.logger.warning(msg)
        print(msg)

    def error(self, msg, post_to_slack=False):
        self.logger.error(msg)
        print(msg)

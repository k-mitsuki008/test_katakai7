import logging


class Logger:
    def __init__(self, name: any = __name__) -> None:
        self.logger: any = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

    def debug(self, msg: any) -> None:
        self.logger.debug(msg)

    def info(self, msg: any) -> None:
        self.logger.info(msg)

    def warning(self, msg: any) -> None:
        self.logger.warning(msg)

    def error(self, msg: any) -> None:
        self.logger.error(msg)

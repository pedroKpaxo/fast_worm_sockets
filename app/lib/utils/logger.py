import logging


class ColorfulFormatter(logging.Formatter):
    """
    ColorfulFormatter class for logging
    """
    COLORS = {
        'DEBUG': '\033[94m',  # Blue
        'INFO': '\033[92m',   # Green
        'WARNING': '\033[93m',  # Yellow
        'ERROR': '\033[91m',  # Red
        'CRITICAL': '\033[91m',  # Red
    }

    RESET = '\033[0m'

    def __init__(self, app_name: str):
        super().__init__()
        self.app_name = app_name

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        message = f"{color}[{self.app_name}] {record.levelname}{self.RESET}: {record.msg}"  # noqa
        return f'{message}'


def setup_logger(app_name: str):
    logger = logging.getLogger(app_name)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = ColorfulFormatter(app_name=app_name)
    ch.setFormatter(formatter)

    logger.addHandler(ch)
    return logger

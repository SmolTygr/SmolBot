"""Smolbot logging module"""
import logging
from logging import handlers
import os

# Logging Settings
# TODO: Stop being hardcoded
LOG_BACKUP_COUNT = 5
LOG_NAME = 'smolLog.log'
CONFIG_NAME = 'smolConfig.ini'
DIR_ = os.path.dirname(__file__)


def setup_logging() -> logging.Logger:

    # Setup logging
    logger = logging.getLogger('SmolBot')
    logger.setLevel(logging.DEBUG)

    # All-purpose formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Console handler
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    logger.addHandler(console)

    # File handler
    file = handlers.RotatingFileHandler(filename=os.path.join(DIR_, LOG_NAME),
                                        mode='a',
                                        encoding='UTF-8',
                                        backupCount=LOG_BACKUP_COUNT)
    file.setLevel(logging.DEBUG)
    file.setFormatter(formatter)
    logger.addHandler(file)

    return logger


#TODO: Rewrite as a wrapper function.
def log_command(ctx, logger: logging.Logger, command_name: str, *, level: int = logging.DEBUG):
    """Basic logging for when a user calls a command"""
    logger.log(level=level, msg='%s called: "%s"' %(str(ctx.author), command_name))
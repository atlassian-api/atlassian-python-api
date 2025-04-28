import logging


def get_default_logger(name):
    """Get a logger from default logging manager. If no handler
    is associated, add a default NullHandler"""

    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        # If logging is not configured in the current project, configure
        # this logger to discard all logs messages. This will  avoid
        # redirecting errors to the default 'lastResort' StreamHandler
        logger.addHandler(logging.NullHandler())
    return logger

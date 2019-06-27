import logging
from six import PY3


# Additional log methods
def logger_has_handlers(logger):
    """Since Python 2 doesn't provide Logger.hasHandlers(), we have to
    perform the lookup by ourself."""

    if PY3:
        return logger.hasHandlers()
    else:
        c = logger
        rv = False
        while c:
            if c.handlers:
                rv = True
                break
            if not c.propagate:
                break
            else:
                c = c.parent
        return rv


def get_default_logger(name):
    """Get a logger from default logging manager. If no handler
    is associated, add a default NullHandler"""

    logger = logging.getLogger(name)
    if not logger_has_handlers(logger):
        # If logging is not configured in the current project, configure
        # this logger to discard all logs messages. This will prevent
        # the 'No handlers could be found for logger XXX' error on Python 2,
        # and avoid redirecting errors to the default 'lastResort'
        # StreamHandler on Python 3
        logger.addHandler(logging.NullHandler())
    return logger

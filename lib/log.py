"""
This is a library for logging initialization
"""
import sys
import logging
import logging.handlers
import flex_env

ALL_LOGGERS = ['command', 'background', 'objects', 'globals', 'rest_client', 'api', 'Sshoperation', 'utils']

VERB_HDLR = None

def init(filename, log_level=logging.INFO):
    """
    Initialize logging.
    @Returns: Logger object
    """

    global VERB_HDLR
    fname = '/tmp/default.log'
    formatter = logging.Formatter('%(asctime)s - %(threadName)s- %(levelname)s - %(message)s')
    if filename:
        fname = filename

    if VERB_HDLR is None:
        VERB_HDLR = logging.FileHandler(fname, mode='w')
        VERB_HDLR.setFormatter(formatter)
        VERB_HDLR.setLevel(log_level)

    for log_type in ALL_LOGGERS:
        my_logger = logging.getLogger(log_type)
        my_logger.addHandler(VERB_HDLR)
        my_logger.setLevel(log_level)


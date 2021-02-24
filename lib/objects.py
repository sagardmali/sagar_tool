"""This file is initiate hyperscale objects"""

import log
import os
import sys
import logging
import flex_env
import config
import globals

class objects():

    def __init__(self):
        """
        Library to initiate objects
        """

        #initiate logging
        file_name = os.path.splitext(sys.argv[0])
        tc_name = file_name[0].split('/')[-1]
        log_name = os.path.join(config.LOG_DIR, ''.join([tc_name, '.log']))
        log.init(log_name)
        self.logging = logging.getLogger('objects')


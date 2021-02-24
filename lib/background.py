import os
import sys
import logging
import threading
from multiprocessing import Process
sys.path.append(os.path.dirname(os.path.abspath(sys.argv[0])))

logger = logging.getLogger('background')
logger.addHandler(logging.NullHandler())

class background(threading.Thread):
    '''
    This is a class to run function in background and capture output
    '''
    def __init__(self, func, func_args, func_kwargs):
        threading.Thread.__init__(self)
        self.out = None
        self.func = func
        self.func_args = func_args
        self.func_kwargs = func_kwargs

    def run(self):
        self.out = self.func(*self.func_args, **self.func_kwargs)

class background_multi(Process):
    '''
    This is a class to run function in background and capture output
    '''
    def __init__(self, func, func_args, func_kwargs):
        Process.__init__(self)
        self.out = None
        self.func = func
        self.func_args = func_args
        self.func_kwargs = func_kwargs

    def run(self):
        self.out = self.func(*self.func_args, **self.func_kwargs)

def run_in_background(func_list, wait_complete=False, multi_process=False):
    ''' Run several functions in parallel.  func_list is a list of function
    specifications.  Each specification is a dict with the following
    keys:

    - function: The function to run.  This key is required.
    - args: The arguments for the function.  This key is optional.
    - kwargs: Keyword arguments for the function.  This key is
      optional.
    return: list of function thread objects with its output stored in out
    '''
    functions = []

    for func in func_list:
        function = func.get('function', None)
        function_args = func.get('args', ())
        function_kwargs = func.get('kwargs', {})
        if multi_process:
            myfunc = background_multi(function, function_args, function_kwargs)
        else:
            myfunc = background(function, function_args, function_kwargs)
        functions.append(myfunc)
        myfunc.start()
    if wait_complete:
        for func in functions:
            func.join()
    return functions

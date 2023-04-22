import os
import psutil
import time
import warnings
import threading
import sys


class ControlsMemoryUsage(threading.Thread):
    '''
    Takes into account the consumption of RAM when the program is running.
    '''
    def __init__(self, soft_limit, hard_limit, poll_interval):
        '''
        :param str soft_limit: soft limit of memory usage. If the function exceeds this limit, warning is displayed (by default None)
        :param str hard_limit: hard memory usage limit. If the function exceeds this limit, return exception and the function ends (by default None)
        :param int or float poll_interval: time interval (in seconds) between memory usage checks
        '''
        super().__init__()
        self.soft_limit = self.human_readable_to_bytes(soft_limit)
        self.hard_limit = self.human_readable_to_bytes(hard_limit)
        self.poll_interval = poll_interval

    @staticmethod
    def get_memory_usage():
        '''
        Shows the current memory consumption of the process.

        :return: int usage memory in Bytes
        '''
        process = psutil.Process(os.getpid())
        mem_info = process.memory_info()
        return mem_info.rss

    @staticmethod
    def bytes_to_human_readable(n_bytes):
        '''
        Converts bytes to a human-readable record.

        :param int or float n_bytes: number of bytes
        :return: string format human-readable record
        '''
        symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
        prefix = {}
        for idx, s in enumerate(symbols):
            prefix[s] = 1 << (idx + 1) * 10
        for s in reversed(symbols):
            if n_bytes >= prefix[s]:
                value = float(n_bytes) / prefix[s]
                return f"{value:.2f}{s}"
        return f"{n_bytes}B"

    @staticmethod
    def human_readable_to_bytes(memory_as_str):
        '''
        Converts human-readable used memory to bytes.

        :param str memory_as_str: human-readable record of memory
        :return: float format bytes
        '''
        if isinstance(memory_as_str, type(None)):
            return None
        else:
            symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
            prefix = {}
            for idx, s in enumerate(symbols):
                prefix[s] = 1 << (idx + 1) * 10
            symb = memory_as_str[-1]
            n_bytes = prefix[symb] * float(memory_as_str[:-1])
            return int(n_bytes)

    def run(self):
        '''
        Run
        Starts the job of tracking RAM consumption.

        :return: None
        '''
        has_over_soft_limit = False
        while True:
            cur_mem_info = self.get_memory_usage()
            if self.soft_limit != None and cur_mem_info > self.soft_limit and has_over_soft_limit is False:
                readable_soft_limit = self.bytes_to_human_readable(self.soft_limit)
                readable_used_mem = self.bytes_to_human_readable(cur_mem_info)
                warnings.warn(
                        f'Uses lots of memory. Soft limit is {readable_soft_limit}; used - {readable_used_mem}.')
                has_over_soft_limit = True
            elif self.hard_limit != None and cur_mem_info > self.hard_limit:
                print('MemoryError: RAM limit exceeded', file=sys.stderr)
                os._exit(1)
            time.sleep(self.poll_interval)

def memory_limit(soft_limit, hard_limit, poll_interval):
    '''
    Decorator for tracking RAM consumption of function.

    :param str soft_limit: soft limit of memory usage. If the function exceeds this limit, warning is displayed (by default None)
    :param str hard_limit: hard memory usage limit. If the function exceeds this limit, return exception and the function ends (by default None)
    :param int or float poll_interval: time interval (in seconds) between memory usage checks
    :return: wrapped function with RAM usage
    '''
    def decorator(func):
        def inner_func():
            control_memory = ControlsMemoryUsage(soft_limit, hard_limit, poll_interval)
            control_memory.start()
            while True:
                func()
        return inner_func
    return decorator


@memory_limit(soft_limit='512M', hard_limit='1.5G', poll_interval=0.1)
def memory_increment():
    """
    Function for testing.
    """
    lst = []
    for i in range(50000000):
        if i % 500000 == 0:
            time.sleep(0.1)
        lst.append(i)
    return lst

import time
import multiprocessing


class ParallelRunning:
    '''
    Universal class for parallelization across processes.
    '''
    def __init__(self, target_func, args_container=None, kwargs_container=None, n_jobs=None):
        '''
        :param function or list target_func: objective function or functions
        :param list or None args_container: container with positional arguments numbers or tuples (by default None)
        :param list kwargs_container: container with named arguments
        :param int n_jobs: number of processes
        '''
        self._target_funcs = target_func
        self._args_container = args_container
        self._kwargs_container = kwargs_container
        self._n_jobs = n_jobs
        self._counter = 0

    def _compare_containers_len(self):
        '''
        Compares the number of named and positional arguments.
        '''
        if self._args_container is not None and self._kwargs_container is not None and len(
                self._args_container) != len(self._kwargs_container):
            raise ValueError(
                'the number of positional and named arguments differs')

    def _check_n_funcs(self):
        '''
        Checks the number of target functions. If there is only one function, then convert it to a list of length 1.
        '''
        if isinstance(self._target_funcs, list):
            self._target_funcs = self._target_funcs
        else:
            self._target_funcs = [self._target_funcs]

    def _fill_empty_args_kwargs(self):
        '''
        Containers are filled with empty values, if positional and/or named containers is None.
        '''
        if self._args_container is None and self._kwargs_container is not None:
            self._args_container = [tuple() for _ in range(len(self._kwargs_container))]
        elif self._kwargs_container is None and self._args_container is not None:
            self._kwargs_container = [dict() for _ in range(len(self._args_container))]
        elif self._args_container is None and self._kwargs_container is None:
            self._args_container = [tuple() for _ in range(self._n_jobs)]
            self._kwargs_container = [dict() for _ in range(self._n_jobs)]

    def _check_n_jobs(self):
        '''
        Adapts the number of processes to use according to the number of input arguments.
        '''
        if self._n_jobs is None:
            self._n_jobs = multiprocessing.cpu_count()
        self._fill_empty_args_kwargs()
        self._n_jobs = min(self._n_jobs, len(self._args_container))

    def _add_tasks_in_queue(self, queue):
        '''
        Adds tasks to the queue.

        :param queue: multiprocessing.Queue() object
        :return: filled queue
        '''
        counter = 0
        for arg, kwarg in zip(self._args_container, self._kwargs_container):
            queue.put((counter, arg, kwarg))
            counter += 1
        return queue

    def _process_tasks(self, func, queue, manager_dict):
        '''
        Handles tasks from the queue.

        :param function func: input target function
        :param queue: filled queue
        :param dict manager_dict: multiprocessing.Manager object
        :return: None
        '''
        while not queue.empty():
            counter, args, kwargs = queue.get()
            if not isinstance(args, tuple):
                args = (args,)
            call_func = func(*args, **kwargs)
            manager_dict[counter] = call_func
        return None

    def parallel_map(self):
        '''
        Multiprocessing run of target function/functions.

        :return: list of results
        '''
        self._compare_containers_len()
        self._check_n_funcs()
        self._check_n_jobs()
        processes = []
        results = []
        for func in self._target_funcs:
            queue = self._add_tasks_in_queue(multiprocessing.Queue())
            manager = multiprocessing.Manager()
            manager_dict = manager.dict()  # need to remember what the process is first, second, etc
            for job in range(self._n_jobs):
                process = multiprocessing.Process(target=self._process_tasks, args=(func, queue, manager_dict))
                processes.append(process)
                process.start()
            for process in processes:
                process.join()

            manager_dict = dict(sorted(manager_dict.items()))
            interm_res = []
            for key in manager_dict:
                interm_res.append(manager_dict[key])
            results.append(interm_res)
            interm_res = []
        return '\n'.join(map(str, results))

# def test_func(x=1, s=2, a=1, b=1, c=1):
#     time.sleep(s)
#     return a * x ** 2 + b * x + c

# def test_func3():
#     def inner_test_func(sleep_time):
#         time.sleep(sleep_time)
#     return ParallelRunning(inner_test_func, args_container=[1, 2, 3]).parallel_map()

# test_func3()

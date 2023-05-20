# Homework 4: Parallel programming

In this work, functions and classes were written that allow the execution of multiprocessor or multithreaded code.

### Task 1 -  ```task1.py```

The ability to train a random forest (```RandomForestClassifierCustom```) in parallel and use parallelism for predictions using multithreading. 

__Methods__ that can be executed in multiple processes:
- ```fit``` - basic method for fitting trees;
- ```predict_proba``` - predicting classes by array of features;
- ```predict``` - maximizes received predictions.

### Task 2 -  ```task2.py```

The ```memory_limit``` decorator has been implemented, which allows you to limit the memory usage of the decorated function.

The decorator takes the following arguments:
- ```soft_limit``` - soft limit of memory usage. If the function exceeds this limit, warning is displayed; 
- ```hard_limit``` - hard memory usage limit. If the function exceeds this limit, return exception and the function ends; 
- ```poll_interval``` - time interval (in seconds) between memory usage checks.

### Task 3 -  ```task3.py```

Universal class ```ParallelRunning``` for parallelization across processes.

This class has the following attributes:

- ```target_func``` - objective function or functions 
- ```args_container``` - container with positional arguments numbers or tuples; 
- ```kwargs_container``` - container with named arguments; 
- ```n_jobs``` - number of processes.

All modules required for installation are located in ```requirements.txt```.

class Args:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __rlshift__(self, function):
        return function(*self.args, **self.kwargs)

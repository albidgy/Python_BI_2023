class StrangeFloat(float):
    def __init__(self, number):
        self._number = number
        super().__init__()

    def __getattr__(self, command):
        func = command.split('_')[0][0:3]
        value = StrangeFloat(command.split('_')[1])
        if func == 'div':  # attribute for division is not __div__ but __truediv__; need to add true
            func = '__true' + func + '__'
        else:
            func = '__' + func + '__'

        bound_method = StrangeFloat.__getattribute__(self, func)
        return StrangeFloat(bound_method(value))

def swich_property(cls):
    for name_attr in dir(cls):
        if name_attr[0] != '_':
            renamed_method = f'_{cls.__name__}__' + name_attr
        elif name_attr.startswith(f'_{cls.__name__}__'):
            renamed_method = name_attr.split('__')[1]
        else:
            continue
        attr = getattr(cls, name_attr)
        setattr(cls, renamed_method, attr)
        delattr(cls, name_attr)

    return cls


@swich_property
class ExampleClass:
    def public_method(self):
        return 1

    def _protected_method(self):
        return 2

    def __private_method(self):
        return 3

    def __dunder_method__(self):
        pass

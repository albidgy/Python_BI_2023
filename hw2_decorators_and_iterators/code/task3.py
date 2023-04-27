no_change_this_dunders = ['__class__', '__dict__', '__new__', '__str__',
                          '__repr__', '__init__', '__name__', '__module__']


def get_obj_type(method):
    def inner_func(self, other=None):
        if other is None:
            if isinstance(method(self), (str, set)):
                result = type(self)(method(self))
            else:
                result = method(self)
        else:
            if isinstance(method(self, other), (str, set)):
                result = type(self)(method(self, other))
            else:
                result = method(self, other)
        return result
    return inner_func

def change_obj_type(cls):
    for name_attr in dir(cls):  # find all methods of class
        if name_attr not in no_change_this_dunders:
            attr = getattr(cls, name_attr)
            setattr(cls, name_attr, get_obj_type(attr))  # change type of return value
    return cls


@change_obj_type
class MyString(str):
    def reverse(self):
        return self[::-1]

    def make_uppercase(self):
        return "".join([chr(ord(char) - 32) if 97 <= ord(char) <= 122 else char for char in self])

    def make_lowercase(self):
        return "".join([chr(ord(char) + 32) if 65 <= ord(char) <= 90 else char for char in self])

    def capitalize_words(self):
        return " ".join([word.capitalize() for word in self.split()])


@change_obj_type
class MySet(set):
    def is_empty(self):
        return len(self) == 0

    def has_duplicates(self):
        return len(self) != len(set(self))

    def union_with(self, other):
        return self.union(other)

    def intersection_with(self, other):
        return self.intersection(other)

    def difference_with(self, other):
        return self.difference(other)

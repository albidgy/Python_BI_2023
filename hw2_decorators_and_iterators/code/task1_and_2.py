# task 1
class MyDict(dict):
    def __iter__(self):
        for key, val in self.items():
            yield key, val


# task 2
def iter_append(iterator, item):
    yield from iterator
    yield item

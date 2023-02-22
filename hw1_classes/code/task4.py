import numpy as np


matrix = []
for idx in range(0, 100, 10):
    matrix.__iadd__([list(range(idx, idx.__add__(10)))])

selected_columns_indices = list(filter(lambda x: x in range(1, 5, 2), range(matrix.__len__())))
selected_columns = map(lambda x: [x.__getitem__(col) for col in selected_columns_indices], matrix)

arr = np.array(list(selected_columns))
mask = arr.__getitem__((slice(None), 1)).__mod__(3).__eq__(0)
new_arr = arr.__getitem__(mask)

product = new_arr.__matmul__(new_arr.T)

if product.__getitem__(0).__lt__(1000).__eq__(True).__and__(product.__getitem__(2).__gt__(1000)).__contains__(True):
    print(product.mean())

import numpy as np

t1 = np.zeros([3])
t2 = np.zeros([3])
t1[:] = [12, 50, 99]
t2[:] = [70, 72, 123]

tm = np.vstack([t1, t2])
index_sort = tm.argsort(kind='mergesort', axis=0)  # stable sorting
tm = tm[index_sort]
mask_t2 = np.hstack([np.zeros(t1.size, dtype=bool), np.ones(t2.size, dtype=bool)])[index_sort]
print('t1', t1, type(t1), np.shape(t1))
print('t2', t2)
print('tm', tm)
print(mask_t2)
print('index_sort', index_sort)

t1 = np.array([12, 50, 99])
t2 = np.array([70, 72, 123])

tm = np.hstack([t1, t2])
index_sort = tm.argsort(kind='mergesort')  # stable sorting
tm = tm[index_sort]
mask_t2 = np.hstack([np.zeros(t1.size, dtype=bool), np.ones(t2.size, dtype=bool)])[index_sort]
print('t1', t1, type(t1), np.shape(t1))
print('t2', t2)
print('tm', tm)
print(mask_t2)
print('index_sort', index_sort)

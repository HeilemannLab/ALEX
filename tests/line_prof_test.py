'''######################################################################
# File Name:
# Project:
# Version:
# Creation Date:
# Created By:
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
import line_profiler
import numpy as np
import fib2
# print(fib2.fib.__doc__)


# @profile
def slow(N=1000000):
    total = 0
    for i in range(N):
        total += i
    return total


# @profile
def pythonic(N=1000000):
    total = sum(range(N))
    return total


@profile
def merge_files_arrays(ts_1, ts_2, ts, det, f1_num, f2_num):
    i = np.array([0])   # indices ts_1
    j = np.array([0])   # indices ts_2
    k = 0   # indices ts
    i_temp = np.array([0])
    j_temp= np.array([0])

    t1 = ts_1[i[0], 0]
    t2 = ts_2[j[0], 0]
    check = 1
    while check:
        i_temp[0] = i[0]
        j_temp[0] = j[0]
        # ts[k], i_neu, j_neu, check = iterate(i, j, t1, t2, f1_num, f2_num, check)
        # ts[k], i_neu, j_neu, check = fib2.fib(i, j, t1, t2, f1_num, f2_num)
        ts[k], check = fib2.fib(i, j, t1, t2, f1_num, f2_num)
        if (i[0] > i_temp[0]):
            # i = i_neu
            if i[0] < f1_num:
                t1 = ts_1[i[0], 0]
                det[k] = 0
                k += 1
        if (j[0] > j_temp[0]):
            # j = j_neu
            if j[0] < f2_num:
                t2 = ts_2[j[0], 0]
                det[k] = 1
                k += 1
    if i[0] == f1_num:
        # t1 has ended first, rest of ts is ts_2
        k += 1
        for o in range(j[0], f2_num):
            ts[k] = ts_2[o, 0]
            det[k] = 1
            k += 1
    if j[0] == f2_num:
        # t2 has ended first, rest is ts_1
        k += 1
        for p in range(i[0], f1_num):
            ts[k] = ts_1[p, 0]
            det[k] = 0
            k += 1


@profile
def merge_files_scalars(ts_1, ts_2, ts, det, f1_num, f2_num):
    i = 0   # indices ts_1
    j = 0   # indices ts_2
    k = 0   # indices ts

    t1 = ts_1[i, 0]
    t2 = ts_2[j, 0]
    check = 1
    while check:
        ts[k], i_neu, j_neu, check = iterate(i, j, t1, t2, f1_num, f2_num, check)
        # ts[k], i_neu, j_neu, check = fib2.fib(i, j, t1, t2, f1_num, f2_num)
        if (i_neu > i):
            i = i_neu
            if (i < f1_num):
                t1 = ts_1[i, 0]
                det[k] = 0
                k += 1
        if (j_neu > j):
            j = j_neu
            if (j < f2_num):
                t2 = ts_2[j, 0]
                det[k] = 1
                k += 1
    if i == f1_num:
        # t1 has ended first, rest of ts is ts_2
        k += 1
        for o in range(j, f2_num):
            ts[k] = ts_2[o, 0]
            det[k] = 1
            k += 1
    if j == f2_num:
        # t2 has ended first, rest is ts_1
        k += 1
        for p in range(i, f1_num):
            ts[k] = ts_1[p, 0]
            det[k] = 0
            k += 1


def iterate(i, j, t1, t2, f1_num, f2_num, check):
    if t1 > t2:
        t = t2
        j += 1
    else:
        t = t1
        i += 1
    if (i == f1_num) or (j == f2_num):
        check = 0
    # out = np.array([t, i, j, check])
    return t, i, j, check


if __name__ == '__main__':
    N = 100000
    ts_1 = np.zeros([N, 2])
    part1 = np.arange(1, N + 1)
    ts_1[0:N, 0] = part1
    ts_2 = np.zeros([N, 2])
    part2 = np.arange(2, N + 2)
    ts_2[0:N, 0] = part2
    ts = np.zeros([2 * N, ])
    det = np.zeros([2 * N, ])

    merge_files_scalars(ts_1, ts_2, ts, det, N, N)
    print(ts)

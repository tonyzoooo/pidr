#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Loïc Bertrand, Tony Zhou
"""
from typing import List

import numpy as np


def upsample(arr: np.array, n: int) -> np.array:
    """
    Increase sample rate by integer factor (based on the MATLAB(R)
    function of the same name).

    :param arr:     source array
    :param n:       integer factor
    :return:        resulting array

    Examples
    --------
    >>> upsample(np.array([1, 2, 3]), 3)
    array([1, 0, 0, 2, 0, 0, 3, 0, 0])
    >>> upsample(np.array([[1, 2], [3, 4]]), 2)
    array([[1, 2],
           [0, 0],
           [3, 4],
           [0, 0]])
    """
    if n <= 0:
        raise ValueError('value n must be positive: ' + str(n))
    if arr.ndim == 2:
        rows = arr.shape[0]
        cols = arr.shape[1]
        result = np.empty((rows * n, cols), dtype=arr.dtype)
        for i in range(rows):
            result[i * n] = arr[i]
            for j in range(1, n):
                result[i * n + j] = np.zeros(cols, dtype=arr.dtype)
        return result
    elif arr.ndim == 1:
        result = np.zeros(len(arr) * n, dtype=arr.dtype)
        for i in range(len(arr)):
            result[i * n] = arr[i]
        return result
    else:
        raise ValueError('array dimension must be 1 or 2: ' + str(n))


def readMatrix(file: str):
    """
    Read a space-separated file containing numbers and converts it to
    a numpy 2D array.

    :param file:    file path
    :return:        numpy array
    """
    with open(file, "r") as f:
        M = np.array([[float(num) for num in line.split(" ")] for line in f])
    return M


def reshapeMeshgrid(lst: List[np.ndarray]) -> np.ndarray:
    """
    Reshapes the result of np.meshgrid(X, Y, Z) to get expected shape.

    :param lst:     list of numpy arrays
    :return:        reshaped array
    """
    rows = len(lst)
    cols = lst[0].size
    result = np.empty((rows, cols))
    for i in range(rows):
        result[i] = np.reshape(lst[i], cols)
    return result.transpose()


def closedRange(start: float, stop: float, step: float = 1) -> np.ndarray:
    """
    Creates a closed range of numbers as a numpy array.

    Examples
    --------
    >>> closedRange(1.1, 5.9, 1.2)
    array([1.1, 2.3, 3.5, 4.7, 5.9])
    >>> closedRange(6, 2, -2)
    array([6, 4, 2])
    >>> closedRange(4.5, 2.31, -1.1)
    array([4.5, 3.4])
    """
    if int is type(start) is type(stop) is type(step):
        epsilon = 0.5 if step > 0 else -0.5
        return np.arange(start, stop + epsilon, step, dtype='int64')
    else:
        epsilon = 1e-12 if step > 0 else -1e-12
        return np.arange(start, stop + epsilon, step, dtype='float64')


def auto_str(cls):
    """
    Decorator which adds a default implementation for the __str__ method of a class.
    """

    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )

    cls.__str__ = __str__
    return cls

def retrieveNetpyneData(filename):
    data = list()
    with open(filename) as f:
        lines = f.readline()
        lines = lines.lstrip('[').rstrip(']')
        lines = lines.split('][')
        for line in lines:
            sublist = list()
            line = line.split(', ')
            for element in line:
                sublist.append(float(element))
            data.append(sublist)
    return np.array(data)

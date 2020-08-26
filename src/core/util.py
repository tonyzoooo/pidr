#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Loïc Bertrand, Tony Zhou
"""

import numpy as np


def upsample(arr: np.array, n: int) -> np.array:
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
        result = np.zeros(len(arr) * n)
        for i in range(len(arr)):
            result[i * n] = arr[i]
        return result
    else:
        raise ValueError('array dimension must be 1 or 2: ' + str(n))


def readMatrix(file: str):
    with open(file, "r") as f:
        M = np.array([[float(num) for num in line.split(" ")] for line in f])
    return M


def reshapeMeshgrid(lst: list):
    rows = len(lst)
    cols = lst[0].size
    result = np.empty((rows, cols))
    for i in range(rows):
        result[i] = np.reshape(lst[i], cols)
    return result.transpose()


def closedRange(start: float, stop: float, step: float = 1) -> np.ndarray:
    """
    Closed integer range.
    Example: closedRange(3, 9, step=2) == array([3, 5, 7, 9])
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

import io

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def upsample(arr: np.array, n: int) -> np.array:
    if n <= 0:
        raise ValueError('value n must be positive: ' + str(n))
    if arr.ndim == 2:
        rows = arr.shape[0]
        cols = arr.shape[1]
        result = np.empty((rows*n, cols), dtype=arr.dtype)
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
    if len(lst) == 0:
        raise ValueError('list lst cannot be empty')
    rows = len(lst)
    cols = lst[0].size
    result = np.empty((rows, cols))
    for i in range(rows):
        result[i] = np.reshape(lst[i], cols)
    return result

def figToImage():
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    im = Image.open(buf)
    return im

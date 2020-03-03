from numpy import array, empty, reshape, zeros, cov, mean


def upsample(arr: array, n: int) -> array:
    if n <= 0:
        raise ValueError('value n must be positive: ' + str(n))
    if arr.ndim == 2:
        rows = arr.shape[0]
        cols = arr.shape[1]
        result = empty((rows*n, cols), dtype=arr.dtype)
        for i in range(rows):
            result[i * n] = arr[i]
            for j in range(1, n):
                result[i * n + j] = zeros(cols, dtype=arr.dtype)
        return result
    elif arr.ndim == 1:
        result = zeros(len(arr) * n)
        for i in range(len(arr)):
            result[i * n] = arr[i]
        return result
    else:
        raise ValueError('array dimension must be 1 or 2: ' + str(n))


def readMatrix(file: str):
    with open(file, "r") as f:
        M = array([[float(num) for num in line.split(" ")] for line in f])
    return M


def reshapeMeshgrid(lst: list):
    l = list()
    element = lst[0]
    size = element.size
    for i in range(len(lst)):
        element = lst[i]
        l.append(reshape(element, size))
    return array(l)


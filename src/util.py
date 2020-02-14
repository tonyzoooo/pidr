from numpy import array, empty, zeros, reshape


def upsample(arr: array, n: int) -> array:
    if n <= 0:
        raise ValueError('value n must be positive: ' + str(n))
    if arr.ndim == 2:
        result = empty((arr.shape[0], arr.shape[1] * n))
        for i in range(len(arr)):
            result[i] = upsample(arr[i], n)
        return array(result)
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

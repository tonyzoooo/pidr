from numpy import array, zeros, reshape


def upsample(arr: array, n: int) -> array:
    if n <= 0:
        raise ValueError('value n must be positive: ' + str(n))
    if arr.ndim > 2:
        raise ValueError('dimension must be 1 or 2: ' + str(n))
    if arr.ndim == 2:
        lst = []
        for col in arr:
            lst.append(upsample(col, n))
        return array(lst)
    else:
        result = zeros(arr.size * n)
        for i in range(arr.size):
            result[i * n] = arr[i]
        return result

def readMatrix(file: str):
    with open(file, "r") as f:
        M = array([[float(num) for num in line.split(" ")] for line in f])
    return M

def reshapeMeshgrid(lst : list):
    l = list()
    element = lst[0]
    size = element.size
    for i in range(len(lst)):
        element = lst[i]
        l.append(reshape(element, size))
    return array(l)
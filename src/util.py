from numpy import array, zeros


def upsample(arr: array, n: int) -> array:
    if n <= 0:
        raise ValueError('value n must be positive: ' + str(n))
    result = zeros(arr.size * n)
    for i in range(arr.size):
        result[i * n] = arr[i]
    return result

def readMatrix(file: str):
    with open(file, "r") as f:
        M = array([[float(num) for num in line.split(" ")] for line in f])
    return M

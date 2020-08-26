import unittest

import numpy as np
from numpy.testing import assert_array_equal

from src.core import util


class UtilTest(unittest.TestCase):

    def test_closedRange_int_ascendant(self):
        assert_array_equal(util.closedRange(2, 6, 2), np.array([2, 4, 6]))
        assert_array_equal(util.closedRange(2, 7, 2), np.array([2, 4, 6]))
        assert_array_equal(util.closedRange(2, 4, 2), np.array([2, 4]))

    def test_closedRange_int_descendant(self):
        assert_array_equal(util.closedRange(6, 2, -2), np.array([6, 4, 2]))
        assert_array_equal(util.closedRange(6, 3, -2), np.array([6, 4]))
        assert_array_equal(util.closedRange(6, 1, -2), np.array([6, 4, 2]))

    def test_closedRange_float_ascendant(self):
        assert_array_equal(util.closedRange(2.3, 4.5, 1.1), np.array([2.3, 3.4, 4.5]))
        assert_array_equal(util.closedRange(2.3, 4.49, 1.1), np.array([2.3, 3.4]))
        assert_array_equal(util.closedRange(2.3, 4.51, 1.1), np.array([2.3, 3.4, 4.5]))

    def test_closedRange_float_descendant(self):
        assert_array_equal(util.closedRange(4.5, 2.3, -1.1), np.array([4.5, 3.4, 2.3]))
        assert_array_equal(util.closedRange(4.5, 2.31, -1.1), np.array([4.5, 3.4]))
        assert_array_equal(util.closedRange(4.5, 2.29, -1.1), np.array([4.5, 3.4, 2.3]))


if __name__ == '__main__':
    unittest.main()

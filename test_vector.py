import unittest
import numpy as np

import vector

class VectorTest(unittest.TestCase):
    def test_normal(self):
        z_axis = vector.normal([0,0,0], [1,0,0], [0,1,0])
        z_axis_neg = vector.normal([0,0,0], [0,1,0], [1,0,0])

        np.testing.assert_almost_equal([0,0,1], z_axis)
        np.testing.assert_almost_equal([0,0,-1], z_axis_neg)

    def test_rotate_y(self):
        x_axis = [1,0,0]

        rotate_0 = vector.rotate_y(x_axis, 0)
        rotate_90 = vector.rotate_y(x_axis, 90)
        rotate_180 = vector.rotate_y(x_axis, 180)
        rotate_270 = vector.rotate_y(x_axis, 270)
        rotate_360 = vector.rotate_y(x_axis, 360)

        np.testing.assert_almost_equal([1,0,0], rotate_0)
        np.testing.assert_almost_equal([0,0,-1], rotate_90)
        np.testing.assert_almost_equal([-1,0,0], rotate_180)
        np.testing.assert_almost_equal([0,0,1], rotate_270)
        np.testing.assert_almost_equal([1,0,0], rotate_360)

    def test_rotate_x(self):
        y_axis = [0,1,0]

        rotate_0 = vector.rotate_x(y_axis, 0)
        rotate_90 = vector.rotate_x(y_axis, 90)
        rotate_180 = vector.rotate_x(y_axis, 180)
        rotate_270 = vector.rotate_x(y_axis, 270)
        rotate_360 = vector.rotate_x(y_axis, 360)

        np.testing.assert_almost_equal([0,1,0], rotate_0)
        np.testing.assert_almost_equal([0,0,1], rotate_90)
        np.testing.assert_almost_equal([0,-1,0], rotate_180)
        np.testing.assert_almost_equal([0,0,-1], rotate_270)
        np.testing.assert_almost_equal([0,1,0], rotate_360)

    def test_rotate_z(self):
        x_axis = [1,0,0]

        rotate_0 = vector.rotate_z(x_axis, 0)
        rotate_90 = vector.rotate_z(x_axis, 90)
        rotate_180 = vector.rotate_z(x_axis, 180)
        rotate_270 = vector.rotate_z(x_axis, 270)
        rotate_360 = vector.rotate_z(x_axis, 360)

        np.testing.assert_almost_equal([1,0,0], rotate_0)
        np.testing.assert_almost_equal([0,1,0], rotate_90)
        np.testing.assert_almost_equal([-1,0,0], rotate_180)
        np.testing.assert_almost_equal([0,-1,0], rotate_270)
        np.testing.assert_almost_equal([1,0,0], rotate_360)

if __name__ == "__main__":
    unittest.main()

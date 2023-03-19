import unittest
import numpy as np
from ddt import ddt, data, unpack

import vector

@ddt
class VectorTest(unittest.TestCase):
    def test_normal(self):
        v0 = [0,0,0]
        v1 = [1,0,0]
        v2 = [0,1,0]
        v3 = [1,1,0]

        normal = vector.normal(v0, v1, v2)
        reversed = vector.normal(v0, v2, v1)

        np.testing.assert_almost_equal([0,0,1], normal)
        np.testing.assert_almost_equal([0,0,-1], reversed)

        normal = vector.normal(v3, v2, v1)
        reversed = vector.normal(v3, v1, v2)

        np.testing.assert_almost_equal([0,0,1], normal)
        np.testing.assert_almost_equal([0,0,-1], reversed)

    def test_normal_reversed(self):
        v0 = [0,0,0]
        v1 = [0,1,0]
        v2 = [1,0,0]
        v3 = [1,1,0]
    
        reversed = vector.normal(v0, v1, v2)
        normal = vector.normal(v0, v2, v1)

        np.testing.assert_almost_equal([0,0,1], normal)
        np.testing.assert_almost_equal([0,0,-1], reversed)

        reversed = vector.normal(v3, v2, v1)
        normal = vector.normal(v3, v1, v2)

        np.testing.assert_almost_equal([0,0,1], normal)
        np.testing.assert_almost_equal([0,0,-1], reversed)

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

    @data(
        (0, 0, 1, True),
        (1, 0, 1, True),
        (0, 1, 1, True),
        (1, 1, 1, True),

        (0.0001, 0.0001, 1, True),
        (0.9999, 0.0001, 1, True),
        (0.0001, 0.9999, 1, True),
        (0.9999, 0.9999, 1, True),

        (-0.0001, -0.0001, 1, False),
        (1.0001, -0.0001, 1, False),
        (-0.0001, 1.0001, 1, False),
        (1.0001, 1.0001, 1, False),

        (0, 0, -1, False),
        (1, 0, -1, False),
        (0, 1, -1, False),
        (1, 1, -1, False),

        (0.0001, 0.0001, -1, False),
        (0.9999, 0.0001, -1, False),
        (0.0001, 0.9999, -1, False),
        (0.9999, 0.9999, -1, False),
    )
    @unpack
    def test_intersect_quad(self, x: float, y: float, z: float, expected: bool):
        ray_origin = np.array([x, y, z])
        ray_direction = np.array([0, 0, -z])

        v0 = np.array([0, 0, 0])
        v1 = np.array([1, 0, 0])
        v2 = np.array([0, 1, 0])
        v3 = np.array([1, 1, 0])

        (hit, hitDistance, hitPoint) = vector.intersect_quad(
            ray_origin, ray_direction, v0, v1, v2, v3
        )

        self.assertEqual(expected, hit)

        if expected:
            np.testing.assert_almost_equal([x, y, 0], hitPoint)
            np.testing.assert_almost_equal(z, hitDistance)

            normal = vector.normal(v0, v1, v2)
            product = np.dot(ray_direction, normal)
            
            np.testing.assert_almost_equal([0,0,1], normal)
            self.assertTrue(product < 0)

    @data(
        (0, 0, 1, True),
        (1, 0, 1, True),
        (0, 1, 1, True),
        (0.5, 0.5, 1, True),

        (0.0001, 0.0001, 1, True),
        (0.9999, 0.0001, 1, True),
        (0.0001, 0.9999, 1, True),
        (0.4999, 0.4999, 1, True),

        (-0.0001, -0.0001, 1, False),
        (1.0001, -0.0001, 1, False),
        (-0.0001, 0.0001, 1, False),
        (5.0001, 5.0001, 1, False),

        (0, 0, -1, False),
        (1, 0, -1, False),
        (0, 1, -1, False),
        (0.5, 0.5, -1, False),

        (0.0001, 0.0001, -1, False),
        (0.9999, 0.0001, -1, False),
        (0.0001, 0.9999, -1, False),
        (0.4999, 0.4999, -1, False),
    )
    @unpack
    def test_intersect_triangle(self, x: float, y: float, z: float, expected: bool):
        ray_origin = np.array([x, y, z])
        ray_direction = np.array([0, 0, -z])

        v0 = np.array([0, 0, 0])
        v1 = np.array([1, 0, 0])
        v2 = np.array([0, 1, 0])

        (hit, hitDistance, hitPoint) = vector.intersect_triangle(
            ray_origin, ray_direction, v0, v1, v2
        )

        self.assertEqual(expected, hit)

        if expected:
            np.testing.assert_almost_equal([x, y, 0], hitPoint)
            np.testing.assert_almost_equal(z, hitDistance)

            normal = vector.normal(v0, v1, v2)
            product = np.dot(ray_direction, normal)
            
            np.testing.assert_almost_equal([0,0,1], normal)
            self.assertTrue(product < 0)

if __name__ == "__main__":
    unittest.main()

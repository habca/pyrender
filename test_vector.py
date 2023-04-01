import unittest
import numpy as np
from ddt import ddt, data, unpack

import vector

@ddt
class NormalVectorTest(unittest.TestCase):
    def test_normal_vector(self):
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

    def test_normal_vector_reversed(self):
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

@ddt
class RotateAxisTest(unittest.TestCase):
    def test_rotate_axis_y(self):
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

    def test_rotate_axis_x(self):
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

    def test_rotate_axis_z(self):
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

    def test_rotate_axis_angle_xy(self):
        v1 = np.array([1, 0, 0])
        v2 = np.array([0, 1, 0])

        rotation = vector.rotate_axis_angle(v1, v2)
        rotation_inverse = vector.rotate_axis_angle(v2, v1)

        np.testing.assert_almost_equal(v2, np.dot(rotation, v1))
        np.testing.assert_almost_equal(v2, vector.rotate_z(v1, 90))

        np.testing.assert_almost_equal(v1, np.dot(rotation_inverse, v2))
        np.testing.assert_almost_equal(v1, vector.rotate_z(v2, -90))

    def test_rotate_axis_angle_xz(self):
        v1 = np.array([1, 0, 0])
        v2 = np.array([0, 0, 1])

        rotation = vector.rotate_axis_angle(v1, v2)
        rotation_inverse = vector.rotate_axis_angle(v2, v1)

        np.testing.assert_almost_equal(v2, np.dot(rotation, v1))
        np.testing.assert_almost_equal(v2, vector.rotate_y(v1, -90))

        np.testing.assert_almost_equal(v1, np.dot(rotation_inverse, v2))
        np.testing.assert_almost_equal(v1, vector.rotate_y(v2, 90))

    def test_rotate_axis_angle_yz(self):
        v1 = np.array([0, 1, 0])
        v2 = np.array([0, 0, 1])

        rotation = vector.rotate_axis_angle(v1, v2)
        rotation_inverse = vector.rotate_axis_angle(v2, v1)

        np.testing.assert_almost_equal(v2, np.dot(rotation, v1))
        np.testing.assert_almost_equal(v2, vector.rotate_x(v1, 90))

        np.testing.assert_almost_equal(v1, np.dot(rotation_inverse, v2))
        np.testing.assert_almost_equal(v1, vector.rotate_x(v2, -90))

    def test_rotate_axis_angle_identity(self):
        v1 = np.array([1, 0, 0])

        rotation = vector.rotate_axis_angle(v1, v1)
        rotation_inverse = vector.rotate_axis_angle(v1, v1)

        np.testing.assert_almost_equal(v1, np.dot(rotation, v1))
        np.testing.assert_almost_equal(v1, np.dot(rotation_inverse, v1))

        np.testing.assert_almost_equal(v1, vector.rotate_x(v1, 0))
        np.testing.assert_almost_equal(v1, vector.rotate_y(v1, 0))
        np.testing.assert_almost_equal(v1, vector.rotate_z(v1, 0))

    def test_rotation_matrix(self):
        v, axis, theta = [3,5,0], [4,4,1], 1.2

        rotation = np.dot(vector.rotation_matrix(axis, theta), v)
        expected = [2.74911638, 4.77180932, 1.91629719]

        np.testing.assert_almost_equal(expected, rotation)

@ddt
class ProjectToTest(unittest.TestCase):
    @data(
        (0, 0, 1, True),
        (1, 0, 1, True),
        (0, 1, 1, True),
        (0.5, 0.5, 1, True),

        (0.0001, 0.0001, 1, True),
        (0.9999, 0.0001, 1, True),
        (0.0001, 0.9999, 1, True),
        (0.4999, 0.4999, 1, True),

        (-0.0001, -0.0001, 1, True),
        (1.0001, -0.0001, 1, True),
        (-0.0001, 0.0001, 1, True),
        (5.0001, 5.0001, 1, True),

        (0, 0, -1, True),
        (1, 0, -1, True),
        (0, 1, -1, True),
        (0.5, 0.5, -1, True),

        (0.0001, 0.0001, -1, True),
        (0.9999, 0.0001, -1, True),
        (0.0001, 0.9999, -1, True),
        (0.4999, 0.4999, -1, True),
    )
    @unpack
    def test_project_to_plane(self, x: float, y: float, z: float, expected: bool):
        ray_origin = np.array([x, y, z])
        ray_direction = np.array([0, 0, -z])

        v0 = np.array([0, 0, 0])
        v1 = np.array([1, 0, 0])
        v2 = np.array([0, 1, 0])

        normal = vector.normal(v0, v1, v2)
        product = np.dot(ray_direction, normal)

        (hit, hitDistance, hitPoint) = vector.project_to_plane(
            ray_origin, ray_direction, v0, normal)
        
        self.assertEqual(expected, hit)
        self.assertEqual(expected, product != 0)

        np.testing.assert_almost_equal([x, y, 0], hitPoint)
        np.testing.assert_almost_equal([0, 0, 1], normal)
        np.testing.assert_almost_equal(abs(z), hitDistance)

@ddt
class IntersectTest(unittest.TestCase):
    @data(
        (0, 0, 1, True),
        (1, 0, 1, True),
        (0, 1, 1, True),
        (0.5, 0.5, 1, True),

        (0.0001, 0.0001, 1, True),
        (0.9999, 0.0001, 1, True),
        (0.0001, 0.9999, 1, True),
        (0.4999, 0.4999, 1, True),

        (-0.0001, -0.0001, 1, True),
        (1.0001, -0.0001, 1, True),
        (-0.0001, 0.0001, 1, True),
        (5.0001, 5.0001, 1, True),

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
    def test_intersect_plane(self, x: float, y: float, z: float, expected: bool):
        ray_origin = np.array([x, y, z])
        ray_direction = np.array([0, 0, -z])

        v0 = np.array([0, 0, 0])
        v1 = np.array([1, 0, 0])
        v2 = np.array([0, 1, 0])

        normal = vector.normal(v0, v1, v2)
        product = np.dot(ray_direction, normal)

        (hit, hitDistance, hitPoint) = vector.intersect_plane(
            ray_origin, ray_direction, v0, normal)

        self.assertEqual(expected, hit)
        self.assertEqual(expected, product < 0)

        if expected:
            np.testing.assert_almost_equal([x, y, 0], hitPoint)
            np.testing.assert_almost_equal([0, 0, 1], normal)
            np.testing.assert_almost_equal(abs(z), hitDistance)

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

        normal = vector.normal(v3, v2, v1)
        product = np.dot(ray_direction, normal)

        (hit, hitDistance, hitPoint) = vector.intersect_quad(
            ray_origin, ray_direction, v0, v1, v2, v3)

        self.assertEqual(expected, hit)
        self.assertEqual(expected, hit and product < 0)

        if expected:
            np.testing.assert_almost_equal([x, y, 0], hitPoint)
            np.testing.assert_almost_equal([0, 0, 1], normal)
            np.testing.assert_almost_equal(abs(z), hitDistance)

    def test_intersect_quad_precision(self):
        cameraPosition = np.array([0, 0, 3.16])
        worldPosition = np.array([-1, 1, 1])

        ray_origin = np.array(worldPosition)
        ray_direction = np.array([0.38732932, -0.38732932, 0.83663134])

        v0 = np.array([-1, -1, 2.16])
        v1 = np.array([1, -1, 2.16])
        v2 = np.array([-1, 1, 2.16])
        v3 = np.array([1, 1, 2.16])

        (hit, _, _) = vector.intersect_quad(
            ray_origin, ray_direction, v0, v2, v1, v3)
        
        self.assertTrue(hit)

        ray_direction = vector.subtract(cameraPosition, worldPosition)
        ray_direction = vector.normalize(ray_direction)

        (hit, _, _) = vector.intersect_quad(
            ray_origin, ray_direction, v0, v2, v1, v3)
        
        self.assertTrue(hit)

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

        normal = vector.normal(v0, v1, v2)
        product = np.dot(ray_direction, normal)

        (hit, hitDistance, hitPoint) = vector.intersect_triangle(
            ray_origin, ray_direction, v0, v1, v2)

        self.assertEqual(expected, hit)
        self.assertEqual(expected, hit and product < 0)

        if expected:
            np.testing.assert_almost_equal([x, y, 0], hitPoint)
            np.testing.assert_almost_equal([0, 0, 1], normal)
            np.testing.assert_almost_equal(abs(z), hitDistance)

@ddt
class PointInTest(unittest.TestCase):
    @data(
        (0, 0, 0, True),
        (1, 0, 0, True),
        (0, 1, 0, True),
        (1, 1, 0, True),
        (0.0001, 0.0001, 0, True),
        (0.9999, 0.0001, 0, True),
        (0.0001, 0.9999, 0, True),
        (0.9999, 0.9999, 0, True),
        (-0.0001, -0.0001, 0, False),
        (1.0001, -0.0001, 0, False),
        (-0.0001, 1.0001, 0, False),
        (1.0001, 1.0001, 0, False)
    )
    @unpack
    def test_point_in_quad(self, x: float, y: float, z: float, expected: bool):
        point = np.array([x, y, z])

        v0 = np.array([0, 0, 0])
        v1 = np.array([1, 0, 0])
        v2 = np.array([0, 1, 0])
        v3 = np.array([1, 1, 0])

        normal = vector.normal(v3, v2, v1)
        (result, triangleNormal) = vector.point_in_quad(point, v0, v1, v2, v3)

        self.assertEqual(expected, result)
        np.testing.assert_almost_equal(normal, triangleNormal)

    @data(
        (0, 0, 0, True),
        (1, 0, 0, True),
        (0, 1, 0, True),
        (0.5, 0.5, 0, True),
        (0.0001, 0.0001, 0, True),
        (0.9999, 0.0001, 0, True),
        (0.0001, 0.9999, 0, True),
        (0.4999, 0.4999, 0, True),
        (-0.0001, -0.0001, 0, False),
        (1.0001, -0.0001, 0, False),
        (-0.0001, 1.0001, 0, False),
        (5.0001, 5.0001, 0, False)
    )
    @unpack
    def test_point_in_triangle(self, x: float, y: float, z: float, expected: bool):
        point = np.array([x, y, z])
        
        v0 = np.array([0, 0, 0])
        v1 = np.array([1, 0, 0])
        v2 = np.array([0, 1, 0])

        normal = vector.normal(v0, v1, v2)
        (result, triangleNormal) = vector.point_in_triangle(point, v0, v1, v2)
        
        self.assertEqual(expected, result)
        np.testing.assert_almost_equal(normal, triangleNormal)

if __name__ == "__main__":
    unittest.main()

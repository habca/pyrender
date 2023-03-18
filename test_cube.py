import unittest
import numpy as np

import vector
from cube import Cube

class CubeTest(unittest.TestCase):
    def test_get_triangles(self):
        cube = Cube((0.5,0.5,0.5), (1,1,1))
        vertices = cube.get_vertices()

        v0 = vertices[0]
        v1 = vertices[1]
        v2 = vertices[2]
        v3 = vertices[3]
        v4 = vertices[4]
        v5 = vertices[5]
        v6 = vertices[6]
        v7 = vertices[7]

        face0 = vector.normal(v0, v1, v2)
        face1 = vector.normal(v3, v2, v1)
        face2 = vector.normal(v7, v5, v6)
        face3 = vector.normal(v4, v6, v5)

        self.assertTrue(np.array_equal(face0, face1))
        self.assertTrue(np.array_equal(face2, face3))
        self.assertTrue(np.array_equal(face0, -face2))
        self.assertTrue(np.array_equal(face1, -face3))

        face4 = vector.normal(v4, v0, v6)
        face5 = vector.normal(v2, v6, v0)
        face6 = vector.normal(v1, v5, v3)
        face7 = vector.normal(v7, v3, v5)

        self.assertTrue(np.array_equal(face4, face5))
        self.assertTrue(np.array_equal(face6, face7))
        self.assertTrue(np.array_equal(face4, -face6))
        self.assertTrue(np.array_equal(face5, -face7))

        face8 = vector.normal(v2, v3, v6)
        face9 = vector.normal(v7, v6, v3)
        face10 = vector.normal(v5, v1, v4)
        face11 = vector.normal(v0, v4, v1)

        self.assertTrue(np.array_equal(face8, face9))
        self.assertTrue(np.array_equal(face10, face11))
        self.assertTrue(np.array_equal(face8, -face10))
        self.assertTrue(np.array_equal(face9, -face11))

if __name__ == "__main__":
    unittest.main()

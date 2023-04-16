import math
import numpy as np

import vector

class Camera:
    def __init__(self, cameraPosition: np.ndarray, screenResolution: tuple[int, int]):
        self.cameraPosition = cameraPosition
        self.orbitTarget = np.array([0,0,0])

        self.cameraDirection = np.array([0,0,-1])
        self.upDirection = np.array([0,1,0])

        self.look_at(self.cameraPosition, self.orbitTarget)

        self.imageWidth = screenResolution[0]
        self.imageHeight = screenResolution[1]

    def look_at(self, look_from: np.ndarray, look_to: np.ndarray) -> None:
        old_direction = self.cameraDirection
        old_direction = vector.normalize(old_direction)

        new_direction = vector.subtract(look_to, look_from)
        new_direction = vector.normalize(new_direction)
        
        rotation = vector.rotate_axis_angle(old_direction, new_direction)

        self.cameraPosition = look_from
        self.orbitTarget = look_to

        self.cameraDirection = np.dot(rotation, self.cameraDirection)
        self.cameraDirection = vector.normalize(self.cameraDirection)

        self.upDirection = np.dot(rotation, self.upDirection)
        self.upDirection = vector.normalize(self.upDirection)

    def right_direction(self) -> np.ndarray:
        right = vector.crossProduct(self.cameraDirection, self.upDirection)
        right = vector.normalize(right)
        return right

    def up_direction(self) -> np.ndarray:
        up = vector.crossProduct(self.right_direction(), self.cameraDirection)
        up = vector.normalize(up)
        return up

    def rotate_orbit(self, angle_x: float, angle_y: float) -> None:
        rotate_x = vector.rotation_matrix(self.up_direction(), angle_y)
        rotate_y = vector.rotation_matrix(self.right_direction(), angle_x)

        line_segment = self.cameraPosition - self.orbitTarget
        line_segment = np.dot(rotate_x, line_segment)
        line_segment = np.dot(rotate_y, line_segment)
        new_position = line_segment + self.orbitTarget
        self.look_at(new_position, self.orbitTarget)

    def scale_orbit(self, zoom_z: float) -> None:
        new_position = self.cameraPosition + zoom_z * self.cameraDirection
        self.look_at(new_position, self.orbitTarget)

    def screen_center(self) -> np.ndarray:
        return self.cameraPosition + self.cameraDirection

    def screen_corner(self) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        center = self.screen_center()
        right = self.right_direction()
        up = self.up_direction()

        v0 = center - right - up
        v1 = center + right - up
        v2 = center - right + up
        v3 = center + right + up

        return (v0, v1, v2, v3)

    def projection(self, worldPosition: np.ndarray
        ) -> tuple[bool, float, np.ndarray]:
        
        ray_origin = np.array(worldPosition)
        ray_direction = vector.subtract(self.cameraPosition, worldPosition)
        ray_direction = vector.normalize(ray_direction)

        (v0, v1, v2, v3) = self.screen_corner()

        # Reverse triangle vertices for ray casting because
        # otherwise triangle normals point towards the camera.
        (hit, hitDistance, hitPoint) = vector.intersect_quad(
            ray_origin, ray_direction, v0, v2, v1, v3)

        # There is neither intersection nor distance.
        if not hit: return (hit, hitDistance, hitPoint)

        center = self.screen_center()
        right = self.right_direction()
        up = self.up_direction()

        # Forward vector should zero out on projection.
        normalized = vector.subtract(hitPoint, center)

        normal_width = (1 + vector.dotProduct(right, normalized)) / 2 # [0,1]
        normal_height = (1 + vector.dotProduct(up, normalized)) / 2 # [0,1]

        pixel_width = self.imageWidth
        pixel_height = self.imageHeight

        pixel_x = math.floor(normal_width * pixel_width)
        pixel_y = math.floor((1 - normal_height) * pixel_height)

        hitPoint = np.array([pixel_x, pixel_y])

        return (hit, hitDistance, hitPoint)

    def visible_surface(self, v0: np.ndarray, v1: np.ndarray, v2: np.ndarray) -> bool:
        """
        In right-handed coordinate system: right ^ up = forward
        When camera points downwards the Z axis: up ^ right = forward
        """

        normal = vector.normal(v0, v2, v1)
        ray_direction = vector.subtract(v0, self.cameraPosition)
        return vector.dotProduct(normal, ray_direction) < 0

    def screen_to_ray(self, screenPixel: tuple[int, int]) -> np.ndarray:
        # imageAspectRatio = self.imageWidth / self.imageHeight
        
        x = (1 - 2 * ((screenPixel[0]) / self.imageWidth))
        y = (1 - 2 * ((screenPixel[1]) / self.imageHeight))

        fieldOfView = 90

        mx = x * (math.tan(vector.RADIANS * (fieldOfView / 2)))
        my = y * (math.tan(vector.RADIANS * (fieldOfView / 2)))

        dx = vector.product(-1 * mx, self.right_direction())
        dy = vector.product(my, self.up_direction())

        ray_direction = self.cameraDirection
        ray_direction = vector.add(ray_direction, dx)
        ray_direction = vector.add(ray_direction, dy)
        ray_direction = vector.normalize(ray_direction)

        return ray_direction

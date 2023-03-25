import numpy as np
import math

def normal(v0: np.ndarray, v1: np.ndarray, v2: np.ndarray) -> np.ndarray:
    edge0 = np.subtract(v1, v0)
    edge1 = np.subtract(v2, v0)
    cross = np.cross(edge0, edge1)
    return normalize(cross)

def normalize(v0: np.ndarray) -> np.ndarray:
    return v0 / np.linalg.norm(v0)

def rotate(v0: np.ndarray, origin: np.ndarray, degrees: np.ndarray) -> np.ndarray:
    v0 = np.add(origin, rotate_x(np.subtract(v0, origin), degrees[0]))
    v0 = np.add(origin, rotate_y(np.subtract(v0, origin), degrees[1]))
    v0 = np.add(origin, rotate_z(np.subtract(v0, origin), degrees[2]))
    return v0

def radian(degree: float) -> float:
    return degree * (math.pi / 180)

def degree(radian: float) -> float:
    return radian * (180 / math.pi)

def rotate_x(direction: np.ndarray, degrees: float) -> np.ndarray:
    radians = radian(degrees)
    return np.array([
        direction[0],
        direction[1] * math.cos(radians) -
        direction[2] * math.sin(radians),
        direction[1] * math.sin(radians) +
        direction[2] * math.cos(radians)
    ])

def rotate_y(direction: np.ndarray, degrees: float) -> np.ndarray:
    radians = radian(degrees)
    return np.array([
        direction[0] * math.cos(radians) +
        direction[2] * math.sin(radians),
        direction[1],
        -direction[0] * math.sin(radians) +
        direction[2] * math.cos(radians)
    ])

def rotate_z(direction: np.ndarray, degrees: float) -> np.ndarray:
    radians = radian(degrees)
    return np.array([
        direction[0] * math.cos(radians) -
        direction[1] * math.sin(radians),
        direction[0] * math.sin(radians) +
        direction[1] * math.cos(radians),
        direction[2]
    ])

def project_to_plane(
        ray_origin: np.ndarray,
        ray_direction: np.ndarray,
        plane_origin: np.ndarray,
        plane_normal: np.ndarray
    ) -> tuple[bool, float, np.ndarray]:

    line = np.subtract(plane_origin, ray_origin)
    scale = np.dot(ray_direction, plane_normal)

    EPSILON = 1e-6

    # DivideByZeroError.
    if -EPSILON < scale < EPSILON:
        return (False, 0, np.array([]))

    hitDistance = np.dot(line, plane_normal) / scale
    hitPoint = ray_origin + hitDistance * ray_direction

    return (True, hitDistance, hitPoint)

def intersect_plane(
        ray_origin: np.ndarray,
        ray_direction: np.ndarray,
        plane_origin: np.ndarray,
        plane_normal: np.ndarray
    ) -> tuple[bool, float, np.ndarray]:

    (hit, hitDistance, hitPoint) = project_to_plane(
        ray_origin, ray_direction, plane_origin, plane_normal)

    if not hit: return (hit, hitDistance, hitPoint)

    hit = hit and np.dot(ray_direction, plane_normal) < 0
    hit = hit and hitDistance > 0

    return (hit, hitDistance, hitPoint)

def intersect_quad(
        ray_origin: np.ndarray,
        ray_direction: np.ndarray,
        v0: np.ndarray,
        v1: np.ndarray,
        v2: np.ndarray,
        v3: np.ndarray
    ) -> tuple[bool, float, np.ndarray]:
    
    (hit, hitDistance, hitPoint) = intersect_triangle(
        ray_origin, ray_direction, v0, v1, v2
    )
    
    if hit: return (hit, hitDistance, hitPoint)
    
    (hit, hitDistance, hitPoint) = intersect_triangle(
        ray_origin, ray_direction, v3, v2, v1
    )
    
    return (hit, hitDistance, hitPoint)

def intersect_triangle(
        ray_origin: np.ndarray,
        ray_direction: np.ndarray,
        v0: np.ndarray,
        v1: np.ndarray,
        v2: np.ndarray
    ) -> tuple[bool, float, np.ndarray]:

    hit = False
    hitDistance = 0
    hitPoint = np.array([0,0,0])
    
    EPSILON = 1e-4

    edge1 = np.subtract(v1, v0)
    edge2 = np.subtract(v2, v0)

    P = np.cross(ray_direction, edge2)
    determinant = np.dot(P, edge1)
    if determinant < EPSILON:
        return (hit, hitDistance, hitPoint)
    
    inverseDeterminant = 1 / determinant
    
    T = np.subtract(ray_origin, v0)
    u_coordinate = inverseDeterminant * np.dot(P, T)
    if u_coordinate < 0 or 1 < u_coordinate:
        return (hit, hitDistance, hitPoint)

    Q = np.cross(T, edge1)
    v_coordinate = inverseDeterminant * np.dot(Q, ray_direction)
    if v_coordinate < 0 or 1 < u_coordinate + v_coordinate:
        return (hit, hitDistance, hitPoint)
    
    hit = True
    hitDistance = inverseDeterminant * np.dot(Q, edge2)
    hitPoint = ray_origin + hitDistance * ray_direction
    return (hit, hitDistance, hitPoint)

def point_in_quad(
        point: np.ndarray,
        v0: np.ndarray,
        v1: np.ndarray,
        v2: np.ndarray,
        v3: np.ndarray
    ) -> tuple[bool, np.ndarray]:

    (result, normal) = point_in_triangle(point, v0, v1, v2)
    if result: return (result, normal)
    
    (result, normal) = point_in_triangle(point, v3, v2, v1)
    if result: return (result, normal)
    
    return (False, normal)

def point_in_triangle(
        point: np.ndarray,
        v0: np.ndarray,
        v1: np.ndarray,
        v2: np.ndarray
    ) -> tuple[bool, np.ndarray]:

    e1 = np.subtract(v1, v0)
    e2 = np.subtract(v2, v0)

    normal = np.cross(e1, e2)
    normal = normalize(normal)

    EPSILON = 1e-6

    e1 = np.subtract(v1, v0)
    e2 = np.subtract(point, v0)
    n0 = np.cross(e1, e2)
    if np.dot(normal, n0) < -EPSILON:
        return (False, normal)

    e1 = np.subtract(v2, v1)
    e2 = np.subtract(point, v1)
    n1 = np.cross(e1, e2)
    if np.dot(normal, n1) < -EPSILON:
        return (False, normal)
    
    e1 = np.subtract(v0, v2)
    e2 = np.subtract(point, v2)
    n2 = np.cross(e1, e2)
    if np.dot(normal, n2) < -EPSILON:
        return (False, normal)
    
    return (True, normal)

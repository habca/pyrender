import numpy as np
import math

def normal(v0: np.ndarray, v1: np.ndarray, v2: np.ndarray) -> np.ndarray:
    edge0 = subtract(v1, v0)
    edge1 = subtract(v2, v0)
    cross = crossProduct(edge0, edge1)
    return normalize(cross)

def subtract(v0: np.ndarray, v1: np.ndarray) -> np.ndarray:
    return np.array([v0[0] - v1[0], v0[1] - v1[1], v0[2] - v1[2]])

def dotProduct(v0: np.ndarray, v1: np.ndarray) -> float:
    return v0[0] * v1[0] + v0[1] * v1[1] + v0[2] * v1[2]

def crossProduct(v0: np.ndarray, v1: np.ndarray) -> np.ndarray:
    return np.array([
        v0[1] * v1[2] - v0[2] * v1[1],
        v0[2] * v1[0] - v0[0] * v1[2],
        v0[0] * v1[1] - v0[1] * v1[0]
    ])

def normalize(v0: np.ndarray) -> np.ndarray:
    len = math.sqrt(dotProduct(v0, v0))

    x = v0[0] / len
    y = v0[1] / len
    z = v0[2] / len

    return np.array([x, y, z])

def rotate(v0: np.ndarray, origin: np.ndarray, degrees: np.ndarray) -> np.ndarray:
    v0 = np.add(origin, rotate_x(subtract(v0, origin), degrees[0]))
    v0 = np.add(origin, rotate_y(subtract(v0, origin), degrees[1]))
    v0 = np.add(origin, rotate_z(subtract(v0, origin), degrees[2]))
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

def rotation_matrix(axis: np.ndarray, degrees: float) -> np.ndarray:
    radians = radian(degrees)
    rcos = math.cos(radians)
    rsin = math.sin(radians)
    u,v,w = axis
    return np.array([
        [rcos + u*u*(1-rcos), -w * rsin + u*v*(1-rcos), v * rsin + u*w*(1-rcos)],
        [w * rsin + v*u*(1-rcos), rcos + v*v*(1-rcos), -u * rsin + v*w*(1-rcos)],
        [-v * rsin + w*u*(1-rcos), u * rsin + w*v*(1-rcos), rcos + w*w*(1-rcos)]
    ])

def rotate_axis_angle(v1: np.ndarray, v2: np.ndarray) -> np.ndarray:
    axis = crossProduct(v1, v2)

    EPSILON = 1e-6

    if dotProduct(axis, axis) < EPSILON:
        return np.identity(3)

    axis = normalize(axis)
    
    angle = math.acos(dotProduct(v1, v2))
    return rotation_matrix(axis, degree(angle))

def rotate_axis_angle_matrix(v1: np.ndarray, v2: np.ndarray) -> np.ndarray:
    axis = crossProduct(v1, v2)
    
    EPSILON = 1e-6

    if dotProduct(axis, axis) < EPSILON:
        return np.identity(3)
    
    axis = normalize(axis)

    m1 = np.array([v1, axis, crossProduct(axis, v1)])
    m1 = np.transpose(m1)

    m2 = np.array([v2, axis, crossProduct(axis, v2)])
    m2 = np.transpose(m2)
    
    m1 = np.linalg.inv(m1)
    return np.dot(m2, m1)

def project_to_plane(
        ray_origin: np.ndarray,
        ray_direction: np.ndarray,
        plane_origin: np.ndarray,
        plane_normal: np.ndarray
    ) -> tuple[bool, float, np.ndarray]:

    line = subtract(plane_origin, ray_origin)
    scale = dotProduct(ray_direction, plane_normal)

    EPSILON = 1e-6

    # DivideByZeroError.
    if -EPSILON < scale < EPSILON:
        return (False, 0, np.array([]))

    hitDistance = dotProduct(line, plane_normal) / scale
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

    hit = hit and dotProduct(ray_direction, plane_normal) < 0
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
        ray_origin, ray_direction, v0, v1, v2)
    
    if hit: return (hit, hitDistance, hitPoint)
    
    (hit, hitDistance, hitPoint) = intersect_triangle(
        ray_origin, ray_direction, v3, v2, v1)
    
    return (hit, hitDistance, hitPoint)

def intersect_triangle_moller_trumbore(
        ray_origin: np.ndarray,
        ray_direction: np.ndarray,
        v0: np.ndarray,
        v1: np.ndarray,
        v2: np.ndarray
    ) -> tuple[bool, float, np.ndarray]:

    hit = False
    hitDistance = 0.0
    hitPoint = np.array([0,0,0])
    
    EPSILON = 1e-4

    edge1 = subtract(v1, v0)
    edge2 = subtract(v2, v0)

    P = crossProduct(ray_direction, edge2)
    determinant = dotProduct(P, edge1)
    if determinant < EPSILON:
        return (hit, hitDistance, hitPoint)
    
    inverseDeterminant = 1 / determinant
    
    T = subtract(ray_origin, v0)
    u_coordinate = inverseDeterminant * dotProduct(P, T)
    if u_coordinate < 0 or 1 < u_coordinate:
        return (hit, hitDistance, hitPoint)

    Q = crossProduct(T, edge1)
    v_coordinate = inverseDeterminant * dotProduct(Q, ray_direction)
    if v_coordinate < 0 or 1 < u_coordinate + v_coordinate:
        return (hit, hitDistance, hitPoint)
    
    hit = True
    hitDistance = inverseDeterminant * dotProduct(Q, edge2)
    hitPoint = ray_origin + hitDistance * ray_direction
    return (hit, hitDistance, hitPoint)

def intersect_triangle(
        ray_origin: np.ndarray,
        ray_direction: np.ndarray,
        v0: np.ndarray,
        v1: np.ndarray,
        v2: np.ndarray
    ) -> tuple[bool, float, np.ndarray]:

    (hit, hitDistance, hitPoint) = intersect_plane(
        ray_origin, ray_direction, v0, normal(v0, v1, v2))
    
    if hit: (hit, _) = point_in_triangle(hitPoint, v0, v1, v2)
    
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

    e1 = subtract(v1, v0)
    e2 = subtract(v2, v0)

    normal = crossProduct(e1, e2)
    normal = normalize(normal)

    EPSILON = 1e-6

    e1 = subtract(v1, v0)
    e2 = subtract(point, v0)
    n0 = crossProduct(e1, e2)
    if dotProduct(normal, n0) < -EPSILON:
        return (False, normal)

    e1 = subtract(v2, v1)
    e2 = subtract(point, v1)
    n1 = crossProduct(e1, e2)
    if dotProduct(normal, n1) < -EPSILON:
        return (False, normal)
    
    e1 = subtract(v0, v2)
    e2 = subtract(point, v2)
    n2 = crossProduct(e1, e2)
    if dotProduct(normal, n2) < -EPSILON:
        return (False, normal)
    
    return (True, normal)

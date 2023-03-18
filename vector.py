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

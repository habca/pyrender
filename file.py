import numpy as np

class File:
    def __init__(self, filename: str):
        self.vertices: list[np.ndarray] = []
        self.triangles: list[int] = []
        self.read_file(filename)

    def read_file(self, filename: str) -> None:
        with open(filename) as reader:
            for line in reader:
                line = line.strip()

                if line == "":
                    continue

                line, *args = line.split()

                if line == "v":
                    self.parse_vertice(args)
                if line == "f":
                    self.parse_triangle(args)

    def parse_vertice(self, args: list[str]) -> None:
        vertice = np.array([float(x) for x in args])
        self.vertices.append(vertice)

    def parse_triangle(self, args: list[str]) -> None:
        triangle = [int(x) for x in args]
        self.triangles.append(triangle[0] - 1)
        self.triangles.append(triangle[2] - 1)
        self.triangles.append(triangle[1] - 1)

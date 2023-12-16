from bestErrors import MathError
import math
import sys


sys.setrecursionlimit(106900420)


pi: float = 3.14159265358979323846264338327950288419716939937510


class square_root:
    """Just to find the square root of given x as a parameter."""

    def __new__(self, x: float) -> str | float:
        if x < 0:
            x = abs(x)
            return f"i * {math.sqrt(x)}"

        try:
            return math.sqrt(x)
        except Exception as e:
            raise MathError(e)


class area:
    """Area of different polygons."""

    class Pentagon:
        def __new__(self, a: float) -> float:
            try:
                return (1 / 4) * math.sqrt(5 * (5 + 2 * math.sqrt(5))) * (a**2)
            except Exception as e:
                raise MathError(e)


class interior_angles_of_polygon:
    def __new__(self, n: int) -> float:
        """The parameter n is the number of sides of the polygon."""
        try:
            return ((n - 2) * 180) / n
        except Exception as e:
            raise MathError(e)


class factorial:
    def __new__(self, __x: float | int) -> int | float:
        if __x in [0, 1]:
            return 1
        else:
            return __x * factorial(__x - 1)

class volume:
    class Cylinder:
        def __new__(self, radius, height) -> int | float:
            volume = pi * radius**2 * height
            return volume
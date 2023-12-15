from bestErrors import MathError
import math


class square_root:
    """Just to find the square root of given x as a parameter."""
    def __new__(self, x: float) -> str | float:
        if x < 0:
            x = abs(x)
            return f'i * {math.sqrt(x)}'
        
        try:
            return math.sqrt(x)
        except Exception as e:
            raise MathError(e)

class area:
    """Area of different polygons."""
    class Pentagon:
        def __new__(self, a: float) -> float:
            try:
                return (1/4) * math.sqrt(5*(5 + 2 * math.sqrt(5))) * (a**2)
            except Exception as e:
                raise MathError(e)

class interior_angles_of_polygon:
    def __new__(self, n: int) -> float:
        """The parameter n is the number of sides of the polygon."""
        try:
            return ((n - 2) * 180)/n
        except Exception as e:
            raise MathError(e)
from cerrors import MathError
import math


class square_root:
    def __new__(self, x: float) -> str | float:
        if x < 0:
            x = abs(x)
            return f'i * {math.sqrt(x)}'
        
        try:
            return math.sqrt(x)
        except Exception as e:
            raise MathError(e)

class area:
    class Pentagon:
        def __new__(self, a: float) -> float:
            try:
                return (1/4) * math.sqrt(5*(5 + 2 * math.sqrt(5))) * (a**2)
            except Exception as e:
                raise MathError(e)
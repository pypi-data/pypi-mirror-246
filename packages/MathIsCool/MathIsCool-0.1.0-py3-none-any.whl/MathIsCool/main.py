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
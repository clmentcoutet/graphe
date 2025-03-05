class MathUtils:
    count : int = 0
    name : str = 2
    base : int

    def factorial(self, n) -> int:
        if n > 0:
            return n * self.factorial(n - 1)
        else:
            return 1
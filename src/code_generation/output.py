@staticmethod
def factorial(n):
    if n > 0:
        return n * factorial(n - 1)
    else:
        return 1


def is_positive(x):
    if x > 0:
        return True
    else:
        return not-x > 0
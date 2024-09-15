from abc import ABC, abstractmethod


class Composite(ABC):
    functions = None

    @staticmethod
    @abstractmethod
    def simulate(N):
        pass

    @classmethod
    def real(cls, N):
        value = N
        for function in cls.functions:
            try:
                value = function(value)
            except Exception:
                print(f"Warning: Case uncovered {cls},{N}")
        return value

    @classmethod
    def get_string_length(cls):
        names = len(cls.functions)
        parentheses = names * 2
        name_characters = sum([len(x.__name__) for x in cls.functions])
        return parentheses + name_characters

    @staticmethod
    def guard(N):
        return True

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.functions is None:
            raise NotImplementedError(
                f"Class variable 'required_class_variable' must be overridden in {cls.__name__}"
            )


class RsetSL(Composite):
    functions = (range, set, str, len)

    @staticmethod
    def simulate(N):
        if N == 0:
            return 5

        N = N - 1
        commas_and_spaces = max(0, (N) * 2)
        parentheses = 2

        digits = 0
        start = 1
        num_digits = 1

        while start <= N:
            end = min(N, 10**num_digits - 1)
            count = end - start + 1
            digits += count * num_digits
            start *= 10
            num_digits += 1

        digits += 1  # (0)

        total_length = commas_and_spaces + parentheses + digits
        return total_length


class Rsum(Composite):
    functions = (range, sum)

    @staticmethod
    def simulate(N):
        N -= 1
        return (N * (N + 1)) // 2


class RrevIN(Composite):
    functions = (range, reversed, iter, next)

    @staticmethod
    def simulate(N):
        return N - 1

    @staticmethod
    def guard(N):
        return N > 0


def test_accuracy(composite, values):
    for N in values:
        simulated = composite.simulate(N)
        real = composite.real(N)
        assert simulated == real, f"Failed on {N}, {simulated} != {real}"
    print(f"{composite.__name__} test passed")


if __name__ == "__main__":
    test_accuracy(RsetSL, list(range(10000)))
    test_accuracy(Rsum, list(range(10000)))
    test_accuracy(RrevIN, list(range(1, 10000)))

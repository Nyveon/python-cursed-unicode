from composites import RsetSL


def test_string_lengths(composite, values):
    for N in values:
        assert composite.simulate(N) == composite.real(N)
    

test_string_lengths()
class function:
    pass


class wave(function):
    def __init__(self, frequency, phase):
        self.frequency = frequency
        self.phase = phase
        name = f"Wave[frequency={frequency:4.2f}, phase={phase:4.2f}]"
        fun = lambda x: np.sin(2 * np.pi * frequency * x + phase)
        dfun = constant(2 * np.pi * frequency) * wave(frequency, phase + np.pi / 2)
        super().__init__(name, fun, dfun)


class zero(function):
    def __init__(self):
        name = "Zero"
        fun = lambda x: 0 if np.isscalar(x) else np.zeros_like(x)
        dfun = zero()
        super().__init__(name, fun, dfun)


class constant(function):
    def __init__(self, c):
        name = f"Constant[c={c:4.2f}]"
        fun = lambda x: c if np.isscalar(x) else np.full_like(x, c)
        dfun = zero()
        super().__init__(name, fun, dfun)


class monomial(function):
    def __init__(self, k):
        if k == 0:
            raise ValueError("k must be greater than 0")
        name = f"Monomial[k={k}]"
        fun = lambda x: x**k
        dfun = constant(k) * monomial(k - 1) if k > 1 else constant(1)
        super().__init__(name, fun, dfun)


class exponential(function):
    def __init__(self, alpha):
        name = f"Exponential[alpha={alpha:4.2f}]"
        fun = lambda x: np.exp(alpha * x)
        dfun = constant(alpha) * exponential(alpha)
        super().__init__(name, fun, dfun)


class affine(function):
    def __init__(self, alpha, beta):
        name = f"Affine[alpha={alpha:4.2f}, beta={beta:4.2f}]"
        fun = lambda x: alpha * x + beta
        dfun = constant(alpha)
        super().__init__(name, fun, dfun)


class logarithm(function):
    def __init__(self, base):
        name = f"Logarithm"
        fun = lambda x: np.log(x) / np.log(base)
        dfun = inverse(affine(1.0, 0.0))
        super().__init__(name, fun, dfun)


class plus(function):
    def __init__(self, f1, f2):
        name = f"({f1.name} + {f2.name})"
        fun = lambda x: f1(x) + f2(x)
        dfun = function(name, fun, f1.diff() + f2.diff())
        super().__init__(name, fun, dfun)


class times(function):
    def __init__(self, f1, f2):
        name = f"({f1.name} * {f2.name})"
        fun = lambda x: f1(x) * f2(x)
        dfun = function(name, fun, f1.diff() * f2 + f1 * f2.diff())
        super().__init__(name, fun, dfun)


class inverse(function):
    def __init__(self, f):
        name = f"1 / ({f.name})"
        fun = lambda x: 1 / f(x)
        dfun = function(
            name, fun, constant(-1) * f.diff() / composition(monomial(2), f)
        )
        super().__init__(name, fun, dfun)


class composition(function):
    def __init__(self, f1, f2):
        name = f"({f1.name}) o ({f2.name})"
        fun = lambda x: f1(f2(x))
        dfun = function(name, fun, composition(f1.diff(), f2) * f2.diff())
        super().__init__(name, fun, dfun)

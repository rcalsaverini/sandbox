import marimo

__generated_with = "0.3.10"
app = marimo.App()


@app.cell
def __():
    from sympy import Symbol, simplify
    from numpy.random import uniform, choice
    from dataclasses import dataclass, field
    return Symbol, choice, dataclass, field, simplify, uniform


@app.cell
def __():
    return


@app.cell
def __(choice, uniform):
    def cascade(fns, p=0.5):
        def cascade(*vars):
            if len(fns) > 1:
                head, *tails = fns
                if uniform() < p:
                    return head(vars)
                else:
                    return cascade(tails, p=p)(vars)
            elif len(fns) == 1:
                fn = fns[0]
                return fn()
        return cascade

    def one_of(symbols):
        return lambda *vars: choice(symbols)

    def concat(left, right):
        return lambda *vars: f"{left()}{right()}"
    return cascade, concat, one_of


@app.cell
def __(Symbol, cascade, concat, digits0, digits1, one_of):
    def word(*vars):
        print(vars)
        return primary(*vars)

    digit0 = one_of(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
    digit1 = one_of(["1", "2", "3", "4", "5", "6", "7", "8", "9"])
    digits0 = cascade([digit0, concat(digits0, digit0)])
    digits1 = cascade([digit1, concat(digits1, digit0)])

    number = cascade([
        lambda *vars: float(digits1() + "." +digits0()),
        lambda *vars: int(digits1()),
        lambda *vars: float("0." + digits0()),
        lambda *vars: 0
    ])


    primary = lambda *vars: cascade([
            lambda *vars: number(vars), 
            lambda *vars: -number(vars),
            one_of([Symbol(var) for var in vars])
        ], p=0.5)


    # expneg = lambda *vars: cascade([
    #     lambda *varsprimary,
    #     lambda
            
    # ])
    return digit0, digit1, digits0, digits1, number, primary, word


@app.cell
def __(primary):
    for _ in range(10): 
        x = primary("x", "y")
        print(type(x), x)
    return x,


@app.cell
def __():
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()

def diff(e):
    if isinstance(e, str):
        return 1
    if not isinstance(e, tuple):
        return 0
    op, a, b = e
    da, db = diff(a), diff(b)
    if op == "+":
        return simp(("+", da, db))
    if op == "-":
        return simp(("-", da, db))
    if op == "*":
        return simp(("+", ("*", da, b), ("*", a, db)))
    if op == "/":
        return simp(("/", ("-", ("*", da, b), ("*", a, db)), ("*", b, b)))
    if op == "^":
        return simp(("*", ("*", b, ("^", a, b - 1)), da))


def simp(e):
    if isinstance(e, str) or not isinstance(e, tuple):
        return e
    op, a, b = e
    a, b = simp(a), simp(b)
    if isinstance(a, int) and isinstance(b, int):
        if op == "+":
            return a + b
        if op == "-":
            return a - b
        if op == "*":
            return a * b
        if op == "/" and b and a % b == 0:
            return a // b
    if op == "+":
        if a == 0:
            return b
        if b == 0:
            return a
    if op == "-":
        if b == 0:
            return a
    if op == "*":
        if a == 0 or b == 0:
            return 0
        if a == 1:
            return b
        if b == 1:
            return a
    if op == "/":
        if a == 0:
            return 0
        if b == 1:
            return a
    if op == "^" and b == 1:
        return a
    return (op, a, b)


def to_str(e):
    if isinstance(e, str):
        return e
    if not isinstance(e, tuple):
        return str(e)
    op, a, b = e
    sym = "**" if op == "^" else op
    return f"({to_str(a)} {sym} {to_str(b)})"


def run(e):
    print(f"  expr    = {to_str(e)}")
    print(f"  d/dx    = {to_str(diff(e))}\n")


print("符號微分 sym_diff(expr)\n")
run(("^", "x", 2))
run(("+", ("^", "x", 2), ("*", 3, "x")))
run(("/", 1, "x"))
run(("*", ("^", "x", 3), ("+", "x", 1)))

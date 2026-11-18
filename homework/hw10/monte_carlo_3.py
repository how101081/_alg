"""
第10週習題 3 - n 變數數值微分(梯度)與積分(超體積)
梯度用中心差分，超體積用 n 維方格的中點黎曼和。
"""

from itertools import product
from math import prod


def gradient(f, x, h=1e-5):
    """對每一個變數做中心差分，回傳梯度向量。"""
    g = []
    for i in range(len(x)):
        a, b = list(x), list(x)
        a[i] -= h
        b[i] += h
        g.append((f(b) - f(a)) / (2 * h))
    return g


def integral_grid(f, low, high, steps=10):
    """n 維積分：每一軸切 steps 等分，取格子中點的函數值加總。"""
    n = len(low)
    dx = [(high[i] - low[i]) / steps for i in range(n)]
    centers = [[low[i] + (j + 0.5) * dx[i] for j in range(steps)] for i in range(n)]
    return sum(f(p) for p in product(*centers)) * prod(dx)


if __name__ == "__main__":
    f = lambda p: p[0] ** 2 + p[1] ** 2 + p[2] ** 2

    print("n 變數數值微分與積分")
    print("f(x,y,z) = x^2 + y^2 + z^2")
    print(f"  grad f(1,2,3) = {gradient(f, (1, 2, 3))}  (精確值 (2, 4, 6))")
    vol = integral_grid(f, (0, 0, 0), (1, 1, 1))
    print(f"  ∫[0,1]^3 f dV = {vol:.6f}  (精確值 1)")

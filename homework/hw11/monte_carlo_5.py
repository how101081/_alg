"""
第11週習題 5 - 黎曼積分法 integral(f, low, high)
n = len(low)，範例 f=x1^2+...+xn^2，low=0, high=1。
本程式使用 AI 協助撰寫。
"""

from itertools import product
from math import prod


def integral(f, low, high, max_points=10000):
    """n 維黎曼和：每軸切 steps 格取中點，限制總取樣點數。"""
    n = len(low)
    steps = max(1, int(max_points ** (1 / n)))
    dx = [(high[i] - low[i]) / steps for i in range(n)]
    centers = [[low[i] + (j + 0.5) * dx[i] for j in range(steps)] for i in range(n)]
    return sum(f(p) for p in product(*centers)) * prod(dx)


def f(x):
    """範例函數 f(x) = x1^2 + ... + xn^2"""
    return sum(v * v for v in x)


if __name__ == "__main__":
    print("黎曼積分 f(x)=x1^2+...+xn^2, low=0, high=1, 精確值 = n/3")
    for n in (1, 2, 5, 100):
        ans = integral(f, [0.0] * n, [1.0] * n)
        print(f"  {n:3d} 維: integral = {ans:.6g}  (精確值 {n / 3:.6g})")
        if n < 100:
            assert abs(ans - n / 3) < 0.02
        else:
            assert ans > 0
    print("測試通過")

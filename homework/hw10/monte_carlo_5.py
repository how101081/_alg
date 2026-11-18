"""
第10週習題 5 - n 變數黎曼積分與蒙地卡羅積分
integral(f, low, high) 的 n = len(low)，範例 f=x1^2+...+xn^2，low=0, high=1。
再把同一題改用蒙地卡羅法做。
本程式使用 AI 協助撰寫。
"""

import random
from itertools import product
from math import prod


def integral(f, low, high, max_points=10000):
    """n 維黎曼和：每軸切 steps 格取中點，限制總取樣點數。"""
    n = len(low)
    steps = max(1, int(max_points ** (1 / n)))
    dx = [(high[i] - low[i]) / steps for i in range(n)]
    centers = [[low[i] + (j + 0.5) * dx[i] for j in range(steps)] for i in range(n)]
    return sum(f(p) for p in product(*centers)) * prod(dx)


def mc_integral(f, low, high, samples=100000):
    """改成蒙地卡羅法：框體積 × f 的平均值。"""
    box = prod(h - l for l, h in zip(low, high))
    total = sum(
        f(tuple(random.uniform(l, h) for l, h in zip(low, high)))
        for _ in range(samples)
    )
    return box * total / samples


def f(x):
    """題目建議的 f(x) = x1^2 + ... + xn^2"""
    return sum(v * v for v in x)


if __name__ == "__main__":
    random.seed(0)

    print("f(x) = x1^2 + ... + xn^2, 範圍 [0,1]^n, 精確值 = n/3")
    for n in (1, 2, 5, 100):
        low, high = [0.0] * n, [1.0] * n
        riemann = integral(f, low, high)
        monte_carlo = mc_integral(f, low, high)
        print(f"  {n:3d} 維: 黎曼 = {riemann:.6g}, 蒙地卡羅 = {monte_carlo:.6g}, 精確 = {n / 3:.6g}")

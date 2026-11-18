"""
第11週習題 6 - 蒙地卡羅法做 n 變數積分
與第 5 題相同：f=x1^2+...+xn^2，low=0, high=1，改用蒙地卡羅法。
本程式使用 AI 協助撰寫。
"""

import random
from math import prod


def mc_integral(f, low, high, samples=100000):
    """n 維蒙地卡羅積分：框體積 × f 的平均值。"""
    box = prod(h - l for l, h in zip(low, high))
    total = sum(
        f(tuple(random.uniform(l, h) for l, h in zip(low, high)))
        for _ in range(samples)
    )
    return box * total / samples


def f(x):
    """範例函數 f(x) = x1^2 + ... + xn^2"""
    return sum(v * v for v in x)


if __name__ == "__main__":
    random.seed(0)

    print("蒙地卡羅 n 變數積分 f(x)=x1^2+...+xn^2, low=0, high=1")
    for n in (1, 2, 5, 100):
        ans = mc_integral(f, [0.0] * n, [1.0] * n)
        exact = n / 3
        print(f"  {n:3d} 維: mc_integral = {ans:.6g}  (精確值 {exact:.6g})")
        assert abs(ans - exact) < 0.02 * n
    print("測試通過")

"""
第10週習題 4 - 蒙地卡羅法算 n 變數積分(超體積)
在 n 維框框內隨機撒點，用「框體積 × 命中比例」估計積分或球體體積。
本程式使用 AI 協助撰寫。
"""

import math
import random


def mc_integral(f, low, high, samples=100000):
    """n 維蒙地卡羅積分：框體積 × f 的平均值。"""
    box = math.prod(h - l for l, h in zip(low, high))
    total = sum(
        f(tuple(random.uniform(l, h) for l, h in zip(low, high)))
        for _ in range(samples)
    )
    return box * total / samples


def ball_volume(n, radius=1, samples=100000):
    """用 [-r,r]^n 包住 n 維球，數落入球內的點估計體積。"""
    low, high = [-radius] * n, [radius] * n
    inside = lambda p: 1.0 if sum(x * x for x in p) <= radius * radius else 0.0
    return mc_integral(inside, low, high, samples)


if __name__ == "__main__":
    random.seed(0)

    print("蒙地卡羅 n 維積分 (100000 個樣本)")
    for n in (2, 3, 5):
        exact = math.pi ** (n / 2) / math.gamma(n / 2 + 1)
        print(f"  {n} 維單位球體積 = {ball_volume(n):.6f}  (精確值 {exact:.6f})")

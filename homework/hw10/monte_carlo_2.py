"""
第10週習題 2 - 蒙地卡羅法算單變數積分
在 [low, high] 均勻隨機取樣，用「平均值 × 區間長度」估計積分。
本程式使用 AI 協助撰寫。
"""

import math
import random


def mc_integral(f, low, high, samples=100000):
    """蒙地卡羅積分：∫f(x)dx ≈ (high - low) × f 的平均值。"""
    total = sum(f(random.uniform(low, high)) for _ in range(samples))
    return (high - low) * total / samples


if __name__ == "__main__":
    random.seed(0)

    print("蒙地卡羅單變數積分 (100000 個樣本)")
    ans = mc_integral(math.sin, 0, math.pi)
    print(f"  ∫[0,π] sin(x) dx = {ans:.6f}  (精確值 2)")
    ans = mc_integral(lambda x: x ** 2, 0, 1)
    print(f"  ∫[0,1] x^2 dx     = {ans:.6f}  (精確值 {1/3:.6f})")

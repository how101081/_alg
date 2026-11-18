"""
第11週習題 1 - 單變數數值微分與積分
中心差分算微分，梯形法算積分，只使用 Python 標準函式庫。
本程式使用 AI 協助撰寫。
"""

import math


def derivative(f, x, h=1e-5):
    """中心差分：f'(x) ≈ (f(x+h) - f(x-h)) / (2h)"""
    return (f(x + h) - f(x - h)) / (2 * h)


def integrate(f, low, high, n=1000):
    """梯形法：把 [low, high] 切成 n 個小梯形後加總。"""
    dx = (high - low) / n
    total = (f(low) + f(high)) / 2
    for i in range(1, n):
        total += f(low + i * dx)
    return total * dx


if __name__ == "__main__":
    f = lambda x: x ** 2 + 3 * x + 1
    g = math.sin

    print("單變數數值微分與積分")
    print(f"f(x) = x^2 + 3x + 1")
    print(f"  f'(2)        = {derivative(f, 2):.6f}  (精確值 7)")
    print(f"  ∫[0,1] f(x)dx = {integrate(f, 0, 1):.6f}  (精確值 {1/3 + 3/2 + 1:.6f})")
    print("g(x) = sin(x)")
    print(f"  g'(1)        = {derivative(g, 1):.6f}  (精確值 {math.cos(1):.6f})")
    print(f"  ∫[0,π] g(x)dx = {integrate(g, 0, math.pi):.6f}  (精確值 2)")

    assert abs(derivative(f, 2) - 7) < 1e-4
    assert abs(integrate(f, 0, 1) - (1 / 3 + 3 / 2 + 1)) < 1e-4
    assert abs(derivative(g, 1) - math.cos(1)) < 1e-4
    assert abs(integrate(g, 0, math.pi) - 2) < 1e-4
    print("測試通過")

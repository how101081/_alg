def f(x):
    return x * x - 2


def df(x):
    return 2 * x


def newton(f, df, x0):
    x = x0
    for i in range(20):
        x1 = x - f(x) / df(x)
        print(f"第 {i+1:2d} 次: x = {x1:.10f}")
        if abs(x1 - x) < 1e-10:
            break
        x = x1
    return x


print("用牛頓法求 x^2 - 2 = 0 的根（也就是 √2）\n")
root = newton(f, df, 1.0)
print(f"\n答案: x = {root:.10f}   (√2 = {2**0.5:.10f})")
import time


def power2n1(n):
    """方法 1：直接用 2**n"""
    return 2**n


def power2n2a(n):
    """方法 2a：用遞迴 power2n(n-1)+power2n(n-1)"""
    if n == 0:
        return 1
    return power2n2a(n - 1) + power2n2a(n - 1)


def power2n2b(n):
    """方法 2b：用遞迴 2*power2n(n-1)"""
    if n == 0:
        return 1
    return 2 * power2n2b(n - 1)


table = {0: 1}


def power2n3(n):
    """方法 3：用遞迴+查表 (memoization)"""
    if n in table:
        return table[n]
    table[n] = power2n3(n - 1) + power2n3(n - 1)
    return table[n]


def time_it(label, fn, n):
    start = time.perf_counter()
    value = fn(n)
    elapsed = time.perf_counter() - start
    digits = len(str(value))
    print(f"{label:10s} n={n:3d} 結果為 {digits} 位數  耗時 {elapsed:.6f} 秒")
    return elapsed


def main():
    N = 100
    print(f"測試 n = {N}")
    print("-" * 60)

    time_it("方法 1", power2n1, N)

    time_it("方法 2b", power2n2b, N)

    time_it("方法 3", power2n3, N)

    print("-" * 60)
    print("方法 2a 呼叫次數為 2^100 ≈ 1.27e30 次，跑不完，")
    print("所以只測小 n 讓你看它到底有多慢:")
    small_n = 24
    start = time.perf_counter()
    value = power2n2a(small_n)
    elapsed = time.perf_counter() - start
    print(f"方法 2a  n={small_n:3d} 結果為 {len(str(value))} 位數  耗時 {elapsed:.6f} 秒")
    print(f"推估 n=100 需要約 {elapsed * 2**76 / 3600 / 24 / 365:.2e} 年")

    print("-" * 60)
    print("結果: 方法 1、2b、3 都很快，唯獨方法 2a 出不來!")


if __name__ == "__main__":
    main()
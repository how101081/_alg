def T1(n):
    if n == 1:
        return 1
    return T1(n - 1) + 8


def T2(n):
    if n == 1:
        return 1
    return 2 * T2(n - 1) + 9


def T3(n):
    if n == 1:
        return 1
    return 2 * T3(n // 2) + 1


def T4(n):
    if n == 1:
        return 1
    return T4(n // 2) + 1


def closed1(n):
    return 8 * n - 7


def closed2(n):
    return 10 * (2 ** (n - 1)) - 9


def closed3(n):
    return 2 * n - 1


def closed4(n):
    return n.bit_length()


def main():
    print("=== 遞迴方程式: 精確解 vs 封閉解驗證 ===")

    print("\n1. T(n) = T(n-1) + 8, T(1) = 1")
    for n in [1, 2, 5, 10, 100]:
        assert T1(n) == closed1(n), n
    print(f"   精確解 T(n) = 8n - 7   (例 T(100) = {T1(100)})")
    print("   複雜度: O(n)")

    print("\n2. T(n) = 2T(n-1) + 9, T(1) = 1")
    for n in [1, 2, 5, 10, 20]:
        assert T2(n) == closed2(n), n
    print(f"   精確解 T(n) = 10*2^(n-1) - 9   (例 T(20) = {T2(20)})")
    print("   複雜度: O(2^n)")

    print("\n3. T(n) = 2T(n/2) + 1, T(1) = 1")
    for n in [1, 2, 4, 8, 16, 1024]:
        assert T3(n) == closed3(n), n
    print(f"   精確解 T(n) = 2n - 1 (n 為 2 的冪)   (例 T(1024) = {T3(1024)})")
    print("   複雜度: O(n)")

    print("\n4. T(n) = T(n/2) + 1, T(1) = 1")
    for n in [1, 2, 4, 8, 16, 1024]:
        assert T4(n) == closed4(n), n
    print(f"   精確解 T(n) = log2(n) + 1 (n 為 2 的冪)   (例 T(1024) = {T4(1024)})")
    print("   複雜度: O(log n)")

    print("\n全部驗證通過!")


if __name__ == "__main__":
    main()
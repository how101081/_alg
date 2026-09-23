from itertools import product


def all_assignments(n):
    return product((0, 1), repeat=n)


def eval_clause(clause, a):
    """clause = [literal...]，literal 正 v 表 x_v，負 -v 表 not x_v"""
    for lit in clause:
        v = abs(lit) - 1
        if lit > 0 and a[v] == 1:
            return True
        if lit < 0 and a[v] == 0:
            return True
    return False


def eval_cnf(cnf, a):
    """cnf = [clause...]，各 clause 之間是 AND"""
    return all(eval_clause(c, a) for c in cnf)


def print_truth_table(n, cnf):
    header = " | ".join(f"x{i+1}" for i in range(n)) + " | F"
    print("  " + header)
    print("  " + "-" * len(header))
    for a in all_assignments(n):
        val = eval_cnf(cnf, a)
        assign = " | ".join(str(x) for x in a)
        print(f"  {assign} | {1 if val else 0}")


def sat(n, cnf):
    solutions = [a for a in all_assignments(n) if eval_cnf(cnf, a)]
    return solutions


def demo(title, n, cnf):
    print("=" * 55)
    print(title)
    print("=" * 55)
    print("\n真值表 (系統性列舉所有 2^n 組指派):")
    print_truth_table(n, cnf)
    solutions = sat(n, cnf)
    print()
    if solutions:
        print(f"有解 (SAT)! 滿足的指派共 {len(solutions)} 組:")
        for s in solutions[:10]:
            print("   " + ", ".join(f"x{i+1}={s[i]}" for i in range(n)))
    else:
        print(f"無解 (UNSAT)! 所有 2^{n} = {2**n} 種指派都讓 F = 0")
    print()


def main():
    print("# 用真值表暴力解 SAT 問題 (3-SAT 可列舉，更大則太慢)\n")

    demo("範例 1: F = (x1 ∨ x2) ∧ (¬x1 ∨ ¬x2)  [互斥 OR]", 2,
         [[1, 2], [-1, -2]])

    demo("範例 2: F = x1 ∧ ¬x1  [矛盾，一定沒解]", 1,
         [[1], [-1]])

    demo("範例 3: F = (x1 ∨ x2) ∧ (¬x1 ∨ x2) ∧ (x1 ∨ ¬x2)",
         2, [[1, 2], [-1, 2], [1, -2]])

    demo("範例 4: 三角形的 2-著色問題 (x1≠x2, x2≠x3, x1≠x3)  [不可能]",
         3, [[1, 2], [-1, -2], [2, 3], [-2, -3], [1, 3], [-1, -3]])


if __name__ == "__main__":
    main()
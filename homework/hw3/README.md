# 第三週習題：列舉＋暴力 — 用真值表解 SAT 問題

課程：演算法 | 學生：楊丞皓 | 學號：06

## 題目來源
[ccc115a/_alg Issue #5](https://github.com/ccc115a/_alg/issues/5)

> 請寫一個程式可以系統性的列舉真值表，解決 SAT 問題
> [SAT 問題（Wikipedia）](https://en.wikipedia.org/wiki/Boolean_satisfiability_problem)

## 什麼是 SAT 問題

布林可滿足性問題（Boolean Satisfiability Problem, SAT）：給定一個由多個子句（clause）組成的布林公式
（每個子句由變數的 OR 組成，子句之間用 AND 相連），問是否存在一組變數指派（每個變數只能為
0 或 1）讓整個公式為真。

## 作法：暴力列舉（Brute Force / 真值表法）

若有 n 個布林變數，真值表有 2^n 組指派。

1. 用 `itertools.product((0, 1), repeat=n)` 系統性列舉全部 2^n 種指派。
2. 逐一把每組指派帶入公式求值。
3. 只要有一組使 F = 1 就是 **SAT（有解）**；全部都是 0 就是 **UNSAT（無解）**。

因為是暴力搜尋，時間複雜度為 **O(2^n · m)**（n 個變數、m 個子句）——n 一超過 30 左右就跑不動，這正是 SAT 是 NP 問題的原因。

## 支援的公式表示法（CNF）

- literal（文字）：正整數 `v` 代表 `x_v`，負整數 `-v` 代表 `not x_v`
- clause（子句）：`[v1, v2, ...]`，彼此是 OR
- cnf（公式）：`[[...], [...], ...]`，各子句之間是 AND

例如 `(x1 ∨ x2) ∧ (¬x1 ∨ ¬x2)` 寫成 `[[1, 2], [-1, -2]]`。

## 程式說明

| 函式 | 功能 |
|------|------|
| `all_assignments(n)` | 系統性列舉全部 2^n 種指派 |
| `eval_clause(clause, a)` | 計算一個子句的值 |
| `eval_cnf(cnf, a)` | 計算整個公式的值 |
| `print_truth_table(n, cnf)` | 印出完整真值表 |
| `sat(n, cnf)` | 回傳所有滿足的指派 |

## 執行結果摘要

```
範例 1: F = (x1 ∨ x2) ∧ (¬x1 ∨ ¬x2)  → 有解! (0,1) 與 (1,0)
範例 2: F = x1 ∧ ¬x1                 → 無解! 2 種指派全為 0
範例 3: F = (x1∨x2)(¬x1∨x2)(x1∨¬x2) → 有解! 只有 (1,1)
範例 4: 三角形 2-著色 (x1≠x2, x2≠x3, x1≠x3) → 無解! 8 種指派全為 0
```

## 如何執行

```bash
python sat.py
```
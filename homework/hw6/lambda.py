# 第六週習題：Lambda Calculus 解譯器
# 只有三種東西：變數 x、函數 \x.body、套用 (f a)
# 做法就是「最左最外優先」一步一步做 beta reduction，把過程全印出來

import re

# ---------- 語法樹 ----------
class Var:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Lam:
    def __init__(self, var, body):
        self.var = var
        self.body = body

    def __str__(self):
        return f"(λ{self.var}.{self.body})"


class App:
    def __init__(self, fn, arg):
        self.fn = fn
        self.arg = arg

    def __str__(self):
        return f"({self.fn} {self.arg})"


# ---------- 解析器 ----------
def tokenize(s):
    return re.findall(r"\\|λ|\.|\(|\)|[A-Za-z0-9_]+", s)


def parse(s):
    tokens = tokenize(s)
    pos = [0]

    def peek():
        return tokens[pos[0]] if pos[0] < len(tokens) else None

    def take():
        t = tokens[pos[0]]
        pos[0] += 1
        return t

    def atom():
        t = take()
        if t == "(":
            e = expr()
            take()  # 吃掉 ')'
            return e
        return Var(t)

    def expr():
        if peek() in ("\\", "λ"):  # 函數
            take()
            v = take()
            take()  # 吃掉 '.'
            return Lam(v, expr())
        e = atom()  # 套用：一直黏到右邊
        while peek() is not None and peek() != ")":
            e = App(e, atom())
        return e

    return expr()


# ---------- 取代（小心變數被吃掉，所以必要時改名）----------
def free(e):
    if isinstance(e, Var):
        return {e.name}
    if isinstance(e, Lam):
        return free(e.body) - {e.var}
    return free(e.fn) | free(e.arg)


def subst(e, var, val):
    if isinstance(e, Var):
        return val if e.name == var else e
    if isinstance(e, Lam):
        if e.var == var:
            return e
        if e.var in free(val):  # 會撞名就先改名
            new = e.var + "1"
            return subst(Lam(new, subst(e.body, e.var, Var(new))), var, val)
        return Lam(e.var, subst(e.body, var, val))
    return App(subst(e.fn, var, val), subst(e.arg, var, val))


# ---------- reduction ----------
def step(e):
    # 找最左最外的 redex 做一次 beta reduction，沒有就回 None
    if isinstance(e, App):
        if isinstance(e.fn, Lam):
            return subst(e.fn.body, e.fn.var, e.arg)
        r = step(e.fn)
        if r is not None:
            return App(r, e.arg)
        r = step(e.arg)
        if r is not None:
            return App(e.fn, r)
        return None
    if isinstance(e, Lam):
        r = step(e.body)
        return Lam(e.var, r) if r is not None else None
    return None


def run(e, limit=60):
    print(f"  {e}")
    for _ in range(limit):
        nxt = step(e)
        if nxt is None:
            print("  （沒有可化簡的了，這就是答案）")
            return e
        print(f"= {nxt}")
        e = nxt
    print("  （跑太久了，停下來）")
    return e


# ---------- 讓程式好讀的「名稱」層 ----------
MACROS = {
    "TRUE": r"\x.\y.x",
    "FALSE": r"\x.\y.y",
    "AND": r"\p.\q.p q p",
    "SUCC": r"\n.\f.\x.f (n f x)",
    "ADD": r"\m.\n.\f.\x.m f (n f x)",
    "1": r"\f.\x.f x",
    "2": r"\f.\x.f (f x)",
}


def expand(s):
    out = []
    for t in tokenize(s):
        out.append("(" + MACROS[t] + ")" if t in MACROS else t)
    return " ".join(out)


def demo(title, code):
    print(f"\n===== {title} =====")
    print(f"原始輸入: {code}")
    run(parse(expand(code)))


if __name__ == "__main__":
    # 1. 身分函數，套用後就變回原來那個
    demo(r"身分函數：(\x.x) 套用 (\y.y)", r"(\x.x) (\y.y)")

    # 2. 邏輯運算：TRUE AND FALSE = FALSE
    demo("邏輯：TRUE AND FALSE", "AND TRUE FALSE")

    # 3. 後繼函數：SUCC 1 應該等於 2
    demo("後繼：SUCC 1 → 2", "SUCC 1")

    # 4. 加法：ADD 1 1 應該等於 2
    demo("加法：ADD 1 1 → 2", "ADD 1 1")

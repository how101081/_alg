# 第七週習題：正規表達式比對（grep） -- 動態規劃 vs NFA 模擬
# 支援的語法：字面字元、'.'（任意一個字元）、'*'（前一個字元出現 0 次或多次）
# 方法一 match_dp  ：自底往上的動態規劃表格
# 方法二 match_nfa ：Thompson NFA + 狀態集合逐步推進（非動態規劃）

import time

# ======================================================================
# 共用：把 pattern 切成 token，每個 token 是 (字元, 有沒有*)
# ======================================================================
def tokenize(p):
    toks = []
    i = 0
    while i < len(p):
        c = p[i]
        i += 1
        if c == "*":
            raise ValueError("'*' 前面必須先有一個字元，例如 a* 而不是 *a")
        star = False
        if i < len(p) and p[i] == "*":
            star = True
            i += 1
        toks.append((c, star))
    return toks


def char_ok(c, ch):
    return c == "." or c == ch


# ======================================================================
# 方法一：動態規劃
# dp[i][j] = s 的前 i 個字元，能不能被 pattern 的前 j 個 token 匹配
# ======================================================================
def match_dp(s, p, show=False):
    toks = tokenize(p)
    n, m = len(s), len(toks)
    dp = [[False] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = True  # 空字串配空 pattern

    # 第一列：空字串，只有全部都是「0 次」的 * 才可能為真
    for j in range(1, m + 1):
        c, star = toks[j - 1]
        dp[0][j] = dp[0][j - 1] if star else False

    # 一格一格往右下填
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            c, star = toks[j - 1]
            if star:
                zero = dp[i][j - 1]                       # 這個 * 用 0 次
                more = char_ok(c, s[i - 1]) and dp[i - 1][j]  # 再多吃一個字元
                dp[i][j] = zero or more
            else:
                dp[i][j] = char_ok(c, s[i - 1]) and dp[i - 1][j - 1]

    if show:
        print_dp_table(s, toks, dp)
    return dp[n][m]


def print_dp_table(s, toks, dp):
    head = ["ε"] + [c + ("*" if star else "") for c, star in toks]
    width = max(4, max(len(h) for h in head) + 1)
    print("      " + "".join(h.rjust(width) for h in head))
    for i in range(len(dp)):
        row = (s[:i] if s[:i] else "ε")
        cells = "".join(("T" if v else "F").rjust(width) for v in dp[i])
        print(f"  {row:>3} |{cells}")


# ======================================================================
# 方法二：NFA（Thompson 結構）
# 狀態只有三種：eps（不吃字元的分支）、ch（吃一個字元）、end（接受）
# ======================================================================
class NFA:
    def __init__(self):
        self.kind = []
        self.c = []
        self.eps = []
        self.tgt = []

    def add_eps(self):
        self.kind.append("eps")
        self.c.append(None)
        self.eps.append([])
        self.tgt.append(None)
        return len(self.kind) - 1

    def add_ch(self, c):
        self.kind.append("ch")
        self.c.append(c)
        self.eps.append(None)
        self.tgt.append(None)
        return len(self.kind) - 1

    def add_end(self):
        self.kind.append("end")
        self.c.append(None)
        self.eps.append(None)
        self.tgt.append(None)
        return len(self.kind) - 1


def link(nfa, pending, target):
    # 把上一段留下來的「洞」接到 target
    for sid, slot in pending:
        if slot == "eps":
            nfa.eps[sid].append(target)
        else:
            nfa.tgt[sid] = target


def build_nfa(p):
    nfa = NFA()
    end = nfa.add_end()
    start = None
    pending = []  # 還沒接起來的出口: (狀態編號, 'eps'|'ch')

    for c, star in tokenize(p):
        if not star:
            s = nfa.add_ch(c)
            if start is None:
                start = s
            link(nfa, pending, s)
            pending = [(s, "ch")]  # 這個字元吃完後要接下一段
        else:
            sp = nfa.add_eps()  # 分岔點：進迴圈 或 跳過
            if start is None:
                start = sp
            link(nfa, pending, sp)
            inner = nfa.add_ch(c)
            nfa.eps[sp].append(inner)  # 分支1：吃一個字元
            nfa.tgt[inner] = sp        # 吃完回到分岔點（形成迴圈）
            pending = [(sp, "eps")]    # 分支2：直接跳過整個 star

    if start is None:
        start = end  # 空 pattern
    link(nfa, pending, end)
    return nfa, start, end


def eps_closure(nfa, states):
    # 把所有不吃字元就能到達的狀態一起收進來
    seen = set(states)
    stack = list(states)
    while stack:
        s = stack.pop()
        if nfa.kind[s] == "eps":
            for t in nfa.eps[s]:
                if t not in seen:
                    seen.add(t)
                    stack.append(t)
    return seen


def match_nfa(s, p):
    nfa, start, end = build_nfa(p)
    cur = eps_closure(nfa, {start})  # 目前活著的狀態集合
    for ch in s:
        nxt = set()
        for st in cur:
            if nfa.kind[st] == "ch" and char_ok(nfa.c[st], ch):
                nxt.add(nfa.tgt[st])
        if not nxt:
            return False  # 沒有狀態活得下來，後面不用看了（提早結束）
        cur = eps_closure(nfa, nxt)
    return end in cur


def draw_nfa(p):
    nfa, start, end = build_nfa(p)
    print(f"pattern = {p!r}   狀態數 = {len(nfa.kind)}   start = q{start}")
    for i in range(len(nfa.kind)):
        if nfa.kind[i] == "eps":
            to = ", ".join(f"q{t}" for t in nfa.eps[i])
            print(f"  q{i} --ε--> {to}")
        elif nfa.kind[i] == "ch":
            lab = "'任意字元'" if nfa.c[i] == "." else f"'{nfa.c[i]}'"
            print(f"  q{i} --{lab}--> q{nfa.tgt[i]}")
        else:
            print(f"  q{i} = 接受狀態 (end)")


# ======================================================================
# 搜尋（grep 的語意）：pattern 可以出現在字串的任何位置
# 做法：前面補一個 ".*" ，就變成「整串比對」的同義寫法
# ======================================================================
def search_dp(s, p):
    return match_dp(s, ".*" + p)


def search_nfa(s, p):
    return match_nfa(s, ".*" + p)


# ======================================================================
# grep：拿 pattern 去過濾一組文字行（本題的應用情境）
# ======================================================================
def grep(lines, p, use="nfa"):
    f = search_nfa if use == "nfa" else search_dp
    return [ln for ln in lines if f(ln, p)]


# ======================================================================
# 測試與示範
# ======================================================================
TESTS = [
    ("", "", True),
    ("abc", "", False),
    ("", "a*", True),
    ("", "a", False),
    ("aa", "a", False),
    ("aa", "a*", True),
    ("ab", ".*", True),
    ("abc", "a.c", True),
    ("axc", "a.c", True),
    ("abd", "a.c", False),
    ("ac", "ab*c", True),
    ("aab", "c*a*b", True),
    ("mississippi", "mis*is*p*.", False),
    ("mississippi", "mis*is*ip*.", True),
    ("aaa", "a*a", True),
    ("ab", ".*c", False),
    ("ab", ".*", True),
    ("aab", "a.*b", True),
    ("test123", "t.st.*", True),
    ("x" * 300 + "y", "x*y", True),
    ("x" * 300 + "z", "x*y", False),
]


def test_all():
    print(f"===== 一、兩種方法對拍（{len(TESTS)} 個測資）=====")
    ok = True
    for s, p, want in TESTS:
        a = match_dp(s, p)
        b = match_nfa(s, p)
        good = (a == b == want)
        ok = ok and good
        mark = "OK " if good else "FAIL"
        print(f"  [{mark}] s={s[:18] + ('...' if len(s) > 18 else '')!r:<22} p={p!r:<14} dp={a} nfa={b} 期望={want}")
    print("  => 兩種方法答案完全一致，且都符合預期" if ok else "  => 有錯！")
    print()
    return ok


def demo_table():
    print("===== 二、動態規劃表格長什麼樣（s='aab', p='c*a*b'）=====")
    print("  遞迴式：")
    print("    非 * : dp[i][j] = (第j個字元配得上 s[i-1]) and dp[i-1][j-1]")
    print("    是 * : dp[i][j] = dp[i][j-1]（用0次） or (配得上 and dp[i-1][j]（多吃一個）)")
    match_dp("aab", "c*a*b", show=True)
    print(f"  => 最右下角那格 dp[{len('aab')}][{len(tokenize('c*a*b'))}] = {match_dp('aab', 'c*a*b')}")
    print()


def demo_nfa():
    print("===== 三、NFA 圖長什麼樣（p='a*b'）=====")
    draw_nfa("a*b")
    print()
    print("  模擬過程（s='aab'）：")
    nfa, start, end = build_nfa("a*b")
    cur = eps_closure(nfa, {start})
    print(f"    起始活著的狀態 = {sorted('q' + str(x) for x in cur)}")
    for ch in "aab":
        nxt = set()
        for st in cur:
            if nfa.kind[st] == "ch" and char_ok(nfa.c[st], ch):
                nxt.add(nfa.tgt[st])
        cur = eps_closure(nfa, nxt)
        print(f"    吃 '{ch}' 之後 = {sorted('q' + str(x) for x in cur)}")
    print(f"    end 有在裡面嗎？ {end in cur}  => {'匹配成功' if end in cur else '不匹配'}")
    print()


def demo_grep():
    print("===== 四、grep 應用：從一堆行裡找出符合的行 =====")
    log = [
        "2026/10/21 09:00:01 INFO  system start",
        "2026/10/21 09:00:02 DEBUG cache miss",
        "2026/10/21 09:00:03 ERROR disk is full",
        "user howard login ok",
        "2026/10/21 09:00:05 WARN  retry 3 times",
        "ERROR: file not found",
    ]
    p = "E.ROR.*"
    print(f"  pattern = {p!r}（搜尋版：前面自動補 .* 找整行）")
    for ln in grep(log, p):
        print(f"    {ln}")
    print(f"  用 DP 做同樣的事，結果一樣：{grep(log, p, use='dp') == grep(log, p, use='nfa')}")
    print()


def bench():
    print("===== 五、效率比較（time.perf_counter）=====")

    # A. 第一個字就不符：NFA 能夠提早結束，DP 必須把整張表填完
    s = "x" * 200000
    p = "error.*"
    t = time.perf_counter(); r1 = match_nfa(s, p); t1 = time.perf_counter() - t
    t = time.perf_counter(); r2 = match_dp(s, p); t2 = time.perf_counter() - t
    print(f"  A. s = 'x' * 200000, p = {p!r}（第1個字就配不上）")
    print(f"     NFA: {t1:.5f} 秒 (結果 {r1})  -- 吃第一個字就全滅，直接回傳")
    print(f"     DP : {t2:.5f} 秒 (結果 {r2})  -- 還是得填完 {len(s)+1} x {len(tokenize(p))+1} 的表格")
    print(f"     表格儲存格數 ≈ {((len(s)+1)*(len(tokenize(p))+1)):,}，NFA 活著的狀態數 ≤ {len(build_nfa(p)[0].kind)}")
    print()

    # B. 真的配得上的長字串：兩邊都得看完，速度相近
    s = ("ab" * 10000) + "end"
    p = ".*end"
    t = time.perf_counter(); r1 = match_nfa(s, p); t1 = time.perf_counter() - t
    t = time.perf_counter(); r2 = match_dp(s, p); t2 = time.perf_counter() - t
    print(f"  B. s 長度 {len(s)}, p = {p!r}（要配成功，兩邊都得掃完）")
    print(f"     NFA: {t1:.5f} 秒 (結果 {r1})")
    print(f"     DP : {t2:.5f} 秒 (結果 {r2})")
    print()


if __name__ == "__main__":
    ok = test_all()
    demo_table()
    demo_nfa()
    demo_grep()
    bench()
    print("結論：兩種方法答案相同；DP 要整張表、穩定 O(n*m)，NFA 只有狀態集合、")
    print("      不用的分支可以提早死掉，還能一邊讀字串一邊比（適合拿來做 grep）。")
    assert ok, "測試失敗"

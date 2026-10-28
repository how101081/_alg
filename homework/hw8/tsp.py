"""
第7週習題 - 優化演算法：旅行推銷員問題 (TSP)
比較五種方法：貪婪、改良法(2-opt)、爬山、模擬退火、梯度下降
"""

import math
import random
import time
import numpy as np

# ==================== 測試資料 ====================
N_CITIES = 20
rng = random.Random(42)
CITIES = [(rng.uniform(0, 100), rng.uniform(0, 100)) for _ in range(N_CITIES)]
DIST = np.array([[math.dist(a, b) for b in CITIES] for a in CITIES])

def tour_length(tour):
    """計算路徑總長度（封閉迴路）"""
    total = 0.0
    n = len(tour)
    for i in range(n):
        total += DIST[tour[i], tour[(i + 1) % n]]
    return total

# ==================== 1. 貪婪演算法（最近鄰居） ====================
def greedy(start=0):
    """
    從起點出發，每次走訪最近且尚未造訪的城市，最後回到起點形成迴路
    """
    unvisited = set(range(N_CITIES))
    unvisited.discard(start)
    tour = [start]
    while unvisited:
        current = tour[-1]
        nxt = min(unvisited, key=lambda c: DIST[current, c])
        tour.append(nxt)
        unvisited.discard(nxt)
    return tour

# ==================== 2. 改良法（2-opt） ====================
def two_opt_improve(init=None):
    """
    以初始解為起點，使用 2-opt 進行局部改良
    反覆嘗試交換兩條邊，若能縮短路徑則採用，直到找不到改善為止
    """
    if init is None:
        tour = greedy()
    else:
        tour = list(init)
    n = len(tour)
    improved = True
    while improved:
        improved = False
        best_delta = -1e-12
        best_ij = None
        for i in range(n - 1):
            for j in range(i + 2, n):
                if i == 0 and j == n - 1:
                    continue
                a, b = tour[i], tour[i + 1]
                c, d = tour[j], tour[(j + 1) % n]
                delta = DIST[a, c] + DIST[b, d] - DIST[a, b] - DIST[c, d]
                if delta < best_delta:
                    best_delta = delta
                    best_ij = (i, j)
        if best_ij is not None and best_delta < -1e-12:
            i, j = best_ij
            # 反轉 i+1 到 j 之間的路段
            tour[i + 1 : j + 1] = reversed(tour[i + 1 : j + 1])
            improved = True
    return tour

# ==================== 3. 爬山演算法 ====================
def hill_climbing(iters=20000, seed=123):
    """
    隨機初始解，每次隨機交換兩個城市
    只接受路徑長度變短的解，否則還原
    """
    r = random.Random(seed)
    tour = list(range(N_CITIES))
    r.shuffle(tour)
    cur = tour_length(tour)
    for _ in range(iters):
        i, j = r.sample(range(N_CITIES), 2)
        # 交換
        tour[i], tour[j] = tour[j], tour[i]
        new_len = tour_length(tour)
        if new_len < cur:
            cur = new_len
        else:
            # 還原
            tour[i], tour[j] = tour[j], tour[i]
    return tour

# ==================== 4. 模擬退火法 ====================
def simulated_annealing(T0=100.0, T_end=1e-3, alpha=0.995, per_temp=100, seed=456):
    """
    以 2-opt 式反轉為鄰域
    高溫時有機率接受較差解以跳出局部最佳，溫度逐漸下降
    """
    r = random.Random(seed)
    tour = list(range(N_CITIES))
    r.shuffle(tour)
    cur = tour_length(tour)
    best = tour[:]
    best_len = cur
    T = T0
    while T > T_end:
        for _ in range(per_temp):
            # 隨機選擇兩個不相鄰的位置
            i, j = sorted(r.sample(range(N_CITIES), 2))
            if j - i < 2:
                continue
            # 產生鄰居：反轉 tour[i+1 ... j]
            cand = tour[:]
            cand[i + 1 : j + 1] = reversed(cand[i + 1 : j + 1])
            new_len = tour_length(cand)
            d = new_len - cur
            if d < 0:
                tour, cur = cand, new_len
            else:
                if r.random() < math.exp(-d / T):
                    tour, cur = cand, new_len
            if cur < best_len:
                best = tour[:]
                best_len = cur
        T *= alpha
    return best

# ==================== 5. 梯度下降法（連續鬆弛） ====================
def gradient_descent(steps=3000, lr=0.05, lam=30.0, seed=789):
    """
    將 TSP 轉為連續最佳化：
    P_{k,i} = 第k個位置造訪城市i的機率，以row-softmax表示
    損失 = 期望路徑長度 + λ * (每個城市出現次數偏離1的懲罰)
    用梯度下降最小化後，以貪婪方式解碼成合法排列
    """
    n = N_CITIES
    rng_np = np.random.default_rng(seed)
    W = rng_np.normal(0, 0.1, (n, n))
    Dn = DIST / DIST.mean()

    def softmax(x):
        e = np.exp(x - x.max(axis=1, keepdims=True))
        return e / e.sum(axis=1, keepdims=True)

    for t in range(steps):
        P = softmax(W)
        nxt = np.roll(P, -1, axis=0)
        prv = np.roll(P, 1, axis=0)
        # 期望距離梯度（D對稱）
        gP = nxt @ Dn + prv @ Dn
        # 每個城市恰好造訪一次的懲罰
        col_sum = P.sum(axis=0) - 1.0
        gP = gP + 2.0 * lam * col_sum[None, :]
        # softmax 反向傳播
        gW = P * (gP - (gP * P).sum(axis=1, keepdims=True))
        # 學習率衰減
        lr_t = lr * (1.0 - 0.9 * t / steps)
        W = W - lr_t * 10.0 * gW

    # 解碼
    P = softmax(W)
    tour = [-1] * n
    Pm = P.copy()
    for _ in range(n):
        idx = np.argmax(Pm)
        k = idx // n
        i = idx % n
        tour[k] = int(i)
        Pm[k, :] = -1e18
        Pm[:, i] = -1e18
    return tour

# ==================== 執行與比較 ====================
def plot_all(results):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("（未安裝 matplotlib，略過繪圖）")
        return
    plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei", "Arial Unicode MS", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False
    fig, axes = plt.subplots(1, 5, figsize=(22, 4))
    for ax, (name, tour, L, _) in zip(axes, results):
        xs = [CITIES[c][0] for c in tour] + [CITIES[tour[0]][0]]
        ys = [CITIES[c][1] for c in tour] + [CITIES[tour[0]][1]]
        ax.plot(xs, ys, "-o", ms=4)
        ax.plot(xs[0], ys[0], "go", ms=7)  # 起點
        ax.set_title(f"{name}\n長度 = {L:.2f}")
        ax.grid(True, alpha=0.3)
    plt.suptitle("TSP 五種演算法比較（20 個城市）", fontsize=14)
    plt.tight_layout()
    plt.savefig("tsp_result.png", dpi=120)
    print("\n已輸出圖檔：tsp_result.png")

if __name__ == "__main__":
    methods = [
        ("1.貪婪演算法", greedy),
        ("2.改良法(2-opt)", two_opt_improve),
        ("3.爬山演算法", hill_climbing),
        ("4.模擬退火法", simulated_annealing),
        ("5.梯度下降法", gradient_descent),
    ]
    print("=" * 60)
    print(f"旅行推銷員問題 (TSP) 比較")
    print(f"城市數：{N_CITIES}，隨機種子：42")
    print("=" * 60)
    results = []
    for name, fn in methods:
        t0 = time.time()
        tour = fn()
        # 檢查是否為合法路徑
        if sorted(tour) != list(range(N_CITIES)):
            print(f"[警告] {name} 路徑不合法")
        L = tour_length(tour)
        sec = time.time() - t0
        results.append((name, tour, L, sec))
        print(f"\n{name}")
        print(f"  路徑長度：{L:.2f}")
        print(f"  執行時間：{sec:.3f} 秒")
        print(f"  路徑順序：{tour}")
    print("\n" + "=" * 60)
    print("比較結果（依長度排序）：")
    for i, (name, _, L, sec) in enumerate(sorted(results, key=lambda x: x[2]), 1):
        print(f"  {i}. {name:<14} 長度 = {L:.2f} ({sec:.3f}s)")
    print("=" * 60)
    plot_all(results)

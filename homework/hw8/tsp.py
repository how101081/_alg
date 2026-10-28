"""
旅行推銷員問題 (TSP) - 5種演算法
"""
import math
import random
import time
import numpy as np

# 測試資料
N_CITIES = 20
rng = random.Random(42)
CITIES = [(rng.uniform(0, 100), rng.uniform(0, 100)) for _ in range(N_CITIES)]
DIST = np.array([[math.dist(a, b) for b in CITIES] for a in CITIES])

def tour_length(tour):
    return sum(DIST[tour[i], tour[(i + 1) % len(tour)]] for i in range(len(tour)))

# 1. 貪婪演算法 (最近鄰居)
def greedy(start=0):
    unvisited = set(range(N_CITIES)) - {start}
    tour = [start]
    while unvisited:
        nxt = min(unvisited, key=lambda c: DIST[tour[-1], c])
        tour.append(nxt)
        unvisited.remove(nxt)
    return tour

# 2. 改良法 (2-opt)
def two_opt_improve(init=None):
    tour = list(init) if init else greedy()
    n = len(tour)
    improved = True
    while improved:
        improved = False
        best_delta, best_ij = -1e-9, None
        for i in range(n - 1):
            for j in range(i + 2, n):
                if i == 0 and j == n - 1:
                    continue
                a, b = tour[i], tour[i + 1]
                c, d = tour[j], tour[(j + 1) % n]
                delta = DIST[a, c] + DIST[b, d] - DIST[a, b] - DIST[c, d]
                if delta < best_delta:
                    best_delta, best_ij = delta, (i, j)
        if best_ij:
            i, j = best_ij
            tour[i + 1:j + 1] = reversed(tour[i + 1:j + 1])
            improved = True
    return tour

# 3. 爬山演算法
def hill_climbing(iters=20000, seed=1):
    r = random.Random(seed)
    tour = list(range(N_CITIES))
    r.shuffle(tour)
    cur = tour_length(tour)
    for _ in range(iters):
        i, j = r.sample(range(N_CITIES), 2)
        tour[i], tour[j] = tour[j], tour[i]
        new = tour_length(tour)
        if new < cur:
            cur = new
        else:
            tour[i], tour[j] = tour[j], tour[i]
    return tour

# 4. 模擬退火法
def simulated_annealing(T0=100.0, T_end=1e-3, alpha=0.995, per_temp=100, seed=1):
    r = random.Random(seed)
    tour = list(range(N_CITIES))
    r.shuffle(tour)
    cur = tour_length(tour)
    best, best_len = tour[:], cur
    T = T0
    while T > T_end:
        for _ in range(per_temp):
            i, j = sorted(r.sample(range(N_CITIES), 2))
            cand = tour[:i] + tour[i:j + 1][::-1] + tour[j + 1:]
            new = tour_length(cand)
            d = new - cur
            if d < 0 or r.random() < math.exp(-d / T):
                tour, cur = cand, new
                if cur < best_len:
                    best, best_len = tour[:], cur
        T *= alpha
    return best

# 5. 梯度下降法
def gradient_descent(steps=3000, lr=0.05, lam=30.0, seed=1):
    n = N_CITIES
    r = np.random.default_rng(seed)
    W = r.normal(0, 0.1, (n, n))
    Dn = DIST / DIST.mean()

    def softmax(x):
        e = np.exp(x - x.max(axis=1, keepdims=True))
        return e / e.sum(axis=1, keepdims=True)

    for t in range(steps):
        P = softmax(W)
        nxt, prv = np.roll(P, -1, axis=0), np.roll(P, 1, axis=0)
        gP = nxt @ Dn + prv @ Dn
        col = P.sum(axis=0) - 1.0
        gP += 2 * lam * col[None, :]
        gW = P * (gP - (gP * P).sum(axis=1, keepdims=True))
        W -= lr * (1 - t / steps * 0.9) * gW * 10

    P = softmax(W)
    tour = [-1] * n
    Pm = P.copy()
    for _ in range(n):
        k, i = np.unravel_index(np.argmax(Pm), Pm.shape)
        tour[k] = int(i)
        Pm[k, :] = -1
        Pm[:, i] = -1
    return tour

def plot_all(results):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return
    plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei", "Arial Unicode MS", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False
    fig, axes = plt.subplots(1, 5, figsize=(20, 4))
    for ax, (name, tour, L, _) in zip(axes, results):
        xs = [CITIES[c][0] for c in tour + [tour[0]]]
        ys = [CITIES[c][1] for c in tour + [tour[0]]]
        ax.plot(xs, ys, "-o", ms=4)
        ax.set_title(f"{name}\nL={L:.1f}")
    plt.tight_layout()
    plt.savefig("tsp_result.png", dpi=100)
    print("圖已輸出: tsp_result.png")

if __name__ == "__main__":
    methods = [
        ("1.貪婪", greedy),
        ("2.改良(2-opt)", two_opt_improve),
        ("3.爬山", hill_climbing),
        ("4.模擬退火", simulated_annealing),
        ("5.梯度下降", gradient_descent),
    ]
    print(f"城市數: {N_CITIES}\n")
    res = []
    for name, fn in methods:
        t0 = time.time()
        tour = fn()
        L = tour_length(tour)
        sec = time.time() - t0
        res.append((name, tour, L, sec))
        print(f"{name:12} 長度={L:7.2f} 時間={sec:.3f}s")
    plot_all(res)

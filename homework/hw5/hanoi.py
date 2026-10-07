def hanoi_rec(n, src, aux, dst, moves):
    if n == 0:
        return
    hanoi_rec(n - 1, src, dst, aux, moves)
    moves.append((n, src, dst))
    hanoi_rec(n - 1, aux, src, dst, moves)
    return moves


def hanoi_iter(n, src, aux, dst):
    pegs = {src: list(range(n, 0, -1)), aux: [], dst: []}
    ring = [src, dst, aux] if n % 2 == 1 else [src, aux, dst]
    moves = []
    small = src
    for i in range(2 ** n - 1):
        if i % 2 == 0:
            j = ring.index(small)
            nxt = ring[(j + 1) % 3]
            pegs[nxt].append(pegs[small].pop())
            moves.append((pegs[nxt][-1], small, nxt))
            small = nxt
        else:
            a, b = [p for p in (src, aux, dst) if p != small]
            top_a = pegs[a][-1] if pegs[a] else 10 ** 9
            top_b = pegs[b][-1] if pegs[b] else 10 ** 9
            if top_a < top_b:
                pegs[b].append(pegs[a].pop())
                moves.append((pegs[b][-1], a, b))
            else:
                pegs[a].append(pegs[b].pop())
                moves.append((pegs[a][-1], b, a))
    return moves


def show(title, moves):
    print(title)
    for i, (d, a, b) in enumerate(moves, 1):
        print(f"  {i:2d}. 盤 {d}: {a} -> {b}")
    print(f"  共 {len(moves)} 步\n")


n = 3
print(f"河內塔 n = {n}（A 是起點，C 是終點）\n")
show("遞迴版:", hanoi_rec(n, "A", "B", "C", []))
show("禁止遞迴（迭代版）:", hanoi_iter(n, "A", "B", "C"))

"""
第9週習題 -- 搜尋算法
1. 老鼠走迷宮 (DFS)
2. 狼羊甘藍菜過河 (BFS)
3. 八皇后 (DFS)
4. NPC 搜尋玩家 (A*)
5. IC 電路繞線 (BFS / A*)
"""

import heapq
from collections import deque


# ============================================================
# 1. 老鼠走迷宮問題 (DFS)
# ============================================================
MAZE = [
    "S..#......",
    ".#.#.####.",
    ".#...#....",
    ".####.#.#.",
    "......#.#.",
    ".####...#.",
    ".#...###..",
    ".#.#......",
    "...#.####.",
    ".....E....",
]


def solve_maze(maze):
    """用 DFS 找出從 S 到 E 的一條路徑。"""
    rows, cols = len(maze), len(maze[0])
    start = end = None
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == "S":
                start = (r, c)
            elif maze[r][c] == "E":
                end = (r, c)

    visited = set()
    path = []

    def dfs(r, c):
        if not (0 <= r < rows and 0 <= c < cols):
            return False
        if (r, c) in visited or maze[r][c] == "#":
            return False

        visited.add((r, c))
        path.append((r, c))

        if (r, c) == end:
            return True

        for dr, dc in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            if dfs(r + dr, c + dc):
                return True

        path.pop()
        return False

    dfs(*start)
    return path


def print_maze(maze, path):
    path_set = set(path)
    for r, row in enumerate(maze):
        line = ""
        for c, ch in enumerate(row):
            if (r, c) in path_set and ch not in "SE":
                line += "*"
            else:
                line += ch
        print("  " + line)


# ============================================================
# 2. 狼羊甘藍菜過河問題 (BFS)
# ============================================================
# 狀態：(狼, 羊, 甘藍菜, 農夫)  0=左岸, 1=右岸
START = (0, 0, 0, 0)
GOAL = (1, 1, 1, 1)


def is_valid(state):
    w, g, c, f = state
    # 農夫不在的一岸，若羊和狼單獨在一起，或羊和甘藍菜單獨在一起，就失敗
    if f != w and w == g:
        return False
    if f != g and g == c:
        return False
    return True


def next_states(state):
    w, g, c, f = state
    result = []
    # 農夫獨自過河
    new = list(state)
    new[3] = 1 - f
    result.append(tuple(new))
    # 農夫帶一樣東西過河
    for i, name in enumerate(("狼", "羊", "甘藍菜")):
        if state[i] == f:
            new = list(state)
            new[i] = 1 - f
            new[3] = 1 - f
            result.append(tuple(new))
    return [s for s in result if is_valid(s)]


def solve_river():
    """用 BFS 找出最少過河次數的搬運過程。"""
    queue = deque([START])
    parent = {START: None}
    action = {START: None}

    while queue:
        state = queue.popleft()
        if state == GOAL:
            break
        for nxt in next_states(state):
            if nxt not in parent:
                parent[nxt] = state
                action[nxt] = nxt
                queue.append(nxt)

    # 回溯路徑
    path = []
    cur = GOAL
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()

    steps = []
    for i in range(1, len(path)):
        prev, cur = path[i - 1], path[i]
        moved = [name for j, name in enumerate(("狼", "羊", "甘藍菜"))
                 if prev[j] != cur[j]]
        direction = "右岸" if cur[3] == 1 else "左岸"
        steps.append(f"農夫帶 {moved[0] if moved else '自己'} 到{direction}")
    return steps


# ============================================================
# 3. 八皇后問題 (DFS)
# ============================================================
def solve_queens(n=8):
    """用 DFS 找出全部解，回傳解的數量和第一組解。"""
    solutions = []
    cols = set()
    diag1 = set()  # r - c
    diag2 = set()  # r + c
    board = []

    def dfs(r):
        if r == n:
            solutions.append(board[:])
            return
        for c in range(n):
            if c in cols or (r - c) in diag1 or (r + c) in diag2:
                continue
            cols.add(c)
            diag1.add(r - c)
            diag2.add(r + c)
            board.append(c)
            dfs(r + 1)
            board.pop()
            cols.remove(c)
            diag1.remove(r - c)
            diag2.remove(r + c)

    dfs(0)
    return solutions


def print_board(solution):
    n = len(solution)
    for r in range(n):
        line = ["." for _ in range(n)]
        line[solution[r]] = "Q"
        print("  " + " ".join(line))


# ============================================================
# 4. NPC 搜尋玩家問題 (A*)
# ============================================================
NPC_MAP = [
    "...........",
    ".###.#.###.",
    "...#.#.#...",
    ".#.#...#.#.",
    ".#.###.#.#.",
    ".#.....#...",
    ".#####.###.",
    ".......#...",
    ".###.#.#.#.",
    "...........",
]

PLAYER = (9, 9)
NPC = (0, 0)


def astar(grid, start, goal):
    """A* 搜尋：g 為實際步數，h 為曼哈頓距離。"""
    rows, cols = len(grid), len(grid[0])

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set = [(heuristic(start, goal), 0, start)]
    parent = {start: None}
    g_score = {start: 0}

    while open_set:
        _, g, cur = heapq.heappop(open_set)
        if cur == goal:
            path = []
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            return path[::-1]

        if g > g_score.get(cur, float("inf")):
            continue

        r, c = cur
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            if grid[nr][nc] == "#":
                continue
            ng = g + 1
            if ng < g_score.get((nr, nc), float("inf")):
                g_score[(nr, nc)] = ng
                parent[(nr, nc)] = cur
                priority = ng + heuristic((nr, nc), goal)
                heapq.heappush(open_set, (priority, ng, (nr, nc)))

    return []


def print_npc_map(grid, path):
    path_set = set(path)
    for r, row in enumerate(grid):
        line = ""
        for c, ch in enumerate(row):
            pos = (r, c)
            if pos == NPC:
                line += "N"
            elif pos == PLAYER:
                line += "P"
            elif pos in path_set:
                line += "*"
            else:
                line += ch
        print("  " + line)


# ============================================================
# 5. IC 設計中的電路繞線問題 (BFS)
# ============================================================
CHIP = [
    "A.........",
    ".####.###.",
    "....#.#...",
    ".##.#.#.#.",
    ".#....#.#.",
    ".#.####.#.",
    ".#......#.",
    ".######.#.",
    "........#.",
    "........B.",
]

PIN_A = (0, 0)
PIN_B = (9, 9)


def route_chip(grid, start, goal):
    """用 BFS 找最短繞線路徑（避開障礙物）。"""
    rows, cols = len(grid), len(grid[0])
    queue = deque([start])
    parent = {start: None}

    while queue:
        cur = queue.popleft()
        if cur == goal:
            path = []
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            return path[::-1]

        r, c = cur
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            if grid[nr][nc] == "#":
                continue
            if (nr, nc) not in parent:
                parent[(nr, nc)] = cur
                queue.append((nr, nc))

    return []


def print_chip(grid, path):
    path_set = set(path)
    for r, row in enumerate(grid):
        line = ""
        for c, ch in enumerate(row):
            pos = (r, c)
            if pos == PIN_A:
                line += "A"
            elif pos == PIN_B:
                line += "B"
            elif pos in path_set:
                line += "*"
            else:
                line += ch
        print("  " + line)


# ============================================================
# 主程式
# ============================================================
def main():
    print("=" * 60)
    print("1. 老鼠走迷宮問題 (DFS)")
    print("=" * 60)
    path = solve_maze(MAZE)
    print(f"找到路徑，長度 = {len(path)}")
    print_maze(MAZE, path)

    print()
    print("=" * 60)
    print("2. 狼羊甘藍菜過河問題 (BFS)")
    print("=" * 60)
    steps = solve_river()
    print(f"最少需要 {len(steps)} 趟：")
    for i, step in enumerate(steps, 1):
        print(f"  {i}. {step}")

    print()
    print("=" * 60)
    print("3. 八皇后問題 (DFS)")
    print("=" * 60)
    solutions = solve_queens(8)
    print(f"8 皇后共有 {len(solutions)} 組解，以下顯示第一組：")
    print_board(solutions[0])

    print()
    print("=" * 60)
    print("4. NPC 搜尋玩家問題 (A*)")
    print("=" * 60)
    path = astar(NPC_MAP, NPC, PLAYER)
    print(f"NPC 找到玩家，所需步數 = {len(path) - 1}")
    print_npc_map(NPC_MAP, path)

    print()
    print("=" * 60)
    print("5. IC 設計中的電路繞線問題 (BFS)")
    print("=" * 60)
    path = route_chip(CHIP, PIN_A, PIN_B)
    print(f"完成繞線，線長 = {len(path) - 1}")
    print_chip(CHIP, path)


if __name__ == "__main__":
    main()

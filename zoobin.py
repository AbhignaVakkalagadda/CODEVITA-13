from collections import deque
import sys

def compose(a, b):
    n = len(a) - 1
    r = [0] * (n + 1)
    for i in range(1, n + 1):
        r[i] = a[b[i]]
    return r

def main():
    sys.setrecursionlimit(10**6)
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    E = int(next(it))
    e1, e2 = [], []
    mx = 0

    for _ in range(E):
        a, b = int(next(it)), int(next(it))
        if a > b:
            a, b = b, a
        e1.append((a, b))
        mx = max(mx, a, b)
    for _ in range(E):
        a, b = int(next(it)), int(next(it))
        if a > b:
            a, b = b, a
        e2.append((a, b))
        mx = max(mx, a, b)

    n = mx
    A = [[0] * (n + 1) for _ in range(n + 1)]
    B = [[0] * (n + 1) for _ in range(n + 1)]
    for u, v in e1:
        A[u][v] = A[v][u] = 1
    for u, v in e2:
        B[u][v] = B[v][u] = 1

    degA = [0] * (n + 1)
    degB = [0] * (n + 1)
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            degA[i] += A[i][j]
            degB[i] += B[i][j]

    order = sorted(range(1, n + 1), key=lambda x: (-degA[x], x))
    used = [0] * (n + 1)
    p = [0] * (n + 1)

    def dfs_iso(idx):
        if idx == len(order):
            return True
        v = order[idx]
        for w in range(1, n + 1):
            if used[w] or degA[v] != degB[w]:
                continue
            ok = True
            for i in range(idx):
                u = order[i]
                if p[u] != 0:
                    if A[v][u] and not B[w][p[u]]:
                        ok = False
                        break
                    if not A[v][u] and B[w][p[u]]:
                        ok = False
                        break
            if not ok:
                continue
            used[w] = 1
            p[v] = w
            if dfs_iso(idx + 1):
                return True
            used[w] = 0
            p[v] = 0
        return False

    dfs_iso(0)

    target_inv = [0] * (n + 1)
    for i in range(1, n + 1):
        target_inv[p[i]] = i

    adj = [[] for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            if A[i][j]:
                adj[i].append(j)
                adj[j].append(i)

    cycles = []
    usedv = [0] * (n + 1)
    path = []

    def dfs_cycle(s, u):
        for v in adj[u]:
            if v == s and len(path) >= 3:
                cycles.append(path[:])
                continue
            if not usedv[v] and v > s:
                usedv[v] = 1
                path.append(v)
                dfs_cycle(s, v)
                path.pop()
                usedv[v] = 0

    for s in range(1, n + 1):
        usedv = [0] * (n + 1)
        usedv[s] = 1
        path = [s]
        dfs_cycle(s, s)

    gens = []
    for cy in cycles:
        k = len(cy)
        t = list(range(n + 1))
        for i in range(k):
            a, b = cy[i], cy[(i + 1) % k]
            t[a] = b
        gens.append(t)
        t2 = list(range(n + 1))
        for i in range(k):
            a, b = cy[i], cy[(i - 1 + k) % k]
            t2[a] = b
        gens.append(t2)

    id_perm = list(range(n + 1))
    if target_inv == id_perm:
        print(0, end="")  # no newline or space
        return

    def perm_key(pr):
        return ",".join(map(str, pr[1:]))

    q = deque([id_perm])
    dist = {perm_key(id_perm): 0}

    while q:
        cur = q.popleft()
        d = dist[perm_key(cur)]
        for g in gens:
            nxt = compose(g, cur)
            kstr = perm_key(nxt)
            if kstr not in dist:
                dist[kstr] = d + 1
                if nxt == target_inv:
                    print(d + 1, end="")
                    return
                q.append(nxt)
    print(-1, end="")  

if __name__ == "__main__":
    main()

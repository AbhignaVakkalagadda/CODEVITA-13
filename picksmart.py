import math
from itertools import combinations
TOL = 1e-9
def segment_cross(p1, p2, q1, q2):
    ax, ay = p1
    bx, by = p2
    cx, cy = q1
    dx, dy = q2
    divisor = (ax - bx) * (cy - dy) - (ay - by) * (cx - dx)
    if abs(divisor) < TOL:
        return None
    px = ((ax * by - ay * bx) * (cx - dx) - (ax - bx) * (cx * dy - cy * dx)) / divisor
    py = ((ax * by - ay * bx) * (cy - dy) - (ay - by) * (cx * dy - cy * dx)) / divisor
    pt = (px, py)
    def is_on(s, t, chk):
        return (min(s[0], t[0]) - TOL <= chk[0] <= max(s[0], t[0]) + TOL and
                min(s[1], t[1]) - TOL <= chk[1] <= max(s[1], t[1]) + TOL)
    if is_on(p1, p2, pt) and is_on(q1, q2, pt):
        return (round(px, 6), round(py, 6))
    return None
def line_len(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1])
def polygon_area(pts):
    S = 0.0
    n = len(pts)
    for i in range(n):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % n]
        S += x0 * y1 - x1 * y0
    return abs(S) / 2.0
def process():
    try:
        count = int(input().strip())
    except:
        print("Abandoned", end="")
        return
    segs = []
    for idx in range(count):
        try:
            xa, ya, xb, yb = map(float, input().split())
            segs.append(((xa, ya), (xb, yb)))
        except:
            print("Abandoned", end="")
            return
    nodes = set()
    for start, end in segs:
        nodes.add(start)
        nodes.add(end)
    for (s1, s2), (t1, t2) in combinations(segs, 2):
        crosspt = segment_cross(s1, s2, t1, t2)
        if crosspt:
            nodes.add(crosspt)
    node_list = list(nodes)
    if len(node_list) < 3:
        print("Abandoned", end="")
        return
    graph = {v: set() for v in node_list}
    for s, t in segs:
        on_seg = []
        for v in node_list:
            if abs(line_len(s, v) + line_len(v, t) - line_len(s, t)) < 1e-6:
                on_seg.append((line_len(s, v), v))
        on_seg.sort()
        for k in range(len(on_seg) - 1):
            u = on_seg[k][1]
            w = on_seg[k + 1][1]
            graph[u].add(w)
            graph[w].add(u)
    visited_points = set()
    path_cycle = []
    def search(node, prev, route):
        visited_points.add(node)
        for adj in graph[node]:
            if adj == prev:
                continue
            if adj in route:
                idx = route.index(adj)
                cyc = route[idx:] + [adj]
                return cyc
            if adj not in visited_points:
                found = search(adj, node, route + [adj])
                if found:
                    return found
        return None
    for n in node_list:
        if n not in visited_points:
            discovered = search(n, None, [n])
            if discovered:
                path_cycle = discovered
                break

    if not path_cycle or len(path_cycle) < 3:
        print("Abandoned", end="")
        return
    area_poly = polygon_area(path_cycle)
    total_length = sum(line_len(a, b) for a, b in segs)
    polygon_perim = sum(line_len(path_cycle[i], path_cycle[(i + 1) % len(path_cycle)]) for i in range(len(path_cycle)))
    rem_length = total_length - polygon_perim
    if rem_length > TOL:
        area_circle = (rem_length ** 2) / (4 * math.pi)
    else:
        area_circle = 0.0
    print("Kalyan" if area_poly > area_circle else "Computer", end="")
if __name__ == "__main__":
    process()

def polygon_stats(vertices):
    count = len(vertices)
    if count < 3:
        return 0.0, 0.0, 0.0, 0
    poly_area = 0.0
    poly_perim = 0.0
    slip_sum = 0.0
    abs_slip_sum = 0.0
    for idx in range(count):
        pt_a = vertices[idx]
        pt_b = vertices[(idx + 1) % count]
        seg_len = abs(pt_a[0] - pt_b[0]) + abs(pt_a[1] - pt_b[1])
        slip_item = pt_a[0] * pt_b[1] - pt_b[0] * pt_a[1]
        poly_perim += seg_len
        slip_sum += slip_item
        abs_slip_sum += abs(slip_item)
    poly_area = abs(slip_sum) / 2.0
    return poly_area, poly_perim, slip_sum, abs_slip_sum
def main():
    try:
        num = int(input())
        points = [list(map(float, input().split())) for _ in range(num)]
        shortest = float('inf')
        for idx in range(num):
            pt_a = points[idx]
            pt_b = points[(idx + 1) % num]
            seg_len = abs(pt_a[0] - pt_b[0]) + abs(pt_a[1] - pt_b[1])
            if seg_len < shortest:
                shortest = seg_len
        max_ht = max(0.0, (shortest - 0.1) / 2.0)
        best_vol = 0.0
        if max_ht > 0.0:
            base_area, base_perim, _, _ = polygon_stats(points)
            if base_area == 0.0:
                print("0.00")
                return
            steps = int(max_ht / 0.1)
            for idx in range(1, steps + 1):
                curr_ht = round(idx * 0.1, 1)
                adj_area = base_area - (base_perim * curr_ht) + (4 * curr_ht * curr_ht)
                if adj_area <= 0:
                    continue
                curr_vol = adj_area * curr_ht
                if curr_vol > best_vol:
                    best_vol = curr_vol
        print("{0:.2f}".format(best_vol),end="")
    except EOFError:
        pass
    except Exception:
        pass
main()

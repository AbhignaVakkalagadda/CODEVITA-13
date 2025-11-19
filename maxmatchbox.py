def get_polygon_properties(coords):
    n = len(coords)
    if n < 3:
        return 0.0, 0.0, 0.0, 0
    
    area = 0.0
    perime = 0.0
    shoe_sum = 0.0
    ace_sum = 0.0
    
    for i in range(n):
        p1 = coords[i]
        p2 = coords[(i + 1) % n]
        
        length = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) 
        shoelace = (p1[0] * p2[1]) - (p2[0] * p1[1])
        perime += length
        shoe_sum += shoelace
        ace_sum += abs(shoelace)
        
    area = abs(shoe_sum) / 2.0
    return area, perime, shoe_sum, ace_sum

def solve():
    try:
        n = int(input())
        coords = [list(map(float, input().split())) for _ in range(n)]
        min_len = float('inf')
        for i in range(n):
            p1 = coords[i]
            p2 = coords[(i + 1) % n]
            length = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
            if length < min_len:
                min_len = length
        max_h_possible = max(
            (0.0, (min_len - 0.1) / 2.0)
        )
        max_h = 0.0
        if max_h_possible > 0.0:
            possible = 0.1
            area_0, perim_0, _, _ = get_polygon_properties(coords)
            if area_0 == 0.0:
                print(f"{0.00:.2f}")
                return
            max_volume = 0.0
            num_steps = int(max_h_possible / 0.1)
            for i in range(1, num_steps + 1):
                h = round(i * 0.1, 1)
                base_area = area_0 - (perim_0 * h) + (4 * h * h)
                if base_area <= 0:
                    continue
                volume = base_area * h
                if volume > max_volume:
                    max_volume = volume
        print(f"{max_volume:.2f}",end=" ")

    except EOFError:
        pass
    except Exception:
        pass

solve()

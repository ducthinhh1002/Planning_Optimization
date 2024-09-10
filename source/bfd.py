import sys

def parse_input():
    # Read input from keyboard
    data = input().split()
    
    N = int(data[0])
    K = int(data[1])

    items = []
    index = 2
    for i in range(N):
        w = int(data[index])
        l = int(data[index+1])
        items.append((w, l, i+1))
        index += 2

    trucks = []
    for k in range(K):
        W = int(data[index])
        L = int(data[index+1])
        c = int(data[index+2])
        trucks.append((W, L, c, k+1))
        index += 3

    return N, K, items, trucks

def can_place(truck, x, y, w, l, placed_items):
    # Check if an item can be placed at position (x, y) on the truck
    W, L = truck[0], truck[1]
    if x + w > W or y + l > L:
        return False  # item doesn't fit
    for px, py, pw, pl in placed_items:
        if not (x + w <= px or x >= px + pw or y + l <= py or y >= py + pl):
            return False  # item overlaps with another item
    return True  # item can be placed

def best_fit_search(N, K, items, trucks):
    # Sort trucks by capacity in decreasing order
    trucks.sort(key=lambda x: x[0] * x[1], reverse=True)
    
    # Initialize result and truck usage
    result = [-1] * N
    truck_usage = [[] for _ in range(K)]
    
    # Iterate over items
    for w, l, i in items:
        best_fit_truck = -1
        best_fit_area = float('inf')
        for k, truck in enumerate(trucks):
            W, L, c, truck_id = truck
            if W >= w and L >= l:
                area = W * L
                if area < best_fit_area:
                    best_fit_area = area
                    best_fit_truck = k
        
        if best_fit_truck!= -1:
            truck = trucks[best_fit_truck]
            W, L, c, truck_id = truck
            for x in range(W - w + 1):
                for y in range(L - l + 1):
                    if can_place(truck, x, y, w, l, truck_usage[best_fit_truck]):
                        truck_usage[best_fit_truck].append((x, y, w, l))
                        result[i-1] = (i, truck_id, x, y, 0)
                        break
                if result[i-1]!= -1:
                    break

    return result

def main():
    N, K, items, trucks = parse_input()
    result = best_fit_search(N, K, items, trucks)
    for res in result:
        print(' '.join(map(str, res)))

if __name__ == "__main__":
    main()
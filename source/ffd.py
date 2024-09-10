import sys

def parse_input():
    # input = sys.stdin.read()  # Comment this line to read input from keyboard
    data = input().split()  # Read input from keyboard

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

def best_fit_decreasing(N, K, items, trucks):
    # Sort items by area in decreasing order
    items.sort(key=lambda x: x[0] * x[1], reverse=True)
    
    # Sort trucks by cost in increasing order
    trucks.sort(key=lambda x: x[2])
    
    # Initialize result and truck usage
    result = [-1] * N
    truck_usage = [[] for _ in range(K)]
    
    # Iterate over items
    current_truck = 0
    for w, l, i in items:
        placed = False
        while not placed and current_truck < K:
            W, L, c, truck_id = trucks[current_truck]
            
            # Try to place item in both orientations
            for orientation in [(w, l, 0), (l, w, 1)]:
                item_w, item_l, o = orientation
                for x in range(W - item_w + 1):
                    for y in range(L - item_l + 1):
                        if can_place(trucks[current_truck], x, y, item_w, item_l, truck_usage[current_truck]):
                            truck_usage[current_truck].append((x, y, item_w, item_l))
                            result[i-1] = (i, truck_id, x, y, o)
                            placed = True
                            break
                    if placed:
                        break
                if placed:
                    break
            
            if not placed:
                current_truck += 1

    return result

def main():
    N, K, items, trucks = parse_input()
    result = best_fit_decreasing(N, K, items, trucks)
    for res in result:
        print(' '.join(map(str, res)))

if __name__ == "__main__":
    main()
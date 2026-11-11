import heapq

# Dijkstra's Algorithm for shortest path in a grid
def dijkstra(plant_map, start, goal):
    rows, cols = len(plant_map), len(plant_map[0])
    distances = {start: 0}
    pq = [(0, start)]  # Priority queue for Dijkstra's algorithm
    came_from = {start: None}
    
    while pq:
        current_distance, current = heapq.heappop(pq)
        if current == goal:
            break
        for neighbor in get_neighbors(current, rows, cols):
            if plant_map[neighbor[0]][neighbor[1]] == 1:
                continue  # Skip hazardous cells
            new_distance = current_distance + 1
            if neighbor not in distances or new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                heapq.heappush(pq, (new_distance, neighbor))
                came_from[neighbor] = current
    
    # Reconstruct the path
    path = []
    current = goal
    while current:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

def get_neighbors(pos, rows, cols):
    r, c = pos
    neighbors = [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]  # Down, Up, Right, Left
    return [(r, c) for r, c in neighbors if 0 <= r < rows and 0 <= c < cols]


# Simulated plant layout (0=safe, 1=hazardous)
plant_map = [
    [0, 0, 0, 1],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 0]
]

# Employee's current location (row, col)
start = (3, 0)

# Safe zone (destination) can be fixed or dynamic
goal = (0, 3)

p=dijkstra(plant_map, start, goal)
print(p)

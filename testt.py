from collections import deque

# Определяем направления движения (вверх, вниз, влево, вправо)
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def bfs(start, goal, grid):
    queue = deque([start])  # начальная позиция робота
    visited = set([start])  # посещённые клетки
    parent = {start: None}  # для восстановления пути

    while queue:
        current = queue.popleft()

        if current == goal:
            # Восстанавливаем путь
            path = []
            while current:
                path.append(current)
                current = parent[current]
            return path[::-1]  # Возвращаем путь в обратном порядке

        # Проверяем все возможные направления
        for direction in directions:
            new_pos = (current[0] + direction[0], current[1] + direction[1])

            if new_pos not in visited and is_valid(new_pos, grid):
                queue.append(new_pos)
                visited.add(new_pos)
                parent[new_pos] = current

    return None  # Если путь не найден

def is_valid(pos, grid):
    x, y = pos
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] != 'obstacle'
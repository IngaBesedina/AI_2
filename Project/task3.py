#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from collections import deque


def is_valid(cell, rows, cols, grid, visited):
    """Проверяет, можно ли перейти в указанную клетку."""
    x, y = cell
    return 0 <= x < rows and 0 <= y < cols and grid[x][y] == 1 and not visited[x][y]


def bfs_shortest_path(grid, start, destination):
    """Находит кратчайший путь в лабиринте с помощью BFS."""
    rows, cols = len(grid), len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Верх, низ, влево, вправо
    parent_map = {}  # Для восстановления пути

    queue = deque([(start, 0)])  # Храним текущую клетку и длину пути
    visited[start[0]][start[1]] = True

    while queue:
        current, distance = queue.popleft()

        if current == destination:
            return distance, reconstruct_path(parent_map, start, destination)

        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            if is_valid(neighbor, rows, cols, grid, visited):
                visited[neighbor[0]][neighbor[1]] = True
                parent_map[neighbor] = current  # Сохраняем путь
                queue.append((neighbor, distance + 1))

    return -1, []  # Если путь не найден


def reconstruct_path(parent_map, start, destination):
    """Восстанавливает путь от начала до конца."""
    path = []
    current = destination
    while current != start:
        path.append(current)
        current = parent_map.get(current)
    path.append(start)
    path.reverse()
    return path


def main():
    maze = [
        [1, 1, 1, 1, 1, 0, 0, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
        [0, 0, 1, 0, 1, 1, 1, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
        [0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
        [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [1, 1, 1, 1, 1, 0, 0, 1, 1, 1],
        [0, 0, 1, 0, 0, 1, 1, 0, 0, 1]
    ]

    start = (0, 0)
    destination = (7, 5)

    distance, path = bfs_shortest_path(maze, start, destination)

    if distance != -1:
        print(f"Кратчайший путь имеет длину {distance}.")
        print(f"Путь: {path}")
    else:
        print("Путь от начальной точки до пункта назначения не найден.")


if __name__ == "__main__":
    main()

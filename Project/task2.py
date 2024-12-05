#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from collections import deque


"""
дана бинарная матрица, где 0 представляет воду, а 1 представляет землю.
Связанные единицы формируют остров. Необходимо подсчитать общее
количество островов в данной матрице. Острова могут соединяться как по
вертикали и горизонтали, так и по диагонали.
"""


class IslandProblem:
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0
        self.visited = [
            [False for _ in range(self.cols)] for _ in range(self.rows)
        ]
        self.directions = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]

    def actions(self, state):
        """Возвращает допустимые действия для текущего состояния"""
        x, y = state
        neighbors = []
        for dx, dy in self.directions:
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < self.rows
                and 0 <= ny < self.cols
                and not self.visited[nx][ny]
            ):
                neighbors.append((nx, ny))
        return neighbors

    def result(self, state, action):
        """Возвращает новое состояние после действия."""
        return action

    def bfs(self, start):
        """Выполняет поиск в ширину, начиная с данной клетки."""
        queue = deque([start])
        self.visited[start[0]][start[1]] = True

        while queue:
            current = queue.popleft()
            for neighbor in self.actions(current):
                x, y = neighbor
                if self.grid[x][y] == 1 and not self.visited[x][y]:
                    self.visited[x][y] = True
                    queue.append(neighbor)

    def count_islands(self):
        """Подсчитывает количество островов в матрице."""
        islands = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == 1 and not self.visited[i][j]:
                    # Новый остров найден
                    self.bfs((i, j))
                    islands += 1
        return islands


def main():
    grid = [
        [1, 1, 0, 0, 0],
        [0, 1, 0, 0, 1],
        [1, 0, 0, 1, 1],
        [0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1],
    ]

    problem = IslandProblem(grid)
    print("Количество островов:", problem.count_islands())


if __name__ == "__main__":
    main()

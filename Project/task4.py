#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from collections import deque


"""
Реализуйте алгоритм поиска в ширину (BFS) для решения задачи
о льющихся кувшинах, где цель состоит в том, чтобы получить заданный объем воды
в одном из кувшинов. В этой задаче вам дается набор кувшинов, каждый из которых
имеет размер, скажем, в литрах, и текущий уровень воды (в литрах).
Задача состоит в том, чтобы отмерить определенный объем воды;
он может оказаться в любом из кувшинов.
Состояние представлено кортежем текущих уровней воды,
а доступными действиями являются:
(Fill, i): наполнить i-й кувшин до самого верха
(Dump, i): вылить всю воду из i-го кувшина.
(Pour, i, j): перелить воду из i-го кувшина в j-й кувшин, пока либо кувшин i не
опустеет, либо кувшин j не наполнится, в зависимости от того, что наступит
раньше.
"""


class PourProblem:
    def __init__(self, initial, target, sizes):
        """
        initial: начальное состояние (уровни воды в кувшинах)
        target: целевой объем воды
        sizes: емкости кувшинов
        """
        self.initial = initial
        self.target = target
        self.sizes = sizes

    def is_goal(self, state):
        """Проверяет, достигнуто ли целевое состояние."""
        return self.target in state

    def get_successors(self, state):
        """
        Генерирует все возможные состояния из текущего состояния.
        """
        successors = []
        num_jugs = len(state)

        for i in range(num_jugs):
            # (Fill, i): наполнить i-й кувшин
            new_state = list(state)
            new_state[i] = self.sizes[i]
            successors.append((tuple(new_state), ("Fill", i)))

            # (Dump, i): вылить воду из i-го кувшина
            new_state = list(state)
            new_state[i] = 0
            successors.append((tuple(new_state), ("Dump", i)))

            for j in range(num_jugs):
                if i != j:
                    # (Pour, i, j): перелить из i-го в j-й
                    new_state = list(state)
                    pour_amount = min(state[i], self.sizes[j] - state[j])
                    new_state[i] -= pour_amount
                    new_state[j] += pour_amount
                    successors.append((tuple(new_state), ("Pour", i, j)))

        return successors

    def solve(self):
        """Решает задачу с использованием поиска в ширину (BFS)."""
        queue = deque([(self.initial, [])])  # Очередь (состояние, путь)
        visited = set()  # Посещенные состояния

        while queue:
            state, path = queue.popleft()

            if self.is_goal(state):
                return path, state  # Возвращаем путь и финальное состояние

            if state in visited:
                continue
            visited.add(state)

            for successor, action in self.get_successors(state):
                if successor not in visited:
                    queue.append((successor, path + [action]))

        return None, None  # Целевое состояние недостижимо


def main():
    problem = PourProblem((1, 1, 1), 13, sizes=(2, 16, 32))
    actions, final_state = problem.solve()

    if actions:
        print("Решение найдено:")
        print(actions)
        print(final_state)
    else:
        print("Решение не найдено.")


if __name__ == "__main__":
    main()

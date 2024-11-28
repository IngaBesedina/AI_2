import math
import json
from problem import Problem, Node, breadth_first_search, path_states
from collections import deque


"""
Для построенного графа лабораторной работы 1 напишите программу на языке
программирования Python, которая с помощью алгоритма поиска в ширину 
находит минимальное расстояние между начальным и конечным пунктами.
Сравните найденное решение с решением, полученным вручную.
"""


failure = Node('failure', path_cost=math.inf)
cutoff = Node('cutoff', path_cost=math.inf)


class GraphProblem(Problem):
    def __init__(self, initial, goal, graph):
        super().__init__(initial=initial, goal=goal)
        self.graph = graph

    def actions(self, state):
        return list(self.graph.get(state, {}).keys())

    def result(self, state, action):
        return action

    def action_cost(self, s, a, s1):
        return self.graph[s][s1]


def expand(problem, node):
    """Расширяет узел для получения дочерних узлов."""

    for action in problem.actions(node.state):
        child_state = problem.result(node.state, action)
        cost = node.path_cost + problem.action_cost(node.state, action, child_state)
        yield Node(child_state, node, action, cost)


def breadth_first_search(problem: Problem):
    """Реализация поиска в ширину"""

    node = Node(problem.initial)  # Начальный узел
    if problem.is_goal(problem.initial):
        return node

    frontier = deque([node])  # Очередь для обхода
    reached = {problem.initial}  # Посещённые вершины

    while frontier:
        node = frontier.popleft()
        for child in expand(problem, node):
            s = child.state
            if problem.is_goal(s):
                return child
            if s not in reached:
                reached.add(s)
                frontier.append(child)
    return failure  # Если путь не найден


def load_graph(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)
    

def main():
    graph = load_graph('graph.json')

    problem = GraphProblem("Тамбов", "Рязань", graph)

    result_node = breadth_first_search(problem)

    if result_node != failure:
        path = path_states(result_node)
        print(f"Минимальный путь: {' -> '.join(path)}")
        print(f"Стоимость пути: {result_node.path_cost}")
    else:
        print("Путь не найден.")


if __name__ == "__main__":
    main()

import heapq
import math
from collections import deque


class Problem:
    """Абстрактный класс для формальной задачи. Новый домен
    специализирует этот класс, переопределяя `actions` и `results`, 
    и, возможно, другие методы.
    Эвристика по умолчанию равна 0, а стоимость действия по умолчанию
    равна 1 для всех состояний.
    Когда вы создаете экземпляр подкласса, укажите `начальное` и
    `целевое` состояния
    (или задайте метод `is_goal`) и, возможно, другие ключевые слова для
    подкласса."""

    def __init__(self, initial=None, goal=None, **kwds):
        self.__dict__.update(initial=initial, goal=goal, **kwds)

    def actions(self, state): raise NotImplementedError

    def result(self, state, action): raise NotImplementedError

    def is_goal(self, state): return state == self.goal

    def action_cost(self, s, a, s1): return 1

    def h(self, node): return 0

    def __str__(self):
        return '{}({!r}, {!r})'.format(type(self).__name__, self.initial, self.goal)


class Node:
    "Узел в дереве поиска"

    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.__dict__.update(state=state, parent=parent, action=action, path_cost=path_cost)

    def __repr__(self): return '<{}>'.format(self.state)

    def __len__(self): return 0 if self.parent is None else (1 + len(self.parent))

    def __lt__(self, other): return self.path_cost < other.path_cost

failure = Node('failure', path_cost=math.inf)

cutoff = Node('cutoff', path_cost=math.inf) 


def expand(problem, node):
    "Раскрываем узел, создав дочерние узлы."

    s = node.state
    for action in problem.actions(s):
        s1 = problem.result(s, action)
        cost = node.path_cost + problem.action_cost(s, action, s1)
        yield Node(s1, node, action, cost)

def path_actions(node):
    "Последовательность действий, чтобы добраться до этого узла."

    if node.parent is None:
        return []
    return path_actions(node.parent) + [node.action]

def path_states(node):
    "Последовательность состояний, чтобы добраться до этого узла"

    if node in (cutoff, failure, None):
        return []
    return path_states(node.parent) + [node.state]


FIFOQueue = deque
LIFOQueue = list

class PriorityQueue:
    """Очередь, в которой элемент с минимальным значением f(item) всегда
    выгружается первым."""

    def __init__(self, items=(), key=lambda x: x):
        self.key = key
        self.items = [] # a heap of (score, item) pairs
        for item in items:
            self.add(item)

    def add(self, item):
        """Добавляем элемент в очередь."""
        pair = (self.key(item), item)
        heapq.heappush(self.items, pair)

    def pop(self):
        """Достаем и возвращаем элемент с минимальным значением f(item)."""
        return heapq.heappop(self.items)[1]

    def top(self): return self.items[0][1]

    def __len__(self): return len(self.items)


def breadth_first_search(problem: Problem):

    node = Node(problem.initial)
    if problem.is_goal(problem.initial):

        return node

    frontier = FIFOQueue([node])

    reached = {problem.initial}

    while frontier:

        node = frontier.pop()
        for child in expand(problem, node):

            s = child.state
            if problem.is_goal(s):

                return child
            if s not in reached:

                reached.add(s)
                frontier.appendleft(child)
    return failure



import random
from collections import deque


class State:
    def __init__(self, missionaries, cannibals, boat):
        self.missionaries = missionaries
        self.cannibals = cannibals
        self.boat = boat
        self.parent = None

    def is_valid(self):
        if self.missionaries < 0 or self.missionaries > 3:
            return False
        if self.cannibals < 0 or self.cannibals > 3:
            return False
        if self.missionaries > 0 and self.missionaries < self.cannibals:
            return False
        if self.missionaries < 3 and 3 - self.missionaries < 3 - self.cannibals:
            return False
        return True

    def is_goal(self):
        return self.missionaries == 0 and self.cannibals == 0 and self.boat == 0

    def __eq__(self, other):
        return (self.missionaries == other.missionaries and
                self.cannibals == other.cannibals and
                self.boat == other.boat)

    def __hash__(self):
        return hash((self.missionaries, self.cannibals, self.boat))


def get_successors(cur_state):
    successors = []
    moves = [(2, 0), (0, 2), (1, 1), (1, 0), (0, 1)]
    random.shuffle(moves)  # Shuffle moves to introduce randomness
    for m, c in moves:
        if cur_state.boat == 1:
            new_state = State(cur_state.missionaries - m, cur_state.cannibals - c, 0)
        else:
            new_state = State(cur_state.missionaries + m, cur_state.cannibals + c, 1)
        if new_state.is_valid():
            new_state.parent = cur_state
            successors.append(new_state)
    return successors


def bfs(initial_state):
    queue = deque([initial_state])
    visited = set()
    visited.add(initial_state)

    while queue:
        state = queue.popleft()
        if state.is_goal():
            return state
        for next_state in get_successors(state):
            if next_state not in visited:
                visited.add(next_state)
                queue.append(next_state)
    return None


def solution_to_list(solution):
    path = []
    while solution:
        path.append(solution)
        solution = solution.parent
    return [[state.missionaries, state.cannibals, state.boat] for state in reversed(path)]
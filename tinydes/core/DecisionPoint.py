import random

class DecisionPoint:
    def __init__(self, name, branches, probabilities):
        self.name = name
        self.branches = branches
        self.probabilities = probabilities

    def next_branch(self):
        return random.choices(self.branches, self.probabilities)[0]
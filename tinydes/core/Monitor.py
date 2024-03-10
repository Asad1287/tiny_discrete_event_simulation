class Monitor:
    def __init__(self):
        self.data = []

    def record(self, value):
        self.data.append(value)

    def mean(self):
        return sum(self.data) / len(self.data) if self.data else 0

    def max(self):
        return max(self.data) if self.data else 0

    def min(self):
        return min(self.data) if self.data else 0

    def count(self):
        return len(self.data)

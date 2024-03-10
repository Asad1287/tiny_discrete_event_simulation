class Batch:
    def __init__(self, env, size):
        self.env = env
        self.size = size
        self.batch = []

    def add(self, entity):
        self.batch.append(entity)
        if len(self.batch) == self.size:
            yield self.env.timeout(0)
            batch = self.batch
            self.batch = []
            return batch

    def is_full(self):
        return len(self.batch) == self.size
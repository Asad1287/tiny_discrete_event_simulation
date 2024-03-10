class Queue:
    def __init__(self):
        self.entities = []

    def enqueue(self, entity):
        self.entities.append(entity)

    def dequeue(self):
        return self.entities.pop(0) if self.entities else None

    def is_empty(self):
        return len(self.entities) == 0
class Storage:
    def __init__(self, env, name, capacity):
        self.env = env
        self.name = name
        self.capacity = capacity
        self.store = simpy.Store(env, capacity)

    def put(self, entity):
        yield self.store.put(entity)

    def get(self):
        return self.store.get()
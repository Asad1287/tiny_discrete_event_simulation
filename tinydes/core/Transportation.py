class Transportation:
    def __init__(self, env, name, capacity, speed):
        self.env = env
        self.name = name
        self.capacity = capacity
        self.speed = speed
        self.resource = simpy.Resource(env, capacity)

    def transport(self, entity, destination):
        yield self.env.timeout(abs(entity.location - destination) / self.speed)
        entity.location = destination

class Disposal:
    def __init__(self, env, condition):
        self.env = env
        self.condition = condition

    def dispose(self, entity):
        if self.condition(entity):
            yield self.env.process(self.disposal_process(entity))

    def disposal_process(self, entity):
        # Perform any necessary cleanup or recording before disposing of the entity
        yield self.env.timeout(0)
